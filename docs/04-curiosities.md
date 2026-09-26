# What the disc reveals

* **A symbol table.** `data/rkrpg_1.fst`, 177 KB, which the executable
  never opens: the names, sizes and object files of 4 337 functions of
  another build of the game (`03-executable.md`). "rkrpg" is the project's
  name: Rockman (Mega Man's Japanese name) RPG.
* **Debug tools in the shipped code**: the table names `editor.o` (key
  editors for cels, fog and effects: `hokan_cel_key`, `serch_fog_key`…),
  `viewer_efc.o`, `demoview.o`, `dbgwin` ("debug window") functions, and
  `data/facetest.arc` is on the disc and named in the executable. `main`
  draws a performance overlay when asked ("TASK", "ERR", "CPU", "GPU",
  "GPU2", "ST"). The executable names Intelligent Systems' debugger
  interface ("IS-DOL-VIEWER"), and MetroTRK is linked in.
* **A list of eight-character names** next to the overlay's strings, after
  a few stage and door names (`s02m20_0`, `door02_3`): "BATTLE X", "ZERO",
  "SPIDER", "MASSIMO", "MARINO", "CINNAMON", "AXEL", "X AMR1", "X AMR2",
  "Z AMR1", "FIELD X", "OTHER": the playable characters and X's and Zero's
  armours, as a debug viewer or test menu would list them.
* The **Treasure Radar**: `data/bin/gbaradar.bin`, the Game Boy Advance's
  program the game sends over the link cable (the GBA library is linked).
* The music is **2 264 DSP-ADPCM files** in `movie/BGM_STREAM`, a left and a
  right one per piece, streamed, among them `kichi` (base), `machi` (town),
  `zako_battle` (grunt battle), `ridipus_god1`/`2`, and moods: `fuan`
  (unease), `kincho` (tension), `anshin` (relief), `kanashimi` (sorrow),
  `yorokobi` (joy), `comikal`, `isamasi` (brave), `jaaku` (evil).
