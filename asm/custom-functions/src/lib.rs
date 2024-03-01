#![no_std]
#![feature(split_array)]
#![allow(dead_code)]
#![deny(clippy::no_mangle_with_rust_abi)]
#![deny(improper_ctypes)]
#![deny(improper_ctypes_definitions)]

mod game;
mod rando;
mod system;
mod utils;

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    loop {}
}
