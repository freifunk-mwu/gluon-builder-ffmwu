:orphan:

.. |prepare_e| replace:: Checks out Gluon sources and site-conf repositories at proper commit-ids or tags according to the branch to build.
.. |prepare_site_e| replace:: Generates a site-conf.
.. |bconf_e| replace:: Provides all information needed by the builder in placing a ``bconf``-file.

.. |builder_e| replace:: This is the main script. The photon helper scripts around get called from within, so this is mostly your starting point for compiling. For example to build a new beta, one would call: ``./build.sh -b beta``

.. |common_e| replace:: Shared code, Configuration and further data is stored in the common-folder.
.. |logger_e| replace:: Logs all actions into a json file for validation of all actions done while compiling (remember: the resulting images needs to get signed for the autoupdater to work)
.. |manifest_e| replace:: Create an unified manifest-file for all branches.

.. |info_e| replace:: Places a json file containing a dictionrary listing each Router-Model with according `factory` & `sysupgrade` image-file names less painful integration of download links into websites.
.. |publish_e| replace:: Publishes freshly built images. This is accomplished by setting symbolic-links in the form of ``communitiy``/``branch`` pointing into the library (in the form of _library/``build``-``branch``/``short-community``)
