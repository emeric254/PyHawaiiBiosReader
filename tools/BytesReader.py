# -*- coding: utf-8 -*-

import struct


# normalized signed types


def read_byte(octets: bytes, pos: int, _: bool=False):
    return struct.unpack('b', bytes(octets[pos]))[0]


def read_short(octets: bytes, pos: int, big_endian: bool = False):
    short_format = ('>' if big_endian else '<') + 'h'
    return struct.unpack(short_format, octets[pos:pos + 2])[0]


def read_int(octets: bytes, pos: int, big_endian: bool = False):
    int_format = ('>' if big_endian else '<') + 'i'
    return struct.unpack(int_format, octets[pos:pos + 4])[0]


def read_long(octets: bytes, pos: int, big_endian: bool = False):
    long_format = ('>' if big_endian else '<') + 'l'
    return struct.unpack(long_format, octets[pos:pos + 4])[0]


def read_longlong(octets: bytes, pos: int, big_endian: bool = False):
    longlong_format = ('>' if big_endian else '<') + 'q'
    return struct.unpack(longlong_format, octets[pos:pos + 8])[0]


# alternative signed types

def read_int8(octets: bytes, pos: int, _: bool=False):
    return read_byte(octets, pos)


def read_int16(octets: bytes, pos: int, big_endian: bool = False):
    return read_short(octets, pos, big_endian)


def read_int24(octets: bytes, pos: int, big_endian: bool = False):
    return read_int(octets, pos, big_endian) & 0x00FFFFFF  # mask for only 24 bits


def read_int32(octets: bytes, pos: int, big_endian: bool = False):
    return read_int(octets, pos, big_endian)


def read_int64(octets: bytes, pos: int, big_endian: bool = False):
    return read_longlong(octets, pos, big_endian)


# normalized unsigned types


def read_ubyte(octets: bytes, pos: int, _: bool=False):
    return struct.unpack('B', bytes(octets[pos]))[0]


def read_ushort(octets: bytes, pos: int, big_endian: bool = False):
    short_format = ('>' if big_endian else '<') + 'H'
    return struct.unpack(short_format, octets[pos:pos + 2])[0]


def read_uint(octets: bytes, pos: int, big_endian: bool = False):
    int_format = ('>' if big_endian else '<') + 'I'
    return struct.unpack(int_format, octets[pos:pos + 4])[0]


def read_ulong(octets: bytes, pos: int, big_endian: bool = False):
    long_format = ('>' if big_endian else '<') + 'L'
    return struct.unpack(long_format, octets[pos:pos + 4])[0]


def read_ulonglong(octets: bytes, pos: int, big_endian: bool = False):
    longlong_format = ('>' if big_endian else '<') + 'Q'
    return struct.unpack(longlong_format, octets[pos:pos + 8])[0]


# alternatives unsigned types


def read_uint8(octets: bytes, pos: int, _: bool=False):
    return read_ubyte(octets, pos)


def read_uint16(octets: bytes, pos: int, big_endian: bool=False):
    return read_ushort(octets, pos, big_endian)


def read_uint24(octets: bytes, pos: int, big_endian: bool = False):
    return read_uint(octets, pos, big_endian) & 0x00FFFFFF  # mask for only 24 bits


def read_uint32(octets: bytes, pos: int, big_endian: bool = False):
    return read_uint(octets, pos, big_endian)


def read_uint64(octets: bytes, pos: int, big_endian: bool = False):
    return read_ulonglong(octets, pos, big_endian)


# float


def read_halffloat(octets: bytes, pos: int, big_endian: bool=False):
    halffloat_format = ('>' if big_endian else '<') + 'e'
    return struct.unpack(halffloat_format, octets[pos:pos + 2])[0]


def read_float(octets: bytes, pos: int, big_endian: bool=False):
    float_format = ('>' if big_endian else '<') + 'f'
    return struct.unpack(float_format, octets[pos:pos + 4])[0]


def read_double(octets: bytes, pos: int, big_endian: bool=False):
    double_format = ('>' if big_endian else '<') + 'd'
    return struct.unpack(double_format, octets[pos:pos + 8])[0]


# other


def read_char(octets: bytes, pos: int, _: bool=False):
    return struct.unpack('c', bytes(octets[pos]))[0]


def read_boolean(octets: bytes, pos: int, _: bool=False):
    return struct.unpack('?', bytes(octets[pos]))[0]


def read_str(octets: bytes, pos: int, length: int, big_endian: bool = False, encoding: str = 'utf-8'):
    str_format = ('>' if big_endian else '<') + str(length) + 's'
    return struct.unpack(str_format, octets[pos:pos + length])[0].decode(encoding)
