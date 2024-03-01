#[repr(i32)]
#[derive(Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum SpecialMinigameState {
    State0,
    BambooCutting,
    FunFunIsland,
    ThrillDigger,
    PumpkinCarry,
    InsectCaptureGame,
    PumpkinClayShooting,
    RollercoasterMinigame,
    TrialTimeAttack,
    BossRush,
    HouseCleaning,
    SpiralChargeTutorial,
    HarpPlaying,
    StateNone = -1,
}

extern "C" {
    static mut SPECIAL_MINIGAME_STATE: SpecialMinigameState;
}

impl SpecialMinigameState {
    pub fn get() -> Self {
        unsafe { SPECIAL_MINIGAME_STATE }
    }

    pub fn is_current(self) -> bool {
        Self::get() == self
    }
}
