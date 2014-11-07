
def args():
    from argparse import ArgumentParser

    a = ArgumentParser(prog='gluon_builder_gen_info', description='do not launch manually', epilog='builder.sh needs this while building', add_help=True)
    a.add_argument('--images', '-i', action='store', required=True, help='The images folder')
    a.add_argument('--sign', '-s', action='store', help='The sign executable')
    return a.parse_args()

def gen_info(images, sign):
    from os import path, listdir
    from photon.util.files import read_json, write_json
    from common import pinit

    p, s = pinit('gen_info', verbose=True)

    info = read_json(s['prepare']['r_inf'])

    images = path.abspath(images)
    for sp in ['factory', 'sysupgrade']:
        im = path.join(images, sp)
        if info and path.exists(im):
            for iname in listdir(im):
                model = iname.split('%s-' %(info['info']['release']))[-1].split('-%s.bin' %(sp))[0]
                checksum = p.m('signing %s' %(model), cmdd=dict(cmd='%s %s %s' %(path.abspath(sign), info['info']['autosign_key'], path.join(im, iname)))).get('out')

                info[model] = info.get(model, dict())
                info[model][sp] = dict(image=iname, checksum=checksum)

            write_json(path.join(images, 'info.json'), info)

    p.m('info generated', more=dict(images=images, info=info))

if __name__ == '__main__':
    a = args()

    gen_info(a.images, a.sign)
