# pc-megamanxcm

Toward a native PC port of **Mega Man X: Command Mission** (GameCube and
PlayStation 2, Capcom, 2004), the turn-based RPG of the Mega Man X series.
It was never re-released. The goal is the GameCube version running
natively on PC, played with a gamepad or the keyboard.

The route is static recompilation: the game's own PowerPC code, translated
to C++ and built for the PC, running on a replacement for the GameCube's
hardware. Nothing is emulated at the instruction level, and nothing of the
game is rewritten.

This repository documents the disc and its code, and holds the port's own
tools and layer. It is the fifth port built on
**[wiikit](https://github.com/vs-sr-dev/wiikit)**, the game-agnostic
toolkit of four Wii ports, and its first GameCube game: the GameCube is the
Wii's older self (the same processor, GPU and DSP), and what it needs of
its own (its discs, its disc drive, ARAM, the controllers on SI) went into
wiikit, not here. wiikit is a submodule at `wiikit/` (clone with
`--recursive`, or `git submodule update --init`).

## Where it stands

After two sessions the game **boots and plays, with its sound**: the
Nintendo and Dolby screens, the memory card check, the CAPCOM logo, the
opening movie, the title, the menu, a new game, the opening scenes in
real-time 3D and play past them, at 50 frames a second (PAL), with the
pad, its music, effects and voices. **It cannot save** yet (no memory
cards), and little past the opening has been played. See
[docs/07-next-session.md](docs/07-next-session.md).

## BYOA — Bring Your Own Assets

This repository contains **documentation and tools only**. No game data, no
executables, no assets. You need your own original disc. The work is done on
the European release, GXRP08; the addresses in `tools/` and `docs/` are that
executable's.

## Layout

    docs/     disc and code analysis, the plan, the session log
    tools/    Mega Man X: Command Mission-specific tools, the port's layer (mmxcm.cpp)
    wiikit/   game-agnostic Wii and GameCube toolkit (submodule: github.com/vs-sr-dev/wiikit)
    build/    (not in git) the disc, everything derived from it, the build

## Tools

The Python tools need only Python 3.8+ and no dependencies (RVZ images
compressed with zstd need Python 3.14; `dolphin.py` needs Pillow for its
screenshots). Building the recompiled code needs CMake, Ninja, a C++20
compiler (clang from MSYS2 is what is used here) and SDL3; running it needs
OpenGL 4.5. Run from the repository root.

```sh
# the disc, straight from the RVZ (or .iso)
python -m wiikit.disc GAME.rvz --info
python -m wiikit.disc GAME.rvz --extract build/extract

# the executable: stripped, but the disc carries another build's symbol
# table, aligned to it by order and size
python -m wiikit.dol build/extract/sys/main.dol --info
python tools/fstmap.py build/extract/sys/main.dol     # -> build/fst_names.tsv
python tools/sigmatch.py build/extract/sys/main.dol \
    --dsy <Dolphin>/Sys/totaldb.dsy --out build/sig_guess.tsv
python tools/names.py build/extract/sys/main.dol      # -> build/names.tsv
```

`fstmap.py` names 4 136 of the executable's 4 222 functions from
`data/rkrpg_1.fst`, a symbol table left on the disc (see
[docs/03-executable.md](docs/03-executable.md)); `sigmatch.py` adds
Dolphin's signatures (`totaldb.dsy`, in every Dolphin's `Sys` folder),
which alone gave 816. `names.py` keeps them, most trusted first, after the
hand names of `tools/names-manual.tsv`, each with its evidence.

```sh
# recompile, build: the port's hooks, and its layer through WIIKIT_EXTRA
python -m wiikit.recomp build/extract/sys/main.dol --out build/recomp \
    --symbols build/names.tsv --hooks tools/mmxcm-hooks.txt
cmake -S build/recomp -B build/recomp-build -G Ninja -DCMAKE_CXX_COMPILER=clang++ \
    -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS_RELEASE=-O1 \
    -DWIIKIT_EXTRA=$PWD/tools/mmxcm.cmake
ninja -C build/recomp-build

# boot the game: the boot ROM's fonts and the DSP ROM's resampling table in
# build/fonts (font_western.bin, font_japanese.bin, dsp_coef.bin: Dolphin's
# Sys/GC has free ones)
build/recomp-build/wiiboot build/extract --symbols build/names.tsv
build/recomp-build/wiiboot build/extract --window 1920x1080
```

`tools/look.py` is `wiikit.ppc` on the stripped DOL: discovery's
functions, these names (`--func SoundInit`, `--callers`, `--xref`).
`tools/dolphin.py` runs the disc in Dolphin as the reference, with
screenshots and key presses on a timeline.

### Playing

A GameCube controller on port 1 is made of the keyboard, the mouse buttons
and the first gamepad at once; every other pad plugged in is the next port.
wiikit reads them as a Wii Classic Controller and hands the game a GameCube
pad: the Classic's A, B, X, Y are the pad's, + is START, ZL and ZR are Z,
L and R press the triggers fully, and the sticks are the stick and the C
stick. On an Xbox pad: the right face button is A, the bottom one B, the
top one X, the left one Y, Start is START, the shoulders are L and R, the
triggers Z. The keys are wiikit's defaults for the Classic Controller, in
`build/keys.txt` (Enter A, Backspace B, R X, F Y, Tab START, WASD the
stick, the arrows the d-pad); a layout for this game is still to come.

The C stick turns the camera the way of today's games: pushed right, the
view turns right. The console's game turns it the other way and has no
option for it; `MMXCM_CAMERA=console` in the environment keeps the
console's way.

## Status

Session 1: **the game runs to its opening scenes.** The disc read from its
RVZ (4 246 files), the executable recompiled at the first try (4 222
units, no gaps) and named from a symbol table found on the disc. wiikit
learnt the GameCube: its discs, its clocks, its disc drive, ARAM and the
controllers. Three stops on the way, each a matter of time (an ARAM
transfer, the disc's commands) or of a status bit (the controllers'), are
told in [docs/00-sessions.md](docs/00-sessions.md).

Session 2: **the sound.** wiikit mixes the GameCube's AX micro-code, which
the game's MusyX drives: the music streamed through ARAM, the effects, the
voices. The opening movie, dark in session 1, plays: its player had been
waiting for its sound. No saving yet.

## Documentation

    00-sessions.md            progress log
    01-disc-layout.md         what is on the disc
    03-executable.md          the DOL: what is linked, the disc's symbol table, landmarks
    04-curiosities.md         what the disc reveals
    05-audio.md               the sound: MusyX over AX, what the game plays, the movie that waited
    07-next-session.md        the plan for the next session
    10-wiikit.md              how this port uses and grows wiikit

## Licence

MIT. This covers the documentation and tools in this repository only. It
says nothing about Mega Man X: Command Mission, which remains the property
of its rights holders.
