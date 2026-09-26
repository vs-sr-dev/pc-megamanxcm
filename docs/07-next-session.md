# TODO — session 2

The game boots to its title and plays its opening scenes in 3D, with the
pad, silent (session 1). No memory card: nothing can be saved.

1. **The sound: the GameCube's AX micro-code.** MusyX boots AX
   (0x3AD3B7AC) and sends it command lists each 5 ms frame; wiikit answers
   the mails and mixes nothing on the GameCube (`hw.cpp`: `ax_command_list`
   is the Wii's). The GameCube's AX differs: its command list numbering,
   its voice (PB) layout, **samples in ARAM** (addresses are ARAM's, 16 MB,
   now real), its output in main memory as the AI reads it, Dolby Pro
   Logic II (the game advertises it: a surround mode of the mix; stereo is
   enough). Reference: Dolphin's `AXUCode` (GameCube) beside the
   `AXWiiUCode` wiikit followed. `WIIKIT_DSPDBG=1` traces the mails. The
   music is streamed (`movie/BGM_STREAM/*.dsp`, left and right) through the
   drive into ARAM, then AX voices: check both effects and music.
2. **Memory cards.** EXI channel 0 and 1, device 0: a card as a file in
   `build/` (Dolphin's raw `.raw` format: 59 or 251 blocks), the CARD
   commands (ID, status, read, write, erase), and CARD's unlock (a DSP task
   of its own, the second DSP program in the DOL: the task switch in the
   DSP's HLE). Then play to a save point, save, load.
3. **The dark screens before the title** (after the CAPCOM logo): the
   opening movie (`movie/op.thp`) drawn too dark, or a fade? Compare with
   Dolphin (`tools/dolphin.py`) at the same seconds.
4. **Play on**: past the opening to the first battle; the pad's layout
   (the GameCube's A is the big right button; the Xbox pad's positions map
   to the Classic's, then to the GameCube's: check it feels right), and
   keys for the keyboard.
5. **60 Hz**: PAL GameCube games may offer 60 Hz (EuRGB60) when the IPL's
   SRAM says so, or when B is held at boot; see what this one does.
6. The intro's draws: 80 000 draws but 62 million vertices in 56 s, far more
   than its look: find which draws (F12's trace) and whether the counts are
   right.

Build and run:

    python tools/fstmap.py build/extract/sys/main.dol
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
pointers). An unattended check: `WIIKIT_PAD="14:A 16:A 18:A 20:A 22:A 30:+
32:+ 34:+ 36:+ 38:A 40:A 42:A"`, 56 s, reaches the opening scenes (the
presses go to port 1 as the Classic's buttons, then the pad's).
