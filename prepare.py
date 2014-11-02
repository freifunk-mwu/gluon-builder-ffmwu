
def args():
    from argparse import ArgumentParser
    from common import sinit

    s = sinit()

    a = ArgumentParser(prog='gluon_builder', description='you must specify a branch', epilog='-.-', add_help=True)
    a.add_argument('--branch', '-b', action='store', choices=s['common']['branches']['avail'].keys(), default=s['common']['branches']['noarg'])
    return a.parse_args()


def prepare(branch):
    from common import pinit, ginit
    from photon.util.locations import change_location
    from gen_bconf import gen_bconf

    p, s = pinit('prepare', clean=True)
    for community in s['common']['communities']:
        change_location(s['gluon']['local'][community], False, move=True)
        tags = s['common']['branches']['avail'][branch]
        gluon, site = ginit(p, community)

        if tags[0]: gluon.tag = None
        else: gluon.branch = None

        if tags[1]: site.tag = None
        else: site.branch = None

        p.m('generating site for %s' %(community), cmdd=dict(cmd='%s generate.py %s --nomodules' %(s['common']['pycmd'], community), cwd=s['site']['local'][community]), verbose=True)

    gen_bconf()

if __name__ == '__main__':
    a = args()

    prepare(a.branch)
