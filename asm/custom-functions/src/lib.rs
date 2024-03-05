#![no_std]
#![feature(split_array)]
#![feature(allocator_api)]
#![feature(ascii_char)]
#![feature(format_args_nl)]
#![allow(dead_code)]
#![deny(clippy::no_mangle_with_rust_abi)]
#![deny(improper_ctypes)]
#![deny(improper_ctypes_definitions)]

use system::heap::DefaultGlobalAllocator;

extern crate alloc;

#[global_allocator]
static DUMMY_ALLOC: DefaultGlobalAllocator = DefaultGlobalAllocator;

mod game;
mod rando;
mod system;
mod utils;

#[macro_export]
macro_rules! print {
    ($($arg:tt)*) => {{
        $crate::utils::printf::debug_print(format_args!($($arg)*));
    }};
}

#[macro_export]
macro_rules! println {
    () => {
        $crate::print!("\n")
    };
    ($($arg:tt)*) => {{
        $crate::utils::printf::debug_print(format_args_nl!($($arg)*));
    }};
}

#[panic_handler]
fn panic(_: &core::panic::PanicInfo) -> ! {
    loop {}
}
