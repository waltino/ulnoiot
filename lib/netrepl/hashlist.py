# Some small utilities for the ulnoiot netrepl to generate
# a list of hashes for files

import os
from uhashlib import sha256
import ubinascii
import gc
import machine


def hashlist(root="/"):
    speed = machine.freq()
    machine.freq(160000000)  # we want to be fast for this
    p = os.getcwd()
    if p == "":
        p = "/"
    os.chdir("/")
    _hashlist(root)
    os.chdir(p)
    machine.freq(speed)  # restore speed


def _hashlist(root):
    if root.endswith("/"):
        root = root[0:-1]  # strip slash
    try:
        st = os.stat(root)
    except:
        # print("noaccess",root) - does not exist, so don't print
        return
    if st[0] & 0x4000:  # stat.S_IFDIR
        print("<dir>", root)
        l = os.listdir(root)
        for f in l:
            gc.collect()
            p = root + "/" + f
            _hashlist(p)
    else:
        h = sha256()
        hf = open(root, "rb")
        while True:
            b = hf.read(40)
            if len(b) == 0: break
            h.update(b)
        print(ubinascii.hexlify(h.digest()).decode(), root)
        hf.close()
