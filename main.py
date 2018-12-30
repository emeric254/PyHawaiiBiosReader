#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from tools import RomReader, RomWriter, BytesReader, BytesWriter
from tools.HawaiiBios import HawaiiBios

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

selected_section = None
bios = None


def save_rom(file_name):
    if bios:
        bios.calculate_checksum()
        RomWriter.write_rom(file_name, bios.rom)
        info_dialog = Gtk.MessageDialog(
            parent = main_window,
            flags = 0,
            message_type = Gtk.MessageType.INFO,
            buttons = Gtk.ButtonsType.OK,
            text = "Bios file saved"
        )
        info_dialog.run()
        info_dialog.destroy()


def load_rom(file_name):
    global bios
    bios = None
    rom = None
    if not file_name.endswith('.rom'):
        error_dialog = Gtk.MessageDialog(
            parent = main_window,
            flags = 0,
            message_type = Gtk.MessageType.ERROR,
            buttons = Gtk.ButtonsType.OK,
            text = "Verify this file is a bios rom"
        )
        error_dialog.run()
        error_dialog.destroy()
        return
    rom = RomReader.read_rom(file_name)
    if not rom:
        return
    bios = HawaiiBios(rom)
    if not bios.is_supported():
        warning_dialog = Gtk.MessageDialog(
            parent = main_window,
            flags = 0,
            message_type = Gtk.MessageType.WARNING,
            buttons = Gtk.ButtonsType.OK,
            text = "Please care, this device id is not listed as supported"
        )
        warning_dialog.run()
        warning_dialog.destroy()


def load_sections():
    # reset selected section
    global selected_section
    selected_section = None
    # reset all displayed data
    field_list_store.clear()
    section_list_store.clear()
    # ensure bios is loaded
    if not bios:
        return
    # fill section displayed data
    for key in sorted(bios.data.keys()):
        section_list_store.append([key])


def load_fields(section):
    # reset diplayed data
    field_list_store.clear()
    # ensure bios is loaded
    if not bios:
        return
    # to know which section is displayed
    global selected_section
    selected_section = section
    # add data to the displayed list from the bios decoded data
    for row in bios.data[section]:
        field_list_store.append(
            [
                row['name'],
                row['value'],
                row['unit'],
                row['position'],
                row['length']
            ]
        )


class Handler:

    @staticmethod
    def onQuit(*args):
        Gtk.main_quit(*args)

    @staticmethod
    def onAbout(*args):
        open_window.show_all()

    @staticmethod
    def onAboutDestroy(*args):
        open_window.hide()

    @staticmethod
    def onEditValue(cell, path, new_value):
        # update the bios decoded data and displayed data
        bios.data[selected_section][int(path)]['value'] = new_value
        field_list_store[path][1] = new_value
        # get value position and length
        pos = int(field_list_store[path][3], 0)
        length = field_list_store[path][4]
        # write the value into the RAM loaded bios hex data
        if length == '8 bits':
            bios.rom = BytesWriter.write_int8(bios.rom, pos, int(new_value))
        elif length == '16 bits':
            bios.rom = BytesWriter.write_int16(bios.rom, pos, int(new_value))
        elif length == '24 bits':
            bios.rom = BytesWriter.write_int24(bios.rom, pos, int(new_value))
        elif length == '32 bits':
            bios.rom = BytesWriter.write_int32(bios.rom, pos, int(new_value))
        elif length.endswith('chars'):
            bios.rom = BytesWriter.write_str(bios.rom, pos, int(length.split(' ')[0]), new_value)

    @staticmethod
    def onSectionChoice(cell, data=None):
        if cell.get_active() in range(len(section_list_store)):
            load_fields(section_list_store[cell.get_active()][0])

    @staticmethod
    def onOpenFile(*args):
        #
        filter_bios_rom = Gtk.FileFilter()
        filter_bios_rom.set_name("Bios rom")
        filter_bios_rom.add_pattern("*.rom")
        #
        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any file")
        filter_any.add_pattern("*")
        #
        dialog = Gtk.FileChooserDialog(
            title = "Open bios file",
            parent = main_window,
            action = Gtk.FileChooserAction.OPEN,
            buttons = (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        )
        dialog.add_filter(filter_bios_rom)
        dialog.add_filter(filter_any)
        try:
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                file_name = dialog.get_filename()
                load_rom(file_name)
                load_sections()
        finally:
            dialog.destroy()

    @staticmethod
    def onSaveFile(*args):
        try:
            dialog = Gtk.FileChooserDialog(
                title = "Save bios file",
                parent = main_window,
                action = Gtk.FileChooserAction.SAVE,
                buttons = (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
            )
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                file_name = dialog.get_filename()
                save_rom(file_name)
        finally:
            dialog.destroy()


builder = Gtk.Builder()
builder.add_from_file("glade-1.glade")
builder.connect_signals(Handler())

main_window = builder.get_object("main_window")
main_window.show_all()
field_list_store = builder.get_object('field_list_store')
section_list_store = builder.get_object('section_list_store')
open_window = builder.get_object("about_window")

Gtk.main()
