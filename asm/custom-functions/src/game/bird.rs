#[repr(C)]
pub struct AcOBird {
    pub pad:   [u8; 0x144],
    pub speed: f32,
}
