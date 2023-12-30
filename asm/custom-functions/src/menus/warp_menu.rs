use crate::menus::simple_menu::SimpleMenu;
use crate::system::button::*;

const NUM_ENTRIES_MAIN: usize = 7;

#[derive(Copy, Clone, PartialEq, Eq)]
enum WarpState {
    Off,
    Main,
    Stage,
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

fn WarpStage_from_num(num: usize) -> WarpStage {
    match num {
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

fn get_num_stages(stage: WarpStage) -> usize {
    match stage {
        WarpStage::Sky => 23,
        WarpStage::Faron => 8,
        WarpStage::Eldin => 8,
        WarpStage::Lanayru => 16,
        WarpStage::SealedGrounds => 8,
        WarpStage::Dungeon => 20,
        WarpStage::SilentRealm => 4,
        WarpStage::None => 0,
    }
}

fn get_stage_name(stage: WarpStage, idx: u8) -> &'static str {
    match stage {
        WarpStage::Sky => {
            match idx {
                0 => "F000",
                1 => "F001r",
                2 => "F002r",
                3 => "F003r",
                4 => "F004r",
                5 => "F005r",
                6 => "F006r",
                7 => "F007r",
                8 => "F008r",
                9 => "F009r",
                10 => "F010r",
                11 => "F011r",
                12 => "F012r",
                13 => "F013r",
                14 => "F014r",
                15 => "F015r",
                16 => "F016r",
                17 => "F017r",
                18 => "F018r",
                19 => "F019r",
                20 => "F020",
                21 => "F021",
                22 => "F023",
                _ => "F000",
            }
        },
        WarpStage::Faron => {
            match idx {
                0 => "F100",
                1 => "F100_1",
                2 => "F101",
                3 => "F102",
                4 => "F102_1",
                5 => "F102_2",
                6 => "F103",
                7 => "F103_1",
                _ => "F100",
            }
        },
        WarpStage::Eldin => {
            match idx {
                0 => "F200",
                1 => "F201_1",
                2 => "F201_2",
                3 => "F201_3",
                4 => "F201_4",
                5 => "F210",
                6 => "F211",
                7 => "F221",
                _ => "F200",
            }
        },
        WarpStage::Lanayru => {
            match idx {
                0 => "F300",
                1 => "F300_1",
                2 => "F300_2",
                3 => "F300_3",
                4 => "F300_4",
                5 => "F300_5",
                6 => "F301",
                7 => "F301_1",
                8 => "F301_2",
                9 => "F301_3",
                10 => "F301_4",
                11 => "F301_5",
                12 => "F301_6",
                13 => "F301_7",
                14 => "F302",
                15 => "F303",
                _ => "F300",
            }
        },
        WarpStage::SealedGrounds => {
            match idx {
                0 => "F400",
                1 => "F401",
                2 => "F402",
                3 => "F403",
                4 => "F404",
                5 => "F405",
                6 => "F406",
                7 => "F407",
                _ => "F400",
            }
        },
        WarpStage::Dungeon => {
            match idx {
                0 => "D000",
                1 => "D100",
                2 => "B100",
                3 => "B100_1",
                4 => "D101",
                5 => "B101",
                6 => "B101_1",
                7 => "D200",
                8 => "B200",
                9 => "D201",
                10 => "D201_1",
                11 => "B201",
                12 => "B201_1",
                13 => "D300",
                14 => "D300_1",
                15 => "B300",
                16 => "D301",
                17 => "D301_1",
                18 => "B301",
                19 => "B400",
                _ => "D000",
            }
        },
        WarpStage::SilentRealm => {
            match idx {
                0 => "S000",
                1 => "S100",
                2 => "S200",
                3 => "S300",
                _ => "S000",
            }
        },
        WarpStage::None => "None",
    }
}

pub struct WarpMenu {
    state:       WarpState,
    stage_state: WarpStage,
    main_cursor: usize,
    sub_cursor:  usize,
}

#[link_section = "data"]
#[no_mangle]
static mut WARP_MENU: WarpMenu = WarpMenu {
    state:       WarpState::Off,
    stage_state: WarpStage::None,
    main_cursor: 0,
    sub_cursor:  0,
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

        let mut next_state = unsafe { WARP_MENU.state };

        match unsafe { WARP_MENU.state } {
            WarpState::Off => {},
            WarpState::Main => {
                if b_pressed {
                    next_state = WarpState::Off;
                } else if a_pressed {
                    next_state = WarpState::Stage;
                    unsafe {
                        WARP_MENU.stage_state = WarpStage_from_num(WARP_MENU.main_cursor);
                        if WARP_MENU.sub_cursor >= get_num_stages(WARP_MENU.stage_state) {
                            WARP_MENU.sub_cursor = 0;
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
                    // next_state = WarpState::Stage;
                    // unsafe {
                    //     WARP_MENU.stage_state = WARP_MENU.main_cursor as
                    // WarpStage;     if WARP_MENU.
                    // sub_cursor >= get_num_stages(WARP_MENU.stage_state) {
                    //         WARP_MENU.sub_cursor = 0;
                    //     }
                    // }
                } else if up_pressed {
                    unsafe {
                        let num_entries = get_num_stages(WARP_MENU.stage_state);
                        WARP_MENU.sub_cursor =
                            (WARP_MENU.sub_cursor + num_entries - 1) % num_entries;
                    }
                } else if down_pressed {
                    unsafe {
                        let num_entries = get_num_stages(WARP_MENU.stage_state);
                        WARP_MENU.sub_cursor = (WARP_MENU.sub_cursor + 1) % num_entries;
                    }
                }
            },
        }

        unsafe { WARP_MENU.state = next_state };
        return next_state == WarpState::Off;
    }

    pub fn display() {
        let mut main_menu =
            SimpleMenu::<{ NUM_ENTRIES_MAIN + 2 }, 17>::new(10, 10, 10, "Select Stage\n");
        main_menu.current_line = unsafe { WARP_MENU.main_cursor as u32 };
        main_menu.add_entry("Sky\n");
        main_menu.add_entry("Faron\n");
        main_menu.add_entry("Eldin\n");
        main_menu.add_entry("Lanayru\n");
        main_menu.add_entry("Sealed Grounds\n");
        main_menu.add_entry("Dungeon\n");
        main_menu.add_entry("Silent Realm\n");
        main_menu.draw();

        match unsafe { WARP_MENU.stage_state } {
            WarpStage::None => {},
            WarpStage::Sky => {
                let mut sub_menu = SimpleMenu::<25, 8>::new(200, 5, 10, "Sky\n");
                sub_menu.current_line = unsafe { WARP_MENU.sub_cursor as u32 };
                for n in 0..get_num_stages(WarpStage::Sky) as u8 {
                    sub_menu.add_entry(get_stage_name(WarpStage::Sky, n));
                }
                sub_menu.draw();
            },
            WarpStage::Faron => {
                let mut sub_menu = SimpleMenu::<25, 8>::new(200, 5, 10, "Faron\n");
                sub_menu.current_line = unsafe { WARP_MENU.sub_cursor as u32 };
                for n in 0..get_num_stages(WarpStage::Faron) as u8 {
                    sub_menu.add_entry(get_stage_name(WarpStage::Faron, n));
                }
                sub_menu.draw();
            },
            WarpStage::Eldin => {
                let mut sub_menu = SimpleMenu::<25, 10>::new(200, 5, 10, "Eldin\n");
                sub_menu.current_line = unsafe { WARP_MENU.sub_cursor as u32 };
                for n in 0..get_num_stages(WarpStage::Eldin) as u8 {
                    sub_menu.add_entry(get_stage_name(WarpStage::Eldin, n));
                }
                sub_menu.draw();
            },
            WarpStage::Lanayru => {
                let mut sub_menu = SimpleMenu::<25, 10>::new(200, 5, 10, "Lanayru\n");
                sub_menu.current_line = unsafe { WARP_MENU.sub_cursor as u32 };
                for n in 0..get_num_stages(WarpStage::Lanayru) as u8 {
                    sub_menu.add_entry(get_stage_name(WarpStage::Lanayru, n));
                }
                sub_menu.draw();
            },
            WarpStage::SealedGrounds => {
                let mut sub_menu = SimpleMenu::<25, 17>::new(200, 5, 10, "Sealed Grounds\n");
                sub_menu.current_line = unsafe { WARP_MENU.sub_cursor as u32 };
                for n in 0..get_num_stages(WarpStage::SealedGrounds) as u8 {
                    sub_menu.add_entry(get_stage_name(WarpStage::SealedGrounds, n));
                }
                sub_menu.draw();
            },
            WarpStage::Dungeon => {
                let mut sub_menu = SimpleMenu::<25, 12>::new(200, 5, 10, "Dungeons\n");
                sub_menu.current_line = unsafe { WARP_MENU.sub_cursor as u32 };
                for n in 0..get_num_stages(WarpStage::Dungeon) as u8 {
                    sub_menu.add_entry(get_stage_name(WarpStage::Dungeon, n));
                }
                sub_menu.draw();
            },
            WarpStage::SilentRealm => {
                let mut sub_menu = SimpleMenu::<25, 10>::new(200, 5, 10, "Trials\n");
                sub_menu.current_line = unsafe { WARP_MENU.sub_cursor as u32 };
                for n in 0..get_num_stages(WarpStage::SilentRealm) as u8 {
                    sub_menu.add_entry(get_stage_name(WarpStage::SilentRealm, n));
                }
                sub_menu.draw();
            },
        }
    }
}
