
def args():
    from argparse import ArgumentParser

    a = ArgumentParser(prog='gluon_builder_gen_info', description='do not launch manually', epilog='builder.sh needs this while building', add_help=True)
    a.add_argument('--images', '-i', action='store', required=True, help='The images folder')
    a.add_argument('--ccmd', '-c', action='store', help='The checksum executable')
    return a.parse_args()

def gen_info(images, ccmd):
    from os import path, listdir
    from photon.util.files import read_json, write_json
    from common import pinit

    p, s = pinit('gen_info', verbose=True)

    info = read_json(path.join(s['prepare']['stage_dir'], s['prepare']['info']))
    images = path.abspath(images)

    for sp in ['factory', 'sysupgrade']:
        im = path.join(images, sp)
        if info and path.exists(im):
            for iname in listdir(im):
                model = iname.split('%s-' %(info['_info']['release']))[-1].split('-%s.bin' %(sp))[0]
                checksum = p.m('checksumming %s' %(model), cmdd=dict(cmd='%s %s' %(path.abspath(ccmd), path.join(im, iname)))).get('out')

                info[model] = info.get(model, dict())
                info[model][sp] = dict(image=iname, checksum=checksum)

            write_json(path.join(images, s['prepare']['info']), info)

    p.m('info generated', more=dict(images=images, info=info))

if __name__ == '__main__':
    a = args()

    gen_info(a.images, a.ccmd)
