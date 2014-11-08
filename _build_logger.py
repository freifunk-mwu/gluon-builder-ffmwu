
def build_logger(msg):
    from common import pinit

    pinit('build_logger', verbose=False)[0].m(msg, verbose=True)

if __name__ == '__main__':
    from common import log_args

    a = log_args()
    build_logger(a.msg)
