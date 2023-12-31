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
        writer.m_char_writer.m_cursor_pos[0] = 0.0f32;

        // TODO: Add logic to limit to a certain number of lines
        //       Control range so that the cursor is only at the top or bottom
        //          when it is at its first/last elements. Otherwise window will scroll

        //  get lower and upper range
        let range = self.max_lines as i32;
        let len = self.line_buf.len() as i32;
        let curr_line = self.current_line as i32;

        let (mut lower, mut upper) = (0, len);
        if len > range {
            let (try_low, try_high) = (curr_line - range / 2, curr_line + range / 2);
            if len > try_high && 0 < try_low {
                (lower, upper) = (try_low, try_high);
            } else {
                if len - curr_line > range / 2 {
                    (lower, upper) = (0, range);
                } else {
                    (lower, upper) = (len - range, len);
                }
            }
        }

        if lower > 0 {
            writer.print_symbol(wchz!(u16, "\n3")); // up arrow
        } else {
            writer.print(wchz!(u16, "\n"));
        }
        for n in lower..upper {
            writer.m_char_writer.m_cursor_pos[0] = 0.0f32;
            if n as usize == self.current_line as usize {
                writer.print_symbol(wchz!(u16, "\n6")); // right arrow
            } else {
                writer.print(wchz!(u16, "\n    "));
            }
            let line = &mut self.line_buf.as_mut_slice()[n as usize];
            line.draw(&mut writer);
        }
        writer.m_char_writer.m_cursor_pos[0] = 0.0f32;
        if upper < len {
            writer.print_symbol(wchz!(u16, "\n4")); // down arrow
        }
    }
}
