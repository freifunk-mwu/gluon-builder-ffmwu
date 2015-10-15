from os import path

from photon.util.files import write_json
from photon.util.system import get_timestamp

from common import ginit, pinit, prepare_args


def gen_bconf(
    branch, targets, signkey,
    gluon_tag=None, site_tag=None,
    broken=False, onlyone=False, priority=None
):
    '''
    Provides all information needed by the builder in placing a ``bconf``-file.

    Since we are already collecting information here, the ``info.json``
    is created as well.

    The same arguments as in :func:`prepare` are used here.

    .. seealso:: :func:`common.prepare_args` for command line syntax
    '''
    photon, settings = pinit('gen_bconf')

    if photon.settings.load(
        'siteconf',
        path.join(
            settings['site']['local']['wi'],
            settings['site']['generator_settings']
        )
    ):
        photon.s2m

        gluon, site = ginit(photon)
        gluon_tag = gluon_tag if gluon_tag else gluon.short_commit[0]
        site_tag = site_tag if site_tag else site.short_commit[0]

        broken = '1' if broken else ''
        version = settings['siteconf']['site']['gluon_release_num']
        priority = (
            priority if priority
            else settings['siteconf']['site']['gluon_priority']
        )
        description = '-%s%s' % (
            branch, '-%s' % (get_timestamp(time=False)) if
            not all(settings['common']['branches']['avail'][branch])
            else ''
        )

        # these fields appear in the info.json
        fields = dict(
            broken_flag=broken,
            call_branch=branch,
            communities=onlyone if onlyone else ' '.join(
                settings['common']['communities'].keys()
            ),
            gluon_tag=gluon_tag,
            site_tag=site_tag,
            priority=priority,
            release='%s%s' % (version, description),
            targets=' '.join(targets),
            version=version
        )
        write_json(
            path.join(
                settings['prepare']['stage_dir'],
                settings['prepare']['info']
            ),
            dict(_info=fields)
        )

        # these fields only appear in the bconf
        fields.update(dict(
            build_branch=settings['common']['branches']['build'],
            build_dir=settings['gluon']['local']['dir'],
            info_file=settings['prepare']['info'],
            library_dir=path.join(
                settings['publish']['library_dir'],
                '%s%s' % (version, description)
            ),
            mkcmd=settings['common']['mkcmd'],
            pycmd=settings['common']['pycmd'],
            signkey=signkey,
            stage_dir=settings['prepare']['stage_dir']
        ))

        bconf = photon.template_handler(
            settings['prepare']['bconf']['tpl'],
            fields=fields
        )
        bconf.write(
            settings['prepare']['bconf']['out'],
            append=False
        )

if __name__ == '__main__':
    args = prepare_args()
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
