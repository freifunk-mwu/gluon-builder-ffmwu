
def gen_bconf(branch, gt=None, st=None):
    '''
    Provides all information needed by the builder in placing a ``bconf``-file.

    Since we are already collecting information here, the ``info.json`` is created as well.

    The same arguments as in :func:`prepare` are used here.

    .. seealso:: :func:`common.prepare_args` for command line syntax
    '''
    from os import path
    from photon.util.system import get_timestamp
    from photon.util.files import write_json
    from common import pinit, ginit

    photon, settings = pinit('gen_bconf')

    if photon.settings.load('siteconf', path.join(settings['site']['local']['wi'], settings['site']['generator_settings'])):
        photon.s2m

        priority = settings['siteconf']['site']['gluon_priority']
        version = settings['siteconf']['site']['gluon_release_num']
        gluon, site = ginit(photon)
        gt = gt if gt else gluon.short_commit[0]
        st = st if st else site.short_commit[0]

        desc = '-%s%s' %(branch, '-%s' %(get_timestamp(time=False)) if not all(settings['common']['branches']['avail'][branch]) else '')

        fields=dict(
            call_branch=branch,
            communities=' '.join(settings['common']['communities'].keys()),
            gluon_t=gt,
            site_t=st,
            priority=priority,
            release='%s%s' %(version, desc),
            version=version
        )
        write_json(path.join(settings['prepare']['stage_dir'], settings['prepare']['info']), dict(_info=fields))

        fields.update(dict(
            autosign_key=settings['publish']['autosign_key'],
            build_branch=settings['common']['branches']['build'],
            build_dir=settings['gluon']['local']['dir'],
            info_file=settings['prepare']['info'],
            library_dir=path.join(settings['publish']['library_dir'], '%s%s' %(version, desc)),
            mkcmd=settings['common']['mkcmd'],
            pycmd=settings['common']['pycmd'],
            stage_dir=settings['prepare']['stage_dir']
        ))

        bconf = photon.template_handler(settings['prepare']['bconf']['tpl'], fields=fields)
        bconf.write(settings['prepare']['bconf']['out'], append=False)

if __name__ == '__main__':
    from common import prepare_args

    args = prepare_args()
    gen_bconf(args.branch, gt=args.gt, st=args.st)
