# TODO — session 3

The game boots, plays its opening movie and scenes, and plays past them,
with its sound (session 2) and the pad. No memory card: nothing can be
saved.

1. **Memory cards.** EXI channel 0 and 1, device 0: a card as a file in
   `build/` (Dolphin's raw `.raw` format: 59 or 251 blocks), the CARD
   commands (ID, status, read, write, erase), and CARD's unlock (a DSP task
   of its own, the second DSP program in the DOL at 803CB420: AX yields,
   the CPU answers `0xCDD10001` for a new task, and the DSP's HLE must
   switch to it and back, resuming AX). Then play to a save point, save,
   load.
2. **The micro-stutter at a spoken line's start** (session 2, in a
   cutscene): most likely the line's voice bank loaded, from the disc and
   then into ARAM, while the next sound frames are due. `WIIKIT_AUDIODBG=1`
   (the output queue, underruns), `WIIKIT_DIDBG=1` and the ARAM DMAs at
   that moment: is it the sound running dry, or a frame the renderer
   missed? The drive's and ARAM's timings are the console's, on purpose
   (`00-sessions.md`, session 1): the answer may be a larger cushion, not
   faster loads.
3. **Play on**: to the first battle and past it; the pad's layout (the
   GameCube's A is the big right button; the Xbox pad's positions map to
   the Classic's, then to the GameCube's: check it feels right), and keys
   for the keyboard.
4. **60 Hz**: PAL GameCube games may offer 60 Hz (EuRGB60) when the IPL's
   SRAM says so, or when B is held at boot; see what this one does.
5. The intro's draws: 80 000 draws but 62 million vertices in 56 s, far more
   than its look: find which draws (F12's trace) and whether the counts are
   right.

Build and run:

    python tools/fstmap.py build/extract/sys/main.dol
    python tools/sigmatch.py build/extract/sys/main.dol \
        --dsy <Dolphin>/Sys/totaldb.dsy --out build/sig_guess.tsv
    python tools/names.py build/extract/sys/main.dol
    python -m wiikit.recomp build/extract/sys/main.dol --out build/recomp \
        --symbols build/names.tsv --hooks tools/mmxcm-hooks.txt
    cmake -S build/recomp -B build/recomp-build -G Ninja -DCMAKE_CXX_COMPILER=clang++ \
        -DCMAKE_BUILD_TYPE=Release -DCMAKE_CXX_FLAGS_RELEASE=-O1 -DWIIKIT_EXTRA=$PWD/tools/mmxcm.cmake
    ninja -C build/recomp-build
    cd build/run1 && ../recomp-build/wiiboot ../extract --symbols ../names.tsv

`build/fonts` holds the boot ROM's fonts and `dsp_coef.bin` (copied from
ARF's build). The debugging switches of this session: `WIIKIT_DIDBG=1`
(`=bt` with the guest's call chain), `WIIKIT_SIDBG=1`, `WIIKIT_DSPDBG=1`,
`WIIKIT_DISCLOG=1`, `WIIKIT_ICALLS=1` (the game's tasks run through
pointers), and for the sound `WIIKIT_AUDIODUMP=file.wav`,
`WIIKIT_AXTRACE=first:count` (`05-audio.md`). `MMXCM_CAMERA=console`
keeps the C stick's console direction.

An unattended check: `WIIKIT_PAD="14:A 16:A 18:A 20:A 22:A 30:+ 32:+ 34:+
36:+ 38:A 40:A 42:A"`, 56 s, reaches the opening scenes, the movie played
on the way (the presses go to port 1 as the Classic's buttons, then the
pad's).

Housekeeping (2026-09-26, after session 2): wiikit is pushed up to
`0d235b5`, whose README names this port; the four Wii ports are bumped to
it and pushed. This repository is published at
[vs-sr-dev/pc-megamanxcm](https://github.com/vs-sr-dev/pc-megamanxcm).
A fresh `clone --recursive` was checked from nothing but the disc and
Dolphin's `totaldb.dsy`: `fstmap.py` needed `build/units.tsv`, which only
`look.py` wrote, and now runs the discovery itself; then the names came
out byte for byte as this build's, the recompiled C++ the same, and the
build booted to the opening scenes, the movie played on the way.
