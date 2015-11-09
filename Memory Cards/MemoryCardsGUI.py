"""
This module is used to manage application GUI.
"""

import tkinter as tk
from tkinter import ttk
import MemoryCards as mc
import random
import temp

LARGE_FONT = ("Verdana", 12)


class PageManager(tk.Tk):
    """ This class represents general page manager """

    def __init__(self, *args, **kwargs):
        """ Constructor function """

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "Memory Cards")

        # Set single container
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # Dictionary for frames
        self.frames = {}

        # Text variable for label
        self.wordcount = tk.StringVar()
        self.wordcount.set('')

        # Text variable for label
        self.word = tk.StringVar()
        self.word.set('')

        # Currently viewed card
        self.card = None

        # Iteration through frames
        for F in (StartPage, AddWord, Repeat):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        # Start frame
        self.show_frame(StartPage)

    def show_frame(self, cont):
        """ Shows current frame """
        frame = self.frames[cont]
        frame.tkraise()

    def update_status(self):
        """" Updates frame """
        cards = temp.lista.give_list()
        # Shows current card or indicates that there are no more cards to repeat
        if len(cards) > 0:
            self.card = cards[0]
            self.word.set(self.card.give_polish())
        else:
            self.card = None
            self.word.set("No more words to repeat")

        # Shows words to repeat left
        self.wordcount.set("Words left: " + str(temp.lista.list_length()))
        # Updates all
        self.after(100, self.update_status)


class StartPage(tk.Frame):
    """ This class represents start page """

    def __init__(self, parent, controller):
        """ Constructor function """
        tk.Frame.__init__(self, parent)

        # Label
        label = tk.Label(self, text="Menu", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        # Buttons
        button1 = ttk.Button(self, text="Add word",
                             command=lambda: controller.show_frame(AddWord))
        button1.pack()

        button2 = ttk.Button(self, text="Repeat",
                             command=lambda: controller.show_frame(Repeat))
        button2.pack()

        button3 = ttk.Button(self, text="Exit",
                             command=lambda: exit())
        button3.pack()


class AddWord(tk.Frame):
    """ This class represents add word page """

    def __init__(self, parent, controller):
        """ Constructor function """
        tk.Frame.__init__(self, parent)

        # Labels
        label = tk.Label(self, text="Add Word", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        pl = ttk.Label(self, text="Polish:")
        pl.pack()

        # Entry fields and label
        self.ent1 = ttk.Entry(self)
        self.ent1.pack()

        fr = ttk.Label(self, text="French:")
        fr.pack()

        self.ent2 = ttk.Entry(self)
        self.ent2.pack()

        # Buttons
        button1 = ttk.Button(self, text="Add word",
                             command=lambda: self.button_clicked())
        button1.pack()

        button2 = ttk.Button(self, text="Back to Menu",
                             command=lambda: controller.show_frame(StartPage))
        button2.pack()

    def button_clicked(self):
        """ Handles the button click """
        if self.ent1.get() != '' and self.ent2.get() != '':
            temp.lista.add_card(self.ent1.get(), self.ent2.get())
            self.ent1.delete(0, 'end')
            self.ent2.delete(0, 'end')
        else:
            self.ent1.delete(0, 'end')
            self.ent1.insert(0, 'You have to fill both fields')


class Repeat(tk.Frame):
    """ This class represents repeat page """
    def __init__(self, parent, controller):
        """ Constructor function """
        tk.Frame.__init__(self, parent)

        self.controller = controller

        # Labels
        label = tk.Label(self, text="Repeat", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        lbl = ttk.Label(self, textvariable=controller.wordcount)
        lbl.pack()

        word = ttk.Label(self, textvariable=controller.word)
        word.pack()

        # Entry field
        self.ent1 = ttk.Entry(self, width=50)
        self.ent1.pack()

        # Buttons
        button1 = ttk.Button(self, text="Back to Menu",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack(side=tk.LEFT)

        button2 = ttk.Button(self, text="Next Word",
                             command=lambda: self.button_clicked(2))

        button2.pack(side=tk.RIGHT)

        button3 = ttk.Button(self, text="Confirm",
                             command=lambda: self.button_clicked(3))

        button3.pack()

        button4 = ttk.Button(self, text="Check as correct",
                             command=lambda: self.button_clicked(4))

        button4.pack()

    def button_clicked(self, button_number):
        """ Handles the buttons clicks """
        if button_number == 2:
            self.ent1.delete(0, 'end')
            if self.controller.card:
                temp.next_word(self.controller.card)
        if button_number == 3:
            if self.controller.card:
                word = self.ent1.get()
                if temp.check(self.controller.card, word):
                    self.ent1.delete(0, 'end')
                    self.ent1.insert(0, "Correct!")
                else:
                    self.ent1.delete(0, 'end')
                    self.ent1.insert(0, "Your word: " + word +
                                     ". Correct: " + self.controller.card.give_french())
        if button_number == 4:
            if self.controller.card:
                temp.check(self.controller.card, self.controller.card.give_french())
                self.ent1.delete(0, 'end')
                self.ent1.insert(0, "Correct!")
