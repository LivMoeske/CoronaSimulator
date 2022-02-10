from microbit import *
from collections import OrderedDict
import radio
import random
#importerer forskjellige typer objekter som blir brukt i koden


radio.on()
#skrur på radioen

gameStart = False
participants = OrderedDict([]) #listen av spillere
keysList = list() #blir definert nede

while True:
    received = radio.receive() #"radio.receive()" er innkommende signaler
    if gameStart == False: #hvis spillet ikke er i gang
        display.show(str(len(participants))) #viser antall spillere
        if received and received != "Virus": #hvis masteren får en melding og meldingen ikke er "Virus"
            participants[received] = False #legger til signalet (IDen til en spiller) til listen participants. 
            #(Denne er False, fordi den ikke er smittet.)
            keysList = list(participants.keys()) #listen av "keys" i "participants" (IDene til spillerne)
        if button_a.was_pressed():
            if len(keysList) > 1: #hvis lengden av denne listen (antall spillere) er større enn 1
                display.scroll(len(keysList))
                randomNumber = random.randint(0, len(keysList) - 1) #velger en tilfellig spiller til å bli smittet på begynnelsen
                keyInfected = str(keysList[randomNumber]) #velger IDen til den tilfeldige spilleren
                radio.send(keyInfected) #sender IDen
                radio.send("start") #spillet begynner
                gameStart = True
            else: #hvis lengden av listen (antall spillere) er mindre enn 2
                display.scroll("NEEDS 2 PLAYERS")
    else: #hvis spillet er i gang
        if button_a.was_pressed():
            radio.send("end") #slutter spiller
            participants.clear()
            keysList.clear()
            #clear() gjør listene tomme sånn at de kan registreres igjen
            gameStart = False
    
