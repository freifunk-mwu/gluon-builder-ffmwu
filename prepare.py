#!/usr/bin/env python3

def prepare(branch, target, gt=None, st=None, modules=False, broken=False):
    '''
    Checks out Gluon sources and site-conf repositories at proper commit-ids or tags according to the branch to build.
    Generates a site-conf afterwards.
    Automatically invokes :func:`_gen_bconf` afterwards

    .. seealso:: :func:`common.prepare_args` for command line syntax
    '''

    from common import pinit, ginit
    from photon.util.locations import change_location
    from _gen_bconf import gen_bconf

    photon, settings = pinit('prepare', clean=True)

    for community in settings['common']['communities'].keys():
        change_location(settings['gluon']['local'][community], False, move=True)
        tags = settings['common']['branches']['avail'][branch]
        gluon, site = ginit(photon, community=community)

        if gt:
            if gluon.tag and gt in gluon.tag:
                gluon.tag = gt
            elif gluon.commit and (gt in gluon.commit or gt in gluon.short_commit):
                gluon.commit = gt
            else:
                photon.m('Invalid git commit-id or tag specified for gluon', state=True)
        else:
            if tags[0]:
                gluon.tag = None
            else:
                gluon.branch = None

        if st:
            if site.tag and st in site.tag:
                site.tag = st
            elif site.commit and (st in site.commit or st in site.short_commit):
                site.commit = st
            else:
                photon.m('Invalid git commit-id or tag specified for site', state=True)
        else:
            if tags[1]:
                site.tag = None
            else:
                site.branch = None

        photon.m(
            'generating site for %s' %(community),
            cmdd=dict(
                cmd='%s generate.py %s %s' %(settings['common']['pycmd'], community, '--nomodules' if not modules else ''),
                cwd=settings['site']['local'][community]
            ),
            verbose=True
        )

    gen_bconf(branch, target, gt, st, broken)

if __name__ == '__main__':
    from common import prepare_args

    args = prepare_args()
    prepare(args.branch, args.target, gt=args.gt, st=args.st, modules=args.modules, broken=args.broken)
