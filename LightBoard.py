import board
import neopixel
import time
import config
import random
from CommandReceived import CommandReceived
from ThreadDatabase import DB


class LightBoard:
    """Communicate with NeoPixel based addressable lights indexed by character."""
    pixels = neopixel.NeoPixel(board.D18, config.num_lights)
    db = DB()

    def __init__(self, db):
        """Initialize the string of lights with the proper database.

            Keyword arguments:
            db -- The threading safe database where commands are stored (default new DB).
        """
        self.db = db
        
    def pixel_on(self, idx):
        """Turn on given pixel in string.

            Keyword arguments:
            idx -- The index of the pixel on the string.
        """
        self.pixels[idx] = (255, 255, 255)
        
    def pixel_off(self, idx):
        """Turn off given pixel in string.

            Keyword arguments:
            idx -- The index of the pixel on the string.
        """
        self.pixels[idx] = (0, 0, 0)

    def show_letter(self, s):
        """Light up the associated light on the string of lights.

            Keyword arguments:
            s -- The letter in the letter mapping.
        """
        if self.db.command_list:
            state = self.db.lock_stop("get", 0)
            if self.db.command_list[0] is "<RESTART>" and not state:
                pass
            else:
                raise CommandReceived
        if s not in config.letter_mapping:
            return
        self.pixel_on(config.letter_mapping[s])
        time.sleep(1)
        self.pixel_off(config.letter_mapping[s])
        time.sleep(.5)

    def spell_word(self, word):
        """Light up the associated light for each letter in the word.

            Keyword arguments:
            word -- The word to be displayed on the light string.
        """
        for s in word:
            if s != "!" and s != " ":
                self.show_letter(s)
            elif s == "!":
                self.go_crazy()
            elif s is " ":
                time.sleep(.75)
        self.db.lock_messages("remove", 0)
        time.sleep(1)
        
    def turn_all_off(self):
        """Turns off all lights on the string."""
        for i in range(config.num_lights):
            self.pixel_off(i)
        

    def go_crazy(self):
        """Randomly light up and turn off lights on the light string."""
        for i in range(50):
            if self.db.command_list:
                state = self.db.lock_stop("get", 0)
                if self.db.command_list[0] is "<RESTART>" and not state:
                    pass
                else:
                    raise CommandReceived
            for j in range(15):
                letter = random.choice(list(config.letter_mapping.values()))
                self.pixel_on(letter)
            for j in range(15):
                letter = random.choice(list(config.letter_mapping.values()))
                self.pixel_off(letter)
        
            time.sleep(.075)
        self.turn_all_off()
        return
