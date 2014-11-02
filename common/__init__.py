
from os import path
DEFAULTS = path.join(path.dirname(__file__), 'builder_defaults.yaml')

def pinit(mname, clean=False, verbose=True):

    from photon import Photon
    from photon.util.locations import search_location

    p = Photon(DEFAULTS, config=None, meta='builder_%s_meta.json' %(mname), verbose=verbose)
    s = p.settings.get

    p.meta.stage(search_location('builder_meta.json', create_in=s['prepare']['stage_dir']), clean=clean)
    return p, s

def sinit(verbose=False):

    from photon import Settings

    return Settings(DEFAULTS, config=None, verbose=verbose).get

def ginit(p, c='wi'):

    s = p.settings.get

    gluon = p.git_handler(s['gluon']['local'][c], remote_url=s['gluon']['remote'])
    site = p.git_handler(s['site']['local'][c], remote_url=s['site']['remote'])

    return gluon, site

def branch_args():
    from argparse import ArgumentParser

    s = sinit()

    a = ArgumentParser(prog='gluon_builder', description='you must specify a branch', epilog='-.-', add_help=True)
    a.add_argument('--branch', '-b', action='store', choices=s['common']['branches']['avail'].keys(), default=s['common']['branches']['noarg'])
    return a.parse_args()
