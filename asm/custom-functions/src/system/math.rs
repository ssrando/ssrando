#[repr(C)]
#[derive(Default, Clone, Copy)]
pub struct Vec3f {
    pub x: f32,
    pub y: f32,
    pub z: f32,
}

#[repr(C)]
#[derive(Default, Clone, Copy)]
pub struct Vec3s {
    pub x: i16,
    pub y: i16,
    pub z: i16,
}

#[repr(C)]
#[derive(Default, Clone, Copy)]
pub struct Matrix34f {
    pub m: [[f32; 4]; 3],
}

#[repr(C)]
#[derive(Default, Clone, Copy)]
pub struct Matrix44f {
    pub m: [[f32; 4]; 4],
}

extern "C" {
    pub fn C_MTXOrtho(
        m: *mut Matrix44f,
        top: f32,
        bottom: f32,
        left: f32,
        right: f32,
        near: f32,
        far: f32,
    );
    pub fn PSMTXIdentity(mtx: *mut Matrix34f);
}
