# -*- coding: utf-8 -*-

import struct


def read_int8(octet: bytes, pos: int):
    return octet[pos]


def read_int16(octet: bytes, pos: int, big_endian: bool = False):
    int16_format = ('>' if big_endian else '<') + 'H'
    return struct.unpack(int16_format, octet[pos:pos + 2])[0]


def read_int24(octet: bytes, pos: int, big_endian: bool = False):
    return read_int32(octet, pos, big_endian) & 0x00FFFFFF  # mask for only 24 bits


def read_int32(octet: bytes, pos: int, big_endian: bool = False):
    int32_format = ('>' if big_endian else '<') + 'I'
    return struct.unpack(int32_format, octet[pos:pos + 4])[0]


def read_str(octet: bytes, pos: int, length: int, big_endian: bool = False):
    str_format = ('>' if big_endian else '<') + str(length) + 's'
    return struct.unpack(str_format, octet[pos:pos + length])[0].decode('utf-8')
