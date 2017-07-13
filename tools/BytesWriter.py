# -*- coding: utf-8 -*-

import struct


def write_int8(octet: bytes, pos: int, value: int):
    octet = bytearray(octet)
    octet[pos] = value


def write_int16(octet: bytes, pos: int, value: int, big_endian: bool = False):
    octet = bytearray(octet)
    if big_endian:
        octet[pos] = value & 0xFF00
        octet[pos + 1] = value & 0x00FF
    else:
        octet[pos + 1] = value & 0xFF00
        octet[pos] = value & 0x00FF


def write_int24(octet: bytes, pos: int, value: int, big_endian: bool = False):
    octet = bytearray(octet)
    if big_endian:
        octet[pos] = value & 0xFF0000
        octet[pos + 1] = value & 0x00FF00
        octet[pos + 2] = value & 0x0000FF
    else:
        octet[pos + 2] = value & 0xFF0000
        octet[pos + 1] = value & 0x00FF00
        octet[pos] = value & 0x0000FF


def write_int32(octet: bytes, pos: int, value: int, big_endian: bool = False):
    octet = bytearray(octet)
    if big_endian:
        octet[pos] = byte(value & 0xFF000000)
        octet[pos + 1] = value & 0x00FF0000
        octet[pos + 2] = value & 0x0000FF00
        octet[pos + 3] = value & 0x000000FF
    else:
        octet[pos + 3] = value & 0xFF000000
        octet[pos + 2] = value & 0x00FF0000
        octet[pos + 1] = value & 0x0000FF00
        octet[pos] = value & 0x000000FF


def write_str(octet: bytes, pos: int, length: int, value: str, big_endian: bool = False):
    octet = bytearray(octet)
    if big_endian:
        for i in range(length):
            octet[pos + length - i - 1] = value[i]
    else:
        for i in range(length):
            octet[pos + i] = value[i]
