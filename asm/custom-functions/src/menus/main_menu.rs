use super::sample_menu::SampleMenu;
use super::simple_menu::SimpleMenu;
use super::warp_menu::WarpMenu;
use crate::system::button::*;

#[derive(Clone, Copy, PartialEq, Eq)]
enum MenuState {
    Off,
    MenuSelect,
    SampleMenu,
    WarpMenu,
}
const NUM_MENU_ENTRIES: usize = 2;

pub struct MainMenu {
    state:       MenuState,
    main_cursor: usize,
    force_close: bool,
}

#[link_section = "data"]
#[no_mangle]
pub static mut MAIN_MENU: MainMenu = MainMenu {
    state:       MenuState::Off,
    main_cursor: 0,
    force_close: false,
};

impl MainMenu {
    // returns treu if menu is active
    pub fn disable() {
        unsafe { MAIN_MENU.force_close = true };
        set_buttons_not_pressed(B);
    }

    pub fn display() -> bool {
        let mut next_menu = unsafe { MAIN_MENU.state };
        match unsafe { MAIN_MENU.state } {
            MenuState::Off => {
                if is_down(DPAD_RIGHT) && is_down(TWO) {
                    next_menu = MenuState::MenuSelect;
                }
            },
            MenuState::MenuSelect => {
                let mut menu = SimpleMenu::<5, 20>::new(10, 10, 10, "Main Menu Select");
                menu.current_line = unsafe { MAIN_MENU.main_cursor as u32 };
                menu.add_entry("Sample Menu");
                menu.add_entry("Warp Menu");
                menu.draw();
                if is_pressed(B) {
                    next_menu = MenuState::Off;
                    set_buttons_not_pressed(B);
                } else if is_pressed(A) {
                    next_menu = match menu.current_line {
                        0 => {
                            SampleMenu::enable();
                            MenuState::SampleMenu
                        },
                        1 => {
                            WarpMenu::enable();
                            MenuState::WarpMenu
                        },
                        _ => next_menu,
                    };
                } else if is_pressed(DPAD_UP) {
                    unsafe {
                        MAIN_MENU.main_cursor = (MAIN_MENU.main_cursor + NUM_MENU_ENTRIES - 1) % 2;
                    }
                } else if is_pressed(DPAD_DOWN) {
                    unsafe {
                        MAIN_MENU.main_cursor = (MAIN_MENU.main_cursor + 1) % 2;
                    }
                }
            },
            MenuState::SampleMenu => {
                SampleMenu::display();
                if SampleMenu::input() {
                    next_menu = MenuState::MenuSelect;
                }
            },
            MenuState::WarpMenu => {
                WarpMenu::display();
                if WarpMenu::input() {
                    next_menu = MenuState::MenuSelect;
                }
            },
        }
        unsafe {
            if MAIN_MENU.force_close {
                MAIN_MENU.force_close = false;
                MAIN_MENU.state = MenuState::Off;
            } else {
                MAIN_MENU.state = next_menu;
            }
        }
        return next_menu != MenuState::Off;
    }
}
