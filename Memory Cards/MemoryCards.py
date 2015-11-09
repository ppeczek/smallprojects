"""
Application allows to learn french using virtual "memory cards". It may also be used to study other subjects.
Memory cards are stored in database. Application has repetition system to empower learning.
"""

# -*- coding: utf-8 -*-
import sqlite3
import datetime
import temp


class MemoryCard(object):
    """ This class represents single memory card """

    def __init__(self, polish, french, guesses, days):
        """ Constructor function """

        # Word in polish
        self.polish = polish
        # Word in french
        self.french = french
        # Number of correct guesses in a row
        self.guesses_in_row = guesses
        # Date of card creation (each start of programme creates cards to repeat)
        now = datetime.datetime.now().strftime('%y/%m/%d')
        self.last_guess_date = datetime.datetime.strptime(now, "%y/%m/%d")
        # Number of days to next repetition
        self.days_to_repeat = days
        # Flag if card is guessed in current session
        self.guessed = False

    def get_repeat_date(self):
        """ Calculates date of next repetition """
        return self.last_guess_date + datetime.timedelta(days=self.days_to_repeat)

    def guess(self):
        """ Flags card as guessed and increments number of guesses in a row """
        self.guessed = True
        self.guesses_in_row += 1

    def check_answer(self, answer):
        """ Checks if answer is correct """
        return answer == self.french

    def give_polish(self):
        """ Returns polish word of card """
        return self.polish

    def give_french(self):
        """ Returns french word of card """
        return self.french

    def card_guessed(self):
        """ Returns information if card is guessed """
        return self.guessed

    def set_guesses_to0(self):
        """ Sets number of correct guesses in a row to 0 """
        self.guesses_in_row = 0

    def to_repeat(self):
        """
        Calculates number of days to repetition
        based on number of correct guesses in a row
        """
        if self.guesses_in_row <= 1:
            self.days_to_repeat = 1
        if self.guesses_in_row == 2:
            self.days_to_repeat = 2
        if self.guesses_in_row == 3:
            self.days_to_repeat = 5
        if self.guesses_in_row == 4:
            self.days_to_repeat = 5
        if self.guesses_in_row > 4:
            self.days_to_repeat = 30


class CardList(object):
    """ This class represents list of cards. """

    def __init__(self):
        """ Constructor function """

        # List of cards to repeat
        self.list = []

    def add_card(self, polish, french):
        """ Adds memory card to database """
        card = MemoryCard(polish, french, 0, 1)
        con = sqlite3.connect('memorycards.sqlite')
        cur = con.cursor()
        cur.execute('INSERT INTO Words (Polish, French, Date, Guess, Days, Guesses) VALUES (?, ?, ?, ?, ?, ?)',
                    (polish, french, card.last_guess_date,
                     card.get_repeat_date(), card.days_to_repeat,
                     card.guesses_in_row))
        con.commit()
        con.close()

    def update_list(self, new_list):
        """ Updates list of cards to repeat """
        self.list = new_list

    def list_length(self):
        """ Returns length of list of cards to repeat """
        return len(self.list)

    def give_list(self):
        """ Returns list of cards to repeat """
        return self.list


def main():
    """ Main program function. """
    # Window size
    temp.app.geometry("400x300")
    # Start updating GUI
    temp.app.after(1, temp.app.update_status())
    # GUI mainloop
    temp.app.mainloop()

# Call the main function, start up
if __name__ == "__main__":
    main()

