
def gen_bconf(branch):
    from os import path
    from random import shuffle
    from photon.util.system import get_timestamp
    from photon.util.files import write_json
    from common import pinit, ginit

    p, s = pinit('gen_bconf')

    if p.settings.load('siteconf', path.join(s['site']['local']['wi'], 'meta.yaml')):
        p.s2m

        priority, version = s['siteconf']['site']['gluon_priority'], s['siteconf']['site']['gluon_release_num']
        gluon, site = ginit(p)
        desc = '%s-g_%s-s_%s' %(get_timestamp(), gluon.short_commit, site.short_commit)
        release = '%s-%s' %(version, desc)
        archive_dir = path.join(s['publish']['archive_dir'], '%s-%s-%s' %(version, branch, desc))
        shuffle(s['common']['communities'])

        fields=dict(
            archive_dir=archive_dir,
            autosign_key=s['publish']['autosign_key'],
            build_branch=s['common']['branches']['build'],
            build_dir=s['gluon']['local']['dir'],
            call_branch=branch,
            communities=' '.join(s['common']['communities']),
            info_file=s['prepare']['info'],
            mkcmd=s['common']['mkcmd'],
            priority=priority,
            pycmd=s['common']['pycmd'],
            release=release,
            stage_dir=s['prepare']['stage_dir']
        )
        write_json(path.join(s['prepare']['stage_dir'], s['prepare']['info']), dict(_info=fields))

        bconf = p.template_handler(s['prepare']['bconf']['tpl'], fields=fields)
        bconf.write(s['prepare']['bconf']['out'], append=False)

if __name__ == '__main__':
    from common import branch_args
    a = branch_args()

    gen_bconf(a.branch)
