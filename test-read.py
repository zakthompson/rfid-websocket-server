from time import sleep
from mfrc522 import SimpleMFRC522

reader = SimpleMFRC522()

print("Waiting for card...")
while True:
    id, text = reader.read()
    print("ID: %s\nText: %s" % (id, text))
    sleep(1)
