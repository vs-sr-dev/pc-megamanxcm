# The disc

**GXRP08**, "MEGA MAN X COMMAND MISSION", the European release (Capcom,
2004; English, French and German), a GameCube disc. The work is done on an
RVZ image, which `wiikit.disc` reads as it is (its GameCube support was
written for this port, `10-wiikit.md`):

    python -m wiikit.disc "Mega Man X - Command Mission (Europe) (En,Fr,De).rvz" --info
    python -m wiikit.disc "Mega Man X - Command Mission (Europe) (En,Fr,De).rvz" --extract build/extract

A GameCube disc has no partitions and no encryption: 1.46 GB of image, 4 246
files, 1.35 GB extracted in 16 seconds. The DOL at 0x20300, the FST at
0x40FE00 (100 793 bytes). No RELs; `sys/main.dol` is the whole program
(`03-executable.md`).

| Directory | Size | Files | What |
|---|---|---|---|
| `data/` (its root) | 362 MB | 219 | the game's archives (`.arc`): `first`, `common`, `fcommon`, `gameover` in three languages (`…E`, `…F`, `…G`), the stages (`s0001`, `s0101`…), `logo`, `tuto`, `facetest`; the symbol table `rkrpg_1.fst` (`03-executable.md`) |
| `data/demo/` | 324 MB | 752 | the story's scenes: captions (`cap/`), clips (`clp/`), and 112 key files (`key/`, text: "FRAME MAX 3160" and rows of numbers) |
| `movie/` | 236 MB | 2 | THP movies: the opening (`op.thp`) and the ending (`ed.thp`) |
| `movie/BGM_STREAM/` | 207 MB | 2 264 | the music, streamed: DSP-ADPCM (`.dsp`), each piece a left and a right file (`s01_l.dsp`, `s01_r.dsp`…), the executable naming them |
| `data/battle/` | 126 MB | 401 | battles: enemies (`b_em…`), the party, per-language text (`en/`, `fr/`, `ge/`) |
| `data/figure/`, `effect/`, `design/`, `npc/` | 80 MB | 444 | characters, effects, 2D |
| `data/help/`, `mes/` | 8 MB | 131 | help and messages, three languages |
| `data/haken/`, `subwin/` | 8 MB | 31 | the dispatch missions ("haken"), sub-windows |
| `data/bin/gbaradar.bin` | 61 KB | 1 | the Game Boy Advance's program for the Treasure Radar (sent over the link cable) |
| `opening.bnr` | 6 KB | 1 | the banner: "Mega Man X Command Mission", "(c)CAPCOM CO., LTD. 2004" |

By extension: 2 264 `.dsp`, 1 864 `.arc`, 112 `.txt`, 2 `.thp`, 2 `.bin`,
one `.fst`, one `.bnr`. The `.arc` files are Capcom's own archive, not U8:
a 0x20-byte header whose first eight bytes are a name, reversed (`nommoc`,
"common", in `commonE.arc` and in `firstE.arc` too; `91m20s` in
`tuto.arc`). The game's formats are not studied yet: the port runs the
game's code on them.
