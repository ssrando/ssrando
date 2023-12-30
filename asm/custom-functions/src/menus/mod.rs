pub mod sample_menu;
pub mod simple_menu;

use crate::system::button::*;
use sample_menu::SampleMenu;

#[derive(Clone, Copy, PartialEq, Eq)]
enum MenuState {
    Off,
    SampleMenu,
}

#[link_section = "data"]
#[no_mangle]
static mut MENU_STATE: MenuState = MenuState::Off;

// Returns true if any menu is active
pub fn display_menus() -> bool {
    let mut next_menu = unsafe { MENU_STATE };
    match unsafe { MENU_STATE } {
        MenuState::Off => {
            if is_down(DPAD_RIGHT) && is_down(TWO) {
                next_menu = MenuState::SampleMenu;
                SampleMenu::enable();
            }
        },
        MenuState::SampleMenu => {
            SampleMenu::display();
            if SampleMenu::input() {
                next_menu = MenuState::Off;
            }
        },
    }
    unsafe {
        MENU_STATE = next_menu;
    }
    return next_menu != MenuState::Off;
}
