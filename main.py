#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
# from tools import RomReader, HawaiiBios

# rom_bytes = RomReader.read_rom('290X_NOMOD_STOCK_V1.8.rom')

fenetre = Tk()
fenetre.title("PyhawaiiBiosReader")

label = Label(fenetre, text="Work in progress ...")
label.pack()
bouton=Button(fenetre, text="Quit", command=fenetre.quit)
bouton.pack(side='bottom')

fenetre.mainloop()
