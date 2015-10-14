
The builder
===========

Below is the full source of the build script with comments in it.

.. _commandline:

commandline
-----------

The primary goal of the builder is to run unattended in the crontab. So a simple ``./builder.sh`` without any arguments builds a new experimental from the most recent sources.

* Use  the ``-b`` Flag to specify a branch to build. The builder will checkout the following if no ``-gt`` / ``--gluon_tag`` (gluon tag or commit id) or ``-st`` / ``--site_tag`` (site tag or commit id) is given:

============ ================ ==============
branch       gluon            site
============ ================ ==============
experimental latest commit    latest commit
beta         latest tag       latest commit
stable       latest tag       latest tag
============ ================ ==============

* Use ``--broken`` to build images for unsupported (broken) hardware.
* Use ``--onlyone`` or ``-oo`` to build images for only one community.
* Use ``--nomodules`` to skip module creation in site.conf generator
* Use ``--target`` or ``-t`` to specify a list of platforms to build images for, e.g. ``-t ar71xx-generic x86-generic`` for two platforms (this overwrites the default setting, of building all available).

* See ``./builder.sh --help`` for more, or see :func:`common.prepare_args` for more.

.. _builder:

builder.sh
----------

This is the main script. The photon helper scripts around get called from within, so this is the starting point for compiling.

.. literalinclude:: ../builder.sh
    :language: bash
    :linenos:

