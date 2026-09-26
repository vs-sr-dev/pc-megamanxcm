# The sound

## The chain

The game's sound goes through three layers before the hardware:

1. **Capcom's sound driver**, `slib.a` ("snddrv: ver:1.69v Sep 21 2004"):
   `SoundInit` configures it, and the game talks to it through
   `CpCall_SndDriver` and its commands.
2. **MusyX** (Factor 5's sound system, `musyx.a`): the driver's engine.
   It boots the DSP itself (`salInitDsp`), with the AX micro-code linked
   into the DOL at 803D2160 (0x1EC0 bytes, Dolphin's hash 0x3AD3B7AC, the
   one Paper Mario: The Thousand-Year Door and Naruto 3 use). It then
   writes AX's command lists and voices (PBs) itself: no `ax.a` is linked.
3. **The AX micro-code** on the DSP: each 5 ms it runs one command list.
   The list mixes the voices, sends the aux buses to the CPU's effects,
   and writes 160 stereo samples where the AI DMA plays them.

The port replaces only the third layer. wiikit's `ax.cpp` does what the
micro-code does with each list, as Dolphin's `AXUCode` describes it
(`10-wiikit.md`). Everything above it is the game's own code, recompiled.

## What the game plays

A trace of the voices (`WIIKIT_AXTRACE=3000:9000`, from the Nintendo
screens to the opening scenes) shows three kinds:

| Voices | Format | Rate (resampler ratio) | What |
|---|---|---|---|
| two, always on | DSP-ADPCM | 32 kHz (1.0) | the music, left and right (`movie/BGM_STREAM/*.dsp`), streamed into ARAM; one of the two also feeds aux B (the effect) |
| two, during the movie | 16-bit PCM | 48 kHz (1.5) | the opening movie's sound (`movie/op.thp`) |
| a few, briefly | DSP-ADPCM | 20 kHz (0.625) | effects and voices |

At most four voices played at once. The mixer control words are `000B`
(main left and right, with volume ramps) and `460B` (the same, plus aux B
left and right; `4000` is the Dolby Pro Logic II flag, which Dolphin
reads as the choice of aux B's input and which the stereo mix ignores).
The per-millisecond PB updates (MusyX's way to start a note between two
frames) were used 30 times: they are applied. No DTK (the drive's own
audio streaming) is used, although `dtk.a` is linked: the disc has no
ADP file.

## The movie that waited for its sound

In session 1 the screens after the CAPCOM logo stayed dark: that was the
opening movie, `op.thp`, not playing. Its player learns which of its sound
buffers has been played from its AX voice's position. With the command
lists unmixed, nothing moved that position: the player waited for ever.
With the lists mixed, the movie plays, with its sound.

## By ear

In session 2 the user played past the opening scenes and judged the
music, the effects, the voices, the movie and the menus "perfect". Left: one micro-stutter at
the start of a spoken line in a cutscene, most likely the voices' bank
loaded (disc, then ARAM) while the sound is being prepared. To be traced
(`07-next-session.md`).

`WIIKIT_AUDIODUMP=file.wav` writes everything played; `WIIKIT_AXTRACE=
first:count` writes the voices of those AX frames (200 a second) to
`axtrace.txt`; `WIIKIT_DSPDBG=1` traces the DSP's mails.
