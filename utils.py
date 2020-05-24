import struct
import collections

def write_u8(data, value, pos=None):
    if pos != None:
        data.seek(pos)
    data.write(struct.pack('>B', value))

def write_u24(data, value, pos=None):
    if pos != None:
        data.seek(pos)
    high=value>>16
    low=value&0xFFFF
    data.write(struct.pack('>BH', high, low))

def write_u32(data, value, pos=None):
    if pos != None:
        data.seek(pos)
    data.write(struct.pack('>I', value))

def read_u8(data, pos=None):
    if pos != None:
        data.seek(pos)
    return struct.unpack(">B", data.read(1))[0]

def read_u24(data, pos=None):
    if pos != None:
        data.seek(pos)
    d=struct.unpack(">BH", data.read(3))
    return (d[0]<<16)|d[1]

def read_u32(data, pos=None):
    if pos != None:
        data.seek(pos)
    return struct.unpack(">I", data.read(4))[0]

def read_null_term_string(data, pos=None):
    if pos != None:
        data.seek(pos)
    buf=b''
    read=data.read(1)
    while read != b'\x00':
        buf=buf+read
        read=data.read(1)
    return buf.decode('ASCII')

def unpack(fields, formatstr, item):
    return collections.namedtuple('_',fields)._make(struct.unpack(formatstr,item))._asdict()

def toStr(bytestr):
    return bytestr.split(b'\x00',1)[0].decode('shift-jis')