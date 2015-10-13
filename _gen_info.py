from os import listdir, path

from photon.util.files import read_json, write_json

from common import info_args, pinit


def gen_info(images, ccmd, start=None, finish=None):
    '''
    Before the build gets started, :ref:`bconf` starts the ``info.json``
    with some general information.
    It's purpose is to provide a single file to easily include links to the
    latest firmware in foreign websites.

    This file gets extended here, to hold a dictionary mapping each
    router-model (keys) to appropriate `factory` and `sysupgrade` image
    files with checksums.

    To produce checksums, gluon's ``scripts/sha512sum.sh`` is used.
    It is possible to change this using the ``-c`` command line flag.

    .. seealso:: :func:`common.info_args` for command line syntax
    '''
    photon, settings = pinit('gen_info', verbose=True)

    info = read_json(path.join(
        settings['prepare']['stage_dir'],
        settings['prepare']['info']
    ))
    images = path.abspath(images)

    if start and finish:
        info['_build_duration'] = abs(int(finish) - int(start))

    for sp in ['factory', 'sysupgrade']:
        im = path.join(images, sp)
        if info and path.exists(im):
            for imgname in listdir(im):
                model = imgname.split(
                    '%s-' % (info['_info']['release'])
                )[-1].split(
                    '-%s.bin' % (sp)
                )[0].split(
                    '.bin'
                )[0]

                checksum = photon.m(
                    'checksumming %s' % (model),
                    cmdd=dict(
                        cmd='%s %s' % (
                            path.abspath(ccmd),
                            path.join(im, imgname)
                        )
                    )
                ).get('out')

                info[model] = info.get(model, dict())
                info[model][sp] = dict(image=imgname, checksum=checksum)

            write_json(path.join(images, settings['prepare']['info']), info)

    photon.m('info generated', more=dict(images=images, info=info))


if __name__ == '__main__':
    args = info_args()
    gen_info(args.images, args.ccmd)
