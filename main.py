
#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from tools import RomReader
from tools.HawaiiBios import HawaiiBios

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

bios = None


def load_rom(file_name):
    global bios
    bios = HawaiiBios(RomReader.read_rom(file_name))


def load_sections():
    section_list_store.clear()
    for key in sorted(bios.data.keys()):
        section_list_store.append([key])


def load_fields(section):
    field_list_store.clear()
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
        dialog = Gtk.FileChooserDialog("Open bios file", main_window, Gtk.FileChooserAction.OPEN, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            file_name = dialog.get_filename()
            print('File selected:', file_name)
            #
            load_rom(file_name)
            #
            section_list_store.clear()
            field_list_store.clear()
            #
            load_sections()
        dialog.destroy()

    @staticmethod
    def onSaveFile(*args):
        dialog = Gtk.FileChooserDialog("Save bios file", main_window, Gtk.FileChooserAction.SAVE, (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            print("File saved: " + dialog.get_filename())
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
