
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from tools import RomReader
from tools.HawaiiBios import HawaiiBios

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

rom = None
bios = None


def load_rom(file_name):
    global rom
    rom = None
    if file_name.endswith('.rom'):
        rom = RomReader.read_rom(file_name)
        return
    error_dialog = Gtk.MessageDialog(main_window, 0, Gtk.MessageType.ERROR, Gtk.ButtonsType.OK, "Verify this file is a bios rom")
    error_dialog.run()
    error_dialog.destroy()

def load_bios():
    global bios
    bios = None
    if rom:
        bios = HawaiiBios(rom)
        if not bios.is_supported():
            warning_dialog = Gtk.MessageDialog(main_window, 0, Gtk.MessageType.WARNING, Gtk.ButtonsType.OK, "Please care, this device id is not listed as supported")
            warning_dialog.run()
            warning_dialog.destroy()


def load_sections():
    field_list_store.clear()
    section_list_store.clear()
    if bios:
        for key in sorted(bios.data.keys()):
            section_list_store.append([key])


def load_fields(section):
    field_list_store.clear()
    if bios:
        for row in bios.data[section]:
            field_list_store.append([row['name'], row['value'], row['unit'], row['position'], row['length']])


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
    def onEditValue(cell, path, new_text):
        field_list_store[path][1] = new_text
        print(field_list_store[path][1])

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
        dialog = Gtk.FileChooserDialog("Open bios file", main_window, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        dialog.add_filter(filter_bios_rom)
        dialog.add_filter(filter_any)
        try:
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                file_name = dialog.get_filename()
                load_rom(file_name)
                load_bios()
                load_sections()
        finally:
            dialog.destroy()

    @staticmethod
    def onSaveFile(*args):
        try:
            dialog = Gtk.FileChooserDialog("Save bios file", main_window, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
            response = dialog.run()
            if response == Gtk.ResponseType.OK:
                print("File saved: " + dialog.get_filename())
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
