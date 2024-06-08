#![no_std]
#![feature(split_array)]
#![feature(allocator_api)]
#![feature(ascii_char)]
#![feature(format_args_nl)]
#![feature(slice_ptr_get)]
#![feature(slice_partition_dedup)]
#![allow(dead_code)]
#![deny(clippy::no_mangle_with_rust_abi)]
#![deny(improper_ctypes)]
#![deny(improper_ctypes_definitions)]

extern crate alloc;

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
fn panic(_info: &core::panic::PanicInfo) -> ! {
    // println!("{}", info);
    loop {}
}
