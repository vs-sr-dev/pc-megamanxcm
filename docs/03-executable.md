# The executable

`sys/main.dol`, 4.1 MB, stripped. Entry 80003154; text 80003100–802430A0
(588 516 instructions); bss 803E75A0 + 0x1CFE5C. No RELs. r13 (SDA)
805B33C0, r2 (SDA2) 805B4680, the stack's top 805C7400 (the arena starts
there).

## What is linked

The GameCube's Dolphin SDK, every library `0x2301`:

| Library | Build |
|---|---|
| OS | May 21 2004 |
| VI | Apr 7 2004 |
| EXI, SI, DVD, GX, PAD, AI, AR, ARQ, DSP, CARD | Apr 5 2004 |
| THP | Jan 9 2004 |
| GBA | Dec 3 2003 |

Middleware and the rest, from the disc's symbol table (below): **MusyX**
(Factor 5's sound system, `musyx.a`, 383 functions), under Capcom's own
sound driver (`slib.a`: "snddrv: ver:1.69v Sep 21 2004"; `SoundInit`,
`CpInitSoundDriver`, `CpCall_SndDriver`, its commands). MusyX drives the
DSP itself: it boots the **AX micro-code** (Dolphin's hash 0x3AD3B7AC, the
one of Paper Mario: The Thousand-Year Door and Naruto 3; at 803D2160,
0x1EC0 bytes) and builds AX's command lists; no `ax.a` is linked. THP
(`thp.a`, the game's `movie.a`) for the two movies, DTK (`dtk.a`, the
drive's audio streaming), GBA (the Treasure Radar), MetroTRK and the
debugger's stubs (`TRK_MINNOW_DOLPHIN.a`, `OdemuExi2.a`, `amcstubs.a`,
`hio.a`), MSL. The DOL also holds a second, small DSP program at 803CB420
that nothing names; the CARD library's unlock code is the likeliest.

## Names

The disc carries a **symbol table**: `data/rkrpg_1.fst` ("rkrpg": Rockman
RPG), which the executable never reads. A header (`fst\0`, the count at
0x18, the strings' size at 0x1C), the strings, then 16-byte entries:
address, size, mangled name, object file (offsets from the file's start).
4 337 functions in 571 objects: 27 libraries and 544 of the game's
(`Mdlware.o` 181 functions, `scl_efc.o` 92, `btl_calc.o` 81, `gclib.o` 78,
`btl_seq.o` 75, `editor.o` 72, `btl_core.o` 65, `demoview.o` 53,
`battle.o` 52…).

It is **another build's**: its addresses reach 80267E24, this DOL's text
ends at 802430A0. The libraries are the same code, shifted (by 0x24040 to
0x24DB4, growing along the text); the game's own code differs a little
(`main`: 0x94C bytes there, 0x904 here). `tools/fstmap.py` aligns the two
lists by order and size (runs of at least three consecutive functions of
equal sizes, found by difflib) and names **4 136 of the 4 222 functions**
discovery finds. Against Dolphin's signatures: 806 agree, 16 differ, and in
those the table is right (signatures from other games' databases,
`glplatAbortFrame`, `cFielder__EndAction`, where this game has
`init_file__Fv`, `hwGetStreamPlayBuffer`; aliases, `DVDReadAsync` for
`DVDReadAsyncPrio`). Names are mangled (CodeWarrior's), and `fstmap.py`
writes the demangled form beside them.

`tools/names.py` gathers, most trusted first:

| Source | Names |
|---|---|
| by hand, each with its evidence (`tools/names-manual.tsv`) | 10 |
| the disc's symbol table (`tools/fstmap.py` → `build/fst_names.tsv`) | 4 119 |
| SDK functions that print their own name | 0 (all named already) |
| signatures (`tools/sigmatch.py`, Dolphin's `totaldb.dsy`), unique | 10 |

The hand names came first, found as on ARF's DOL (`OSLoadContext` after
`OSSaveContext`, `PPCHalt` by its halt loop, `RealMode` by its `rfi`,
`OSCreateThread` by its place and arguments, `__start`, `OSInit`, `main`),
and the table confirms each. They stay: the runtime's hooks must not depend
on a table of another build. Before the table was found, the signatures
alone gave 816 names.

`tools/look.py` is `wiikit.ppc` on this DOL: discovery's functions, these
names (`--func`, `--callers`, `--xref`).

## Recompiled

    python -m wiikit.recomp build/extract/sys/main.dol --out build/recomp \
        --symbols build/names.tsv --hooks tools/mmxcm-hooks.txt

4 222 units, no gaps; 262 switch tables sized, none unresolved; two
branches to 0x60 (`OSInit`'s jump to the debugger's handler, never taken);
74 words undecoded (data in text). 71 files of C++, compiled and linked at
the first try.

## Landmarks

| Address | What |
|---|---|
| 80003154 | `__start` |
| 80022344 | `main`: the loop, the frame, a debug overlay ("TASK %6d", "CPU:%4d.%2d", "GPU:%4d.%2d") |
| 800120B0 | `ARAMInit__Fv`: `ARInit`, `ARQInit`, a first ARAM transfer waited for with `VIWaitForRetrace` |
| 8023596C | `SoundInit`: the sound driver's configuration, command 0x20000 to `CpCall_SndDriver` (8022B104) |
| 8022ED5C | `CpInitSoundDriver`: "snddrv: ver:1.69v"; its heap from the configuration's +0x10 (`10-wiikit.md`, the layer) |
| 80015D50 | `load_file__FPcPc`: a file read in 0x6000-byte pieces, `DVDReadAsync` chained from its callback (80015C2C) |
| 8003D47C | the boot's task: a state byte at +0x18 (-10 to 11, a switch table at 802C1E48); -9 loads the file list (`firstE.arc`…) |
| 800239B4 | the drive's heartbeat: every 50 frames `tuto.arc`'s first 32 bytes are read again |
| 80013508 | the frame's end: `GXDrawDone`, `GXCopyDisp`, `VISetNextFrameBuffer`, `VIWaitForRetrace` |
| 803D2160 | the AX micro-code (0x1EC0 bytes), booted by MusyX's `salInitDsp` |
