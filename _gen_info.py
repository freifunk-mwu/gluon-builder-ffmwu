from os import listdir, path

from common import info_args, pinit
from photon.util.files import read_json, write_json


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
        try:
            seconds = abs(int(finish) - int(start))
        except (TypeError, ValueError):
            seconds = None
        if seconds:
            info['_info']['build_seconds'] = seconds
            build_time = []
            for name, val in [
                ('d', 60*60*24),
                ('h', 60*60),
                ('m', 60),
                ('s', 1)
            ]:
                if seconds > val:
                    pval, seconds = divmod(seconds, val)
                    build_time.append('%d%s' % (pval, name))
            info['_info']['build_time'] = ' '.join(build_time)

    for variety in ['factory', 'sysupgrade']:
        image_dir = path.join(images, variety)
        if info and path.exists(image_dir):
            for image_name in [
                i for i in listdir(image_dir) if not i.endswith('manifest')
            ]:
                model = image_name.split(
                    '%s-' % (info['_info']['release'])
                )[-1].split(
                    '-%s.bin' % (variety)
                )[0].split(
                    '.bin'
                )[0]

                checksum = photon.m(
                    'checksumming %s' % (model),
                    cmdd=dict(
                        cmd='%s %s' % (
                            path.abspath(ccmd),
                            path.join(image_dir, image_name)
                        )
                    )
                ).get('out')

                info[model] = info.get(model, dict())
                info[model][variety] = dict(
                    image=image_name,
                    checksum=checksum
                )

            write_json(path.join(images, settings['prepare']['info']), info)

    photon.m('info generated', more=dict(images=images, info=info))


if __name__ == '__main__':
    args = info_args()
    gen_info(args.images, args.ccmd, start=args.start, finish=args.finish)
