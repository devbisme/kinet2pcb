=======
History
=======

1.0.1 (2022-06-30)
------------------

* Fixed incompatibilities with KiCad V6 Python API (pcbnew).


1.0.0 (2021-09-16)
------------------

* Decided this tool was mature to the point it could be called 1.0.0.


0.1.3 (2021-05-19)
------------------

* The parts in the PCB are now given a non-overlapping arrangement
  grouped according to their hierarchical nesting.


0.1.2 (2021-05-18)
------------------

* The ``kinet2pcb()`` function will now generate a KiCad PCB file when given
  a netlist file name, a PyParsing object, or a SKiDL Circuit object.
* ``kinet2pcb`` can now be installed in the default Python interpreter on
  a system and it will look in ``/usr/lib/python3/dist-packages`` to find
  the ``pcbnew`` module installed by KiCad.  If the ``pcbnew`` module
  is not found there, add the correct location to the ``PYTHONPATH``
  environment variable.


0.1.1 (2019-03-09)
------------------

* Now runs under Python 2 & 3.


0.1.0 (2019-10-28)
------------------

* First release on PyPI.
