# This port and wiikit

This port takes [wiikit](https://github.com/vs-sr-dev/wiikit) as a
submodule at `wiikit/`, like the four Wii ports (pc-victorious,
pc-dragonquestswords, pc-conduit2, pc-arcrisefantasia). It is its fifth
user and its first GameCube game: the GameCube support went into wiikit
itself, one toolkit, because the two consoles share the processor, the
GPU, the DSP and most of the SDK. Changes made for it are described by what
they do (wiikit's commits of sessions 1 and 2 call it "a stripped 2004
GameCube game", written before this port was published), and checked on every port before they go in.

## What this port used as it is

`dol`, `ppc`, `cw`, the recompiler with discovery (4 222 units, 0 gaps),
and the whole runtime: the CPU, the OS layer (threads, interrupts, the
decrementer), GX and the renderer (the logos, the title, the menus, the
opening scenes in 3D, drawn right at the first sight), VI, the EXI's IPL
chip (fonts, SRAM, RTC), the DSP's mailboxes and boot, the AI DMA, the
port's layer.

In session 2, for the sound: the Wii's accelerator (its ADPCM and PCM
decoding, loops, streams), resampler and filters, the AI DMA's pacing,
the host's audio output (`audio.cpp`), the Classic filter of the port's
layer.

## What it gave wiikit (sessions 1–2)

| Commit | Change | Layer | Why it is not game knowledge |
|---|---|---|---|
| `a4fc05f` | **GameCube discs** in `wiikit.disc`: the GameCube magic, no partitions, the whole disc as the volume, boot.bin's and the FST's offsets in bytes (`Volume`, `GcVolume`); `--info` says Wii or GameCube | 1–2 | every GameCube disc |
| `d403beb` | **the console from the disc**: `g_gamecube`, the bus clock (162 MHz; the time base at 40.5 MHz), the IPL's globals (board, clocks, ARAM size, the region from BI2), no NAND, SYSCONF, IOS or Remote | 5 | every GameCube game |
| `d403beb` | **the disc drive** at its registers (DI): read (and the disc id), inquiry, request error, the audio stream's commands; each ends after a drive's time, the data with the interrupt | 5 | the GameCube's SDK reads the disc itself; a game that sets its busy flag after `DVDReadAsync` returns stayed busy for ever when commands ended at once |
| `d403beb` | **ARAM**: 16 MB, DMA both ways, addresses wrapping as with no expansion (ARInit's check finds 16 MB), `AR_MODE` ready; a transfer lasts as long as the console's | 5 | every GameCube game; a transfer ended too early let this game read a stack slot the wait would have written |
| `d403beb` | **controllers on SI**: a standard pad on each port the host has one for (port 1: the keyboard too, there from the start), type, origin, the direct state, the poll at each retrace (INBUFH/L, RDST, its interrupt), rumble; `COMERR` read only, the last transfer's | 5 | every GameCube game; with `COMERR` kept, the SDK refused the pad's type |
| `d403beb` | `WIIKIT_DIDBG=1` (`=bt`: the guest's call chain), `WIIKIT_SIDBG=1` | 5 | debugging any GameCube game |
| `761b9a7` | **the GameCube's AX micro-code** (`ax.cpp`, from Dolphin's `AXUCode`): 5 ms frames of 160 samples, each voice a millisecond at a time with the queued PB updates, three buses, the 16-bit mixer control, a signed envelope, its commands; the Wii's accelerator reading ARAM (`aram_read`) | 5 | every GameCube game on AX, MusyX's included; a movie player that follows its voice's position waited for ever without it |
| `761b9a7` | the port's Classic filter (`wpad_set_classic_filter`) also on the GameCube's controllers on SI | 5 | a port that reshapes its game's input (Conduit 2's mouse on a stick, this game's camera) does it the same way on both consoles |
| `761b9a7` | `WIIKIT_AUDIODUMP`'s WAV header written each second | 5 | the runtime quits with `_Exit`: the header stayed empty |

The Wii's paths are unchanged (Victorious's self-test 15/15; the four Wii
ports to the same screens as before, old and new builds side by side; after
`761b9a7` also their sound, dumped: the same loudness second by second).

## What it will give wiikit

| Addition | Layer | Why |
|---|---|---|
| memory cards on EXI, CARD's unlock (a second DSP task) | 5 | every GameCube game that saves |
| EuRGB60 for PAL GameCube games (the SRAM's flag) | 5 | PAL GameCube games |
| `tools/fstmap.py`'s alignment (a symbol list of another build, by order and size) | 3 | any stripped executable with a near symbol list: ARF aligned objects by hand the same way |
