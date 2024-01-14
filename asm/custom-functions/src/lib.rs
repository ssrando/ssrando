#![no_std]
#![feature(split_array)]

mod game;
mod rando;
mod system;
mod utils;

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    loop {}
}
