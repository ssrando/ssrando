SECTIONS
{
    .text : {
        __text_start = . ;
        KEEP(*(.text))
        KEEP(*custom_func*(.text.*))
        *(.text.*)
        __text_end  = . ;
    }

    .data : {
        __data_start = . ;
        *(.rodata)
        *(.data)
        *(.bss)
        *(COMMON)
        __data_end  = . ;
    }
}
