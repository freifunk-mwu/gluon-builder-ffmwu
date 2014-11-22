.. include:: shared.rst

Tools while building
====================

.. _common:

common
------

|common_e|


.. automodule:: common
    :members:
    :undoc-members:
    :private-members:

.. _defaults:

builder_defaults.yaml
^^^^^^^^^^^^^^^^^^^^^

.. literalinclude:: ../common/builder_defaults.yaml
    :language: yaml
    :linenos:

.. note::
    The builder heavily integrates with this config file!

    If you are not building firmware for freifunk-mwu, it is best to fork this repository and create a branch for local changes. This way, you can keep track of updates here, or have the possibility merge code back. Thanks


.. _logger:

_build_logger.py
----------------

|logger_e|

.. automodule:: _build_logger
    :members:
    :undoc-members:
    :private-members:

.. _manifest:

_uni_manifest.py
----------------

|manifest_e|

Creates a central unified manifest and sets a symbolic-link named ``branch``.manifest for each branch

.. seealso:: you can read about the details `here <http://github.com/freifunk-gluon/gluon/issues/123>`_

.. automodule:: _uni_manifest
    :members:
    :undoc-members:
    :private-members:
