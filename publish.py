#!/usr/bin/env python3

def publish(folder, branch):
    from os import path
    from photon.util.locations import search_location, change_location
    from common import pinit

    p, s = pinit('publish')

    folder = path.abspath(folder)
    if not s['publish']['library_dir'] == path.dirname(folder):
        p.m('wrong folder selected!', more=dict(folder=folder, should_be_subfolder_of=s['publish']['library_dir']), state=True)

    for community_s, community_l in s['common']['communities'].items():
        fulltgt = search_location(branch, create_in=path.join(s['publish']['http_fw_dir'], community_l))
        change_location(fulltgt, False, move=True)
        tgt = path.dirname(fulltgt)
        lnk = path.relpath(path.join(folder, community_s), tgt)

        p.m('linking release', cmdd=dict(cmd='ln -s %s %s' %(lnk, branch), cwd=tgt), more=dict(fulltgt=fulltgt))

if __name__ == '__main__':
    from common import publish_args

    a = publish_args()
    publish(a.folder, a.branch)
