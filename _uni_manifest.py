
def uni_manifest(branch, manifest):
    from os import path
    from photon.util.files import read_file
    from photon.util.locations import change_location
    from common import pinit

    p, s = pinit('uni_manifest', verbose=True)

    manifest = path.abspath(manifest)
    mf = read_file(manifest)
    if mf and mf.count('BRANCH=') == 1:

        uni_branch = '\n'.join('BRANCH=%s' %(branch) for branch in sorted(s['common']['branches']['avail'].keys()))
        m = p.template_handler(
            mf.replace('BRANCH=%s' %(branch), '${uni_branch}'),
            fields=dict(uni_branch=uni_branch)
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

        p.m('uni_manifest written', more=dict(branch=branch), verbose=True)

if __name__ == '__main__':
    from common import uni_args

    a = uni_args()
    uni_manifest(a.branch, a.manifest)
