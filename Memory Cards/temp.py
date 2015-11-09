"""
This module is temporary. Contains initializations and auxiliary functions.
"""

# -*- coding: utf-8 -*-
import MemoryCards as mc
import MemoryCardsGUI as mcg
import datetime
import sqlite3

# TODO - transfer auxiliary functions from temp to Cardlist object


def words_to_repeat(entries):
    """ Given all memory cards from database returns cards to repeat """
    cards = []
    for row in entries:
        # Get repetition date from database
        date = row[3].replace(':', ' ')
        # Format and change data to datetime object
        date = date.replace('-', ' ')
        date = date.split(' ')
        date = datetime.datetime(int(date[0]), int(date[1]), int(date[2]), int(date[3]), int(date[4]), int(date[5]))
        # Get current date
        now = datetime.datetime.now().strftime('%y/%m/%d')
        now = datetime.datetime.strptime(now, "%y/%m/%d")
        # Check if current date is equal or bigger than repetition date
        if date <= now:
            # Create MemoryCard object based on data from database
            card = mc.MemoryCard(row[0], row[1], row[5], row[4])
            # Append MemoryCard to cards to repeat
            cards.append(card)
    return cards


def check(card, answer):
    """ Checks if answer to memory card is correct """
    if card.check_answer(answer) and not card.card_guessed():
        # Update card guessed status
        card.guess()
        # Update card repetition date
        card.to_repeat()
        cur.execute('UPDATE Words SET Date=?, Guess=?, Days=?, Guesses=? WHERE Polish=?',
                            (card.last_guess_date, card.get_repeat_date(), card.days_to_repeat,
                             card.guesses_in_row, card.polish))
        con.commit()
        return True
    else:
        return False


def next_word(card):
    """ Change memory card to guess """
    # If card is guessed correctly remove it from cards to repeat
    if card.card_guessed():
        cards_to_repeat.remove(card)
    # Else update consecutive guesses and add card in the end of repetition list
    else:
        card.set_guesses_to0()
        cards_to_repeat.remove(card)
        cards_to_repeat.append(card)
        lista.update_list(cards_to_repeat)

# Card list
lista = mc.CardList()
# Connect to database and set cursor
con = sqlite3.connect('memorycards.sqlite')
cur = con.cursor()
# GUI manager
app = mcg.PageManager()
# Get all rows from database
cur.execute("SELECT * FROM Words")
rows = cur.fetchall()
# Get cards to repeat
cards_to_repeat = words_to_repeat(rows)
lista.update_list(cards_to_repeat)