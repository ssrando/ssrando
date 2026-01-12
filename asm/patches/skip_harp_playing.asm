.open "d_a_obj_warpNP.rel"

; At the end of dAcOWarp::executeState_GateWait
; check to see if we should open the trial gate
.org 0x2818 ; 80cd1688
b check_and_open_trial_gate ; originally lwz r0, 0x24(r1)

; After opening the gate, branch to our cleanup start replacement
.org 0x280C ; 80cd167c
b gate_wait_cleanup_start

.close