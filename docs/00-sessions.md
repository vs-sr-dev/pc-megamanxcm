# Session log

## Session 1 — from the disc to the first cutscene

Goal: feasibility, as Arc Rise Fantasia's first session was: what is on the
disc (a leftover map? RELs? which SDK, which sound library), a recompile, a
first boot, and the GameCube support that needs in wiikit. It went past
that: the game boots to its title, a new game starts, and its opening
scenes play in 3D with the pad, silent.

Results:

* **The disc** (`01-disc-layout.md`): GXRP08, the European release,
  English, French and German; the RVZ read by `wiikit.disc`, which learnt
  GameCube discs for it (no partitions, no encryption, offsets in bytes):
  4 246 files, 1.35 GB. THP movies, the music as 2 264 streamed DSP-ADPCM
  files, Capcom's own `.arc` archives.
* **The executable** (`03-executable.md`): stripped, the Dolphin SDK of
  April–May 2004; the sound is **MusyX** under Capcom's own driver
  ("snddrv 1.69v"), MusyX booting the **AX micro-code** itself (Dolphin's
  hash 0x3AD3B7AC): no custom micro-code, the risk the plan named. Names:
  816 from Dolphin's signatures, then the find of the session, a **symbol
  table on the disc** (`data/rkrpg_1.fst`, another build's): aligned by
  order and size, it names 4 136 of the 4 222 functions, the game's own
  included (`04-curiosities.md`). Recompiled at the first try: 4 222 units,
  no gaps, every switch table sized; compiled and linked at the first try.
* **The GameCube in wiikit** (`10-wiikit.md`): the console decided by the
  disc; its 162 MHz bus (the time base at 40.5 MHz); the IPL's globals
  without IOS; the disc drive at its registers; 16 MB of ARAM; the
  controllers on SI, from the host's pads and keyboard. The Wii's paths are
  unchanged, checked on the four Wii ports.
* **Three boots that stopped, and why**:
  - the sound driver took its heap from a stack slot the game never writes
    (`SoundInit` passes a pointer to an uninitialised local): on the console
    it holds 0, left by `VIWaitForRetrace` during `ARAMInit`'s wait; here the
    ARAM transfer ended before the wait began and an interrupt frame's back
    chain landed there, a heap of 0x805Cxxxx, a crash. ARAM transfers now
    last as long as the console's, and the port's layer gives the slot the
    console's 0 (`tools/mmxcm.cpp`): timing alone cannot guarantee it;
  - the controller's type was refused: `COMERR`, left by the empty ports,
    was kept across transfers; it is the last transfer's, read only;
  - `load_file` set its "busy" flag after `DVDReadAsync` returned, and the
    disc's commands, finishing at once, had run all their callbacks before
    that: busy for ever, a black screen. Disc commands now take a drive's
    time (1 ms, and 16 MB/s).
* **It runs**: "Licensed by Nintendo", "Presented in Dolby Pro Logic II",
  the memory card check ("No Memory Card found in Slot A and Slot B", A to
  go on), the CAPCOM logo, the title ("Press START"), the menu (New Game,
  Load Game, Options), a new game ("ACCESS"), the opening scenes in real-time
  3D with their subtitles (X, Zero and Axl in the rain, the briefing on Giga
  City). 50 frames a second (PAL). Played with scripted presses
  (`WIIKIT_PAD`) and seen in dumped frames; an Xbox One pad is found and
  answers.

Left: the sound (the GameCube's AX), the memory cards (no save yet), the
dark screens before the title (a movie? to compare with Dolphin), play
beyond the opening.

## Session 2 — the sound

Goal: the GameCube's AX micro-code, the first item of the plan. Done in
one step, and it answered a second item on the way.

Results:

* **The sound** (`05-audio.md`): wiikit mixes the GameCube's AX command
  lists (`10-wiikit.md`), written from Dolphin's `AXUCode`: 5 ms frames,
  each voice run a millisecond at a time with MusyX's queued updates,
  three buses, samples read from ARAM. It worked at the first build: the
  music (DSP-ADPCM streamed into ARAM), the effects and the voices, played
  by the user past the opening and judged perfect, but for one
  micro-stutter at the start of a spoken line.
* **The dark screens before the title were the opening movie**, waiting:
  its player follows its sound by its AX voice's position, which nothing
  moved while the lists went unmixed. With the sound, `op.thp` plays.
* **The camera**: the C stick turns the view the way of 2004 (the other
  way from today's games), with no option in the game. The port's layer
  turns the C stick's X around (`MMXCM_CAMERA=console` keeps the
  console's way); the vertical axis moves nothing. For it, wiikit's port
  filter for the Classic Controller now also sees the GameCube's
  controllers.
* The four Wii ports were checked with the new wiikit: the same screens
  and, their sound dumped, the same loudness second by second.

Left: the memory cards, the micro-stutter, play on.
