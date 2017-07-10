# -*- coding: utf-8 -*-

import struct


def read_int8(octet: bytes, pos: int, big_endian: bool = False):
    # print('reading int8 @' + str(pos), 'in', 'big endian' if big_endian else 'little endian')
    int8_format = 'B'
    if big_endian:
        int8_format = '>' + int8_format
    else:
        int8_format = '<' + int8_format
    return struct.unpack(int8_format, octet[pos:pos + 1])[0]


def read_int16(octet: bytes, pos: int, big_endian: bool = False):
    # print('reading int16 @' + str(pos), 'in', 'big endian' if big_endian else 'little endian')
    int16_format = 'H'
    if big_endian:
        int16_format = '>' + int16_format
    else:
        int16_format = '<' + int16_format
    return struct.unpack(int16_format, octet[pos:pos + 2])[0]


def read_int24(octet: bytes, pos: int, big_endian: bool = False):
    # print('reading int24 @' + str(pos), 'in', 'big endian' if big_endian else 'little endian')
    int24_format = 'I'  # int32 but on a 24 bit + a 8 bit null padding
    if big_endian:
        int24_format = '>' + int24_format
    else:
        int24_format = '<' + int24_format
    return struct.unpack(int24_format, octet[pos:pos + 3] + '\0'.encode('ASCII'))[0]


def read_int32(octet: bytes, pos: int, big_endian: bool = False):
    # print('reading int32 @' + str(pos), 'in', 'big endian' if big_endian else 'little endian')
    int32_format = 'I'
    if big_endian:
        int32_format = '>' + int32_format
    else:
        int32_format = '<' + int32_format
    return struct.unpack(int32_format, octet[pos:pos + 4])[0]


def read_str(octet: bytes, pos: int, length: int, big_endian: bool = False):
    # print('reading str (', length, 'chars) @' + str(pos), 'in', 'big endian' if big_endian else 'little endian')
    str_format = str(length) + 's'
    if big_endian:
        str_format = '>' + str_format
    else:
        str_format = '<' + str_format
    return struct.unpack(str_format, octet[pos:pos + length])[0].decode('utf-8')
