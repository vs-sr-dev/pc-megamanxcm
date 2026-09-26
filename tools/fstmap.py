"""Name the DOL's functions from data/rkrpg_1.fst, the symbol table on the disc.

The disc carries a symbol table of another build of the game
(`docs/03-executable.md`): 4 337 functions, each with its address, size,
mangled name and object file. Its addresses are not this DOL's (the code
after main is shifted, and some of the game's functions differ in size), so
the two lists are aligned by order and size: runs of consecutive functions
of equal sizes, found by difflib, are taken as the same functions. The
signature names of build/names.tsv check the result.

    python tools/fstmap.py build/extract/sys/main.dol        # -> build/fst_names.tsv
"""
import argparse
import collections
import difflib
import os
import struct
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))  # wiikit/

from wiikit.cw import demangle  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")


def read_fst(path):
    """[(addr, size, mangled name, object)] by address. Header: 'fst\\0', ...,
    u32 count at 0x18, u32 string bytes at 0x1C; the strings from 0x20, then
    16-byte entries (addr, size, name offset, object offset; offsets from the
    file's start), ended by a zero entry."""
    d = open(path, "rb").read()
    if d[:4] != b"fst\0":
        raise SystemExit(f"{path}: not a symbol table")
    nb = struct.unpack_from(">I", d, 0x1C)[0]

    def s(o):
        return d[o:d.index(b"\0", o)].decode("latin1")

    out = []
    for i in range(0x20 + nb, len(d) - 15, 16):
        a, size, n, o = struct.unpack_from(">4I", d, i)
        if a:
            out.append((a, size, s(n), s(o)))
    return sorted(out)


def read_units(path):
    units = []
    with open(path) as f:
        for line in f:
            a, b = line.split()[:2]
            units.append((int(a, 16), int(b, 16) - int(a, 16)))
    return units


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("dol")
    ap.add_argument("--fst", default=os.path.join(ROOT, "build", "extract", "files", "data", "rkrpg_1.fst"))
    ap.add_argument("--units", default=os.path.join(ROOT, "build", "units.tsv"))
    ap.add_argument("--names", default=os.path.join(ROOT, "build", "names.tsv"))
    ap.add_argument("--min-run", type=int, default=3, help="shortest run of equal sizes taken")
    ap.add_argument("--out", default=os.path.join(ROOT, "build", "fst_names.tsv"))
    a = ap.parse_args()

    fst = read_fst(a.fst)
    units = read_units(a.units)
    sm = difflib.SequenceMatcher(None, [s for _, s in units], [e[1] for e in fst], autojunk=False)
    mapped = {}
    for blk in sm.get_matching_blocks():
        if blk.size < a.min_run:
            continue
        for k in range(blk.size):
            mapped[units[blk.a + k][0]] = fst[blk.b + k]

    known = {}
    if os.path.exists(a.names):
        with open(a.names) as f:
            for line in f:
                p = line.rstrip("\n").split("\t")
                if len(p) >= 2 and p[0] != "addr":
                    known[int(p[0], 16)] = p[1]
    agree = sum(1 for u, e in mapped.items() if u in known and known[u] == e[2])
    differ = [(u, known[u], e[2]) for u, e in mapped.items() if u in known and known[u] != e[2]]
    objs = collections.Counter(e[3] for e in mapped.values())
    print(f"{len(fst)} symbols, {len(units)} units: {len(mapped)} named; "
          f"against names.tsv {agree} agree, {len(differ)} differ")
    for u, k, n in differ[:20]:
        print(f"  {u:08X}  names.tsv {k}  fst {n}")
    with open(a.out, "w", newline="\n") as f:
        f.write("addr\tname\tsize\tobject\tdemangled\n")
        for u in sorted(mapped):
            _, size, name, obj = mapped[u]
            try:
                dm = demangle(name)
            except Exception:
                dm = name
            f.write(f"{u:08X}\t{name}\t{size:#x}\t{obj}\t{dm}\n")
    print(f"-> {a.out}; objects: {len(objs)}")


if __name__ == "__main__":
    main()
