#![allow(non_camel_case_types)]
#![allow(non_snake_case)]
#![allow(unused)]
use core::ffi::c_void;

use super::math::{Matrix34f, Matrix44f};
#[repr(C)]
pub enum GXPrimitive {
    GX_QUADS         = 0x80, // 0x80
    GX_TRIANGLES     = 0x90, // 0x90
    GX_TRIANGLESTRIP = 0x98, // 0x98
    GX_TRIANGLEFAN   = 0xA0, // 0xA0
    GX_LINES         = 0xA8, // 0xA8
    GX_LINESTRIP     = 0xB0, // 0xB0
    GX_POINTS        = 0xB8, // 0xB8
}

#[repr(C)]
pub enum GXCullMode {
    GX_CULL_NONE,  // 0x0
    GX_CULL_FRONT, // 0x1
    GX_CULL_BACK,  // 0x2
    GX_CULL_ALL,   // 0x3
}

#[repr(C)]
pub enum GXBool {
    GX_FALSE = 0,
    GX_TRUE  = 1,
}

#[repr(C)]
pub enum GXTexMapID {
    GX_TEXMAP0        = 0x000, // 0x000
    GX_TEXMAP1        = 0x001, // 0x001
    GX_TEXMAP2        = 0x002, // 0x002
    GX_TEXMAP3        = 0x003, // 0x003
    GX_TEXMAP4        = 0x004, // 0x004
    GX_TEXMAP5        = 0x005, // 0x005
    GX_TEXMAP6        = 0x006, // 0x006
    GX_TEXMAP7        = 0x007, // 0x007
    GX_MAX_TEXMAP     = 0x008, // 0x008
    GX_TEXMAP_NULL    = 0x0FF, // 0x0FF
    GX_TEXMAP_DISABLE = 0x100, // 0x100
}

#[repr(C)]
pub enum GXTevStageID {
    GX_TEVSTAGE0,    // 0x00
    GX_TEVSTAGE1,    // 0x01
    GX_TEVSTAGE2,    // 0x02
    GX_TEVSTAGE3,    // 0x03
    GX_TEVSTAGE4,    // 0x04
    GX_TEVSTAGE5,    // 0x05
    GX_TEVSTAGE6,    // 0x06
    GX_TEVSTAGE7,    // 0x07
    GX_TEVSTAGE8,    // 0x08
    GX_TEVSTAGE9,    // 0x09
    GX_TEVSTAGE10,   // 0x0A
    GX_TEVSTAGE11,   // 0x0B
    GX_TEVSTAGE12,   // 0x0C
    GX_TEVSTAGE13,   // 0x0D
    GX_TEVSTAGE14,   // 0x0E
    GX_TEVSTAGE15,   // 0x0F
    GX_MAX_TEVSTAGE, // 0x10
}

#[repr(C)]
pub enum GXTexCoordID {
    GX_TEXCOORD0,           // 0x00
    GX_TEXCOORD1,           // 0x01
    GX_TEXCOORD2,           // 0x02
    GX_TEXCOORD3,           // 0x03
    GX_TEXCOORD4,           // 0x04
    GX_TEXCOORD5,           // 0x05
    GX_TEXCOORD6,           // 0x06
    GX_TEXCOORD7,           // 0x07
    GX_MAXCOORD,            // 0x08
    GX_TEXCOORD_NULL = 255, // 0xFF
}

#[repr(C)]
pub enum GXChannelID {
    GX_COLOR0,           // 0x00
    GX_COLOR1,           // 0x01
    GX_ALPHA0,           // 0x02
    GX_ALPHA1,           // 0x03
    GX_COLOR0A0,         // 0x04
    GX_COLOR1A1,         // 0x05
    GX_COLOR_ZERO,       // 0x06
    GX_ALPHA_BUMP,       // 0x07
    GX_ALPHA_BUMPN,      // 0x08
    GX_COLOR_NULL = 255, // 0xFF
}

#[repr(C)]
pub enum GXColorSrc {
    GX_SRC_REG, // 0x0
    GX_SRC_VTX, // 0x1
}

#[repr(C)]
pub enum GXLightID {
    GX_LIGHT_NULL = 0,      // 0x000
    GX_LIGHT0     = 1 << 0, // 0x001
    GX_LIGHT1     = 1 << 1, // 0x002
    GX_LIGHT2     = 1 << 2, // 0x004
    GX_LIGHT3     = 1 << 3, // 0x008
    GX_LIGHT4     = 1 << 4, // 0x010
    GX_LIGHT5     = 1 << 5, // 0x020
    GX_LIGHT6     = 1 << 6, // 0x040
    GX_LIGHT7     = 1 << 7, // 0x080
    GX_MAX_LIGHT  = 1 << 8, // 0x100
}

#[repr(C)]
pub enum GXDiffuseFn {
    GX_DF_NONE,  // 0x0
    GX_DF_SIGN,  // 0x1
    GX_DF_CLAMP, // 0x2
}

#[repr(C)]
pub enum GXAttnFn {
    GX_AF_SPEC, // 0x0
    GX_AF_SPOT, // 0x1
    GX_AF_NONE, // 0x2
}

#[repr(C)]
pub enum GXDistAttnFn {
    GX_DA_OFF,    // 0x0
    GX_DA_GENTLE, // 0x1
    GX_DA_MEDIUM, // 0x2
    GX_DA_STEEP,  // 0x3
}

#[repr(C)]
pub enum GXSpotFn {
    GX_SP_OFF,   // 0x0
    GX_SP_FLAT,  // 0x1
    GX_SP_COS,   // 0x2
    GX_SP_COS2,  // 0x3
    GX_SP_SHARP, // 0x4
    GX_SP_RING1, // 0x5
    GX_SP_RING2, // 0x6
}

#[repr(C)]
pub enum GXTevMode {
    GX_MODULATE, // 0x0
    GX_DECAL,    // 0x1
    GX_BLEND,    // 0x2
    GX_REPLACE,  // 0x3
    GX_PASSCLR,  // 0x4
}

#[repr(C)]
pub enum GXBlendMode {
    GX_BM_NONE,       // 0x0
    GX_BM_BLEND,      // 0x1
    GX_BM_LOGIC,      // 0x2
    GX_BM_SUBTRACT,   // 0x3
    GX_MAX_BLENDMODE, // 0x4
}

#[repr(C)]
pub enum GXBlendFactor {
    GX_BL_ZERO,          // 0x0
    GX_BL_ONE,           // 0x1
    GX_BL_SRC_COLOR,     // 0x2
    GX_BL_INV_SRC_COLOR, // 0x3
    GX_BL_SRC_ALPHA,     // 0x4
    GX_BL_INV_SRC_ALPHA, // 0x5
    GX_BL_DST_ALPHA,     // 0x6
    GX_BL_INV_DST_ALPHA, // 0x7
}
impl GXBlendFactor {
    pub const GX_BL_DST_COLOR: Self = Self::GX_BL_SRC_COLOR; // 0x2
    pub const GX_BL_INV_DST_COLOR: Self = Self::GX_BL_INV_SRC_COLOR; // 0x3
}

#[repr(C)]
pub enum GXLogicOp {
    GX_LO_CLEAR,    // 0x0
    GX_LO_AND,      // 0x1
    GX_LO_REV_AND,  // 0x2
    GX_LO_COPY,     // 0x3
    GX_LO_INV_AND,  // 0x4
    GX_LO_NOOP,     // 0x5
    GX_LO_XOR,      // 0x6
    GX_LO_OR,       // 0x7
    GX_LO_NOR,      // 0x8
    GX_LO_EQUIV,    // 0x9
    GX_LO_INV,      // 0xA
    GX_LO_REV_OR,   // 0xB
    GX_LO_INV_COPY, // 0xC
    GX_LO_INV_OR,   // 0xD
    GX_LO_NAND,     // 0xE
    GX_LO_SET,      // 0xF
}

#[repr(C)]
pub enum GXVtxFmt {
    GX_VTXFMT0,    // 0x0
    GX_VTXFMT1,    // 0x1
    GX_VTXFMT2,    // 0x2
    GX_VTXFMT3,    // 0x3
    GX_VTXFMT4,    // 0x4
    GX_VTXFMT5,    // 0x5
    GX_VTXFMT6,    // 0x6
    GX_VTXFMT7,    // 0x7
    GX_MAX_VTXFMT, // 0x8
}

#[repr(C)]
pub enum GXAttr {
    GX_VA_PNMTXIDX,   // 0x00
    GX_VA_TEX0MTXIDX, // 0x01
    GX_VA_TEX1MTXIDX, // 0x02
    GX_VA_TEX2MTXIDX, // 0x03
    GX_VA_TEX3MTXIDX, // 0x04
    GX_VA_TEX4MTXIDX, // 0x05
    GX_VA_TEX5MTXIDX, // 0x06
    GX_VA_TEX6MTXIDX, // 0x07
    GX_VA_TEX7MTXIDX, // 0x08
    GX_VA_POS,        // 0x09
    GX_VA_NRM,        // 0x0A
    GX_VA_CLR0,       // 0x0B
    GX_VA_CLR1,       // 0x0C
    GX_VA_TEX0,       // 0x0D
    GX_VA_TEX1,       // 0x0E
    GX_VA_TEX2,       // 0x0F
    GX_VA_TEX3,       // 0x10
    GX_VA_TEX4,       // 0x11
    GX_VA_TEX5,       // 0x12
    GX_VA_TEX6,       // 0x13
    GX_VA_TEX7,       // 0x14
    GX_POS_MTX_ARRAY, // 0x15
    GX_NRM_MTX_ARRAY, // 0x16
    GX_TEX_MTX_ARRAY, // 0x17
    GX_LIGHT_ARRAY,   // 0x18
    GX_VA_NBT,        // 0x19
    GX_VA_MAX_ATTR,   // 0x1A
    GX_VA_NULL = 255, // 0xFF
}

#[repr(C)]
pub enum GXCompCnt {
    GX_COMP_CNT0 = 0,
    GX_COMP_CNT1 = 1,
    GX_COMP_CNT2 = 2,
}
impl GXCompCnt {
    pub const GX_POS_XY: Self = Self::GX_COMP_CNT0; // 0x0
    pub const GX_POS_XYZ: Self = Self::GX_COMP_CNT1; // 0x1
    pub const GX_NRM_XYZ: Self = Self::GX_COMP_CNT0; // 0x0
    pub const GX_NRM_NBT: Self = Self::GX_COMP_CNT1; // 0x1
    pub const GX_NRM_NBT3: Self = Self::GX_COMP_CNT2; // 0x2
    pub const GX_CLR_RGB: Self = Self::GX_COMP_CNT0; // 0x0
    pub const GX_CLR_RGBA: Self = Self::GX_COMP_CNT1; // 0x1
    pub const GX_TEX_S: Self = Self::GX_COMP_CNT0; // 0x0
    pub const GX_TEX_ST: Self = Self::GX_COMP_CNT1; // 0x1
}

#[repr(C)]
pub enum GXCompType {
    GX_COMP_TYPE0 = 0,
    GX_COMP_TYPE1 = 1,
    GX_COMP_TYPE2 = 2,
    GX_COMP_TYPE3 = 3,
    GX_COMP_TYPE4 = 4,
    GX_COMP_TYPE5 = 5,
}

impl GXCompType {
    pub const GX_U8: Self = Self::GX_COMP_TYPE0; // 0x0
    pub const GX_S8: Self = Self::GX_COMP_TYPE1; // 0x1
    pub const GX_U16: Self = Self::GX_COMP_TYPE2; // 0x2
    pub const GX_S16: Self = Self::GX_COMP_TYPE3; // 0x3
    pub const GX_F32: Self = Self::GX_COMP_TYPE4; // 0x4
    pub const GX_RGB565: Self = Self::GX_COMP_TYPE0; // 0x0
    pub const GX_RGB8: Self = Self::GX_COMP_TYPE1; // 0x1
    pub const GX_RGBX8: Self = Self::GX_COMP_TYPE2; // 0x2
    pub const GX_RGBA4: Self = Self::GX_COMP_TYPE3; // 0x3
    pub const GX_RGBA6: Self = Self::GX_COMP_TYPE4; // 0x4
    pub const GX_RGBA8: Self = Self::GX_COMP_TYPE5; // 0x5
}

#[repr(C)]
pub enum GXAttrType {
    GX_NONE,    // 0x0
    GX_DIRECT,  // 0x1
    GX_INDEX8,  // 0x2
    GX_INDEX16, // 0x3
}

#[repr(C)]
pub enum GXTevOp {
    GX_TEV_ADD           = 0,  // 0x0
    GX_TEV_SUB           = 1,  // 0x1
    GX_TEV_COMP_R8_GT    = 8,  // 0x8
    GX_TEV_COMP_R8_EQ    = 9,  // 0x9
    GX_TEV_COMP_GR16_GT  = 10, // 0xA
    GX_TEV_COMP_GR16_EQ  = 11, // 0xB
    GX_TEV_COMP_BGR24_GT = 12, // 0xC
    GX_TEV_COMP_BGR24_EQ = 13, // 0xD
    GX_TEV_COMP_RGB8_GT  = 14, // 0xE
    GX_TEV_COMP_RGB8_EQ  = 15, // 0xF
}

impl GXTevOp {
    pub const GX_TEV_COMP_A8_GT: Self = Self::GX_TEV_COMP_RGB8_GT; // 0xE
    pub const GX_TEV_COMP_A8_EQ: Self = Self::GX_TEV_COMP_RGB8_EQ; // 0xF
}

#[repr(C)]
pub enum GXTevBias {
    GX_TB_ZERO,     // 0x0
    GX_TB_ADDHALF,  // 0x1
    GX_TB_SUBHALF,  // 0x2
    GX_MAX_TEVBIAS, // 0x3
}

#[repr(C)]
pub enum GXTevColorArg {
    GX_CC_CPREV, // 0x0
    GX_CC_APREV, // 0x1
    GX_CC_C0,    // 0x2
    GX_CC_A0,    // 0x3
    GX_CC_C1,    // 0x4
    GX_CC_A1,    // 0x5
    GX_CC_C2,    // 0x6
    GX_CC_A2,    // 0x7
    GX_CC_TEXC,  // 0x8
    GX_CC_TEXA,  // 0x9
    GX_CC_RASC,  // 0xA
    GX_CC_RASA,  // 0xB
    GX_CC_ONE,   // 0xC
    GX_CC_HALF,  // 0xD
    GX_CC_KONST, // 0xE
    GX_CC_ZERO,  // 0xF
}

#[repr(C)]
pub enum GXTevColorChan {
    GX_CH_RED,   // 0x0
    GX_CH_GREEN, // 0x1
    GX_CH_BLUE,  // 0x2
    GX_CH_ALPHA, // 0x3
}

#[repr(C)]
pub enum GXTevScale {
    GX_CS_SCALE_1,   // 0x0
    GX_CS_SCALE_2,   // 0x1
    GX_CS_SCALE_4,   // 0x2
    GX_CS_DIVIDE_2,  // 0x3
    GX_MAX_TEVSCALE, // 0x4
}

#[repr(C)]
pub enum GXTevRegID {
    GX_TEVPREV,    // 0x0
    GX_TEVREG0,    // 0x1
    GX_TEVREG1,    // 0x2
    GX_TEVREG2,    // 0x3
    GX_MAX_TEVREG, // 0x4
}

#[repr(C)]
pub enum GXTevAlphaArg {
    GX_CA_APREV, // 0x0
    GX_CA_A0,    // 0x1
    GX_CA_A1,    // 0x2
    GX_CA_A2,    // 0x3
    GX_CA_TEXA,  // 0x4
    GX_CA_RASA,  // 0x5
    GX_CA_KONST, // 0x6
    GX_CA_ZERO,  // 0x7
}

#[repr(C)]
pub enum GXTexFmt {
    GX_TF_I4     = 0x0,  // 0x0
    GX_TF_I8     = 0x1,  // 0x1
    GX_TF_IA4    = 0x2,  // 0x2
    GX_TF_IA8    = 0x3,  // 0x3
    GX_TF_RGB565 = 0x4,  // 0x4
    GX_TF_TGB5A3 = 0x5,  // 0x5
    GX_TF_RGBA8  = 0x6,  // 0x6
    GX_TF_CI4    = 0x7,  // 0x7
    GX_TF_CI8    = 0x8,  // 0x8
    GX_TF_CI14   = 0x9,  // 0x9
    GX_TF_CMPR   = 0xE,  // 0xE
    _GX_TF_ZTF   = 0x10, // 0x10
    GX_TF_Z8     = 0x11, // 0x11
    GX_TF_Z16    = 0x13, // 0x13
    GX_TF_Z24X8  = 0x16, // 0x16
    _GX_TF_CTF   = 0x20, // 0x20
    _GX_CTF_R8   = 0x28, // 0x28
    GX_CTF_Z4    = 0x30, // 0x30
    GX_CTF_Z8M   = 0x39, // 0x39
    GX_CTF_Z8L   = 0x3A, // 0x3A
    GX_CTF_Z16L  = 0x3C, // 0x3C
}

#[repr(C)]
pub enum GXGamma {
    GX_GM_1_0, // 0x0
    GX_GM_1_7, // 0x0
    GX_GM_2_2, // 0x0
}

#[repr(C)]
pub enum GXTlutFmt {
    GX_TL_IA8,    // 0x0
    GX_TL_RGB565, // 0x1
    GX_TL_RGB5A3, // 0x2
}

#[repr(C)]
pub enum GXTlut {
    GX_TLUT0,    // 0x00
    GX_TLUT1,    // 0x01
    GX_TLUT2,    // 0x02
    GX_TLUT3,    // 0x03
    GX_TLUT4,    // 0x04
    GX_TLUT5,    // 0x05
    GX_TLUT6,    // 0x06
    GX_TLUT7,    // 0x07
    GX_TLUT8,    // 0x08
    GX_TLUT9,    // 0x09
    GX_TLUT10,   // 0x0A
    GX_TLUT11,   // 0x0B
    GX_TLUT12,   // 0x0C
    GX_TLUT13,   // 0x0D
    GX_TLUT14,   // 0x0E
    GX_TLUT15,   // 0x0F
    GX_BIGTLUT0, // 0x10
    GX_BIGTLUT1, // 0x11
    GX_BIGTLUT2, // 0x12
    GX_BIGTLUT3, // 0x13
}

#[repr(C)]
pub enum GXTexWrapMode {
    GX_CLAMP,            // 0x0
    GX_REPEAT,           // 0x1
    GX_MIRROR,           // 0x2
    GX_MAX_TEXWRAP_MODE, // 0x3
}

#[repr(C)]
pub enum GXTexFilter {
    GX_NEAR,          // 0x0
    GX_LINEAR,        // 0x1
    GX_NEAR_MIP_NEAR, // 0x2
    GX_LIN_MIP_NEAR,  // 0x3
    GX_NEAR_MIP_LIN,  // 0x4
    GX_LIN_MIP_LIN,   // 0x5
}

#[repr(C)]
pub enum GXAnisotropy {
    GX_ANISO_1,        // 0x0
    GX_ANISO_2,        // 0x1
    GX_ANISO_4,        // 0x2
    GX_MAX_ANISOTROPY, // 0x3
}

#[repr(C)]
pub enum GXTexMtxType {
    GX_MTX3x4, // 0x0
    GX_MTX2x4, // 0x1
}

#[repr(C)]
pub enum GXCompare {
    GX_NEVER,   // 0x0
    GX_LESS,    // 0x1
    GX_EQUAL,   // 0x2
    GX_LEQUAL,  // 0x3
    GX_GREATER, // 0x4
    GX_NEQUAL,  // 0x5
    GX_GEQUAL,  // 0x6
    GX_ALWAYS,  // 0x7
}

#[repr(C)]
pub enum GXAlphaOp {
    GX_AOP_AND,     // 0x0
    GX_AOP_OR,      // 0x1
    GX_AOP_XOR,     // 0x2
    GX_AOP_XNOR,    // 0x3
    GX_MAX_ALPHAOP, // 0x4
}

#[repr(C)]
pub enum GXClipMode {
    GX_CLIP_ENABLE,  // 0x0
    GX_CLIP_DISABLE, // 0x1
}

#[derive(Clone, Copy)]
pub struct Color {
    pub r: u8,
    pub g: u8,
    pub b: u8,
    pub a: u8,
}
impl Color {
    pub fn from_u32(clr: u32) -> Self {
        Self {
            r: (clr >> 24) as _,
            g: (clr >> 16) as _,
            b: (clr >> 08) as _,
            a: (clr >> 00) as _,
        }
    }
    pub fn as_u32(&self) -> u32 {
        return ((self.r as u32) << 24)
            | ((self.g as u32) << 16)
            | ((self.b as u32) << 8)
            | ((self.a as u32) << 0);
    }
}

extern "C" {
    pub fn GXSetProjection(mtx: *const Matrix44f, _: u32);
    pub fn GXSetViewport(
        x_orig: f32,
        y_orig: f32,
        width: f32,
        height: f32,
        near_z: f32,
        far_z: f32,
    );
    pub fn GXSetScissor(left: u32, top: u32, width: u32, height: u32);
    pub fn GXBegin(_: GXPrimitive, _: GXVtxFmt, _: u16);
    pub fn GXSetVtxAttrFmt(_: GXVtxFmt, _: GXAttr, _: GXCompCnt, _: GXCompType, _: u8);
    pub fn GXLoadPosMtxImm(mtx: *mut Matrix34f, id: u32);
    pub fn GXSetCurrentMtx(id: u32);
    pub fn GXInvalidateVtxCache();
    pub fn GXSetAlphaCompare(
        compare1: GXCompare,
        param2: u8,
        alphaop: GXAlphaOp,
        compare2: GXCompare,
        param5: u8,
    );
    pub fn GXSetNumIndStages(num: u8);
    pub fn GXSetVtxDesc(_: GXAttr, _: GXAttrType);
    pub fn GXClearVtxDesc();
    pub fn GXSetTevOp(_: GXTevStageID, _: GXTevMode);
    pub fn GXSetTevOrder(_: GXTevStageID, _: GXTexCoordID, _: GXTexMapID, _: GXChannelID);
    pub fn GXSetNumTevStages(num: u8);
    pub fn GXSetNumChans(num: u8);
    pub fn GXSetClipMode(_: GXClipMode);
    pub fn GXSetNumTexGens(num: u32);
    pub fn GXSetBlendMode(
        mode: GXBlendMode,
        src_factor: GXBlendFactor,
        dst_factor: GXBlendFactor,
        op: GXLogicOp,
    );
    pub fn GXSetColorUpdate(en_update: GXBool);
    pub fn GXSetAlphaUpdate(en_update: GXBool);
    pub fn GXSetZMode(en_comp: GXBool, comp: GXCompare, en_update: GXBool);
    pub fn GXSetCullMode(_: GXCullMode);
    pub fn GXSetChanCtrl(
        chan: GXChannelID,
        enable: GXBool,
        amb_src: GXColorSrc,
        mat_src: GXColorSrc,
        light_mask: u32,
        diff_fn: GXDiffuseFn,
        attn_fn: GXAttnFn,
    );
    pub fn __GXSetIndirectMask(mask: u32);
    pub fn GXSetChanMatColor(_: GXChannelID, clr: *const u32);
    pub static mut GX_FIFO: *mut c_void;

}

pub fn GXWriteFifo<T>(val: T) {
    return unsafe { core::ptr::write_volatile((0xCC008000 as *mut T), val) };
}

pub fn GXPosition3f32(x: f32, y: f32, z: f32) {
    GXWriteFifo::<f32>(x);
    GXWriteFifo::<f32>(y);
    GXWriteFifo::<f32>(z);
}
pub fn GXColor1u32(clr: u32) {
    GXWriteFifo::<u32>(clr);
}
