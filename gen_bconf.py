
def gen_bconf():
    from os import path
    from photon.util.system import get_timestamp
    from common import pinit, ginit

    p, s = pinit('gen_bconf')

    if p.settings.load('siteconf', path.join(s['site']['local']['wi'], 'meta.yaml')):

        priority, release = s['siteconf']['site']['gluon_priority'], s['siteconf']['site']['gluon_release_num']
        gluon, site = ginit(p)
        release = '%s-%s-g_%s-s_%s' %(release, get_timestamp(), gluon.short_commit, site.short_commit)

        bconf = p.template_handler(
            s['prepare']['bconf']['tpl'],
            fields=dict(
                archive_dir=s['publish']['archive_dir'],
                autosign_key=s['publish']['autosign_key'],
                build_branch=s['common']['branches']['build'],
                build_dir=s['gluon']['local']['dir'],
                communities=' '.join(s['common']['communities']),
                mkcmd=s['common']['mkcmd'],
                priority=priority,
                pycmd=s['common']['pycmd'],
                release=release,
                stage_dir=s['prepare']['stage_dir']
            )
        )
        bconf.write(s['prepare']['bconf']['out'], append=False)

        p.s2m


if __name__ == '__main__':
    gen_bconf()
