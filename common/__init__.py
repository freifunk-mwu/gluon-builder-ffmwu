
from os import path
DEFAULTS = path.join(path.dirname(__file__), 'builder_defaults.yaml')
from argparse import ArgumentParser

def pinit(mname, clean=False, verbose=True):

    from photon import Photon
    from photon.util.locations import change_location, search_location

    p = Photon(DEFAULTS, config=None, meta='builder_%s_meta.json' %(mname), verbose=verbose)
    s = p.settings.get

    if clean: change_location(s['prepare']['stage_dir'], False, move=True)
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

def prepare_args():
    s = sinit()
    a = ArgumentParser(prog='gluon_builder_prepare', description='Prepare gluon builds', epilog='-.-')
    a.add_argument('--branch', '-b', action='store', choices=s['common']['branches']['avail'].keys(), default=s['common']['branches']['noarg'], help='The branch to build')
    a.add_argument('--gt', '-g', action='store', help='A git commit-id or tag for gluon')
    a.add_argument('--st', '-s', action='store', help='A git commit-id or tag for site')
    return a.parse_args()

def log_args():
    a = ArgumentParser(prog='gluon_builder_build_logger', description='do not launch manually', epilog='builder.sh needs this while building')
    a.add_argument('msg', action='store', help='The log message')
    return a.parse_args()

def uni_args():
    s = sinit()
    a = ArgumentParser(prog='gluon_builder_uni_manifest', description='Do not launch manually', epilog='builder.sh needs this while building')
    a.add_argument('--branch', '-b', action='store', required=True, choices=s['common']['branches']['avail'].keys(), help='The build branch')
    a.add_argument('--manifest', '-m', action='store', required=True, help='The manifest file')
    return a.parse_args()

def info_args():
    a = ArgumentParser(prog='gluon_builder_gen_info', description='Do not launch manually', epilog='builder.sh needs this while building')
    a.add_argument('--images', '-i', action='store', required=True, help='The images folder')
    a.add_argument('--ccmd', '-c', action='store', help='The checksum executable')
    return a.parse_args()

def publish_args():
    s = sinit()
    a = ArgumentParser(prog='gluon_builder_release', description='Release gluon builds', epilog='-.-')
    a.add_argument('folder', action='store', help='The folder from the library containing the builds')
    a.add_argument('--branch', '-b', action='store', required=True, choices=s['common']['branches']['avail'].keys(), help='The release branch')
    return a.parse_args()
