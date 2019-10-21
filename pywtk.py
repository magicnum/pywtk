import os
import sys
import glob
import itertools
from lazyMerger import *
from getHashes import *
from time import perf_counter
from json import dumps, loads
from os.path import basename, getsize, isfile, isdir, abspath, splitext
from riposte import Riposte
from riposte.exceptions import RiposteException

BANNER = """
                                                   88
                                             ,d    88
                                             88    88
8b,dPPYba,  8b       d8 8b      db      d8 MM88MMM 88   ,d8
88P'    "8a `8b     d8' `8b    d88b    d8'   88    88 ,a8"
88       d8  `8b   d8'   `8b  d8'`8b  d8'    88    8888[
88b,   ,a8"   `8b,d8'     `8bd8'  `8bd8'     88,   88`"Yba,
88`YbbdP"'      Y88'        YP      YP       "Y888 88   `Y8a
88              d8'
88             d8'
                                                 by magicnum

"""

mainrepl = Riposte(prompt="pywtk:~$ ", banner=BANNER)
SUBCOMMANDS = ['wordlists', 'dbs', 'all']
WORDLISTS = []
DBS = {}


@mainrepl.command("chdir")
def cdir(path: str):
    if isdir(path):
        os.chdir(path)
        mainrepl.success(f'Working folder: {path}')
    else:
        raise RiposteException('Provided path is not a directory')


@mainrepl.command("show")
def show(mode: str):

    show_all = True if mode == 'all' else False

    if mode == 'wordlists' or show_all:
        mainrepl.status('Wordlists: ')
        mainrepl.info(WORDLISTS)

    if mode == 'dbs' or show_all:
        mainrepl.status('DBs: ')
        mainrepl.info(dumps(DBS, indent=2))


@mainrepl.command("merge")
def merge(mode: str, name: str):

    if mode == 'wordlists':
        if len(WORDLISTS):
            wordlists = WORDLISTS
        else:
            raise RiposteException('List of wordlists is empty')

    elif mode == 'dbs':
        if len(DBS):
            wordlists = list(DBS.keys())
        else:
            raise RiposteException('List of DBs is empty')
    else:
        raise RiposteException('Unknown mode')

    mainrepl.status('Merging wordlists. Be patient..')
    elapsed_time = lazyMerger(wordlists, name)

    mainrepl.success(f'Done! Wordlists merged: {basename(name)}')
    mainrepl.success(f'Merging takes {elapsed_time:.1f}s')


@mainrepl.command("load")
def load(*args):

    if not len(args):
        raise RiposteException('Arguments missing')

    fpaths = [glob.glob(x) for x in args]
    fpaths = list(itertools.chain(*fpaths))

    if not len(fpaths):
        raise RiposteException('Provided files not found')

    for fpath in fpaths:
        if splitext(fpath)[-1] == '.json':
            with open(fpath, 'r') as data:
                DBS.update(loads(data.read()))
        else:
            WORDLISTS.append(abspath(fpath))
            temp = list(set(WORDLISTS))
            WORDLISTS.clear()
            WORDLISTS.extend(temp)

        mainrepl.success(f'File {basename(fpath)} added')


@mainrepl.command("makedb")
def makedb(name: str):
    if len(WORDLISTS):
        mainrepl.status('Creating DB')
        for wordlist in WORDLISTS:
            size = getsize(wordlist) * 10e-7
            DBS.update({abspath(wordlist): {'hashes': getHashSum(
                wordlist), 'size_mb': round(size, 2)}})
        with open(name, 'w') as f:
            f.write(dumps(DBS, indent=2))
        mainrepl.success('New DB created successfully')
    else:
        raise RiposteException('List of wordlists is empty')


@mainrepl.command("exit")
def exit():
    if sys.platform == 'linux':
        os.system('clear')
    else:
        os.system('cls')
    sys.exit(0)


@mainrepl.complete("show")
def completer_start(text, line, start_index, end_index):

    return [
        subcommand
        for subcommand in SUBCOMMANDS
        if subcommand.startswith(text)
    ]


@mainrepl.complete("load")
def completer_start(text, line, start_index, end_index):

    return [
        subcommand
        for subcommand in SUBCOMMANDS[:-1]
        if subcommand.startswith(text)
    ]


@mainrepl.complete("merge")
def completer_start(text, line, start_index, end_index):

    return [
        subcommand
        for subcommand in SUBCOMMANDS[:-1]
        if subcommand.startswith(text)
    ]


mainrepl.run()
