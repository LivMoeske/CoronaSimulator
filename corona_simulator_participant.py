from microbit import *
import radio
import random
import machine
#importerer forskjellige objekter som blir brukt i koden


radio.on()
#skrur på radioen

gameStart = False
isReadyToStart = False

idPlayer = str(hash(str(machine.unique_id()))) + str(random.randint(1000, 9999))
#IDen til spilleren.

MASK_IMAGE = Image("09090:00000:98689:97679:07970")
INFECTED_MASK_IMAGE = Image("09090:00040:98689:97679:07970")
NO_MASK_IMAGE = Image("09090:00000:90009:09990:00000")
INFECTED_IMAGE = Image("09090:00000:09990:90009:99999")
#Dette er de forskjellige bildene som blir brukt i spillet.

SIGNAL_POWER_WITH_MASK = 2
SIGNAL_POWER_WITHOUT_MASK = 7
signalPower = SIGNAL_POWER_WITHOUT_MASK
radio.config(power=signalPower)
#Signal Power står for hvor sterkt "radio"-signalet er.

PROBABILITY_0V = 1
PROBABILITY_1V = 0.7
PROBABILITY_2V = 0.3
PROBABILITY_3V = 0.1
VACCINATIONS_LIST = [PROBABILITY_0V,PROBABILITY_1V,PROBABILITY_2V,PROBABILITY_3V]
vaccinations = random.randint(0,3)
vaccination_probability = VACCINATIONS_LIST[vaccinations]
#Dette er de forskjellige sannsynlighetene man har å bli smittet med 0-3 vaksiner.

infected = False
#Infected er True når spilleren er smittet.
PROBABILITY_REMOTE_ENCOUNTER = 0.02
PROBABILITY_CLOSE_ENCOUNTER = 0.3
#De forskjellige sannsynlighetene å bli smittet ved nære
#og fjerne møter med infiserte spillere.
PROBABILITY_MASK = 0.02
isWearingMask = False
#Sannsynligheten for å bli smittet når man har på maske.

while True:
    details = radio.receive_full()
    #"radio.receive_full()" tar opp signaler fra andre microbits og får tre typer
    #informasjon; meldingen (msg), hvor sterkt signalet er (rssi) og hvor lang 
    #tid det tar å få meldingen.
    if details:
        msg = str(details[0], 'UTF-8')
        msg = msg[3:len(msg)]
        rssi = details[1]
    if details and msg == "end": #hvis meldingen spilleren får er "end"
        gameStart = False
        isReadyToStart = False
        infected = False
        isWearingMask = False
        vaccinations = random.randint(0,3)
        vaccination_probability = VACCINATIONS_LIST[vaccinations]
        display.show("")
        #går alt tilbake til sin opprinnelige verdi.
    if gameStart: #hvis spillet er i gang
        if button_a.was_pressed(): #hvis a blir trykket
            if isWearingMask: #og hvis spilleren har på maske
                signalPower = SIGNAL_POWER_WITHOUT_MASK #blir signalet så sterkt som uten maske
                isWearingMask = False #masken blir tatt av
            else: #hvis den ikke har på maske
                signalPower = SIGNAL_POWER_WITH_MASK #blir signalet så sterkt som med maske
                isWearingMask = True #masken blir tatt på
            radio.config(power=signalPower)
        if infected:
            if isWearingMask:
                display.show(INFECTED_MASK_IMAGE)
            else:
                display.show(INFECTED_IMAGE)
                #viser bildet med/uten maske
            radio.send("Virus") #sender "Virus" til andre microbits
        else: #hvis spilleren ikke er smittet
            if isWearingMask:
                display.show(MASK_IMAGE)
            else:
                display.show(NO_MASK_IMAGE)
                #viser bildet med/uten maske
            if details and msg == "Virus": #hvis spilleren får signalet "Virus" 
                randomNumber = random.random() #dette er et tilfeldig nummer mellom 0 og 1 (viktig senere).
                if rssi >= -65: #hvis rssi (styrken av signalet) er over eller likt -65:
                    probability = PROBABILITY_CLOSE_ENCOUNTER #da er dette sannsynligheten.
                else: #hvis rssi (styrken av signalet) er under -65:
                    probability = PROBABILITY_REMOTE_ENCOUNTER #da er dette sannsynligheten osv.
                if isWearingMask:
                    probability *= PROBABILITY_MASK
                probability *= vaccination_probability
                if randomNumber <= probability: #hvis det tilfeldige nummeret er mindre enn sannsynligheten
                    infected = True #blir man smittet
        if vaccinations == 1 or vaccinations == 3:
            display.set_pixel(0,1,7)
        if vaccinations == 2 or vaccinations == 3:
            display.set_pixel(0,0,7)
            #viser hvor mange vaksiner man har
        sleep(2000)
    else: #hvis spillet IKKE er i gang (registrering)
        if not isReadyToStart: #hvis spilleren ikke er klar:
            display.scroll("PRESS A")
            sleep(200)
            display.show(Image.ARROW_W)
            sleep(500)
        if button_a.was_pressed(): #hvis a knappen blir trykket
            radio.send(idPlayer) #sender spilleren IDen sin
            isReadyToStart = True #spilleren er klar
            display.scroll("READY")
            sleep(1000)
        elif isReadyToStart and details: #hvis spilleren er klar + man får et signal
            if msg == idPlayer: #hvis signalet som blir mottatt er det samme som IDen
                infected = True
            if msg == "start": #hvis spilleren får startsignal
                gameStart = True #begynner spillet
                