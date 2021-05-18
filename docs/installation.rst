.. highlight:: shell

============
Installation
============

This is a Python package, and it requires the ``pcbnew`` module included with KiCad.
Therefore, you'll have to install it using the ``pip`` executable included in the 
KiCad ``bin`` directory like so:

.. code-block:: console

    $ pip install kinet2pcb

This is the preferred method to install ``kinet2pcb``, as it will always install the most recent stable release.

You can also install ``kinet2pcb`` in the Python interpreter on your system using its ``pip`` command,
but your system libraries probably won't include the ``pcbnew`` module.
By default, ``kinet2pcb`` adds ``/usr/lib/python3/dist-packages`` to the Python library
search path which is where KiCad normally stores ``pcbnew`` in a linux system.
If your system doesn't follow this convention, then you'll have to search for
the ``pcbnew.py`` file and add its path to the ``PYTHONPATH`` environment variable.
