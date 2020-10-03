from twilio.rest import Client
import config
import pickle
import time
from datetime import datetime, timedelta
from ThreadDatabase import DB


class TextClient:
    """Communicate with the Twilio account and update the database with any new messages."""
    account_sid = config.account_sid
    auth_token = config.auth_token
    db = DB()
    temp_list = []

    def __init__(self, account_sid, auth_token, db):
        """Initialize the connection to Twilio and associate with the database.

            Keyword arguments:
            account_sid -- The account SID of the Twilio account.
            auth_token -- The auth token of the Twilio account.
            db -- The threading safe database.
        """
        self.client = Client(account_sid, auth_token)
        self.db = db

    def parse_message(self, sms):
        """Parse the message into commands or into show-able words.

            Keyword arguments:
            sms -- The dictionary containing sms information.
        """
        body = sms.body
        l = []
        if len(body) == 0:
            return
        state = self.db.lock_stop("get", 0)
        if body[0] == "<":
            for s in body:
                l.append(s.upper())
                if s == ">":
                    break
            if l[-1] == ">":
                new_command = "".join(l)
                self.db.command_list.insert(0, new_command)
        elif not state:
            for s in body:
                if s.isalpha() or s is "!":
                    l.append(s.upper())
            self.temp_list.insert(0, "".join(l))

    def update_messages(self):
        """Update the list of messages with recent messages from the Twilio account."""
        while True:
            self.temp_list = []

            try:
                with open('objs.pkl', 'rb') as f:
                    last_checked = pickle.load(f)
            except Exception as e:
                last_checked = datetime.now() + timedelta(hours=6)

            messages = self.client.messages.list(
                date_sent_after=last_checked,
                limit=200
            )

            current_check = datetime.now() + timedelta(hours=6)
            i = 0
            for sms in messages:
                if sms.to == config.twilio_number:
                    self.parse_message(sms)
                    i += 1
            if self.temp_list:
                self.db.lock_messages("add", self.temp_list)
            last_checked = current_check + timedelta(seconds=.05)
            with open('objs.pkl', 'wb') as f:
                pickle.dump(last_checked, f)
            
            return
