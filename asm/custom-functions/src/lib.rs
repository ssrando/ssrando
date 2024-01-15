#![no_std]
#![feature(split_array)]
#![allow(dead_code)]

mod game;
mod rando;
mod system;
mod utils;

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    loop {}
}
