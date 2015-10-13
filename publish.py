#!/usr/bin/env python3
from os import path

from photon.util.locations import change_location

from common import _pinit, publish_args


def publish(folder, branch):
    '''
    Publishes freshly built images. This is accomplished by setting symbolic-links in the form of ``communitiy``/``branch`` pointing into the library (in the form of _library/``build``-``branch``/``short-community``)

    .. seealso:: :func:`common.uni_args` for command line syntax
    '''
    photon = _pinit('publish')
    settings = photon.settings.get

    folder = path.realpath(folder)
    if not settings['publish']['library_dir'] == path.dirname(folder):
        photon.m(
            'wrong folder selected!',
            more=dict(
                folder=folder,
                should_be_subfolder_of=settings['publish']['library_dir']
            ),
            state=True
        )

    for community_s, community_l in settings['common']['communities'].items():
        fulltgt = path.join(
            settings['publish']['http_fw_dir'],
            community_l,
            branch
        )
        change_location(fulltgt, False, move=True)
        tgt = path.dirname(fulltgt)
        lnk = path.relpath(path.join(folder, community_s), tgt)

        photon.m(
            'linking release',
            cmdd=dict(
                cmd='ln -s %s %s' % (lnk, branch),
                cwd=tgt
            ),
            more=dict(fulltgt=fulltgt)
        )

if __name__ == '__main__':
    args = publish_args()
    publish(args.folder, args.branch)
