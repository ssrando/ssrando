use super::simple_menu::SimpleMenu;
use crate::menus::main_menu::MainMenu;
use crate::send_to_start;
use crate::system::button::*;

#[derive(Clone, Copy, PartialEq, Eq)]
enum SampleMenuState {
    Off,
    Main,
    Sub,
}

pub struct SampleMenu {
    state:       SampleMenuState,
    main_cursor: usize,
    sub_cursor:  usize,
}

#[link_section = "data"]
#[no_mangle]
pub static mut SAMPLE_MENU: SampleMenu = SampleMenu {
    state:       SampleMenuState::Off,
    main_cursor: 0,
    sub_cursor:  0,
};

const NUM_ENTRIES_MAIN: usize = 1;
const NUM_ENTRIES_SUB: usize = 1;

impl SampleMenu {
    pub fn enable() {
        unsafe { SAMPLE_MENU.state = SampleMenuState::Main };
    }
    // returns true if in off state
    pub fn input() -> bool {
        let up_pressed = is_pressed(DPAD_UP);
        let down_pressed = is_pressed(DPAD_DOWN);
        let b_pressed = is_pressed(B);
        let a_pressed = is_pressed(A);

        let mut next_menu = unsafe { SAMPLE_MENU.state };

        match unsafe { SAMPLE_MENU.state } {
            SampleMenuState::Off => {},
            SampleMenuState::Main => {
                if b_pressed {
                    next_menu = SampleMenuState::Off;
                } else if a_pressed {
                    match unsafe { SAMPLE_MENU.main_cursor } {
                        0 => {
                            next_menu = SampleMenuState::Sub;
                        },
                        _ => {},
                    }
                } else if up_pressed {
                    unsafe {
                        SAMPLE_MENU.main_cursor =
                            (SAMPLE_MENU.main_cursor + (NUM_ENTRIES_MAIN - 1)) % NUM_ENTRIES_MAIN;
                    }
                } else if down_pressed {
                    unsafe {
                        SAMPLE_MENU.main_cursor = (SAMPLE_MENU.main_cursor + 1) % NUM_ENTRIES_MAIN;
                    }
                }
            },
            SampleMenuState::Sub => {
                if b_pressed {
                    next_menu = SampleMenuState::Main;
                } else if a_pressed {
                    match unsafe { SAMPLE_MENU.main_cursor } {
                        0 => {
                            send_to_start();
                            next_menu = SampleMenuState::Off;
                            MainMenu::disable();
                        },
                        _ => {},
                    }
                } else if up_pressed {
                    unsafe {
                        SAMPLE_MENU.main_cursor =
                            (SAMPLE_MENU.main_cursor + (NUM_ENTRIES_MAIN - 1)) % NUM_ENTRIES_SUB;
                    }
                } else if down_pressed {
                    unsafe {
                        SAMPLE_MENU.main_cursor = (SAMPLE_MENU.main_cursor + 1) % NUM_ENTRIES_SUB;
                    }
                }
            },
        }
        unsafe {
            SAMPLE_MENU.state = next_menu;
        }
        return next_menu == SampleMenuState::Off;
    }

    pub fn display() {
        match unsafe { SAMPLE_MENU.state } {
            SampleMenuState::Off => {},
            SampleMenuState::Main => {
                let mut menu =
                    SimpleMenu::<{ NUM_ENTRIES_MAIN + 2 }, 20>::new(10, 10, 10, "Sample Menu");
                menu.current_line = unsafe { SAMPLE_MENU.main_cursor as u32 };
                menu.add_entry("Load");
                menu.draw();
            },
            SampleMenuState::Sub => {
                let mut menu =
                    SimpleMenu::<{ NUM_ENTRIES_SUB + 2 }, 20>::new(10, 10, 10, "Sample Sub Menu");
                menu.current_line = unsafe { SAMPLE_MENU.sub_cursor as u32 };
                menu.add_entry("Warp To Start");
                menu.draw();
            },
        }
    }
}
