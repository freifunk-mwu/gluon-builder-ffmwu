'''
.. |mname| replace:: Name your initial meta file
.. |verbose| replace:: Set verbose flag of Photon instance
.. |argparse| replace:: :py:class:`argparse.ArgumentParser` command line
'''

from argparse import ArgumentParser
from os import path

from photon import Photon, Settings
from photon.util.locations import change_location, search_location

DEFAULTS = path.join(path.dirname(__file__), 'builder_defaults.yaml')


def _pinit(mname, verbose=True):
    '''
    We need the raw Photon instance without staging in :func:`publish`. Otherwise this is a helper for :func:`pinit`.

    :param mname: |mname|
    :param verbose: |verbose|
    '''
    return Photon(
        DEFAULTS,
        config=None,
        meta='builder_%s_meta.json' % (mname),
        verbose=verbose
    )


def pinit(mname, clean=False, verbose=True):
    '''
    Creates a new Photon instance and stages into common stage dir defined in :ref:`defaults`.
    It is some subfolder of the httpd-dir, so you can see what's going on while building

    :param mname: |mname|
    :param clean: Starts a new meta file replacing the old one. Used in :func:`prepare`
    :param verbose: |verbose|
    :returns: a new :py:class:`photon.Photon` instance with it's :py:class:`settings.Settings` as tuple
    '''
    photon = _pinit(mname, verbose)
    settings = photon.settings.get

    if clean:
        change_location(settings['prepare']['stage_dir'], False, move=True)

    photon.meta.stage(
        search_location(
            'builder_meta.json',
            create_in=settings['prepare']['stage_dir']
        ),
        clean=clean
    )
    return photon, settings


def sinit(verbose=False):
    '''
    Creates a single :py:class:`settings.Settings` instance of Photon

    :param verbose: |verbose|
    :returns: the settings compiled from :ref:`defaults` as dictionary
    '''
    return Settings(
        DEFAULTS,
        config=None,
        verbose=verbose
    ).get


def ginit(photon, community='wi'):
    '''
    Common git handler for Gluon and Site used by :func:`prepare` and :func:`_gen_bconf`

    :param p: A photon instance
    :param c: Short flag of community to use
    '''
    settings = photon.settings.get

    gluon = photon.git_handler(
        settings['gluon']['local'][community],
        remote_url=settings['gluon']['remote']
    )
    site = photon.git_handler(
        settings['site']['local'][community],
        remote_url=settings['site']['remote']
    )
    return gluon, site


def prepare_args():
    '''
    |argparse| for :func:`prepare`

    :param --branch -b: The branch to build
    :param --target -t: Specify a list of GLUON_TARGETs to build
    :param --gt -g: A git commit-id or tag for gluon
    :param --st -s: A git commit-id or tag for site
    :param --broken: Build experimental images even for unsupported (broken) hardware
    :param --signkey: Specify location to a key to sign the images
    :param --nomodules: Prevent building modules (will be passed to siteconf generator)
    :param --oneonly: Just build images for specified community (only used for testing purposes)
    '''
    settings = sinit()
    args = ArgumentParser(
        prog='gluon_builder_prepare',
        description='Prepare gluon builds',
        epilog='-.-'
    )
    args.add_argument(
        '--branch', '-b',
        action='store',
        choices=settings['common']['branches']['avail'].keys(),
        default=settings['common']['branches']['noarg'],
        help='The branch to build'
    )
    args.add_argument(
        '--targets', '-t',
        action='store',
        nargs='+',
        default=settings['common']['targets'],
        help='The GLUON_TARGETs to build'
    )
    args.add_argument(
        '--gt', '-g',
        action='store',
        help='A git commit-id or tag for gluon'
    )
    args.add_argument(
        '--st', '-s',
        action='store',
        help='A git commit-id or tag for site'
    )
    args.add_argument(
        '--broken',
        action='store_true',
        help='Build also models which are flagged as broken'
    )
    args.add_argument(
        '--signkey',
        action='store',
        default=settings['publish']['autosign_key']
    )
    args.add_argument(
        '--nomodules',
        action='store_true',
        help='Do not prepare modules in siteconf generator'
    )
    args.add_argument(
        '--oneonly', '-oo',
        action='store',
        choices=settings['common']['communities'].keys(),
        help='Build only one Community, skip the other'
    )
    return args.parse_args()


def log_args():
    '''
    |argparse| for :func:`_build_logger`

    :param msg: The log message
    '''
    args = ArgumentParser(
        prog='gluon_builder_build_logger',
        description='do not launch manually',
        epilog='builder.sh needs this while building'
    )
    args.add_argument(
        'msg',
        action='store',
        help='The log message'
    )
    return args.parse_args()


def uni_args():
    '''
    |argparse| for :func:`_uni_manifest`

    :param --branch -b: The branch the initial manifest was created
    :param --manifest -m: Path to the manifest file
    '''
    settings = sinit()
    args = ArgumentParser(
        prog='gluon_builder_uni_manifest',
        description='Do not launch manually',
        epilog='builder.sh needs this while building'
    )
    args.add_argument(
        '--branch', '-b',
        action='store',
        required=True,
        choices=settings['common']['branches']['avail'].keys(),
        help='The build branch'
    )
    args.add_argument(
        '--manifest', '-m',
        action='store',
        required=True,
        help='The manifest file'
    )
    return args.parse_args()


def info_args():
    '''
    |argparse| for :func:`_gen_info`

    :param --images -i: Path to the images folder
    :param --ccmd -c: Checksumming command. calls ``$ccmd $image``
    :param --start: Calculates build duration if passed together with ``--finish``
    :param --finish: Calculates build duration if passed together with ``--start``
    '''
    args = ArgumentParser(
        prog='gluon_builder_gen_info',
        description='Do not launch manually',
        epilog='builder.sh needs this while building'
    )
    args.add_argument(
        '--images', '-i',
        action='store',
        required=True,
        help='The images folder'
    )
    args.add_argument(
        '--ccmd', '-c',
        action='store',
        help='The checksum executable'
    )
    args.add_argument(
        '--start',
        action='store',
        help='give me a date to calculate statistics'
    )
    args.add_argument(
        '--finish',
        action='store',
        help='give me a date to calculate statistics'
    )
    return args.parse_args()


def publish_args():
    '''
    |argparse| for :func:`publish`

    :param folder: Path to library folder containing build to publish
    :param --branch -b: The branch to publish as
    '''
    settings = sinit()
    args = ArgumentParser(
        prog='gluon_builder_release',
        description='Release gluon builds',
        epilog='-.-'
    )
    args.add_argument(
        'folder',
        action='store',
        help='Path to library folder containing build to publish'
    )
    args.add_argument(
        '--branch', '-b',
        action='store',
        required=True,
        choices=settings['common']['branches']['avail'].keys(),
        help='The release branch'
    )
    return args.parse_args()
