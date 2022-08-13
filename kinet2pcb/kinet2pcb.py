# -*- coding: utf-8 -*-


from past.builtins import basestring
import argparse
import logging
import os
import os.path
import re
import shutil
import sys

import kinparse

sys.path.append('/usr/lib/python3/dist-packages')
import pcbnew
import hierplace

from .pckg_info import __version__

# Global logger.
logger = logging.getLogger("kinet2pcb")

def rmv_quotes(s):
    """Remove starting and ending quotes from a string."""
    if not isinstance(s, basestring):
        return s

    mtch = re.match(r'^\s*"(.*)"\s*$', s)
    if mtch:
        try:
            s = s.decode(mtch.group(1))
        except (AttributeError, LookupError):
            s = mtch.group(1)

    return s


def to_list(x):
    """
    Return x if it is already a list, return a list containing x if x is a scalar unless
    x is None in which case return an empty list.
    """
    if x is None:
        # Return empty list if x is None.
        return []
    if isinstance(x, (list, tuple)):
        return x  # Already a list, so just return it.
    return [x]  # Wasn't a list, so make it into one.


def get_global_fp_lib_table_fn():
    """Get the full path of the global fp-lib-table file or return an empty string."""

    paths = (
        "$HOME/.config/kicad",
        "~/.config/kicad",
        "%APPDATA%/kicad",
        "$HOME/Library/Preferences/kicad",
        "~/Library/Preferences/kicad",
        "%ProgramFiles%/KiCad/share/kicad/template",
        "/usr/share/kicad/template",
    )
    for path in paths:
        path = os.path.normpath(os.path.expanduser(os.path.expandvars(path)))
        fp_lib_table_fn = os.path.join(path, 'fp-lib-table')
        if os.path.exists(fp_lib_table_fn):
            return fp_lib_table_fn

    logger.warning("Unable to find global fp-lib-table file.")
    return ""


class LibURIs(dict):
    """Dict for storing library URIs from all directories in fp-lib-table file."""

    def __init__(self, *fp_lib_table_fns):
        super(self.__class__, self).__init__()

        # Set KISYSMOD to a default value if it isn't already defined.
        if 'KISYSMOD' not in os.environ.keys():
            if os.name == 'nt':
                os.environ['KISYSMOD'] = '%ProgramFiles%/KiCad/share/kicad/modules'
            else:
                os.environ['KISYSMOD'] = '/usr/share/kicad/modules'

        # Load URIs for libraries found in each library table file.
        for fp_lib_table_fn in fp_lib_table_fns:
            self.load(fp_lib_table_fn)

    def load(self, fp_lib_table_fn):
        """Load cache with URIs for libraries in fp-lib-table file."""

        # Read contents of footprint library file into a single string.
        try:
            with open(fp_lib_table_fn) as fp:
                tbl = fp.read()
        except IOError:
            return

        # Get individual "(lib ...)" entries from the string.
        libs = re.findall(
            r"\(\s*lib\s* .*? \)\)", tbl, flags=re.IGNORECASE | re.VERBOSE | re.DOTALL
        )

        # Add the footprint modules found in each enabled KiCad library.
        for lib in libs:

            # Skip disabled libraries.
            disabled = re.findall(
                r"\(\s*disabled\s*\)", lib, flags=re.IGNORECASE | re.VERBOSE
            )
            if disabled:
                continue

            # Skip non-KiCad libraries (primarily git repos).
            type_ = re.findall(
                r'(?:\(\s*type\s*) ("[^"]*?"|[^)]*?) (?:\s*\))',
                lib,
                flags=re.IGNORECASE | re.VERBOSE,
            )[0]
            if type_.lower() != "kicad":
                continue

            # Get the library directory and nickname.
            uri = re.findall(
                r'(?:\(\s*uri\s*) ("[^"]*?"|[^)]*?) (?:\s*\))',
                lib,
                flags=re.IGNORECASE | re.VERBOSE,
            )[0]
            nickname = re.findall(
                r'(?:\(\s*name\s*) ("[^"]*?"|[^)]*?) (?:\s*\))',
                lib,
                flags=re.IGNORECASE | re.VERBOSE,
            )[0]

            # Remove any quotes around the URI or nickname.
            uri = rmv_quotes(uri)
            nickname = rmv_quotes(nickname)

            # Expand variables and ~ in the URI.
            uri = os.path.expandvars(os.path.expanduser(uri))

            if nickname in self:
                print("Overwriting {nickname}:{self[nickname]} with {nickname}:{uri}".format(**locals()))
            self[nickname] = uri


def get_user_lib_uris(fp_lib_dirs):
    """Return a dict of .pretty footprint library nicknames and their absolute directory names.

    Args:
        fp_lib_dirs (list/str): Single or list of directory paths to search for footprint libraries.

    Returns:
        Dictionary with library nicknames as keys and library directories as values.
    """

    def add_lib(dir):
        """Add a directory as a footprint library if it ends with ".pretty"."""

        # Get the extension of the directory name.
        _, basename = os.path.split(dir)
        base, ext = os.path.splitext(basename)

        if ext.lower() == ".pretty":
            # Add directory using the base of the file name as the library nickname.
            user_lib_uris[base] = dir
            return True  # Directory was added as a footprint library.
        
        return False # Directory was not a footprint library.

    user_lib_uris = dict()

    for dir in to_list(fp_lib_dirs):

        # Fully expand the directory path.
        dir = os.path.abspath(os.path.expandvars(os.path.expanduser(dir)))

        if not add_lib(dir):
            # If the dir wasn't a footprint library, then see if it contains
            # any footprint libraries and add those.
            for subdir in os.listdir(dir):
                add_lib(os.path.join(dir, subdir))

    return user_lib_uris


def kinet2pcb(netlist_origin, brd_filename, fp_lib_dirs=None):
    """Create a .kicad_pcb from a KiCad netlist file.

    Args:
        netlist_origin (netlist filename or Circuit object): Netlist for circuit.
        brd_filename (str): Name of file to hold KiCad PCB.
        user_lib_dirs (list, optional): List of footprint library directories. Defaults to None.
    """

    # Get the global and local fp-lib-table footprint library URIs.
    fp_libs = LibURIs(get_global_fp_lib_table_fn(), os.path.join(".", "fp-lib-table"))

    # Add the footprint libraries from user-supplied directories.
    fp_libs.update(get_user_lib_uris(fp_lib_dirs))

    # Create a blank KiCad PCB.
    brd = pcbnew.BOARD()

    # Get the netlist.
    if isinstance(netlist_origin, type('')):
        # Parse the netlist into an object if given a file name string.
        netlist = kinparse.parse_netlist(netlist_origin)
    else:
        # otherwise, the netlist is already an object that can be processed directly.
        netlist = netlist_origin

    # Add the components in the netlist to the PCB.
    for part in netlist.parts:

        # Get the library and footprint name for the part.
        fp_lib, fp_name = part.footprint.split(":")

        # Get the URI of the library directory.
        lib_uri = fp_libs[fp_lib]

        # Create a module from the footprint file.
        fp = pcbnew.FootprintLoad(lib_uri, fp_name)
        if not fp:
            # Could not find footprint so give warning and skip to next part.
            logger.warning("Unable to find footprint {fp_name} in {lib_uri}".format(**locals()))
            continue

        # Set the module parameters based on the part data.
        fp.SetParent(brd)
        fp.SetReference(part.ref)
        fp.SetValue(part.value)
        # fp.SetTimeStamp(part.sheetpath.tstamps)
        try:
            # Newer PCBNEW API.
            fp.SetPath(pcbnew.KIID_PATH(part.sheetpath.names))
        except TypeError:
            # Older PCBNEW API.
            fp.SetPath(part.sheetpath.names)
        except AttributeError:
            pass

        # Add the module to the PCB.
        brd.Add(fp)

    # Add the nets in the netlist to the PCB.
    cnct = brd.GetConnectivity()
    for net in netlist.nets:

        # Create a net with the current net name.
        pcb_net = pcbnew.NETINFO_ITEM(brd, net.name)

        # Add the net to the PCB.
        brd.Add(pcb_net)

        # Connect the part pins on the netlist net to the PCB net.
        for pin in net.pins:

            # Find the PCB module pad for the current part pin.
            pad = None
            try:
                # Newer PCBNEW API.
                module = brd.FindFootprintByReference(pin.ref)
                if module:
                    pad = module.FindPadByNumber(pin.num)
            except AttributeError:
                # Older PCBNEW API.
                module = brd.FindModuleByReference(pin.ref)
                if module:
                    pad = module.FindPadByName(pin.num)

            # Connect the pad to the PCB net.
            if pad:
                cnct.Add(pad)
                pad.SetNet(pcb_net)

    # Recalculate the PCB part and net data.
    brd.BuildListOfNets()
    cnct.RecalculateRatsnest()
    pcbnew.Refresh()

    # Place the board parts into non-overlapping areas that follow the design hierarchy.
    hierplace.hier_place(brd)

    # Save the PCB into the KiCad PCB file.
    pcbnew.SaveBoard(brd_filename, brd)


###############################################################################
# Command-line interface.
###############################################################################


def main():
    parser = argparse.ArgumentParser(
        description="""Convert KiCad netlist into a PCBNEW .kicad_pcb file."""
    )
    parser.add_argument(
        "--version", "-v", action="version", version="kinet2pcb " + __version__
    )
    parser.add_argument(
        "--input",
        "-i",
        type=str,
        metavar="file",
        help="""Input file containing KiCad netlist.""",
    )
    parser.add_argument(
        "--output",
        "-o",
        nargs="?",
        type=str,
        metavar="file",
        help="""Output file for storing KiCad board.""",
    )
    parser.add_argument(
        "--overwrite",
        "-w",
        action="store_true",
        help="Allow overwriting of an existing board file.",
    )
    parser.add_argument(
        "--nobackup",
        "-nb",
        action="store_true",
        help="""Do *not* create backups before modifying files.
            (Default is to make backup files.)""",
    )
    parser.add_argument(
        "--libraries",
        "-l",
        nargs="+",
        type=str,
        metavar="footprint_dir",
        help="Specify one or more directories containing .pretty footprint libraries."
    )
    parser.add_argument(
        "--debug",
        "-d",
        nargs="?",
        type=int,
        default=0,
        metavar="LEVEL",
        help="Print debugging info. (Larger LEVEL means more info.)",
    )

    args = parser.parse_args()

    if args.debug is not None:
        log_level = logging.DEBUG + 1 - args.debug
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(log_level)
        logger.addHandler(handler)
        logger.setLevel(log_level)

    if args.output is None:
        args.output = os.path.splitext(args.input)[0] + ".kicad_pcb"
    
    if os.path.isfile(args.output):
        if not args.overwrite and args.nobackup:
            logger.critical(
                """File {} already exists! Use the --overwrite option to
                allow modifications to it or allow backups.""".format(
                    args.output
                )
            )
            sys.exit(1)
        if not args.nobackup:
            # Create a backup file.
            index = 1  # Start with this backup file suffix.
            while True:
                backup_file = args.output + ".{}.bak".format(index)
                if not os.path.isfile(backup_file):
                    # Found an unused backup file name, so make backup.
                    shutil.copy(args.output, backup_file)
                    break  # Backup done, so break out of loop.
                index += 1  # Else keep looking for an unused backup file name.

    kinet2pcb(args.input, args.output, args.libraries)


###############################################################################
# Main entrypoint.
###############################################################################
if __name__ == "__main__":
    main()
