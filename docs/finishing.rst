
Postbuild
=========

.. _info:

_gen_info.py
------------

.. automodule:: _gen_info
    :members:
    :undoc-members:
    :private-members:

The common starting point is the ``info.json`` in the stage::

    /var/www/html/_stage/info.json

For each community, this file gets extended and is written to the ``images`` directory from gluon::

    ~/gluon_builder/${community}/images/info.json

After building is done as well as copying produced files the ``info.json`` files are located under::

    /var/www/html/firmware/_library/${release}/${community}/info.json

So after setting symlinks with :ref:`publish`, the ``info.json`` of the latest stable could also be accessed using::

    /var/www/html/firmware/${community}/stable/info.json

E.g. this results in (depending of the webserver's configuration):

    http://firmware.freifunk-mwu.de/wiesbaden/stable/info.json

.. _publish:

publish.py
----------

.. automodule:: publish
    :members:
    :undoc-members:
    :private-members:
