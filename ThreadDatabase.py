import threading


class DB:
    """Threading safe database for keeping track of the messages and commands."""
    lock_message = threading.Lock()
    stop_lock = threading.Lock()

    message_list = []
    stop_all = False
    command_list = []

    def lock_messages(self, command, value):
        """Safely add items into the message and command lists without causing problems with threading.

            Keyword arguments:
            command -- What to do to the database. Can be add, get, remove, or clear
            value -- The value passed with the command.
        """
        with self.lock_message:
            if command == "add":
                self.message_list.extend(value)
                return
            if command == "get":
                if not self.message_list:
                    return ""
                return self.message_list[0]
            if command == "remove":
                self.message_list.pop(0)
                return
            if command == "clear":
                self.message_list.clear()
                return

    def lock_stop(self, command, value):
        """Safely add items into the message and command lists without causing problems with threading.

            Keyword arguments:
            command -- What to do to the database. Can be set or get.
            value -- The value passed with the command.
            Returns:
            The value of the stop_all variable if get is chosen.
        """
        with self.stop_lock:
            if command == "set":
                self.stop_all = value
                return
            if command == "get":
                return self.stop_all
