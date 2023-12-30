use crate::system::text_print::{TextWriterBase, WCharWriter};
use core::{
    ffi::{c_char, c_void},
    fmt::{write, Arguments, Write},
};
use wchar::wchz;

// Simple menu to Interact with. Will be revised heavily propbably
// Can control how many lines to display.
pub struct SimpleMenu<const NUM_LINES: usize, const LINE_SIZE: usize> {
    pub posx:         i32,
    pub posy:         i32,
    pub max_lines:    u32,
    pub current_line: u32,
    pub heading:      WCharWriter<LINE_SIZE>,
    pub line_buf:     arrayvec::ArrayVec<WCharWriter<LINE_SIZE>, NUM_LINES>,
}

impl<const NUM_LINES: usize, const LINE_SIZE: usize> SimpleMenu<NUM_LINES, LINE_SIZE> {
    pub fn new(posx: i32, posy: i32, max_lines: u32, name: &str) -> Self {
        let mut heading = WCharWriter::<LINE_SIZE>::new();
        let _ = heading.write_str(&name);
        Self {
            posx,
            posy,
            max_lines,
            current_line: 0,
            heading,
            line_buf: Default::default(),
        }
    }

    pub fn add_entry(&mut self, entry: &str) {
        if !self.line_buf.is_full() {
            let mut writer_entry = WCharWriter::<LINE_SIZE>::new();
            let _ = writer_entry.write_str(entry);
            if !entry.ends_with('\n') {
                let _ = writer_entry.write_str("\n");
            }
            self.line_buf.try_push(writer_entry).unwrap();
        }
    }
    pub fn add_entry_args(&mut self, args: Arguments<'_>) {
        if !self.line_buf.is_full() {
            let mut writer_entry = WCharWriter::<LINE_SIZE>::new();
            let _ = writer_entry.write_fmt(args);
            self.line_buf.try_push(writer_entry).unwrap();
        }
    }

    pub fn draw(&mut self) {
        let mut writer = TextWriterBase::new();
        // Black Font
        writer.set_font_color([0x000000FF, 0x000000FF]);
        writer.set_position(self.posx, self.posy);
        self.heading.draw(&mut writer);
        writer.print(wchz!(u16, "\n"));

        // TODO: Add logic to limit to a certain number of lines
        //       Control range so that the cursor is only at the top or bottom
        //          when it is at its first/last elements. Otherwise window will scroll
        for n in 0..self.line_buf.len() {
            if n == self.current_line as usize {
                writer.print_symbol(wchz!(u16, "6"));
            } else {
                writer.print(wchz!(u16, "    "));
            }
            let line = &mut self.line_buf.as_mut_slice()[n];
            line.draw(&mut writer);

            // Make sure that it is back to the leftmost side (formatting sucks)
            writer.m_char_writer.m_cursor_pos[0] = 0.0f32;
        }
    }
}
