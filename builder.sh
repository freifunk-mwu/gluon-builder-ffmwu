#!/bin/bash

# Stop the builder on any failed command
set -e
set -o pipefail

# Do not build as root!
if [ "$EUID" -eq 0 ]; then echo -e "~ error: you are root."; exit 23; fi

# Locates own directory
# CDIR is used later on for calling helper scripts with their correct path
CDIR=$(cd "$(dirname "$0")"; pwd)

# Run the prepare.py helper script, passing all arguments into it.
# Let Python do the argument parsing!
$CDIR/prepare.py $@

# Check if the prepare helper was successful (and correctly invoked
# _gen_bconf.py) by checking for the generated bconf file.
# Deletes bconf immediately, we have the content now stored in the variables
if [ ! -f "$CDIR/bconf" ]; then echo -e "~ error: no bconf found"; exit 42; fi
. $CDIR/bconf
rm $CDIR/bconf

# A shortcut for the meta file-logger
LOGP="$PYCMD $CDIR/_build_logger.py"

for C in $COMMUNITIES; do
    START=$(date +%s)
    WDIR="$BUILDDIR/$C"
    SUMS="$STAGEDIR/${C}_$RELEASE.sha512"
    LOGF="$STAGEDIR/${C}_$RELEASE.log"
    $LOGP "~ ${C}_$RELEASE" > $LOGF
    # Another logger-shortcut, this time: stdout to file
    # (one per community)
    LOG="tee -a $LOGF"

    # To boldly go where no man has gone before
    cd $WDIR

    $LOGP "~ ${C}_$RELEASE ~ update" 2>&1 | $LOG
    $MKCMD update 2>&1 | $LOG

    # BUILDBRANCH is set in the defaults (['common']['branches']['build']), it could be anything,
    # but should occur in your available branches (['common']['branches']['avail']) for correct replacing
    # of branches in _uni_manifest.py (below)

    # Using GLUON_BRANCH here is the only way to enable the autoupdater, for the Branch BUILDBRANCH.
    # Set BUILDBRANCH to your 'stable' Branch. Any 'experimental' or 'beta' user will auto update to the
    # next 'stable' Release, unless the Autoupdater-Settings on the Node are changed.
    $LOGP "~ ${C}_$RELEASE ~ images (GLUON_BRANCH=$BUILDBRANCH GLUON_RELEASE=$RELEASE GLUON_TARGET=$TARGET BROKEN=$BROKEN)" 2>&1 | $LOG
    $MKCMD GLUON_BRANCH=$BUILDBRANCH GLUON_RELEASE=$RELEASE GLUON_TARGET=$TARGET BROKEN=$BROKEN 2>&1 | $LOG

    # Create a (temporary) manifest
    $LOGP "~ ${C}_$RELEASE ~ manifest (GLUON_BRANCH=$CALLBRANCH GLUON_PRIORITY=$PRIORITY)" 2>&1 | $LOG
    $MKCMD manifest GLUON_BRANCH=$CALLBRANCH GLUON_PRIORITY=$PRIORITY 2>&1 | $LOG

    # Take the temporary manifest and replace it's BUILDBRANCH by all available branches.
    # Rewrites the manifest and creates symlinks for each branch onto it: ./$branch.manifest -> ./manifest
    $PYCMD $CDIR/_uni_manifest.py -b $CALLBRANCH -m "$WDIR/images/sysupgrade/$CALLBRANCH.manifest"

    # Now the manifest is fixed, let's sign!
    # Remember to increase the 'good_signatures' in your siteconf if signing automatically.
    if [ -f "$SIGNKEY" ]; then
        $LOGP "~ ${C}_$RELEASE ~ sign ($SIGNKEY images/sysupgrade/$CALLBRANCH.manifest)" 2>&1 | $LOG
        "$WDIR/contrib/sign.sh" $SIGNKEY "$WDIR/images/sysupgrade/$CALLBRANCH.manifest" 2>&1 | $LOG
    else
        $LOGP "~ ${C}_$RELEASE ~ skipping signing, no key found ($SIGNKEY)" | $LOG
    fi

    # Hard part is done
    $LOGP "~ ${C}_$RELEASE ~ appendix" 2>&1 | $LOG

    # The info file is a json containing a mapping of router models matching image-file names.
    # So let's store the checksums too.
    $PYCMD $CDIR/_gen_info.py -i "$WDIR/images" -c "$WDIR/scripts/sha512sum.sh" --start $START --finish $(date +%s)
    for g in images/*/*; do echo "$($WDIR/scripts/sha512sum.sh $g) $g" >> $SUMS; done
    if [ -f "$SIGNKEY" ]; then
        "$WDIR/contrib/sign.sh" $SIGNKEY $SUMS 2>&1 | $LOG
    fi

    # Move freshly built images into the library
    # Compress stdio log and copy metadata from stagedir
    mkdir -p "$LIBRARYDIR/${C}" 2>&1 | $LOG
    cp -rv "$WDIR/images/." "$LIBRARYDIR/${C}/" 2>&1 | $LOG
    gzip $LOGF

    # Because we are building multiple communities the configuration differs.
    # For us, it is machine created, so store the results as well.
    SITEFILES=("$WDIR/site/site.conf" "$WDIR/site/site.mk" "$WDIR/site/modules" "$WDIR/site/i18n/*.po")
    zip -j "$STAGEDIR/${C}_${RELEASE}_site.zip" ${SITEFILES[*]} | $LOG

    # Last, copy the stagedir.
    cp -rv "$STAGEDIR/." $LIBRARYDIR

done

# Set symlinks to the fresh release for the autoupdater.
$PYCMD $CDIR/publish.py $LIBRARYDIR -b $CALLBRANCH

# Clean up afterwards.
rm -rf $BUILDDIR $STAGEDIR

echo "~ finished"
exit 0
