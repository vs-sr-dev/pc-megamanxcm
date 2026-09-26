// Mega Man X: Command Mission — the port's own layer over the wiikit runtime.
//
// Linked into wiiboot by mmxcm.cmake. What belongs here is what only this
// game needs.
#include "mem.h"
#include "rt.h"

namespace {

// SoundInit gives the sound driver (CpInitSoundDriver, through
// CpCall_SndDriver) a pointer to a local it never writes (its r1 + 8), and
// the driver takes its heap from there. On the console that slot holds what
// the last call at that depth left: the r30 VIWaitForRetrace saved while
// ARAMInit waited for its transfer, 0 since __init_registers, so the driver
// allocates from heap 0. Here the transfer can end before that wait starts
// (the host's thread can be held up longer than the whole transfer), and an
// interrupt frame's back chain lands in the slot instead: a heap of
// 0x805Cxxxx, and a crash in OSAllocFromHeap. The slot is given the
// console's 0 before the call.
PPCFunc orig_sound_init = nullptr;
void sound_init(PPCContext& c) {
    st32(c.r[1] - 0x20 + 8, 0);                  // its frame is 0x20 bytes
    orig_sound_init(c);
}

void install() {
    orig_sound_init = ppc_hook("SoundInit", sound_init);
}

RtGameLayer layer("Mega Man X: Command Mission", install);

}  // namespace
