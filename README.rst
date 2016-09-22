DEPRECATED
==========

This gluon builder is deprecated. We use the build-scripts in https://github.com/freifunk-mwu/sites-ffmwu instead.

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

Installation
------------

Steps were taken on a fresh Ubuntu 14.10 Desktop

To get going you should first install the packages needed for the builder::

    $ sudo aptitude install git python3-pip

Then install the builder by cloning it anywhere (in your home-folder) and installing the requirements::

    $ git clone http://github.com/freifunk-mwu/gluon-builder-ffmwu.git ~/clones/gluon-builder
    $ cd ~/clones/gluon-builder
    $ sudo pip3 install -r requirements.txt -U

To actually compile gluon, you need some more packages::

    $ sudo aptitude install build-essential subversion libncurses5-dev zlib1g-dev gawk

Then check the output locations (``['publish']['http_root_dir']`` in ``common/defaults.yaml``) and make then writable for your user or change them.
Now your are ready to build the first experimental::

    ./builder.sh

See ``./prepare.py --help`` for furher options (``builder.sh`` calls ``prepare.py``, so they share the same arguments..)
