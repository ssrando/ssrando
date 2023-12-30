#![allow(unused)]
use core::{
    ffi::{c_char, c_void},
    fmt::{write, Arguments, Write},
};
use wchar::wchz;

use crate::LINK_PTR;

#[repr(C)]
struct ConsoleHead {
    text_buf:            u32, // u8*
    width:               u16,
    height:              u16,
    priority:            u16,
    attr:                u16,
    print_top:           u16,
    print_x_pos:         u16,
    ring_top:            u16,
    __pad_0:             u16,
    ring_top_line_count: i32,
    view_top_lin:        i32,
    view_pos_x:          u16,
    view_pos_y:          u16,
    view_lines:          u16,
    is_visible:          u8,
    __pad_1:             u8,
    writer:              u32, // TextWriteBase*
    next:                u32, // next consolehead pointer
}

#[repr(C)]
#[derive(Default)]
pub struct CharWriter {
    pub m_color_mapping:  [u32; 2],
    pub m_vertex_colors:  [u32; 4],
    pub m_text_color:     [u32; 2],
    pub m_text_gradation: u32,
    pub m_scale:          [f32; 2],
    pub m_cursor_pos:     [f32; 3],
    pub m_texture_filter: [u32; 2],
    pub __pad:            u16,
    pub m_alpha:          u8,
    pub m_is_width_fixed: u8,
    pub m_fixed_width:    f32,
    pub m_font_ptr:       u32,
}

#[repr(C)]
#[derive(Default)]
pub struct TextWriterBase {
    pub m_char_writer:   CharWriter,
    pub m_width_limit:   f32,
    pub m_char_space:    f32,
    pub m_line_space:    f32,
    pub m_tab_width:     i32,
    pub m_draw_flag:     u32,
    pub m_tag_processor: u32, // pointer to TagProcessor
}

#[repr(C)]
struct Matrix {
    mtx: [[f32; 4]; 3],
}

#[repr(C)]
struct MTX44 {
    mtx: [f32; 16],
}

extern "C" {
    fn FontMgr__GetFont(idx: u32) -> u32;

    fn C_MTXOrtho(
        mtx: *mut MTX44,
        float1: f32,
        float2: f32,
        float3: f32,
        float4: f32,
        float5: f32,
        float6: f32,
    );
    fn GXSetProjection(mtx: *mut MTX44, param2: u32);
    fn PSMTXIdentity(mtx: *mut Matrix);
    fn GXLoadPosMtxImm(mtx: *mut Matrix, param2: u32);
    fn GXSetCurrentMtx(param1: u32);
    fn GXSetAlphaCompare(compare1: u32, param2: u8, alphaop: u32, compare2: u32, param5: u8);
    fn CharWriter__GetWidth(writer: *mut CharWriter) -> f32;
    fn CharWriter__SetupGX(writer: *mut CharWriter);
    fn CharWriter__SetupGXWithColorMapping(min: *const u32, max: *const u32);
    fn CharWriter__UpdateVertexColor(writer: *mut CharWriter);
    fn __ct__TextWriterBase_WChar(writer: *mut TextWriterBase);
    fn __dt__TextWriterBase_WChar(writer: *mut TextWriterBase, _: i32);
    fn Printf_TextWriterBase_WChar(writer: *mut TextWriterBase, str: *const u16, ...);
    fn Print_TextWriterBase_WChar(writer: *const TextWriterBase, str: *const u16, len: u32);

    fn DirectPrint_DrawString(posh: u32, posv: u32, turnOver: u8, str: *const c_char, ...);
    fn DirectPrint_SetupFB(renderModeObj: *mut c_void) -> *mut c_void;
    fn Console_Create(
        console: *mut ConsoleHead,
        width: u16,
        height: u16,
        view_lines: u16,
        priority: u16,
        attr: u16,
    );
    fn Console_Printf(console: *mut ConsoleHead, str: *const c_char, ...);
    fn Console_DrawDirect(console: *mut ConsoleHead);
    fn Console_DoDrawConsole(console: *mut ConsoleHead, textwriter: *mut TextWriterBase);
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
        text_writer.m_char_writer.m_scale = [0.5f32, 0.5f32];
        text_writer.m_char_writer.m_text_gradation = 2;
        text_writer.set_font_color([0x000000FF, 0x000000FF]);
        text_writer.m_char_writer.m_color_mapping[0] = 0x00000000;
        text_writer.m_char_writer.m_color_mapping[1] = 0xFFFFFFFF;
        text_writer
    }

    // Sets the font [0, 1] = normal, [2, 3] = special, [4] = symbols
    // Returns if it is null
    pub fn set_font(&mut self, fontidx: u32) -> bool {
        self.m_char_writer.m_font_ptr = unsafe { FontMgr__GetFont(fontidx) };
        self.m_char_writer.m_font_ptr != 0
    }

    // Sets position to draw
    pub fn set_position(&mut self, posx: i32, posy: i32) {
        // Create Matrix to draw on screen
        // [1.f,  0.f, 0.f, posx-300]
        // [0.f, -1.f, 0.f, 220-posy]
        // [0.f,  0.f, 1.f,      0.f]
        let mtx: *mut Matrix = &mut Matrix {
            mtx: [
                [1f32, 0f32, 0f32, (posx - 300) as f32],
                [0f32, -1f32, 0f32, (220 - posy) as f32],
                [0f32, 0f32, 1f32, 0f32],
            ],
        };

        unsafe {
            GXLoadPosMtxImm(mtx, 0);
            GXSetCurrentMtx(0);
        }

        self.m_char_writer.m_cursor_pos = [0.0f32; 3];
    }

    // Sets the font colors
    // Set both to the same to make it a solid color
    // will vertically gradient it
    pub fn set_font_color(&mut self, colors: [u32; 2]) {
        self.m_char_writer.m_text_color[0] = colors[0];
        self.m_char_writer.m_text_color[1] = colors[1];
        unsafe {
            CharWriter__UpdateVertexColor(&mut self.m_char_writer as *mut _);
        }
    }

    // Prints text directly to screen
    pub fn print(&mut self, string: &[u16]) {
        if !self.set_font(0) {
            return;
        }
        unsafe {
            CharWriter__SetupGX(&mut self.m_char_writer);
            GXSetAlphaCompare(7, 0, 0, 7, 0);
        }
        let old_colors = self.m_char_writer.m_text_color;
        let old_cursor_pos = self.m_char_writer.m_cursor_pos;
        // White background for readability
        self.set_font_color([0xFFFFFFFF, 0xFFFFFFFF]);
        unsafe {
            Print_TextWriterBase_WChar(self as *const _, string.as_ptr(), string.len() as u32);
        }
        self.m_char_writer.m_cursor_pos = old_cursor_pos;
        self.set_font_color(old_colors);
        unsafe {
            Print_TextWriterBase_WChar(self as *const _, string.as_ptr(), string.len() as u32);
        }
    }

    // Prints symbols directly to screen
    pub fn print_symbol(&mut self, string: &[u16]) {
        if !self.set_font(4) {
            return;
        }
        unsafe {
            Print_TextWriterBase_WChar(self as *const _, string.as_ptr(), string.len() as u32);
        }
    }
}

// WCharWriter can have fixed size based on use case.
pub struct WCharWriter<const CAP: usize> {
    pub buf: arrayvec::ArrayVec<u16, CAP>,
}

impl<const CAP: usize> Write for WCharWriter<CAP> {
    fn write_str(&mut self, s: &str) -> core::fmt::Result {
        for c in s.encode_utf16() {
            self.buf.try_push(c).map_err(|_| core::fmt::Error)?;
        }
        Ok(())
    }
}

impl<const CAP: usize> WCharWriter<CAP> {
    pub fn new() -> Self {
        Self {
            buf: Default::default(),
        }
    }

    pub fn draw(&mut self, text_writer: &mut TextWriterBase) {
        let _ = self.buf.try_push(0);
        if let Some(last) = self.buf.last_mut() {
            *last = 0;
        }
        text_writer.print(&self.buf);
    }

    pub fn draw_text_at(&mut self, posx: i32, posy: i32) {
        let _ = self.buf.try_push(0);
        if let Some(last) = self.buf.last_mut() {
            *last = 0;
        }
        let mut text_writer = TextWriterBase::new();
        text_writer.set_position(posx, posy);
        text_writer.print(&self.buf);
    }
}

// A function made to write Directly to screen - no Questions Asked
pub fn write_to_screen(args: Arguments<'_>, posx: i32, posy: i32) {
    let mut writer = WCharWriter::<512>::new();
    let _ = writer.write_fmt(args);
    writer.draw_text_at(posx, posy);
}
