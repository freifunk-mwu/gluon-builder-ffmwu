
The builder
===========

Below is the full source of the build script with comments in it.

.. _builder:

builder.sh
----------

This is the main script. The photon helper scripts around get called from within, so this is the starting point for compiling.

To build a new beta, call: ``./build.sh -b beta``

.. literalinclude:: ../builder.sh
    :language: bash
    :linenos:
