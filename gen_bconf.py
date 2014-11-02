
def gen_bconf(branch):
    from os import path
    from random import shuffle
    from photon.util.system import get_timestamp
    from common import pinit, ginit

    p, s = pinit('gen_bconf')

    if p.settings.load('siteconf', path.join(s['site']['local']['wi'], 'meta.yaml')):

        priority, version = s['siteconf']['site']['gluon_priority'], s['siteconf']['site']['gluon_release_num']
        gluon, site = ginit(p)

        release = '%s-%s-g_%s-s_%s' %(version, get_timestamp(), gluon.short_commit, site.short_commit)

        communities = s['common']['communities']
        shuffle(communities)

        bconf = p.template_handler(
            s['prepare']['bconf']['tpl'],
            fields=dict(
                archive_dir=s['publish']['archive_dir'],
                autosign_key=s['publish']['autosign_key'],
                build_branch=s['common']['branches']['build'],
                build_dir=s['gluon']['local']['dir'],
                callbranch=branch,
                communities=' '.join(communities),
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
    from common import branch_args
    a = branch_args()

    gen_bconf(a.branch)
