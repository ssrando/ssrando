use crate::system::{
    gx::*,
    math::{C_MTXOrtho, Matrix34f, Matrix44f},
    ppc::float_to_unsigned,
};

pub fn draw_rect(posx: f32, posy: f32, width: f32, height: f32, z: f32, clr: u32) {
    let pos_mtx = &mut Matrix34f {
        m: [
            [1f32, 0f32, 0f32, 0f32],
            [0f32, 1f32, 0f32, 0f32],
            [0f32, 0f32, 1f32, 0f32],
        ],
    };

    let ortho_mtx = &mut Matrix44f::default();
    unsafe {
        C_MTXOrtho(
            ortho_mtx,
            posy,
            posy + height,
            posx,
            posx + width,
            0f32,
            1f32,
        );
        GXSetProjection(ortho_mtx, 1);
        GXSetViewport(posx, posy, width, height, 0f32, 1f32);
        GXSetScissor(
            float_to_unsigned(posx),
            float_to_unsigned(posy),
            float_to_unsigned(width),
            float_to_unsigned(height),
        );
        GXLoadPosMtxImm(pos_mtx, 0);
        GXSetCurrentMtx(0);
        GXClearVtxDesc();
        GXInvalidateVtxCache();
        GXSetVtxDesc(GXAttr::GX_VA_POS, GXAttrType::GX_DIRECT);
        GXSetVtxAttrFmt(
            GXVtxFmt::GX_VTXFMT0,
            GXAttr::GX_VA_POS,
            GXCompCnt::GX_POS_XYZ,
            GXCompType::GX_F32,
            0,
        );
        GXSetNumChans(1);
        GXSetChanMatColor(GXChannelID::GX_COLOR0A0, &clr);
        GXSetChanCtrl(
            GXChannelID::GX_COLOR0A0,
            GXBool::GX_FALSE,
            GXColorSrc::GX_SRC_REG,
            GXColorSrc::GX_SRC_REG,
            0,
            GXDiffuseFn::GX_DF_NONE,
            GXAttnFn::GX_AF_NONE,
        );
        GXSetNumTexGens(0);
        GXSetNumIndStages(0);
        __GXSetIndirectMask(0);
        GXSetNumTevStages(1);
        GXSetTevOp(GXTevStageID::GX_TEVSTAGE0, GXTevMode::GX_PASSCLR);
        GXSetTevOrder(
            GXTevStageID::GX_TEVSTAGE0,
            GXTexCoordID::GX_TEXCOORD_NULL,
            GXTexMapID::GX_TEXMAP_NULL,
            GXChannelID::GX_COLOR0A0,
        );
        if clr & 0xFF == 0xFF {
            GXSetBlendMode(
                GXBlendMode::GX_BM_NONE,
                GXBlendFactor::GX_BL_ONE,
                GXBlendFactor::GX_BL_ZERO,
                GXLogicOp::GX_LO_SET,
            );
        } else {
            GXSetBlendMode(
                GXBlendMode::GX_BM_BLEND,
                GXBlendFactor::GX_BL_SRC_ALPHA,
                GXBlendFactor::GX_BL_INV_SRC_ALPHA,
                GXLogicOp::GX_LO_SET,
            );
        }
        GXSetColorUpdate(GXBool::GX_TRUE);
        GXSetAlphaUpdate(GXBool::GX_TRUE);
        GXSetZMode(GXBool::GX_FALSE, GXCompare::GX_NEVER, GXBool::GX_FALSE);
        GXSetCullMode(GXCullMode::GX_CULL_BACK);
        GXBegin(GXPrimitive::GX_QUADS, GXVtxFmt::GX_VTXFMT0, 4);
        GXPosition3f32(posx, posy, z);
        GXPosition3f32(posx + width, posy, z);
        GXPosition3f32(posx + width, posy + height, z);
        GXPosition3f32(posx, posy + height, z);
    }
}
