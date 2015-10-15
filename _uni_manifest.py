from os import path

from photon.util.files import read_file
from photon.util.locations import change_location

from common import pinit, uni_args


def uni_manifest(branch, manifest):
    '''
    After building the images, a manifest file gets created.

    :param branch: The branch currently building
    :param manifest: The path to the manifest file

    Before the manifest gets signed, this function is called to enable
    cross releasing of branches by clever symlinking.

    .. seealso:: :func:`common.uni_args` for command line syntax
    '''
    photon, settings = pinit('uni_manifest', verbose=True)

    manifest = path.abspath(manifest)
    manifest_content = read_file(manifest)
    if manifest_content and manifest_content.count('BRANCH=') == 1:

        uni_branch = '\n'.join(
            'BRANCH=%s' % (branch) for branch in sorted(
                settings['common']['branches']['avail'].keys()
            )
        )
        new_manifest = photon.template_handler(
            manifest_content.replace('BRANCH=%s' % (branch), '${uni_branch}'),
            fields=dict(uni_branch=uni_branch)
        )
        change_location(manifest, False, move=True)
        new_manifest.write(
            manifest.replace('%s.manifest' % (branch), 'manifest'),
            append=False
        )

        for branch in settings['common']['branches']['avail'].keys():
            manifest_link = manifest.replace(
                '%s.manifest' % (branch), '%s.manifest' % (branch)
            )

            change_location(manifest_link, False, move=True)
            photon.m(
                'linking manifests %s' % (manifest_link),
                cmdd=dict(
                    cmd='ln -s manifest %s' % (path.basename(manifest_link)),
                    cwd=path.dirname(manifest_link)
                )
            )

        photon.m(
            'uni_manifest written',
            more=dict(branch=branch),
            verbose=True
        )

    else:
        photon.m(
            'Refusing to write uni_manifest',
            more=dict(branch=branch, manifest=manifest),
            state=False
        )

if __name__ == '__main__':
    args = uni_args()
    uni_manifest(args.branch, args.manifest)
