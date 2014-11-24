
Tools while building
====================

Shared code, Configuration and further data is stored in the common-folder.

.. _common:

common
------

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

.. automodule:: _build_logger
    :members:
    :undoc-members:
    :private-members:

.. _manifest:

_uni_manifest.py
----------------

.. automodule:: _uni_manifest
    :members:
    :undoc-members:
    :private-members:

.. seealso:: you can read about the details `here <http://github.com/freifunk-gluon/gluon/issues/123>`_

It opens specified `manifest`-file and replaces::

    BRANCH=${branch}

by::

    BRANCH=experimental
    BRANCH=beta
    BRANCH=stable

then it saves it as `manifest` and symlinks `experimental.manifest`, `beta.manifest` and `stable.manifest` to it::

    ~/gluon_builder/${community}/images/sysupgrade/${branch}.manifest

becomes to::

    ~/gluon_builder/${community}/images/sysupgrade/manifest
    ~/gluon_builder/${community}/images/sysupgrade/experimental.manifest -> symlink to ./manifest
    ~/gluon_builder/${community}/images/sysupgrade/beta.manifest -> symlink to ./manifest
    ~/gluon_builder/${community}/images/sysupgrade/stable.manifest -> symlink to ./manifest

