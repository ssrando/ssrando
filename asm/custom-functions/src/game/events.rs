#[repr(C)]
pub struct ActorEventFlowMgr {
    pub vtable:                     u32,
    pub msbf_info:                  u32,
    pub current_flow_index:         u32,
    pub unk1:                       u32,
    pub unk2:                       u32,
    pub unk3:                       u32,
    pub result_from_previous_check: u32,
    pub current_text_label_name:    [u8; 32],
    pub unk4:                       u32,
    pub unk5:                       u32,
    pub unk6:                       u32,
    pub next_flow_delay_timer:      u32,
    pub another_flow_element:       u128,
    pub unk7:                       u32,
    pub unk8:                       u32,
}
