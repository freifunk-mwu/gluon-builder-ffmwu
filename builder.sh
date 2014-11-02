#!/bin/bash

set -e
set -o pipefail

if [ "$EUID" -eq 0 ]; then echo -e "~ error: you are root."; exit 23; fi

CDIR=$(cd "$(dirname "$0")"; pwd)
$CDIR/prepare.py $@

if [ ! -f "bconf" ]; then echo -e "~ error: no bconf found"; exit 42; fi
. $CDIR/bconf
rm $CDIR/bconf

for C in $COMMUNITIES; do
    WDIR="$BUILDDIR/$C"
    ODIR="$ARCHIVEDIR/$RELEASE"
    SUMS="$STAGEDIR/${C}_$RELEASE.sha512"
    LOGF="$STAGEDIR/${C}_$RELEASE.log"
    LOGP="$PYCMD $CDIR/_build_logger.py"
    $LOGP "~~~~ ${C}_$RELEASE" > $LOGF
    LOG="tee -a $LOGF"

    cd $WDIR

    $LOGP "~~~~ ${C}_$RELEASE ~ update" 2>&1 | $LOG
    $MKCMD update 2>&1 | $LOG

    $LOGP "~~~~ ${C}_$RELEASE ~ images (GLUON_BRANCH=$BUILDBRANCH GLUON_RELEASE=$RELEASE)" 2>&1 | $LOG
    $MKCMD GLUON_BRANCH=$BUILDBRANCH GLUON_RELEASE=$RELEASE 2>&1 | $LOG

    $LOGP "~~~~ ${C}_$RELEASE ~ manifest (GLUON_BRANCH=$CALLBRANCH GLUON_PRIORITY=$PRIORITY)" 2>&1 | $LOG
    $MKCMD manifest GLUON_BRANCH=$CALLBRANCH GLUON_PRIORITY=$PRIORITY 2>&1 | $LOG

    #TODO

    $LOGP "~~~~ ${C}_$RELEASE ~ sign ($AUTOSIGNKEY images/sysupgrade/$CALLBRANCH.manifest)" 2>&1 | $LOG
    contrib/sign.sh $AUTOSIGNKEY images/sysupgrade/$CALLBRANCH.manifest 2>&1 | $LOG

    $LOGP "~~~~ ${C}_$RELEASE ~ appendix" 2>&1 | $LOG
    for g in images/*/*; do echo "$(scripts/sha512sum.sh $g) $g" >> $SUMS; done
    contrib/sign.sh $AUTOSIGNKEY $SUMS 2>&1 | $LOG
    gzip $LOGF

    mkdir -p "$ODIR/${C}" 2>&1 | $LOG
    cp -r images "$ODIR/${C}/" 2>&1 | $LOG
    cp -r $STAGEDIR $ODIR 2>&1 | $LOG

done

rm -rf $BUILDDIR $STAGEDIR

exit 0
