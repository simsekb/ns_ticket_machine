from tkinter import *
import time
import XML as xml
import math

huidigStation = 'tiel' #station waar we op beginnen
window = Tk()
window.title("NS Kaartautomaat")

screenX, screenY = 700, 470
window.geometry('%ix%i' % (screenX, screenY))
#window.iconbitmap("favicon.ico")

backgroundColor = '#%02x%02x%02x' % (247, 206, 78)
NSBlueColor = '#%02x%02x%02x' % (6, 37, 109)

toetsenbord = ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '<-', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', 'enter', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', '-']

window.configure(background=backgroundColor)

bottom_rect = Label(background=NSBlueColor, width=80, height=4)
bottom_rect.place(x=0, y=445)

current = time.strftime("%H:%M:%S")
tijdLabel = Label(background=NSBlueColor, foreground=backgroundColor, text=current)

#beginscherm
welkomLabel = Label(background=backgroundColor, foreground=NSBlueColor, text='Welkom bij NS', font=('', 40, ''))
geenOV_button = Button(text="Ik heb geen OV-chipkaart", highlightbackground=backgroundColor, state=DISABLED)
buitenland_button = Button(text="Ik wil naar het buitenland", highlightbackground=backgroundColor, state=DISABLED)

locatieModus = 0 #0: zoeken in XML, 1: zoeken in station

def locatiemodusPressed(): #when pressing the locationbutton to change searching mode
    global locatieModus
    #0: zoeken in stations, 1: zoeken vanuit stations
    if(locatieModus):
        locatiemodusButton['text'] = 'Zoeken in stations..'
        locatieModus = 0
    else:
        locatiemodusButton['text'] = 'Zoeken vanuit stations..'
        locatieModus = 1

def clearXML(): #clear the locations text
    outputXML['text'] = 'Tijd\tStationsnaam\tPerron\n'

#locatiescherm
locatieschermLabel = Label(background=backgroundColor, foreground=NSBlueColor, text='Actuele vertrektijden', font=('', 40, ''))
locatiemodusButton = Button(highlightbackground=backgroundColor, text="Zoeken in stations....", command=locatiemodusPressed)
invoerVeld = Entry(width=30)
paginaDescriptie = Label(background=backgroundColor, foreground=NSBlueColor, text="Aantal pagina's")
huidigStationLabel = Label(background=backgroundColor, foreground=NSBlueColor)

actueleVertrektijden = xml.deActueleVertrektijdenVanNS(huidigStation) #inladen van XML stations via API

def updateTime(): #adjust time each second
    current = time.strftime("%H:%M:%S")
    tijdLabel.configure(text=current)
    window.after(1000, updateTime)

def getButtonAmount(): #calculate amount of buttons to be displayed on location screen
    return int(math.ceil(len(actueleVertrektijden) / maxAmountPP))

maxAmountPP = 6 #max amount locations per page (pagination)
amountPaginationButton = getButtonAmount() #get amount of pagination buttons based on XML API output

for i in range(0, getButtonAmount()):
    outputXML = Label(background=backgroundColor, foreground=NSBlueColor, justify=LEFT, font=('', 16, ''))

def fillLocations(vertrektijden): #gets runned once at beginning
    #print('binner: ', len(vertrektijden))
    createPaginationButtons()
    clearXML()
    #print(len(vertrektijden))

    if(len(vertrektijden) <= maxAmountPP):
        maxAmount = len(vertrektijden)
    else:
        maxAmount = maxAmountPP

    if(len(vertrektijden) > 0): #if results are found display them
        for i in range(0, maxAmount): #len(actueleVertrektijden)
                outputXML['text'] += vertrektijden[i] + '\n'
    else: #no results are found
        outputXML['text'] = 'Er zijn geen resultaten gevonden.'

def buttonPressed(buttonId): #argument; page number each time button gets pressed
    startWith = buttonId * maxAmountPP
    endWith = startWith + maxAmountPP
    maxVertrektijden = len(actueleVertrektijden)
    if(endWith > maxVertrektijden):
        endWith = maxVertrektijden

    clearXML()
    #print(startWith, ' ', endWith)
    for i in range(startWith, endWith):
        outputXML['text'] += actueleVertrektijden[i] + '\n'

def createPaginationButtons():
    for i in range(0, getButtonAmount()):
        pageNumber = i+1
        paginationButton = Button(highlightbackground=backgroundColor, command=lambda pageNumber=i: buttonPressed(pageNumber))
        paginationButton.place(x=280 + (i * 40), y=250)
        paginationButton['text'] = (pageNumber)

def updateLocations():
    global actueleVertrektijden
    if(len(invoerVeld.get()) == 0): #invulbalk leeg
        actueleVertrektijden = xml.deActueleVertrektijdenVanNS(huidigStation)

    clearXML()
    vertrektijden = []
    #print('lengte:', len(actueleVertrektijden))
    '''for j in range(0, len(actueleVertrektijden)):
        print(actueleVertrektijden[j])'''

    for i in range(0, len(actueleVertrektijden)):
        #print('i:', i)
        #print('actuele i', actueleVertrektijden[i])
        #print(str(invoerVeld.get()).lower(), '', str(actueleVertrektijden[i]).lower())

        if(str(invoerVeld.get()).lower() in str(actueleVertrektijden[i]).lower()): #locatie gevonden in XML lijst
            #print(str(invoerVeld.get()).lower(), '', str(actueleVertrektijden[i]).lower())
            vertrektijden.append(actueleVertrektijden[i])
            #print('result: ', actueleVertrektijden[i])

    actueleVertrektijden = xml.deActueleVertrektijdenVanNS(huidigStation)

    fillLocations(vertrektijden)

def insertText(invoerText):
    #print(invoerText)
    global actueleVertrektijden
    invoer = invoerVeld.get()
    textPosition = len(invoer)
    if(invoerText == '<-'): #backspace
        #print('ja')
        laatsteLetter = len(invoer)-1
        invoerVeld.delete(laatsteLetter)
    elif(invoerText == 'space'):
        #print('juist')
        invoerVeld.insert(textPosition, ' ')
    elif(invoerText == 'enter'):
        if(locatieModus): #XML
            global huidigStation
            lowercaseInvoer = str(invoer).lower()
            actueleVertrektijden = xml.deActueleVertrektijdenVanNS(lowercaseInvoer)
            huidigStationLabel.configure(text='U bevind zich op station: ' + lowercaseInvoer)
            huidigStation = lowercaseInvoer
            fillLocations(actueleVertrektijden)
        else: #stations
            updateLocations()
    else: #vul in input
        #print('text to invoer:', invoerVeld.get())
        invoerVeld.insert(textPosition, invoerText)

#toetsenbord
def drawToetsenbord(toetsenbord):
    for i in range(0, 11):
        #print('Toetsenbord:', toetsenbord[i])
        Button(text=toetsenbord[i], highlightbackground=backgroundColor, command=lambda index=i: insertText(toetsenbord[index])).place(x=130 + (i * 45), y=320)
        #lambda index=i is een truucje wat ervoor zorgt dat elke button een aparte functie heeft, anders krijgt elke knop de allerlaatste command mee
    for i in range(11, 21):
        #print('Toetsenbord:', toetsenbord[i])
        Button(text=toetsenbord[i], highlightbackground=backgroundColor, command=lambda index=i: insertText(toetsenbord[index])).place(x=110 + ((i-10) * 45), y=350)

    for i in range(21, len(toetsenbord)):
        #print('Toetsenbord:', toetsenbord[i])
        Button(text=toetsenbord[i], highlightbackground=backgroundColor, command=lambda index=i: insertText(toetsenbord[index])).place(x=130 + ((i-20) * 45), y=380)

    Button(highlightbackground=backgroundColor, width=30, command=lambda: insertText('space')).place(x=200, y=410)

#keuzescherm
def locatieScherm():
    beginScherm(True)
    locatieschermLabel.place(x=180, y=0)
    locatiemodusButton.place(x=130, y=280)
    paginaDescriptie.place(x=150, y=253)
    invoerVeld.place(x=320, y=280)
    invoerVeld.focus()
    outputXML.place(x=225, y=60)
    drawToetsenbord(toetsenbord)
    fillLocations(actueleVertrektijden)
    #createPaginationButtons()
    huidigStationLabel.place(x=250, y=230)
    huidigStationLabel.configure(text='U bevind zich op station: ' + huidigStation)

routeplanner_button = Button(text="Routeplanner", highlightbackground=backgroundColor, command=locatieScherm)

def beginScherm(destroy):
    if (destroy):
        welkomLabel.destroy()
        geenOV_button.destroy()
        buitenland_button.destroy()
        routeplanner_button.destroy()
    else:
        welkomLabel.place(x=220, y=100)
        geenOV_button.place(x=110, y=320)
        buitenland_button.place(x=300, y=320)
        routeplanner_button.place(x=490, y=320)
        tijdLabel.place(x=5, y=445)

beginScherm(False)
updateTime()
window.mainloop()