// This file was adapted using https://github.com/CryZe/libtww-core/blob/master/src/game/gamepad.rs as guidance

#[repr(C)]
struct CoreController {
    pad:              [u8; 0x18],
    buttons_down:     u32,
    buttons_pressed:  u32,
    buttons_released: u32,
}
extern "C" {
    static CORE_CONTROLLER: *mut CoreController;
}

bitflags::bitflags! {
    pub struct Buttons: u32 {
        const DPAD_LEFT = 0x0001;
        const DPAD_RIGHT = 0x0002;
        const DPAD_DOWN = 0x0004;
        const DPAD_UP = 0x0008;
        const PLUS = 0x0010;
        const TWO = 0x0100;
        const ONE = 0x0200;
        const B = 0x0400;
        const A = 0x0800;
        const MINUS = 0x1000;
        const Z = 0x2000;
        const C = 0x4000;
    }
}

pub const DPAD_LEFT: Buttons = Buttons::DPAD_LEFT;
pub const DPAD_RIGHT: Buttons = Buttons::DPAD_RIGHT;
pub const DPAD_DOWN: Buttons = Buttons::DPAD_DOWN;
pub const DPAD_UP: Buttons = Buttons::DPAD_UP;
pub const PLUS: Buttons = Buttons::PLUS;
pub const TWO: Buttons = Buttons::TWO;
pub const ONE: Buttons = Buttons::ONE;
pub const B: Buttons = Buttons::B;
pub const A: Buttons = Buttons::A;
pub const MINUS: Buttons = Buttons::MINUS;
pub const Z: Buttons = Buttons::Z;
pub const C: Buttons = Buttons::C;

pub fn buttons_down() -> Buttons {
    unsafe { Buttons::from_bits_truncate((*CORE_CONTROLLER).buttons_down) }
}

pub fn buttons_pressed() -> Buttons {
    unsafe { Buttons::from_bits_truncate((*CORE_CONTROLLER).buttons_pressed) }
}

pub fn set_buttons_down(buttons: Buttons) {
    unsafe {
        (*CORE_CONTROLLER).buttons_down = buttons.bits();
    }
}

pub fn set_buttons_pressed(buttons: Buttons) {
    unsafe {
        (*CORE_CONTROLLER).buttons_pressed = buttons.bits();
    }
}

pub fn is_down(buttons: Buttons) -> bool {
    buttons_down().contains(buttons)
}

pub fn is_pressed(buttons: Buttons) -> bool {
    buttons_pressed().contains(buttons)
}

pub fn is_any_down(buttons: Buttons) -> bool {
    buttons_down().intersects(buttons)
}

pub fn is_any_pressed(buttons: Buttons) -> bool {
    buttons_pressed().intersects(buttons)
}
