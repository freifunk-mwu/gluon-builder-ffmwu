#!/bin/bash

set -e
set -o pipefail

if [ "$EUID" -eq 0 ]; then echo -e "~ error: you are root."; exit 23; fi

CDIR=$(cd "$(dirname "$0")"; pwd)
$CDIR/prepare.py $@

if [ ! -f "bconf" ]; then echo -e "~ error: no bconf found"; exit 42; fi
. $CDIR/bconf
rm $CDIR/bconf

LOGP="$PYCMD $CDIR/_build_logger.py"

for C in $COMMUNITIES; do
    WDIR="$BUILDDIR/$C"
    SUMS="$STAGEDIR/${C}_$RELEASE.sha512"
    LOGF="$STAGEDIR/${C}_$RELEASE.log"
    $LOGP "~ ${C}_$RELEASE" > $LOGF
    LOG="tee -a $LOGF"

    cd $WDIR

    $LOGP "~ ${C}_$RELEASE ~ update" 2>&1 | $LOG
    $MKCMD update 2>&1 | $LOG

    $LOGP "~ ${C}_$RELEASE ~ images (GLUON_BRANCH=$BUILDBRANCH GLUON_RELEASE=$RELEASE)" 2>&1 | $LOG
    $MKCMD GLUON_BRANCH=$BUILDBRANCH GLUON_RELEASE=$RELEASE 2>&1 | $LOG

    $LOGP "~ ${C}_$RELEASE ~ manifest (GLUON_BRANCH=$CALLBRANCH GLUON_PRIORITY=$PRIORITY)" 2>&1 | $LOG
    $MKCMD manifest GLUON_BRANCH=$CALLBRANCH GLUON_PRIORITY=$PRIORITY 2>&1 | $LOG

    $PYCMD $CDIR/_uni_manifest.py -b $CALLBRANCH -m "$WDIR/images/sysupgrade/$CALLBRANCH.manifest"

    $LOGP "~ ${C}_$RELEASE ~ sign ($AUTOSIGNKEY images/sysupgrade/$CALLBRANCH.manifest)" 2>&1 | $LOG
    "$WDIR/contrib/sign.sh" $AUTOSIGNKEY "$WDIR/images/sysupgrade/$CALLBRANCH.manifest" 2>&1 | $LOG

    $LOGP "~ ${C}_$RELEASE ~ appendix" 2>&1 | $LOG
    $PYCMD $CDIR/_gen_info.py -i "$WDIR/images" -c "$WDIR/scripts/sha512sum.sh"

    for g in images/*/*; do echo "$($WDIR/scripts/sha512sum.sh $g) $g" >> $SUMS; done
    "$WDIR/contrib/sign.sh" $AUTOSIGNKEY $SUMS 2>&1 | $LOG

    mkdir -p "$LIBRARYDIR/${C}" 2>&1 | $LOG
    cp -rv "$WDIR/images/." "$LIBRARYDIR/${C}/" 2>&1 | $LOG
    gzip $LOGF
    cp -rv "$STAGEDIR/." $LIBRARYDIR

done

rm -rf "$LIBRARYDIR/$INFOFILE" $BUILDDIR $STAGEDIR

echo "~ finished"
exit 0
