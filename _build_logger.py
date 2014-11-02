
def args():
    from argparse import ArgumentParser

    a = ArgumentParser(prog='gluon_builder_build_logger', description='do not launch manually', epilog='builder.sh needs this while building', add_help=True)
    a.add_argument('msg', action='store', help='the log message')
    return a.parse_args()

def mlog(msg):
    from common import pinit

    p, s = pinit('build_logger', verbose=False)
    p.m(msg, verbose=True)

if __name__ == '__main__':
    a = args()
    mlog(a.msg)
