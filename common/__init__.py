
from os import path
DEFAULTS = path.join(path.dirname(__file__), 'builder_defaults.yaml')

def pinit(mname, clean=False):

    from photon import Photon
    from photon.util.locations import search_location

    p = Photon(DEFAULTS, config=None, meta='builder_%s_meta.json' %(mname), verbose=True)
    s = p.settings.get

    p.meta.stage(search_location('builder_meta.json', create_in=s['prepare']['stage_dir']), clean=clean)
    return p, s

def sinit():

    from photon import Settings

    return Settings(DEFAULTS, config=None, verbose=True).get

def ginit(p, c='wi'):

    s = p.settings.get

    gluon = p.git_handler(s['gluon']['local'][c], remote_url=s['gluon']['remote'])
    site = p.git_handler(s['site']['local'][c], remote_url=s['site']['remote'])

    return gluon, site
