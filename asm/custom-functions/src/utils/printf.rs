use core::{
    ffi::{c_uint, c_void},
    fmt::{Arguments, Write},
};

extern "C" {
    static CONSOLE_DEVICE: c_void;
    fn _FileWrite(ptr: *const c_void, text: *const u8, length: c_uint);
}

struct DebugConsole;

impl Write for DebugConsole {
    fn write_str(&mut self, s: &str) -> core::fmt::Result {
        unsafe {
            _FileWrite(&CONSOLE_DEVICE as *const c_void, s.as_ptr(), s.len() as u32);
        }
        Ok(())
    }

    fn write_char(&mut self, c: char) -> core::fmt::Result {
        if let Some(c) = c.as_ascii() {
            self.write_str(c.as_str())?;
        }
        Ok(())
    }
}

pub fn debug_print(args: Arguments<'_>) {
    let _ = DebugConsole.write_fmt(args);
}
