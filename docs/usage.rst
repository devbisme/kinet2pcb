=====
Usage
=====

``kinet2pcb`` can be used as a module to provide other scripts with the ability
to create KiCad PCB files, but it is mainly intended to serve as its own stand-alone utility::

    usage: kinet2pcb [-h] [--version] [--input file] [--output [file]]
                    [--overwrite] [--nobackup] [--debug [LEVEL]]

    Convert KiCad netlist into a PCBNEW .kicad_pcb file.

    optional arguments:
    -h, --help            show this help message and exit
    --version, -v         show program's version number and exit
    --input file, -i file
                            Input file containing KiCad netlist.
    --output [file], -o [file]
                            Output file for storing KiCad board.
    --overwrite, -w       Allow overwriting of an existing board file.
    --nobackup, -nb       Do *not* create backups before modifying files.
                            (Default is to make backup files.)
    --debug [LEVEL], -d [LEVEL]
                            Print debugging info. (Larger LEVEL means more info.)


-----------
Examples
-----------

Assuming you've generated a KiCad netlist file called ``example.net``, then
the following command would create a KiCad PCB file called ``example.kicad_pcb``::

    kinet2pcb -i example.net

If a files called ``example.kicad_pcb`` already exists, then ``kinet2pcb`` will
halt and not over-write the file. To override this behavior, use the ``-w`` option::

    kinet2pcb -i example.net -w

The above command will rename the pre-existing ``example.kicad_pcb`` file to
``example.kicad_pcb.bak``.

----------------------------
Preventing Disasters
----------------------------

A lot of work goes into creating a PCB.
For this reason, ``kinet2pcb`` makes a backup of any ``.kicad_pcb`` file it is about to overwrite
(using file names such as ``example.1.kicad_pcb``, ``example.2.kicad_pcb``, etc.).
You can turn off this behavior using the ``--nobackup`` option.

In addition, if ``kinet2pcb`` would overwrite an existing ``.kicad_pcb`` file
and the ``--nobackup`` option is enabled, then you must also use the ``--overwrite`` option
or the operation will be aborted.
