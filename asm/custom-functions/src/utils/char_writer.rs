use core::fmt::{Arguments, Write};

use crate::system::{
    gx::*,
    math::{C_MTXOrtho, Matrix34f, Matrix44f},
};

// Background Color Saved
#[link_section = "data"]
static mut BACKGROUND_COLOR: [u32; 2] = [0x000000FF; 2];

#[repr(C)]
#[derive(Default)]
struct GameCharWriter {
    color_mapping:  [u32; 2],
    vertex_colors:  [u32; 4],
    text_color:     [u32; 2],
    text_gradation: u32,
    scale:          [f32; 2],
    cursor_pos:     [f32; 3],
    texture_filter: [u32; 2],
    pad:            u16,
    alpha:          u8,
    is_width_fixed: u8,
    fixed_width:    f32,
    font_ptr:       u32,
}

#[repr(C)]
#[derive(Default)]
pub struct TextWriterBase {
    char_writer:   GameCharWriter,
    width_limit:   f32,
    char_space:    f32,
    line_space:    f32,
    tab_width:     i32,
    draw_flag:     u32,
    tag_processor: u32, // pointer to TagProcessor
}

#[repr(C)]
pub struct Rect {
    pub left:   f32,
    pub top:    f32,
    pub right:  f32,
    pub bottom: f32,
}

extern "C" {
    fn FontMgr__GetFont(idx: u32) -> u32;

    fn CharWriter__GetFontWidth(writer: *const GameCharWriter, char: u16) -> f32;
    fn CharWriter__GetFontHeight(writer: *const GameCharWriter, char: u16) -> f32;
    fn CharWriter__SetupGX(writer: *mut GameCharWriter);
    fn CharWriter__SetupGXWithColorMapping(min: *const u32, max: *const u32);
    fn CharWriter__UpdateVertexColor(writer: *mut GameCharWriter);
    fn __ct__TextWriterBase_WChar(writer: *mut TextWriterBase);
    fn __dt__TextWriterBase_WChar(writer: *mut TextWriterBase, _: i32);
    fn Printf_TextWriterBase_WChar(writer: *mut TextWriterBase, str: *const u16, ...);
    fn Print_TextWriterBase_WChar(writer: *const TextWriterBase, str: *const u16, len: u32);
    fn PrintMutable_TextWriterBase_WChar(writer: *const TextWriterBase, str: *const u16, len: u32);
    fn CalcStringRect_TextWriterBase_WChar(
        writer: *const TextWriterBase,
        rect: *mut Rect,
        str: *const u16,
        len: u32,
    );
}

// Destroys the TextWriter Properly
impl Drop for TextWriterBase {
    fn drop(&mut self) {
        unsafe {
            __dt__TextWriterBase_WChar(self, -1);
        }
    }
}

impl TextWriterBase {
    pub fn new() -> Self {
        let mut text_writer = TextWriterBase::default();
        unsafe { __ct__TextWriterBase_WChar(&mut text_writer) };
        // Configure Color + Scale
        text_writer.char_writer.scale = [0.5f32, 0.5f32];
        text_writer.char_writer.text_gradation = 2;
        text_writer.set_font_color(0x000000FF, 0x000000FF);
        text_writer.char_writer.color_mapping[0] = 0x00000000;
        text_writer.char_writer.color_mapping[1] = 0xFFFFFFFF;
        text_writer
    }

    // Sets the font [0, 1] = normal, [2, 3] = special, [4] = symbols
    // Returns if it is null
    pub fn set_font(&mut self, fontidx: u32) -> bool {
        self.char_writer.font_ptr = unsafe { FontMgr__GetFont(fontidx) };
        self.char_writer.font_ptr != 0
    }

    pub fn set_fixed_width(&mut self) {
        if self.set_font(0) {
            self.char_writer.fixed_width =
                unsafe { CharWriter__GetFontWidth(&self.char_writer, b'-' as u16) };
            self.char_writer.is_width_fixed = 1;
        }
    }

    pub fn get_font_width(&mut self) -> f32 {
        if self.set_font(0) {
            return unsafe { CharWriter__GetFontWidth(&self.char_writer, b'-' as u16) };
        }
        return 0.0f32;
    }
    pub fn get_font_height(&mut self) -> f32 {
        if self.set_font(0) {
            return unsafe { CharWriter__GetFontHeight(&self.char_writer, b'!' as u16) };
        }
        return 0.0f32;
    }

    pub fn set_scale(&mut self, scale: f32) {
        self.char_writer.scale = [scale; 2];
    }

    // Sets position to draw
    pub fn set_position(&mut self, posx: f32, posy: f32) {
        // Create Matrix to draw on screen
        // [1.f, 0.f, 0.f, posx]
        // [0.f, 1.f, 0.f, posy]
        // [0.f, 0.f, 1.f,  0.f]
        let mtx: *mut Matrix34f = &mut Matrix34f {
            m: [
                [1f32, 0f32, 0f32, posx],
                [0f32, 1f32, 0f32, posy],
                [0f32, 0f32, 1f32, 0f32],
            ],
        };

        let m = &mut Matrix44f::default();
        unsafe {
            C_MTXOrtho(m, 0f32, 480f32, 0f32, 640f32, 0f32, 10f32);
            GXSetProjection(m, 1);
            GXSetViewport(0f32, 0f32, 640f32, 480f32, 0f32, 1f32);
            GXLoadPosMtxImm(mtx, 0);
            GXSetCurrentMtx(0);
        }

        self.char_writer.cursor_pos = [0.0f32; 3];
    }

    // Sets the cursor Position
    pub fn set_cursor(&mut self, pos: [f32; 3]) {
        self.char_writer.cursor_pos = pos;
    }

    pub fn get_cursor(&self) -> [f32; 3] {
        self.char_writer.cursor_pos
    }

    // Sets the font colors
    // Set both to the same to make it a solid color
    // will vertically gradient it
    pub fn set_font_color(&mut self, color1: u32, color2: u32) {
        self.char_writer.text_color[0] = color1;
        self.char_writer.text_color[1] = color2;
        unsafe {
            CharWriter__UpdateVertexColor(&mut self.char_writer as _);
        }
    }

    // Prints text directly to screen
    pub fn print(&mut self, string: &[u16]) {
        // Set to default font
        if !self.set_font(0) {
            return;
        }

        // Setup GX Stuffs
        unsafe {
            CharWriter__SetupGX(&mut self.char_writer);
            GXSetAlphaCompare(
                GXCompare::GX_ALWAYS,
                0,
                GXAlphaOp::GX_AOP_AND,
                GXCompare::GX_ALWAYS,
                0,
            );
        }

        // Save Colors and Background
        let old_colors = self.char_writer.text_color;
        let old_cursor_pos = self.char_writer.cursor_pos;

        // Black background for readability
        unsafe { self.set_font_color(BACKGROUND_COLOR[0], BACKGROUND_COLOR[1]) };

        // Print The Background
        unsafe { Print_TextWriterBase_WChar(self as *const _, string.as_ptr(), string.len() as _) };

        // Restore old position and Color
        self.char_writer.cursor_pos = old_cursor_pos;
        self.set_font_color(old_colors[0], old_colors[1]);

        // Print the foreground
        unsafe { Print_TextWriterBase_WChar(self as *const _, string.as_ptr(), string.len() as _) };
    }

    // Prints symbols directly to screen
    pub fn print_symbol(&mut self, string: &[u16]) {
        if !self.set_font(4) {
            return;
        }
        let old_colors = self.char_writer.text_color;
        self.set_font_color(0xFFFFFFFF, 0xFFFFFFFF);
        self.char_writer.text_gradation = 0;
        unsafe {
            CharWriter__SetupGX(&mut self.char_writer);
            GXSetAlphaCompare(
                GXCompare::GX_ALWAYS,
                0,
                GXAlphaOp::GX_AOP_AND,
                GXCompare::GX_ALWAYS,
                0,
            );
        }
        unsafe {
            Print_TextWriterBase_WChar(self as *const _, string.as_ptr(), string.len() as u32);
        }
        self.set_font_color(old_colors[0], old_colors[1]);
        self.char_writer.text_gradation = 2;
    }
}

pub struct CharWriter<const BUFFER_SIZE: usize> {
    font_color:  Color,
    bg_color:    Color,
    fixed_width: bool,
    pub buffer:  arrayvec::ArrayVec<u16, BUFFER_SIZE>,
}

impl<const BUFFER_SIZE: usize> Write for CharWriter<BUFFER_SIZE> {
    fn write_str(&mut self, s: &str) -> core::fmt::Result {
        for c in s.encode_utf16() {
            self.buffer.try_push(c).map_err(|_| core::fmt::Error)?;
        }
        Ok(())
    }
}

impl<const BUFFER_SIZE: usize> CharWriter<BUFFER_SIZE> {
    pub fn new() -> Self {
        Self {
            font_color:  Color::from_u32(0xFFFFFFFF),
            bg_color:    Color::from_u32(0x000000FF),
            fixed_width: false,
            buffer:      Default::default(),
        }
    }

    pub fn set_bg_color(&mut self, clr: u32) {
        self.bg_color = Color::from_u32(clr);
    }
    pub fn set_font_color(&mut self, clr: u32) {
        self.font_color = Color::from_u32(clr);
    }
    pub fn set_fixed_width(&mut self, is_fixed: bool) {
        self.fixed_width = is_fixed;
    }

    pub fn get_buff_rect(&mut self, writer: *mut TextWriterBase) -> Rect {
        let mut rect = Rect {
            left:   0f32,
            right:  0f32,
            top:    0f32,
            bottom: 0f32,
        };
        if !writer.is_null() {
            // ensure line ending
            if *(self.buffer.last().unwrap()) != 0x0000 {
                let _ = self.buffer.try_push(0);
                if let Some(last) = self.buffer.last_mut() {
                    *last = 0;
                }
            }
            unsafe {
                CalcStringRect_TextWriterBase_WChar(
                    writer,
                    &mut rect,
                    self.buffer.as_mut_ptr(),
                    self.buffer.len() as _,
                );
            }
        }
        rect
    }

    pub fn draw(&mut self, writer: *mut TextWriterBase) {
        if self.buffer.is_empty() {
            return;
        }
        // Set background color as it doesnt originally belong in the writer
        unsafe { BACKGROUND_COLOR = [self.bg_color.as_u32(); 2] };

        // ensure line ending
        if self.buffer.last().is_some_and(|last| *last != 0) {
            let _ = self.buffer.try_push(0);
            if let Some(last) = self.buffer.last_mut() {
                *last = 0;
            }
        }

        if !writer.is_null() {
            unsafe {
                (*writer).set_font_color(self.font_color.as_u32(), self.font_color.as_u32());
                if self.fixed_width {
                    (*writer).set_fixed_width();
                }
                (*writer).print(&self.buffer);
            }
        } else {
            let mut writer = TextWriterBase::new();
            writer.set_font_color(self.font_color.as_u32(), self.font_color.as_u32());
            writer.set_position(0f32, 0f32);
            if self.fixed_width {
                writer.set_fixed_width();
            }
            writer.print(&self.buffer);
        }
    }
}

pub fn write_to_screen(args: Arguments<'_>, posx: f32, posy: f32) {
    let mut writer = CharWriter::<512>::new();
    let _ = writer.write_fmt(args);

    let mut text_writer = TextWriterBase::new();
    text_writer.set_position(posx, posy);

    writer.draw(&mut text_writer);
}
