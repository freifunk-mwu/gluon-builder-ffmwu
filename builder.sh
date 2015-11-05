#!/bin/bash

# Stop the builder on any failed command
set -e
set -o pipefail

# Do not build as root!
if [ "$EUID" -eq 0 ]; then
    echo -e "~ error: you are root."
    exit 23
fi

# Locates own directory
CURRENTDIR=$(cd "$(dirname "$0")"; pwd)

BCONF="$CURRENTDIR/bconf"
BUILDLOGGER="$CURRENTDIR/_build_logger.py"
GENINFO="$CURRENTDIR/_gen_info.py"
PREPARE="$CURRENTDIR/prepare.py"
PUBLISH="$CURRENTDIR/publish.py"
UNIMANIFEST="$CURRENTDIR/_uni_manifest.py"

# Run the prepare.py helper script, passing all arguments into it.
# Let Python do the argument parsing!
$PREPARE "$@"

# Check if the prepare helper was successful (and correctly invoked
# _gen_bconf.py) by checking for the generated bconf file.
# Deletes bconf immediately, we have the content now stored in the variables
if [ ! -f "$BCONF" ]; then
    echo -e "~ error: no bconf found"
    exit 42
fi

. "$BCONF"
rm "$BCONF"

for COMMUNITY in $COMMUNITIES; do
    BUILDSTART=$(date +%s)
    WORKINGDIR="$BUILDDIR/$COMMUNITY"

    CHECKSUMS="$STAGEDIR/${COMMUNITY}_$RELEASE.sha512"
    LOGFILE="$STAGEDIR/${COMMUNITY}_$RELEASE.log"
    SITEZIP="$STAGEDIR/${COMMUNITY}_${RELEASE}_site.zip"

    SHASCRIPT="$WORKINGDIR/scripts/sha512sum.sh"
    SIGNSCRIPT="$WORKINGDIR/contrib/sign.sh"

    # initialize logfile
    echo "start: $BUILDSTART" > "$LOGFILE"

    # logger-shortcut: stdout to file
    # (one per community)
    LOG="tee -a $LOGFILE"

    # A shortcut for the meta file-logger
    function logp {
        $PYCMD "$BUILDLOGGER" "${COMMUNITY}_$RELEASE ~ $*" 2>&1 | $LOG
    }

    function patch_ati_pata {
        X86_ARC=$1
        PATCHSTR="CONFIG_PATA_ATIIXP=y"
        for PATCH in "$WORKINGDIR/openwrt/target/linux/x86/$X86_ARC/config-"*; do
            logp "patching target x86-$X86_ARC for ati pata support ($PATCH)"
            grep "$PATCHSTR" "$PATCH" || echo "$PATCHSTR" >> "$PATCH"
        done
    }

    # To boldly go where no man has gone before
    cd "$WORKINGDIR"

    logp "make update"
    $MKCMD update 2>&1 | $LOG

    # BUILDBRANCH is set in the defaults (['common']['branches']['build']),
    # it could be anything, but should occur in your available branches
    # (['common']['branches']['avail']) for correct replacing of branches in
    # _uni_manifest.py (below)

    # Using GLUON_BRANCH here is the only way to enable the autoupdater,
    # for the Branch BUILDBRANCH.
    # Set BUILDBRANCH to your 'stable' Branch. Any 'experimental' or 'beta'
    # user will auto update to the next 'stable' Release, unless the
    # autoupdater settings on the node are changed.
    for BUILDTARGET in $TARGETS; do
        # Patch OpenWRT Sources
        if [ "$BUILDTARGET" == "x86-generic" ]; then patch_ati_pata "generic"; fi
        if [ "$BUILDTARGET" == "x86-64" ]; then patch_ati_pata "64"; fi

        logp "make images (GLUON_TARGET=$BUILDTARGET GLUON_BRANCH=$BUILDBRANCH GLUON_RELEASE=$RELEASE BROKEN=$BROKEN)"
        $MKCMD GLUON_BRANCH="$BUILDBRANCH" GLUON_RELEASE="$RELEASE" GLUON_TARGET="$BUILDTARGET" BROKEN="$BROKEN" 2>&1 | $LOG
    done

    # Create a (temporary) manifest
    logp "make manifest (GLUON_BRANCH=$CALLBRANCH GLUON_PRIORITY=$PRIORITY)"
    $MKCMD manifest GLUON_BRANCH="$CALLBRANCH" GLUON_PRIORITY="$PRIORITY" 2>&1 | $LOG

    # Take the temporary manifest and replace it's BUILDBRANCH by all
    # available branches. Rewrites the manifest and creates symlinks for
    # each branch onto it: ./$branch.manifest -> ./manifest
    logp "unify manifest ($CALLBRANCH)"
    $PYCMD "$UNIMANIFEST" --branch "$CALLBRANCH" --manifest "$WORKINGDIR/output/images/sysupgrade/$CALLBRANCH.manifest" 2>&1 | $LOG

    # Now the manifest is fixed, let's sign! Remember to increase the
    # 'good_signatures' by one in your siteconf if signing automatically.
    if [ -f "$SIGNKEY" ]; then
        logp "signing ($SIGNKEY output/images/sysupgrade/$CALLBRANCH.manifest)"
        $SIGNSCRIPT "$SIGNKEY" "$WORKINGDIR/output/images/sysupgrade/$CALLBRANCH.manifest" 2>&1 | $LOG
    else
        logp "skipping sign, no key found ($SIGNKEY)"
    fi

    # The info file is a json containing a mapping of router models matching
    # image-file names. So let's store the checksums alongside.
    logp "generating info.json"
    $PYCMD "$GENINFO" --images "$WORKINGDIR/output/images" --ccmd "$SHASCRIPT" --start "$BUILDSTART" --finish "$(date +%s)" 2>&1 | $LOG

    # Provide own checksum files of both factory and sysupgrade images
    logp "getting checksums ($CHECKSUMS)"
    for g in output/images/*/*; do echo "$($SHASCRIPT "$g") $g" >> "$CHECKSUMS"; done
    # Sign them
    if [ -f "$SIGNKEY" ]; then
        logp "signing ($SIGNKEY $CHECKSUMS)"
        $SIGNSCRIPT "$SIGNKEY" "$CHECKSUMS" 2>&1 | $LOG
    fi

    mkdir -p "$STAGEDIR/$COMMUNITY/modules" 2>&1 | $LOG
    # Move freshly built images into the stagedir
    logp "move images into stagedir ($STAGEDIR/$COMMUNITY)"
    cp -rv "$WORKINGDIR/output/images/." "$STAGEDIR/$COMMUNITY/" 2>&1 | $LOG

    # Move freshly built modules alongside the images in the stagedir
    logp "move modules into stagedir ($STAGEDIR/$COMMUNITY/modules)"
    cp -rv "$WORKINGDIR/output/modules/"*"/." "$STAGEDIR/$COMMUNITY/modules/" 2>&1 | $LOG

    # Because we are building multiple communities the configuration differs.
    # For us, it is machine created, so store the results as well.
    logp "store siteconf"
    zip -j "$SITEZIP" "$WORKINGDIR/site/site.conf" "$WORKINGDIR/site/site.mk" "$WORKINGDIR/site/modules" "$WORKINGDIR/site/i18n/"*.po 2>&1 | $LOG

    logp "compress logfile, bye"
    gzip "$LOGFILE"

done

mkdir -p "$LIBRARYDIR"
# Copy the stagedir into the library
cp -rv "$STAGEDIR/." "$LIBRARYDIR"

# Set symlinks to the fresh release for the autoupdater.
$PYCMD "$PUBLISH" "$LIBRARYDIR" --branch "$CALLBRANCH"

# Clean up afterwards.
rm -rfv "$STAGEDIR" "$BUILDDIR"

echo "~ finished"
exit 0
