//  Fragen an Messungen:
//  
//  Wie sieht die Bewegung aus, wenn man steht? --> Messwertaufnahme und Auswertung
function Zeitmessung(Dauer: number) {
    
    if (boStarteMessung == 1) {
        basic.pause(1000)
        ZeitUnbewegt += 1
        if (60 * Dauer <= ZeitUnbewegt) {
            boAlarm = 1
        }
        
        if (boReset > 0 || boBewegungRegistriert > 0) {
            boAlarm = 0
            ZeitUnbewegt = 0
            boReset = 0
            boBewegungRegistriert = 0
        }
        
    }
    
}

function AlarmAusgeben() {
    
    if (boAlarm > 0) {
        //  pass
        if (boAkustisch > 0) {
            music.playMelody("C5 - C5 - C5 - C5 C5 ", 240)
        }
        
        //  , MelodyOptions.ONCE_IN_BACKGROUND)
        if (boOptisch > 0) {
            basic.setLedColor(0xff0000)
            basic.pause(200)
            basic.setLedColor(0x0000ff)
            basic.pause(200)
        }
        
    } else {
        //  pass
        music.stopMelody(MelodyStopOptions.All)
    }
    
}

//  pass
function BewegungErkennen() {
    
    
    //  Neuer Block (ArrayListe) wird ausgewertet
    if (zeiger_Arrays == 1) {
        basic.setLedColor(0xff00ff)
        boBewegungRegistriert = 0
        ZaehlerBewegungX = 0
    }
    
    //  Wurde eine Bewegung festgestellt?
    if (Math.abs(Mittelwert_X - Last_x) > SchwellwertBewegung) {
        ZaehlerBewegungX += 1
        serial.writeValue("Zähler+", ZaehlerBewegungX)
    } else if (Math.abs(Mittelwert_Y - Last_y) > SchwellwertBewegung) {
        ZaehlerBewegungX += 1
    } else if (Math.abs(Mittelwert_Z - Last_z) > SchwellwertBewegung) {
        ZaehlerBewegungX += 1
    }
    
    if (ZaehlerBewegungX > HaeufigkeitBewegungsErkannt) {
        boBewegungRegistriert = 1
        basic.setLedColor(0x00ff00)
    }
    
    Last_x = Mittelwert_X
    Last_y = Mittelwert_Y
    Last_z = Mittelwert_Z
}

//  Fehlerquellen:
//  
//  Erschütterungen (Zugfahrt)
//  
//  Calliope fällt runter
//  
//  Calliope wird zur Seite gelegt und nicht bewegt.
function MesseBeschleunigungXYZSt() {
    
    // global WertelisteX ,WertelisteY, WertelisteZ, WertelisteStaerke, 
    ArrayGroesse
    for (let index = 0; index < 20; index++) {
        Mittelwert_X = (input.acceleration(Dimension.X) + 19 * Mittelwert_X) / 20
        Mittelwert_Y = (input.acceleration(Dimension.Y) + 19 * Mittelwert_Y) / 20
        Mittelwert_Z = (input.acceleration(Dimension.Z) + 19 * Mittelwert_Z) / 20
        Mittelwert_Staerke = (input.acceleration(Dimension.Strength) + 19 * Mittelwert_Staerke) / 20
        basic.pause(50)
    }
    if (WertelisteX.length < ArrayGroesse) {
        WertelisteX.push(Mittelwert_X)
        WertelisteY.push(Mittelwert_Y)
        WertelisteZ.push(Mittelwert_Z)
        WertelisteStaerke.push(Mittelwert_Staerke)
        zeiger_Arrays = zeiger_Arrays + 1
    } else {
        if (boArrayVoll == 0) {
            music.playTone(262, music.beat(BeatFraction.Whole))
            boArrayVoll = 1
        }
        
        if (zeiger_Arrays >= ArrayGroesse) {
            zeiger_Arrays = 0
        } else {
            zeiger_Arrays = zeiger_Arrays + 1
        }
        
        WertelisteX[zeiger_Arrays] = Mittelwert_X
        WertelisteY[zeiger_Arrays] = Mittelwert_Y
        WertelisteZ[zeiger_Arrays] = Mittelwert_Z
        WertelisteStaerke[zeiger_Arrays] = Mittelwert_Staerke
    }
    
    boToggle = 1 - boToggle
    BewegungErkennen()
}

//  Programmablauf:
//  
//  Zu Beginn: Warten 100ms? Danach Bewegungsmesser starten
//  
//  Zeit starten, in der Bewegungsregistration stattfindet.
//  
//  Wenn keine Bewegung erkannt wurde (innerhalb der Zeit), dann Ausgabe
//  
//  Reset der Ausgabe, wenn wieder Bewegung registriert wurde oder manueller Reset
input.onButtonPressed(Button.A, function on_button_pressed_a() {
    
    if (MenueSettings == 0) {
        boStarteMessung = 1
        boReset = 1
    } else if (MenueSettings == 1) {
        MenueSettings = 0
    } else if (MenueSettings == 2) {
        MessdatenAusgebenSeriell()
    } else if (MenueSettings == 3) {
        boOptisch = 1 - boOptisch
    } else if (MenueSettings == 4) {
        boAkustisch = 1 - boAkustisch
    } else {
        
    }
    
})
input.onButtonPressed(Button.B, function on_button_pressed_b() {
    
    boStarteMessung = 0
    boReset = 1
    basic.setLedColor(0x000000)
    if (MenueSettings == 0) {
        MenueSettings = 1
    } else {
        MenueSettings += 1
    }
    
    if (MenueSettings == 5) {
        MenueSettings = 1
    }
    
})
function MessdatenAusgebenSeriell() {
    
    boTransfer = 1
    Zeiger_Senden = zeiger_Arrays
    serial.writeLine("Ausgabe")
    Index = 0
    while (Index <= WertelisteX.length - 1) {
        led.toggle(5, 5)
        serial.writeNumber(WertelisteX[Zeiger_Senden])
        serial.writeString(";")
        serial.writeNumber(WertelisteY[Zeiger_Senden])
        serial.writeString(";")
        serial.writeNumber(WertelisteZ[Zeiger_Senden])
        serial.writeString(";")
        serial.writeNumber(WertelisteStaerke[Zeiger_Senden])
        serial.writeLine("")
        Index += 1
        Zeiger_Senden += 1
        if (Zeiger_Senden >= WertelisteX.length) {
            Zeiger_Senden = 0
        }
        
    }
    music.playTone(349, music.beat(BeatFraction.Double))
}

let Index = 0
let Zeiger_Senden = 0
let boTransfer = 0
let boToggle = 0
let boArrayVoll = 0
let WertelisteStaerke : number[] = []
let WertelisteZ : number[] = []
let WertelisteY : number[] = []
let WertelisteX : number[] = []
let Last_z = 0
let Mittelwert_Z = 0
let Last_y = 0
let Mittelwert_Y = 0
let Last_x = 0
let Mittelwert_X = 0
let zeiger_Arrays = 0
let boBewegungRegistriert = 0
let boReset = 0
let boAlarm = 0
let ZeitUnbewegt = 0
let boStarteMessung = 0
let SchwellwertBewegung = 0
let HaeufigkeitBewegungsErkannt = 0
let ArrayGroesse = 0
let boAkustisch = 0
let boOptisch = 0
let Mittelwert_Staerke = 0
let ZaehlerBewegungX = 0
let AnzeigeEbene = 0
boOptisch = 1
boAkustisch = 1
serial.setBaudRate(BaudRate.BaudRate115200)
ArrayGroesse = 10
//  Dauer in Minuten
let ZeitMaxUnbeweglichkeit = 1
//  Dauer in Minuten
HaeufigkeitBewegungsErkannt = 5
SchwellwertBewegung = 100
let MenueSettings = 0
let MenueSettings2 = 0
basic.forever(function on_forever() {
    
    if (boStarteMessung == 1) {
        if (boToggle) {
            basic.showIcon(IconNames.Heart)
        } else {
            basic.showIcon(IconNames.SmallHeart)
        }
        
    } else if (boTransfer == 1) {
        basic.showIcon(IconNames.ArrowEast)
    } else if (MenueSettings == 0) {
        basic.showIcon(IconNames.Yes)
    }
    
    if (MenueSettings == 1) {
        basic.showIcon(IconNames.House)
    }
    
    if (MenueSettings == 2) {
        basic.showIcon(IconNames.ArrowEast)
    }
    
    if (MenueSettings == 3) {
        basic.showLeds(`
            # . # . #
            . # # # .
            # # # # #
            . # # # .
            # . # . #
            `)
        basic.pause(500)
        if (boOptisch == 1) {
            basic.showString("On")
        } else {
            basic.showString("Off")
        }
        
    }
    
    if (MenueSettings == 4) {
        basic.showLeds(`
            . . # . .
            . . # # .
            . . # . .
            . # # . .
            . # # . .
            `)
        basic.pause(500)
        if (boAkustisch == 1) {
            basic.showString("On")
        } else {
            basic.showString("Off")
        }
        
    }
    
})
//  pass
basic.forever(function on_forever2() {
    if (boStarteMessung == 1) {
        MesseBeschleunigungXYZSt()
        //  Dauer in Minuten
        Zeitmessung(ZeitMaxUnbeweglichkeit)
        AlarmAusgeben()
    }
    
})
