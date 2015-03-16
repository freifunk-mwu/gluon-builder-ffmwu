
Preparing the build
===================

.. _prepare:

prepare.py
----------

.. automodule:: prepare
    :members:
    :undoc-members:
    :private-members:

First, a so called stage gets created. This acts as a place where to store common and log-files while building.
The location of the stage can be configured as ``['prepare']['stage_dir']`` and should be a subfolder of  ``['publish']['http_root_dir']``, one of your httpd served folders::

    /var/www/html -> ['publish']['http_root_dir']
    /var/www/html/_stage

Most important file in the stage is the ``builder_meta.json`` - every photon helper script uses this as logfile. :ref:`logger` is used in the shell part

The topmost working dir ``~/gluon_builder`` can be configured as ``['gluon']['local']['dir']`` in :ref:`defaults` ::

    ~/gluon_builder
    ~/gluon_builder/mz -> gluon checkout for Mainz
    ~/gluon_builder/mz/site -> site checkout for Mainz
    ~/gluon_builder/wi -> gluon checkout for Wiesbaden
    ~/gluon_builder/wi/site -> site checkout for Wiesbaden

Then it creates the siteconf for each community resulting in the files::

    ~/gluon_builder/${community}/site/site.conf
    ~/gluon_builder/${community}/site/site.mk
    ~/gluon_builder/${community}/site/modules (if the site-generator is not called with --nomodules)

.. seealso:: our generator in the `site-ffmwu repository <http://github.com/freifunk-mwu/site-ffmwu>`_

.. _bconf:

_gen_bconf.py
-------------

.. automodule:: _gen_bconf
    :members:
    :undoc-members:
    :private-members:

The purpose of this helper is to pass information to the :ref:`builder`. This is done by placing a ``bconf`` (see :ref:`bconf_tpl` for contents).
After this is done, you should have two new files::

    ~/clones/gluon-builder-ffmwu/bconf
    /var/www/html/_stage/info.json

The json file in the stage is further processed later in :ref:`info`. It's purpose is to provide a single file to easily include links to the latest firmware in foreign websites. At this stage it only contains a header

For example from our first stable release:

.. code-block:: json
    :linenos:

    {
        "_info": {
            "broken_flag": "",
            "call_branch": "stable",
            "communities": "wi mz",
            "gluon_t": "b7187df",
            "priority": "0.2",
            "release": "0.0.1-stable",
            "site_t": "8534e28",
            "version": "0.0.1"
        }
    }

.. _bconf_tpl:

bconf.tpl
^^^^^^^^^

.. literalinclude:: ../common/bconf.tpl
    :language: bash
    :linenos:
