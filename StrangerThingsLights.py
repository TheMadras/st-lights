import threading
import sys
import config
import time
from CommandReceived import CommandReceived
from TextClient import TextClient
from LightBoard import LightBoard
from ThreadDatabase import DB


class LightsProgram:
    """Controlling class for Stranger Things lights display."""
    db = DB()
    text_client = TextClient(config.account_sid, config.auth_token, db)
    light_board = LightBoard(db)

    def strange_scene(self):
        """TODO: Combine soundtrack with associated lights to mimic the Stranger Things scene."""
        pass

    def handle_commands(self):
        """Handles any commands received from the Twilio text messages."""
        while self.db.command_list:
            self.light_board.turn_all_off()
            if self.db.command_list[0] == "<PAUSE>":
                self.db.lock_stop("set", True)
            elif self.db.command_list[0] == "<STOP>":
                self.db.lock_stop("set", True)
                self.db.lock_messages("clear", 0)
            elif self.db.command_list[0] == "<START>":
                self.db.lock_stop("set", False)
            elif self.db.command_list[0] == "<CLEAR>":
                self.db.lock_messages("clear", 0)
            elif self.db.command_list[0] == "<QUIT>":
                sys.exit(0)
            elif self.db.command_list[0] == "<SCENE>":
                self.strange_scene()
            self.db.command_list.pop()
            
    def update_messages(self):
        """Function run asynchronously to continually update messages"""
        while True:
            self.text_client.update_messages()
            time.sleep(2)

    def start_program(self):
        """Start the Stranger Things Lights program with associated Twilio account."""
        # Start message handling thread
        try:
            x = threading.Thread(target=self.update_messages, args=(), daemon=True)
            x.start()
        except Exception as e:
            print(e)
        # Handle the lights
        self.light_board.turn_all_off()
        while True:
            if self.db.command_list:
                self.handle_commands()
            try:
                res = self.db.lock_stop("get", 0)
                if not res:
                    w = self.db.lock_messages("get", 0)
                    if w != "":
                        self.light_board.spell_word(w)
            except CommandReceived as c:
                self.handle_commands()
            except Exception as e:
                print(e)
