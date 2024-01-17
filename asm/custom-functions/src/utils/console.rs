use core::fmt::Write;

use crate::utils::char_writer::{CharWriter, TextWriterBase};

pub struct Console {
    pos:          [f32; 2],
    size:         [f32; 2],
    font_size:    f32,
    bg_color:     u32,
    font_color:   u32,
    dynamic_size: bool,
    buffer:       CharWriter<512>,
}

impl Write for Console {
    fn write_str(&mut self, s: &str) -> core::fmt::Result {
        self.buffer.write_str(s)
    }
}
impl Console {
    pub fn with_pos_and_size(posx: f32, posy: f32, width: f32, height: f32) -> Self {
        Self {
            pos:          [posx, posy],
            size:         [width, height],
            font_size:    0.5f32,
            bg_color:     0x0000003F,
            font_color:   0x000000FF,
            dynamic_size: false,
            buffer:       CharWriter::<512>::new(),
        }
    }

    pub fn with_pos(posx: f32, posy: f32) -> Self {
        Self {
            pos:          [posx, posy],
            size:         [0.0f32, 0.0f32],
            font_size:    0.5f32,
            bg_color:     0x0000003F,
            font_color:   0x000000FF,
            dynamic_size: true,
            buffer:       CharWriter::<512>::new(),
        }
    }

    pub fn set_dynamic_size(&mut self, val: bool) {
        self.dynamic_size = val;
    }

    pub fn set_font_color(&mut self, clr: u32) {
        self.font_color = clr;
    }

    pub fn set_font_size(&mut self, size: f32) {
        self.font_size = size;
    }

    pub fn set_bg_color(&mut self, clr: u32) {
        self.bg_color = clr;
    }

    pub fn draw(&mut self) {
        let mut writer = TextWriterBase::new();
        writer.set_font_color(self.font_color, self.font_color);
        writer.set_scale(self.font_size);
        writer.set_fixed_width();
        // Set size
        if self.dynamic_size {
            let rect = self.buffer.get_buff_rect(&mut writer);
            self.size = [4f32 + rect.right - rect.left, 4f32 + rect.bottom - rect.top];
        }
        crate::utils::graphics::draw_rect(
            self.pos[0],
            self.pos[1],
            self.size[0],
            self.size[1],
            0.0f32,
            self.bg_color,
        );
        writer.set_position(self.pos[0] + 2f32, self.pos[1] + 2f32);
        self.buffer.draw(&mut writer);
    }
}
