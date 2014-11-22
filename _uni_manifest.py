
def uni_manifest(branch, manifest):
    '''
    After building the images, a manifest file gets created.

    :param branch: The branch currently building
    :param manifest: The path to the manifest file

    .. seealso:: :func:`common.uni_args`

    Before it gets signed, this function is called to enable cross releasing of branches by clever symlinking.

    It opens specified `manifest`-file and replaces::

        BRANCH=$branch

    by::

        BRANCH=experimental
        BRANCH=beta
        BRANCH=stable

    then it saves it as `manifest` and symlinks `experimental.manifest`, `beta.manifest` and `stable.manifest` to it.

    (This example assumes the branch names are left to the default values in :ref:`defaults`)

    .. seealso:: :func:`common.uni_args`
    '''

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
    else: p.m('Refusing to write uni_manifest', more=dict(branch=branch, manifest=manifest), state=False)

if __name__ == '__main__':
    from common import uni_args

    a = uni_args()
    uni_manifest(a.branch, a.manifest)
