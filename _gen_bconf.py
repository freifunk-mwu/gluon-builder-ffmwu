
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

    p, s = pinit('gen_bconf')

    if p.settings.load('siteconf', path.join(s['site']['local']['wi'], s['site']['generator_settings'])):
        p.s2m

        priority, version = s['siteconf']['site']['gluon_priority'], s['siteconf']['site']['gluon_release_num']
        gluon, site = ginit(p)
        gt = gt if gt else gluon.short_commit[0]
        st = st if st else site.short_commit[0]

        desc = '-%s' %(get_timestamp(time=False)) if not all(s['common']['branches']['avail'][branch]) else ''

        fields=dict(
            call_branch=branch,
            communities=' '.join(s['common']['communities'].keys()),
            gluon_t=gt,
            site_t=st,
            priority=priority,
            release='%s%s' %(version, desc),
            version=version
        )
        write_json(path.join(s['prepare']['stage_dir'], s['prepare']['info']), dict(_info=fields))
        fields.update(dict(
            autosign_key=s['publish']['autosign_key'],
            build_branch=s['common']['branches']['build'],
            build_dir=s['gluon']['local']['dir'],
            info_file=s['prepare']['info'],
            library_dir=path.join(s['publish']['library_dir'], '%s-%s%s' %(version, branch, desc)),
            mkcmd=s['common']['mkcmd'],
            pycmd=s['common']['pycmd'],
            stage_dir=s['prepare']['stage_dir']
        ))

        bconf = p.template_handler(s['prepare']['bconf']['tpl'], fields=fields)
        bconf.write(s['prepare']['bconf']['out'], append=False)

if __name__ == '__main__':
    from common import prepare_args

    a = prepare_args()
    gen_bconf(a.branch, a.gt, a.st)
