#!/bin/env bash
# small helper script for nerds, who want to read the assembly of the rust code :)

cd `dirname "${BASH_SOURCE[0]}"`

pushd custom-functions
cargo build --release
popd

${DEVKITPPC}/bin/powerpc-eabi-objdump -dr ./custom-functions/target/powerpc-unknown-eabi/release/libcustom_functions.a > out.s
