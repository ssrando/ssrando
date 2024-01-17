pub mod char_writer;
pub mod console;
pub mod graphics;
pub mod menu;

pub fn simple_rng(rng: &mut u32) -> u32 {
    *rng = rng.wrapping_mul(1664525).wrapping_add(1013904223);
    *rng
}
