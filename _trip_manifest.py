
def args():
    from argparse import ArgumentParser
    from common import sinit

    s = sinit()
    a = ArgumentParser(prog='gluon_builder_trip_manifest', description='do not launch manually', epilog='builder.sh needs this while building', add_help=True)
    a.add_argument('--branch', '-b', action='store', choices=s['common']['branches']['avail'].keys(), help='the build branch')
    a.add_argument('--manifest', '-m', action='store', help='the manifest file')
    return a.parse_args()

def trip_manifest(branch, manifest):
    from os import path
    from photon.util.files import read_file
    from photon.util.locations import change_location
    from common import pinit

    p, s = pinit('trip_manifest', verbose=True)

    manifest = path.abspath(manifest)
    mf = read_file(manifest)
    if mf and mf.count('BRANCH=') == 1:

        trip_branch = '\n'.join('BRANCH=%s' %(branch) for branch in sorted(s['common']['branches']['avail'].keys()))
        info_branch = '\n# '.join(i for i in ['sources: %s' %(branch), 'build: %s' %(s['common']['branches']['build'])])
        m = p.template_handler(
            mf.replace('BRANCH=%s' %(branch), '${trip_branch}\n# ${info_branch}'),
            fields=dict(
                trip_branch=trip_branch,
                info_branch=info_branch,
            )
        )
        change_location(manifest, False, move=True)
        m.write(manifest.replace('%s.manifest' %(branch), 'manifest'), append=False)

        for b in s['common']['branches']['avail'].keys():
            ml = manifest.replace('%s.manifest' %(branch), '%s.manifest' %(b))

            change_location(ml, False, move=True)
            p.m(
                'linking manifests %s' %(ml),
                cmdd=dict(cmd='ln -s manifest %s' %(path.basename(ml)), cwd=path.dirname(ml))
            )

        p.m('trip_manifest written', more=dict(branch=branch), verbose=True)

if __name__ == '__main__':
    a = args()
    trip_manifest(a.branch, a.manifest)
