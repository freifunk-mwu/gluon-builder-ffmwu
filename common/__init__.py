'''
.. |mname| replace:: Name your initial meta file
.. |verbose| replace:: Set verbose flag of Photon instance
.. |argparse| replace:: :py:class:`argparse.ArgumentParser`  command line
'''

from os import path
DEFAULTS = path.join(path.dirname(__file__), 'builder_defaults.yaml')
from argparse import ArgumentParser

def _pinit(mname, verbose=True):
    '''
    We need the raw Photon instance without staging in :func:`publish`. Otherwise this is a helper for :func:`pinit`.

    :param mname: |mname|
    :param verbose: |verbose|
    '''
    from photon import Photon
    return Photon(DEFAULTS, config=None, meta='builder_%s_meta.json' %(mname), verbose=verbose)

def pinit(mname, clean=False, verbose=True):
    '''
    Creates a new Photon instance and stages into common stage dir defined in :ref:`defaults`.
    It is some subfolder of the httpd-dir, so you can see what's going on while building

    :param mname: |mname|
    :param clean: Starts a new meta file replacing the old one. Used in :func:`prepare`
    :param verbose: |verbose|
    :returns: a new :py:class:`photon.Photon` instance with it's :py:class:`settings.Settings` as tuple
    '''
    from photon.util.locations import change_location, search_location

    p = _pinit(mname, verbose)
    s = p.settings.get

    if clean: change_location(s['prepare']['stage_dir'], False, move=True)
    p.meta.stage(search_location('builder_meta.json', create_in=s['prepare']['stage_dir']), clean=clean)
    return p, s

def sinit(verbose=False):
    '''
    Creates a single :py:class:`settings.Settings` instance of Photon

    :param verbose: |verbose|
    :returns: the settings compiled from :ref:`defaults` as dictionary
    '''
    from photon import Settings

    return Settings(DEFAULTS, config=None, verbose=verbose).get

def ginit(p, c='wi'):
    '''
    Common git handler for Gluon and Site used by :func:`prepare` and :func:`_gen_bconf`

    :param p: A photon instance
    :param c: Short flag of community to use
    '''

    s = p.settings.get

    gluon = p.git_handler(s['gluon']['local'][c], remote_url=s['gluon']['remote'])
    site = p.git_handler(s['site']['local'][c], remote_url=s['site']['remote'])

    return gluon, site

def prepare_args():
    '''
    |argparse| for :func:`prepare`

    :param --branch -b: The branch to build
    :param --gt -g: A git commit-id or tag for gluon
    :param --st -s: A git commit-id or tag for site
    '''
    s = sinit()
    a = ArgumentParser(prog='gluon_builder_prepare', description='Prepare gluon builds', epilog='-.-')
    a.add_argument('--branch', '-b', action='store', choices=s['common']['branches']['avail'].keys(), default=s['common']['branches']['noarg'], help='The branch to build')
    a.add_argument('--gt', '-g', action='store', help='A git commit-id or tag for gluon')
    a.add_argument('--st', '-s', action='store', help='A git commit-id or tag for site')
    return a.parse_args()

def log_args():
    '''
    |argparse| for :func:`_build_logger`

    :param msg: The log message
    '''
    a = ArgumentParser(prog='gluon_builder_build_logger', description='do not launch manually', epilog='builder.sh needs this while building')
    a.add_argument('msg', action='store', help='The log message')
    return a.parse_args()

def uni_args():
    '''
    |argparse| for :func:`_uni_manifest`

    :param --branch -b: The branch the initial manifest was created
    :param --manifest -m: Path to the manifest file
    '''
    s = sinit()
    a = ArgumentParser(prog='gluon_builder_uni_manifest', description='Do not launch manually', epilog='builder.sh needs this while building')
    a.add_argument('--branch', '-b', action='store', required=True, choices=s['common']['branches']['avail'].keys(), help='The build branch')
    a.add_argument('--manifest', '-m', action='store', required=True, help='The manifest file')
    return a.parse_args()

def info_args():
    '''
    |argparse| for :func:`_gen_info`

    :param --images -i: Path to the images folder
    :param --ccmd -c: Checksumming command. calls ``$ccmd $image``
    '''
    a = ArgumentParser(prog='gluon_builder_gen_info', description='Do not launch manually', epilog='builder.sh needs this while building')
    a.add_argument('--images', '-i', action='store', required=True, help='The images folder')
    a.add_argument('--ccmd', '-c', action='store', help='The checksum executable')
    return a.parse_args()

def publish_args():
    '''
    |argparse| for :func:`publish`

    :param folder: Path to library folder containing build to publish
    :param --branch -b: The branch to publish as
    '''
    s = sinit()
    a = ArgumentParser(prog='gluon_builder_release', description='Release gluon builds', epilog='-.-')
    a.add_argument('folder', action='store', help='Path to library folder containing build to publish')
    a.add_argument('--branch', '-b', action='store', required=True, choices=s['common']['branches']['avail'].keys(), help='The release branch')
    return a.parse_args()
