
def build_logger(msg):
    '''
    This function starts a new photon instance to append a new message into the ``builder_meta.json`` file.
    It is used in :ref:`builder` to mark certain steps taken for validation of all actions done while compiling
    (remember: the resulting images need to get signed for the autoupdater to work)

    :param msg: The message to write into the meta file

    .. seealso:: :func:`common.log_args` for command line syntax
    '''

    from common import pinit

    pinit('build_logger', verbose=False)[0].m(msg, verbose=True)

if __name__ == '__main__':
    from common import log_args

    a = log_args()
    build_logger(a.msg)
