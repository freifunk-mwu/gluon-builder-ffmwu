
gluon-builder-ffmwu
-------------------

This software is written by Members of `Freifunk Mainz, Wiesbaden und Umgebung <http://freifunk-mwu.de/>`_ to provide an automated mechanism compiling the fabulous `Gluon <http://github.com/freifunk-gluon/gluon>`_ firmware..

Since we accomplish to provide multiple mesh networks for multiple (sub-) communities over just one Gateway-Server in parallel (there are however multiple Gateway-Servers to gain redundancy) this software helps us to compile multiple gluon releases fitting to the configuration of the communities.

Contributions are highly welcome, also feel free to use the `issue tracker <http://github.com/freifunk-mwu/gluon-builder-ffmwu/issue>`_ if you encounter any problems.

:Repository: `github.com/freifunk-mwu/gluon-builder-ffmwu <http://github.com/freifunk-mwu/gluon-builder-ffmwu/>`_
:Documentation: `gluon-builder-doku.readthedocs.org <http://gluon-builder-doku.readthedocs.org/en/latest/>`_

Structure
---------

The core is implemented as a shell script (``builder.sh``) - it depends heavily on it's helper scripts - written in Python 3. The helper scripts all are using `photon <http://github/spookey/photon>`_ as a backend for easy and quick programming.

Install all dependencies at once using pip and the ``requirements.txt``::

    $ pip3 install -r requirements.txt
