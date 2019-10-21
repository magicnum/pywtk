
import os
import time
import numpy
import string
import dask.bag as db


unwanted_lines = [x for x in string.whitespace]
unwanted_lines.append('')


def lazyMerger(wordlists, name):

    start = time.perf_counter()
    blocksize = max([os.path.getsize(x) for x in wordlists]) // 16

    bag = db.read_text(wordlists, blocksize=blocksize, encoding='latin-1')
    df = bag.to_dataframe(meta={'p': str})

    if df.p.isin(unwanted_lines).any().compute():
        df = df.replace(unwanted_lines, numpy.nan).dropna()

    df = df.drop_duplicates().compute()

    with open(name, 'w') as out:
        out.write(df.to_string(header=False, index=False).replace(' ', '').replace('\\n', ''))

    return time.perf_counter() - start

