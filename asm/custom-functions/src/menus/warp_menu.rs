use crate::information::stage_info::*;
use crate::menus::main_menu::MainMenu;
use crate::menus::simple_menu::SimpleMenu;
use crate::system::button::*;
use crate::{actuallyTriggerEntrance, Reloader__setReloadTrigger, RELOADER_PTR};

use core::ffi::CStr;
use cstr::cstr;

const NUM_ENTRIES_MAIN: u8 = 7;

#[derive(Copy, Clone, PartialEq, Eq)]
enum WarpState {
    Off,
    Main,
    Stage,
    Details,
}

#[derive(Copy, Clone, PartialEq, Eq)]
enum WarpStage {
    Sky,
    Faron,
    Eldin,
    Lanayru,
    SealedGrounds,
    Dungeon,
    SilentRealm,
    None,
}

impl WarpStage {
    fn from_idx(idx: usize) -> Self {
        match idx {
            0 => WarpStage::Sky,
            1 => WarpStage::Faron,
            2 => WarpStage::Eldin,
            3 => WarpStage::Lanayru,
            4 => WarpStage::SealedGrounds,
            5 => WarpStage::Dungeon,
            6 => WarpStage::SilentRealm,
            _ => WarpStage::None,
        }
    }
    fn get_name(&self) -> &'static str {
        match self {
            WarpStage::Sky => "Sky",
            WarpStage::Faron => "Faron",
            WarpStage::Eldin => "Eldin",
            WarpStage::Lanayru => "Lanayru",
            WarpStage::SealedGrounds => "SealedGrounds",
            WarpStage::Dungeon => "Dungeon",
            WarpStage::SilentRealm => "SilentRealm",
            WarpStage::None => "None",
        }
    }

    fn get_num_stages(&self) -> u8 {
        match self {
            WarpStage::Sky => 22,
            WarpStage::Faron => 8,
            WarpStage::Eldin => 13,
            WarpStage::Lanayru => 16,
            WarpStage::SealedGrounds => 8,
            WarpStage::Dungeon => 20,
            WarpStage::SilentRealm => 4,
            WarpStage::None => 0,
        }
    }

    fn get_stage_info(&self, idx: u8) -> StageInfo {
        match self {
            WarpStage::Sky => {
                match idx {
                    0 => F000,
                    1 => F001r,
                    2 => F002r,
                    3 => F004r,
                    4 => F005r,
                    5 => F006r,
                    6 => F007r,
                    7 => F008r,
                    8 => F009r,
                    9 => F010r,
                    10 => F011r,
                    11 => F012r,
                    12 => F013r,
                    13 => F014r,
                    14 => F015r,
                    15 => F016r,
                    16 => F017r,
                    17 => F018r,
                    18 => F019r,
                    19 => F020,
                    20 => F021,
                    21 => F023,
                    _ => F000,
                }
            },
            WarpStage::Faron => {
                match idx {
                    0 => F100,
                    1 => F100_1,
                    2 => F101,
                    3 => F102,
                    4 => F102_1,
                    5 => F102_2,
                    6 => F103,
                    7 => F103_1,
                    _ => F100,
                }
            },
            WarpStage::Eldin => {
                match idx {
                    0 => F200,
                    1 => F201_1,
                    2 => F201_2,
                    3 => F201_3,
                    4 => F201_4,
                    5 => F202,
                    6 => F202_1,
                    7 => F202_2,
                    8 => F202_3,
                    9 => F202_4,
                    10 => F210,
                    11 => F211,
                    12 => F221,
                    _ => F200,
                }
            },
            WarpStage::Lanayru => {
                match idx {
                    0 => F300,
                    1 => F300_1,
                    2 => F300_2,
                    3 => F300_3,
                    4 => F300_4,
                    5 => F300_5,
                    6 => F301,
                    7 => F301_1,
                    8 => F301_2,
                    9 => F301_3,
                    10 => F301_4,
                    11 => F301_5,
                    12 => F301_6,
                    13 => F301_7,
                    14 => F302,
                    15 => F303,
                    _ => F300,
                }
            },
            WarpStage::SealedGrounds => {
                match idx {
                    0 => F400,
                    1 => F401,
                    2 => F402,
                    3 => F403,
                    4 => F404,
                    5 => F405,
                    6 => F406,
                    7 => F407,
                    _ => F400,
                }
            },
            WarpStage::Dungeon => {
                match idx {
                    0 => D000,
                    1 => D100,
                    2 => B100,
                    3 => B100_1,
                    4 => D101,
                    5 => B101,
                    6 => B101_1,
                    7 => D200,
                    8 => B200,
                    9 => D201,
                    10 => D201_1,
                    11 => B201,
                    12 => B201_1,
                    13 => D300,
                    14 => D300_1,
                    15 => B300,
                    16 => D301,
                    17 => D301_1,
                    18 => B301,
                    19 => B400,
                    _ => D000,
                }
            },
            WarpStage::SilentRealm => {
                match idx {
                    0 => S000,
                    1 => S100,
                    2 => S200,
                    3 => S300,
                    _ => S000,
                }
            },
            WarpStage::None => StageInfo::default(),
        }
    }

    fn get_stage_name(&self, idx: u8) -> &'static str {
        self.get_stage_info(idx).name
    }
}

pub struct WarpMenu {
    state:             WarpState,
    stage_state:       WarpStage,
    stage_selected:    [u8; 8],
    main_cursor:       u8,
    stage_cursor:      u8,
    detail_cursor:     u8,
    selected_room:     u8,
    selected_layer:    u8,
    selected_entrance: u8,
}

impl WarpMenu {
    fn get_room(&self) -> u8 {
        self.stage_state.get_stage_info(self.stage_cursor).rooms[self.selected_room as usize]
    }
    fn get_layer(&self) -> u8 {
        self.stage_state.get_stage_info(self.stage_cursor).layers[self.selected_layer as usize]
    }
    fn get_entrance(&self) -> u8 {
        self.selected_entrance
    }
    fn warp(&mut self) {
        let stage_name = self.stage_state.get_stage_name(self.stage_cursor);
        for n in 0..8 {
            self.stage_selected[n] = if n < stage_name.len() {
                stage_name.as_bytes()[n] as u8
            } else {
                0
            };
        }
        let room = self.get_room();
        let layer = self.get_layer();
        let entrance = self.get_entrance();
        let forced_night: u8 = match self.stage_state {
            WarpStage::Sky => {
                if layer % 2 == 0 {
                    0
                } else {
                    1
                }
            },
            _ => 0,
        };
        let forced_trial: u8 = match self.stage_state {
            WarpStage::SilentRealm => 1,
            _ => 0,
        };
        let transition_type = 0;
        unsafe {
            actuallyTriggerEntrance(
                self.stage_selected.as_ptr(),
                room,
                layer,
                entrance,
                forced_night,
                forced_trial,
                transition_type,
                0xF,  // transition_fade_frames:  u8
                0xFF, // param_9: u8
            );
            Reloader__setReloadTrigger(RELOADER_PTR, 5);
        }
    }

    fn change_room(&mut self, num: i8) {
        let num_rooms = self
            .stage_state
            .get_stage_info(self.stage_cursor)
            .rooms
            .len();
        self.selected_room =
            (self.selected_room as i8 + num_rooms as i8 + num) as u8 % num_rooms as u8;
    }
    fn change_layer(&mut self, num: i8) {
        let num_layers = self
            .stage_state
            .get_stage_info(self.stage_cursor)
            .layers
            .len();
        self.selected_layer =
            (self.selected_layer as i8 + num_layers as i8 + num) as u8 % num_layers as u8;
    }
    fn change_entrance(&mut self, num: i8) {
        self.selected_entrance = (self.selected_entrance as i8 + num) as u8;
    }
}

#[link_section = "data"]
#[no_mangle]
static mut WARP_MENU: WarpMenu = WarpMenu {
    state:             WarpState::Off,
    stage_state:       WarpStage::None,
    stage_selected:    [0u8; 8],
    main_cursor:       0,
    stage_cursor:      0,
    detail_cursor:     0,
    selected_room:     0,
    selected_layer:    0,
    selected_entrance: 0,
};

impl WarpMenu {
    pub fn enable() {
        unsafe { WARP_MENU.state = WarpState::Main };
    }

    pub fn input() -> bool {
        let b_pressed = is_pressed(B);
        let a_pressed = is_pressed(A);
        let up_pressed = is_pressed(DPAD_UP);
        let down_pressed = is_pressed(DPAD_DOWN);
        let right_pressed = is_pressed(DPAD_RIGHT);
        let left_pressed = is_pressed(DPAD_LEFT);

        let mut next_state = unsafe { WARP_MENU.state };

        match next_state {
            WarpState::Off => {},
            WarpState::Main => {
                if b_pressed {
                    next_state = WarpState::Off;
                } else if a_pressed {
                    next_state = WarpState::Stage;
                    unsafe {
                        WARP_MENU.stage_state = WarpStage::from_idx(WARP_MENU.main_cursor.into());
                        if WARP_MENU.stage_cursor >= WARP_MENU.stage_state.get_num_stages() {
                            WARP_MENU.stage_cursor = 0;
                        }
                    }
                } else if up_pressed {
                    unsafe {
                        WARP_MENU.main_cursor =
                            (WARP_MENU.main_cursor + NUM_ENTRIES_MAIN - 1) % NUM_ENTRIES_MAIN;
                    }
                } else if down_pressed {
                    unsafe {
                        WARP_MENU.main_cursor = (WARP_MENU.main_cursor + 1) % NUM_ENTRIES_MAIN;
                    }
                }
            },
            WarpState::Stage => {
                if b_pressed {
                    next_state = WarpState::Main;
                    unsafe { WARP_MENU.stage_state = WarpStage::None };
                } else if a_pressed {
                    next_state = WarpState::Details;
                } else if up_pressed {
                    unsafe {
                        let num_entries = WARP_MENU.stage_state.get_num_stages();
                        WARP_MENU.stage_cursor =
                            (WARP_MENU.stage_cursor + num_entries - 1) % num_entries;
                    }
                } else if down_pressed {
                    unsafe {
                        let num_entries = WARP_MENU.stage_state.get_num_stages();
                        WARP_MENU.stage_cursor = (WARP_MENU.stage_cursor + 1) % num_entries;
                    }
                }
            },
            WarpState::Details => {
                if b_pressed {
                    next_state = WarpState::Stage;
                    unsafe {
                        WARP_MENU.selected_entrance = 0;
                        WARP_MENU.selected_room = 0;
                        WARP_MENU.selected_layer = 0;
                    }
                } else if a_pressed {
                    unsafe { WARP_MENU.warp() };
                    unsafe { WARP_MENU.stage_state = WarpStage::None };
                    next_state = WarpState::Off;
                    MainMenu::disable();
                    unsafe {
                        WARP_MENU.selected_entrance = 0;
                        WARP_MENU.selected_room = 0;
                        WARP_MENU.selected_layer = 0;
                    }
                } else if up_pressed {
                    unsafe {
                        WARP_MENU.detail_cursor = (WARP_MENU.detail_cursor + 3 - 1) % 3;
                    }
                } else if down_pressed {
                    unsafe {
                        WARP_MENU.detail_cursor = (WARP_MENU.detail_cursor + 1) % 3;
                    }
                } else if right_pressed || left_pressed {
                    unsafe {
                        match WARP_MENU.detail_cursor {
                            0 => WARP_MENU.change_room(if right_pressed { 1 } else { -1 }),
                            1 => WARP_MENU.change_layer(if right_pressed { 1 } else { -1 }),
                            2 => WARP_MENU.change_entrance(if right_pressed { 1 } else { -1 }),
                            _ => {},
                        }
                    }
                }
            },
        }

        unsafe { WARP_MENU.state = next_state };
        return next_state == WarpState::Off;
    }

    pub fn display() {
        match unsafe { WARP_MENU.state } {
            WarpState::Details => {
                let mut detail_menu = SimpleMenu::<5, 25>::new(10, 10, 10, unsafe {
                    WARP_MENU.stage_state.get_stage_name(WARP_MENU.stage_cursor)
                });
                detail_menu.current_line = unsafe { WARP_MENU.detail_cursor.into() };
                let (room, layer, entrance) = unsafe {
                    (
                        WARP_MENU.get_room(),
                        WARP_MENU.get_layer(),
                        WARP_MENU.get_entrance(),
                    )
                };
                detail_menu.add_entry_args(format_args!("Room: {room}"));
                detail_menu.add_entry_args(format_args!("Layer: {layer}"));
                detail_menu.add_entry_args(format_args!("Entrance: {entrance}"));
                detail_menu.draw();
            },
            _ => {
                let mut main_menu = SimpleMenu::<{ NUM_ENTRIES_MAIN as usize + 2 }, 17>::new(
                    10,
                    10,
                    10,
                    "Select Stage",
                );
                main_menu.current_line = unsafe { WARP_MENU.main_cursor as u32 };
                main_menu.add_entry("Sky");
                main_menu.add_entry("Faron");
                main_menu.add_entry("Eldin");
                main_menu.add_entry("Lanayru");
                main_menu.add_entry("Sealed Grounds");
                main_menu.add_entry("Dungeon");
                main_menu.add_entry("Silent Realm");
                main_menu.draw();

                let stage_state = unsafe { WARP_MENU.stage_state };
                match stage_state {
                    WarpStage::None => {},
                    _ => {
                        let mut sub_menu =
                            SimpleMenu::<25, 17>::new(200, 5, 10, stage_state.get_name());
                        sub_menu.current_line = unsafe { WARP_MENU.stage_cursor as u32 };
                        for n in 0..stage_state.get_num_stages() as u8 {
                            sub_menu.add_entry(stage_state.get_stage_name(n));
                        }
                        sub_menu.draw();
                    },
                }
            },
        }
    }
}
