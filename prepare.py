#!/usr/bin/env python3

from _gen_bconf import gen_bconf
from common import ginit, pinit, prepare_args
from photon.util.locations import change_location


def prepare(
    branch,
    gluon_tag=None, site_tag=None,
    nomodules=False, onlyone=False, priority=None
):
    '''
    Checks out Gluon sources and site-conf repositories at proper commit-ids
    or tags according to the branch to build.
    Generates a site-conf afterwards.
    Automatically invokes :func:`_gen_bconf` afterwards

    .. seealso:: :func:`common.prepare_args` for command line syntax
    '''
    photon, settings = pinit('prepare', clean=True)

    for community in [
        onlyone
    ] if onlyone else settings['common']['communities'].keys():

        change_location(
            settings['gluon']['local'][community],
            False,
            move=True
        )
        tags = settings['common']['branches']['avail'][branch]
        gluon, site = ginit(photon, community=community)

        if gluon_tag:
            if gluon.tag and gluon_tag in gluon.tag:
                gluon.tag = gluon_tag
            elif gluon.commit and (
                gluon_tag in gluon.commit or gluon_tag in gluon.short_commit
            ):
                gluon.commit = gluon_tag
            else:
                photon.m(
                    'Invalid git commit-id or tag specified for gluon',
                    state=True
                )
        else:
            if tags[0]:
                gluon.tag = None
            else:
                gluon.branch = None

        if site_tag:
            if site.tag and site_tag in site.tag:
                site.tag = site_tag
            elif site.commit and (
                site_tag in site.commit or site_tag in site.short_commit
            ):
                site.commit = site_tag
            else:
                photon.m(
                    'Invalid git commit-id or tag specified for site',
                    state=True
                )
        else:
            if tags[1]:
                site.tag = None
            else:
                site.branch = None

        photon.m(
            'generating site for %s' % (community),
            cmdd=dict(
                cmd='%s generate.py %s %s %s' % (
                    settings['common']['pycmd'],
                    community,
                    '--nomodules' if nomodules else '',
                    '--priority %s' % (priority) if priority else ''
                ),
                cwd=settings['site']['local'][community]
            ),
            verbose=True
        )

if __name__ == '__main__':
    args = prepare_args()
    prepare(
        args.branch,
        gluon_tag=args.gluon_tag,
        site_tag=args.site_tag,
        nomodules=args.nomodules,
        onlyone=args.onlyone,
        priority=args.priority
    )
    gen_bconf(
        args.branch,
        args.targets,
        args.signkey,
        gluon_tag=args.gluon_tag,
        site_tag=args.site_tag,
        broken=args.broken,
        onlyone=args.onlyone,
        priority=args.priority
    )
