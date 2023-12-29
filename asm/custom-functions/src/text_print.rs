use core::{
    ffi::{c_char, c_void},
    fmt::{Arguments, Write},
};

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
struct CharWriter {
    m_color_mapping:  [u32; 2],
    m_vertex_colors:  [u32; 4],
    m_text_color:     [u32; 2],
    m_text_gradation: u32,
    m_scale:          [f32; 2],
    m_cursor_pos:     [f32; 3],
    m_texture_filter: [u32; 2],
    __pad:            u16,
    m_alpha:          u8,
    m_is_width_fixed: u8,
    m_fixed_width:    f32,
    m_font_ptr:       u32,
}

#[repr(C)]
#[derive(Default)]
struct TextWriterBase {
    m_char_writer:   CharWriter,
    m_width_limit:   f32,
    m_char_space:    f32,
    m_line_space:    f32,
    m_tab_width:     i32,
    m_draw_flag:     u32,
    m_tag_processor: u32, // pointer to TagProcessor
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

    fn CharWriter__SetupGX(writer: *mut CharWriter);
    fn CharWriter__SetupGXWithColorMapping(min: *const u32, max: *const u32);
    fn CharWriter__UpdateVertexColor(writer: *mut CharWriter);
    fn __ct__TextWriterBase_WChar(writer: *mut TextWriterBase);
    fn __dt__TextWriterBase_WChar(writer: *mut TextWriterBase, _: i32);
    fn Printf_TextWriterBase_WChar(writer: *mut TextWriterBase, str: *const u16, ...);
    fn Print_TextWriterBase_WChar(writer: *mut TextWriterBase, str: *const u16, len: u32);

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

fn setFontColor(text_writer: *mut TextWriterBase, color1: u32, color2: u32) {
    unsafe {
        (*text_writer).m_char_writer.m_text_color[0] = color1;
        (*text_writer).m_char_writer.m_text_color[1] = color2;
        CharWriter__UpdateVertexColor(&mut (*text_writer).m_char_writer);
    }
}

// Draws the String on the screen (specfied by the top)
fn draw_text(pos_x: i32, pos_y: i32, string: &[u16]) {
    unsafe {
        // only draw if it's safe to do so
        if LINK_PTR.is_null() {
            return;
        }
        // Use the Default font (almost always loaded. Just not between loads)
        let font = FontMgr__GetFont(0);
        if font != 0 {
            // Create Matrix to draw on screen
            // [1.f,  0.f, 0.f, posx-300]
            // [0.f, -1.f, 0.f, 220-posy]
            // [0.f,  0.f, 1.f,      0.f]
            let mtx: *mut Matrix = &mut Matrix {
                mtx: [
                    [1f32, 0f32, 0f32, (pos_x - 300) as f32],
                    [0f32, -1f32, 0f32, (220 - pos_y) as f32],
                    [0f32, 0f32, 1f32, 0f32],
                ],
            };
            GXLoadPosMtxImm(mtx, 0);
            GXSetCurrentMtx(0);

            // Create a Default Textwriter to pass into the constructor
            let text_writer: *mut TextWriterBase = &mut TextWriterBase {
                ..Default::default()
            };
            __ct__TextWriterBase_WChar(text_writer);

            // Configure Color + Scale
            setFontColor(text_writer, 0x000000FF, 0x000000FF);
            (*text_writer).m_char_writer.m_font_ptr = font;
            (*text_writer).m_char_writer.m_scale = [0.5f32, 0.5f32];
            let minColor: u32 = 0x00000000;
            let maxColor: u32 = 0xFFFFFFFF;
            CharWriter__SetupGXWithColorMapping(&minColor, &maxColor);

            // Print the contents to the screen
            Print_TextWriterBase_WChar(text_writer, string.as_ptr(), string.len() as u32);

            // Manually Destroy the writer
            __dt__TextWriterBase_WChar(text_writer, -1);
        }
    }
}

pub struct WCharWriter {
    buf: arrayvec::ArrayVec<u16, 512>,
}

impl Write for WCharWriter {
    fn write_str(&mut self, s: &str) -> core::fmt::Result {
        for c in s.encode_utf16() {
            self.buf.try_push(c).map_err(|_| core::fmt::Error)?;
        }
        Ok(())
    }
}

impl WCharWriter {
    pub fn new() -> Self {
        Self {
            buf: Default::default(),
        }
    }

    pub fn draw_text(mut self, pos_x: i32, pos_y: i32) {
        // don't error if the buffer is full, just cut off the last char
        let _ = self.buf.try_push(0);
        // make sure the buffer is null terminated
        if let Some(last) = self.buf.last_mut() {
            *last = 0;
        }
        draw_text(pos_x, pos_y, &self.buf);
    }
}

pub fn write_to_screen(args: Arguments<'_>, pos_x: i32, pos_y: i32) {
    let mut writer = WCharWriter::new();
    let _ = writer.write_fmt(args);
    writer.draw_text(pos_x, pos_y);
}
