
# pywtk

Easy to use REPL wordlists manager with "lazy" merger for low-memory machines written in Python.
### Main feature: ability to merge large files fast and without a RAM overflow

## Packages

* [dask](https://github.com/dask/dask)
* [riposte](https://github.com/fwkz/riposte)
* [xxhash](https://github.com/ifduyue/python-xxhash)
* [numpy](https://github.com/numpy/numpy)
* [pandas](https://github.com/pandas-dev/pandas)

## Installing

```bash
github clone https://github.com/magicnum/pywtk
cd pywtk
pip install -r requirements.txt
python pywtk.py
```

## Commands

Basic REPL commands:
* `load` [paths]
* `merge` [item, outfilename]
* `makedb` [db_path]
* `show` [item]
* `chdir` [path]
* `exit`

---

`load`: load files paths into a `wordlists` list or files content into `db` dictionary.
Choose of item based on file extension (json for `db`, any other for `wordlists`).
```bash
pywtk:~$ load wordlists abc.txt
```

`load` supports wildcard symbol, so `load hashes0.txt hashes1.txt` is equal to `load hashes*.txt`.

---

`merge`: merges files content and delete duplicates using _dask_ parallel computation.
```bash
pywtk:~$ merge wordlists merged.dic
```

---

`makedb`: make json structure with hashes and full paths of wordlists.
```bash
pywtk:~$ load wordlists old_200*.txt
...
pywtk:~$ makedb old.json
```

---

`show`: output current state of loaded `item`.
```bash
pywtk:~$ show all
```

---

`chdir`: setup current working folder.
```bash
pywtk:~$ chdir /home/user/wordlists/
```
Current items are:

* `wordlist`
* `db`
* `all`

## CLI

Thanks to _riposte_ you can use it as CLI too:

```bash
python pywtk.py -c "load wordlists passwords201*.dic; merge wordlists merged.dic"
```

## TODO

* regex, minimal and maximum length of string filters 
