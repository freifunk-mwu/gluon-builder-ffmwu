#!/usr/bin/env python3

def prepare(branch, gt=None, st=None):
    from common import pinit, ginit
    from photon.util.locations import change_location
    from _gen_bconf import gen_bconf

    p, s = pinit('prepare', clean=True)

    for community in s['common']['communities']:
        change_location(s['gluon']['local'][community], False, move=True)
        tags = s['common']['branches']['avail'][branch]
        gluon, site = ginit(p, community)

        if gt:
            if gt in gluon.tag: gluon.tag = gt
            elif gt in gluon.commit: gluon.commit = gt
            else: p.m('Invalid git commit-id or tag specified for gluon', state=True)
        else:
            if tags[0]: gluon.tag = None
            else: gluon.branch = None

        if st:
            if st in site.tag: site.tag = st
            elif st in site.commit: site.commit = st
            else: p.m('Invalid git commit-id or tag specified for site', state=True)
        else:
            if tags[1]: site.tag = None
            else: site.branch = None

        p.m('generating site for %s' %(community), cmdd=dict(cmd='%s generate.py %s --nomodules' %(s['common']['pycmd'], community), cwd=s['site']['local'][community]), verbose=True)

    gen_bconf(branch, gt, st)

if __name__ == '__main__':
    from common import branch_args
    a = branch_args()

    prepare(a.branch, a.gt, a.st)
