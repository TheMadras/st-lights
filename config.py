"""Configuration file for all necessary variables."""

# Mapping of any given character to an index on the light string.
letter_mapping = {"A": 0, "B": 1, "C": 2, "D": 3, "E": 4, "F": 5, "G": 6, "H": 7,
                  "I": 8, "J": 9, "K": 10, "L": 11, "M": 12, "N": 13, "O": 14, "P": 15,
                  "Q": 16, "R": 17, "S": 18, "T": 19, "U": 20, "V": 21, "W": 22, "X": 23,
                  "Y": 24, "Z": 25}

# Account SID of associated Twilio account.
account_sid = "YOUR_ACCOUNT_SID_HERE"

# Auth Token of associated Twilio account.
auth_token = "YOUR_AUTH_TOKEN_HERE"

# Full phone number of associated Twilio account with country code. In format +15551236789.
twilio_number = "YOUR_NUMBER_HERE"

# Number of lights on the string
num_lights = 100
