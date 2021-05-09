# Fragen an Messungen:
    #
# Wie sieht die Bewegung aus, wenn man steht? --> Messwertaufnahme und Auswertung
def Zeitmessung(Dauer: number):
    global ZeitUnbewegt, boAlarm, boReset, boBewegungRegistriert
    if boStarteMessung == 1:
        basic.pause(1000)
        ZeitUnbewegt += 1
        if 60 * Dauer <= ZeitUnbewegt:
            boAlarm = 1
        if boReset > 0 or boBewegungRegistriert > 0:
            boAlarm = 0
            ZeitUnbewegt = 0
            boReset = 0
            boBewegungRegistriert = 0

def AlarmAusgeben():
    global boAlarm,boAkustisch,boOptisch
    if boAlarm > 0:
        # pass
        if boAkustisch > 0:
            music.play_melody("C5 - C5 - C5 - C5 C5 ", 240)
        # , MelodyOptions.ONCE_IN_BACKGROUND)
        if boOptisch > 0:
            basic.set_led_color(0xff0000)
            basic.pause(200)
            basic.set_led_color(0x0000ff)
            basic.pause(200)
    else:
        # pass
        
        music.stop_melody(MelodyStopOptions.ALL)
# pass
def BewegungErkennen():
    global boBewegungRegistriert, Last_x, Last_y, Last_z,SchwellwertBewegung,Mittelwert_X,Mittelwert_Y,Mittelwert_Z
    global ZaehlerBewegungX
    # Neuer Block (ArrayListe) wird ausgewertet
    if zeiger_Arrays == 1:
        basic.set_led_color(0xff00ff)
        boBewegungRegistriert = 0
        ZaehlerBewegungX = 0
    # Wurde eine Bewegung festgestellt?
    if abs(Mittelwert_X - Last_x) > SchwellwertBewegung:
        ZaehlerBewegungX += 1
        serial.write_value("Zähler+", ZaehlerBewegungX)
    elif abs(Mittelwert_Y - Last_y) > SchwellwertBewegung:
        ZaehlerBewegungX += 1
    elif abs(Mittelwert_Z - Last_z) > SchwellwertBewegung:
        ZaehlerBewegungX += 1
    if ZaehlerBewegungX > HaeufigkeitBewegungsErkannt:
        boBewegungRegistriert = 1
        basic.set_led_color(0x00ff00)
    Last_x = Mittelwert_X
    Last_y = Mittelwert_Y
    Last_z = Mittelwert_Z
# Fehlerquellen:
    #
# Erschütterungen (Zugfahrt)
# 
# Calliope fällt runter
# 
# Calliope wird zur Seite gelegt und nicht bewegt.
def MesseBeschleunigungXYZSt():
    global Mittelwert_X, Mittelwert_Y, Mittelwert_Z, zeiger_Arrays, boArrayVoll, boToggle,Mittelwert_Staerke,ArrayGroesse
    #global WertelisteX ,WertelisteY, WertelisteZ, WertelisteStaerke, 
    ArrayGroesse
    for index in range(20):
        Mittelwert_X = (input.acceleration(Dimension.X) + 19 * Mittelwert_X) / 20
        Mittelwert_Y = (input.acceleration(Dimension.Y) + 19 * Mittelwert_Y) / 20
        Mittelwert_Z = (input.acceleration(Dimension.Z) + 19 * Mittelwert_Z) / 20
        Mittelwert_Staerke = (input.acceleration(Dimension.STRENGTH) + 19 * Mittelwert_Staerke) / 20
        basic.pause(50)
    if len(WertelisteX) < ArrayGroesse:
        WertelisteX.append(Mittelwert_X)
        WertelisteY.append(Mittelwert_Y)
        WertelisteZ.append(Mittelwert_Z)
        WertelisteStaerke.append(Mittelwert_Staerke)
        zeiger_Arrays = zeiger_Arrays + 1
    else:
        if boArrayVoll == 0:
            music.play_tone(262, music.beat(BeatFraction.WHOLE))
            boArrayVoll = 1
        if zeiger_Arrays >= ArrayGroesse:
            zeiger_Arrays = 0
        else:
            zeiger_Arrays = zeiger_Arrays + 1
        WertelisteX[zeiger_Arrays] = Mittelwert_X
        WertelisteY[zeiger_Arrays] = Mittelwert_Y
        WertelisteZ[zeiger_Arrays] = Mittelwert_Z
        WertelisteStaerke[zeiger_Arrays] = Mittelwert_Staerke
    boToggle = 1 - boToggle
    BewegungErkennen()
# Programmablauf:
    #
# Zu Beginn: Warten 100ms? Danach Bewegungsmesser starten
# 
# Zeit starten, in der Bewegungsregistration stattfindet.
# 
# Wenn keine Bewegung erkannt wurde (innerhalb der Zeit), dann Ausgabe
# 
# Reset der Ausgabe, wenn wieder Bewegung registriert wurde oder manueller Reset

def on_button_pressed_a():
    global boStarteMessung, boReset, boOptisch, boAkustisch, MenueSettings, ZeitMaxUnbeweglichkeit
    if MenueSettings == 0:
        boStarteMessung = 1
        boReset = 1
    elif MenueSettings == 1:
        MenueSettings = 0
    elif MenueSettings == 2:
        MessdatenAusgebenSeriell()
    elif MenueSettings == 3:
        boOptisch = 1 - boOptisch
    elif MenueSettings == 4:
        boAkustisch = 1 - boAkustisch
    elif MenueSettings == 5:
        if ZeitMaxUnbeweglichkeit == 1:
            ZeitMaxUnbeweglichkeit=5
        elif ZeitMaxUnbeweglichkeit == 5:
            ZeitMaxUnbeweglichkeit=10
        elif ZeitMaxUnbeweglichkeit == 10:
            ZeitMaxUnbeweglichkeit=20
        elif ZeitMaxUnbeweglichkeit == 20:
            ZeitMaxUnbeweglichkeit=30
        elif ZeitMaxUnbeweglichkeit == 30:
            ZeitMaxUnbeweglichkeit=45
        elif ZeitMaxUnbeweglichkeit == 45:
            ZeitMaxUnbeweglichkeit=60
        elif ZeitMaxUnbeweglichkeit == 60:
            ZeitMaxUnbeweglichkeit=90
        elif ZeitMaxUnbeweglichkeit == 90:
            ZeitMaxUnbeweglichkeit=120
        elif ZeitMaxUnbeweglichkeit == 120:
            ZeitMaxUnbeweglichkeit=1
        else:
            pass
    else:
        pass
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_b():
    global boStarteMessung, boReset,MenueSettings
    boStarteMessung = 0
    boReset = 1
    basic.set_led_color(0x000000)
    if MenueSettings == 0:
        MenueSettings = 1
    else:
        MenueSettings += 1
    if MenueSettings == 6:
        MenueSettings = 1
input.on_button_pressed(Button.B, on_button_pressed_b)

def MessdatenAusgebenSeriell():
    global boTransfer, Zeiger_Senden, Index
    boTransfer = 1
    Zeiger_Senden = zeiger_Arrays
    serial.write_line("Ausgabe")
    Index = 0
    while Index <= len(WertelisteX) - 1:
        led.toggle(5, 5)
        serial.write_number(WertelisteX[Zeiger_Senden])
        serial.write_string(";")
        serial.write_number(WertelisteY[Zeiger_Senden])
        serial.write_string(";")
        serial.write_number(WertelisteZ[Zeiger_Senden])
        serial.write_string(";")
        serial.write_number(WertelisteStaerke[Zeiger_Senden])
        serial.write_line("")
        Index += 1
        Zeiger_Senden += 1
        if Zeiger_Senden >= len(WertelisteX):
            Zeiger_Senden = 0
    music.play_tone(349, music.beat(BeatFraction.DOUBLE))
Index = 0
Zeiger_Senden = 0
boTransfer = 0
boToggle = 0
boArrayVoll = 0
WertelisteStaerke: List[number] = []
WertelisteZ: List[number] = []
WertelisteY: List[number] = []
WertelisteX: List[number] = []
Last_z = 0
Mittelwert_Z = 0
Last_y = 0
Mittelwert_Y = 0
Last_x = 0
Mittelwert_X = 0
zeiger_Arrays = 0
boBewegungRegistriert = 0
boReset = 0
boAlarm = 0
ZeitUnbewegt = 0
boStarteMessung = 0
SchwellwertBewegung = 0
HaeufigkeitBewegungsErkannt = 0
ArrayGroesse = 0
boAkustisch = 0
boOptisch = 0
Mittelwert_Staerke = 0
ZaehlerBewegungX = 0
AnzeigeEbene = 0
boOptisch = 1
boAkustisch = 1
serial.set_baud_rate(BaudRate.BAUD_RATE115200)
ArrayGroesse = 10
# Dauer in Minuten
ZeitMaxUnbeweglichkeit = 1
# Dauer in Minuten
HaeufigkeitBewegungsErkannt = 5
SchwellwertBewegung = 100
MenueSettings=0
MenueSettings2=0

def on_forever():
    global MenueSettings,boStarteMessung,boTransfer,boToggle,ZeitMaxUnbeweglichkeit
    if boStarteMessung == 1:
        
        if boToggle:
            basic.show_icon(IconNames.HEART)
        else:
            basic.show_icon(IconNames.SMALL_HEART)
    elif boTransfer == 1:
        basic.show_icon(IconNames.ARROW_EAST)
    elif MenueSettings == 0:
        basic.show_icon(IconNames.YES)
    if MenueSettings == 1:
        basic.show_icon(IconNames.HOUSE)
    if MenueSettings == 2:
        basic.show_icon(IconNames.ARROW_EAST)
    if MenueSettings == 3:
        basic.show_leds("""
            # . # . #
            . # # # .
            # # # # #
            . # # # .
            # . # . #
            """)
        basic.pause(500)
        if boOptisch == 1:
            basic.show_string("On")
        else:
            basic.show_string("Off")
    if MenueSettings == 4:
        basic.show_leds("""
            . . # . .
            . . # # .
            . . # . .
            . # # . .
            . # # . .
            """)
        basic.pause(500)
        if boAkustisch == 1:
            basic.show_string("On")
        else:
            basic.show_string("Off")
    if MenueSettings == 5:
        basic.show_leds("""
            . # # # .
            # . # . #
            # . # # #
            # . . . #
            . # # # .
            """)
        basic.pause(500)
        basic.show_string(str(ZeitMaxUnbeweglichkeit)+" min")
basic.forever(on_forever)

# pass

def on_forever2():
    if boStarteMessung == 1:
        MesseBeschleunigungXYZSt()
        # Dauer in Minuten
        Zeitmessung(ZeitMaxUnbeweglichkeit)
        AlarmAusgeben()
basic.forever(on_forever2)
