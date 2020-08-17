from time import strftime
from time import sleep
from tkinter import *
from sense_hat import SenseHat
import time
from pygame import mixer

sense = SenseHat() #declaring sense hat

#Setting sense hat background color
r = 30
g = 60
b = 60

color = (r, g, b)

sense.clear(color)  # passing in an RGB tuple

#----
global i
global runsnooze
global stopsnooze
stopsnooze = 0
i = 1
runsnooze = 0

def display():
    
    global hmsnooze #hour/minute snooze time
    global chmsnooze #change in hour/mnute snooze time
    global stopsnooze

    hmsnooze = 0
    chmsnooze = 0
    work = 1 #setting the wake-up-time safeguard
    close = 0 #setting/resetting the while loop break variable
    
    conversion() #calling conversion to get the variable in the correct form for a comparison to be made, specifically in the 'waking up' and 'safeguard' sections
    
    while 1==1:
       
        print (hmat) #printing the designated wakeup time for de-bugging purposes
        print (chmat) #printing the designated safety time for debugging purposes
        print(time.strftime('%H:%M')) 
        sense.clear(color)  #setting wait screen of Sense Hat again

        time.sleep(1) #delay between sense hat scrolling for readability purposes
    
        sense.show_message(time.strftime('%H:%M.%S'), back_colour=[r,g,b]) #showing the time (including seconds)
        
        #waking up
        if time.strftime('%H:%M') == hmat and work==1 or time.strftime('%H:%M') == hmsnooze and work==1:
            print('it worked')
            alarm()
            work = work + 1 #safeguard so song only runs through once
        #----
            
        #safeguard
        if time.strftime('%H:%M') == chmat or time.strftime('%H:%M') == chmsnooze:
            print ("work reset")
            work = 1 #re-setting the safeguard because there now is no risk of song not runnnng through correctly
            if runsnooze >= 1:
                chmsnooze = hsnooze+':'+csnoozemt #correct format
                print(chmsnooze)
        #----
       
            
        #for a change in wake-up times
        for event in sense.stick.get_events():
            if event.direction == 'down': #if the joysticck is held in a backwards position the current while loop will break
                print('It should have worked')
                close = 1 #this is the variable that allows the while loop to break, has t be varable or else for loop would break
            if event.direction == 'up':
                stopsnooze = 1
                print('stop snoozing')
                
        if close == 1: #if statement that breaks while loop to go back into acs or alarm clock settings
            break
        
       
        #---
     
        
        
def alarm(): # contains the alarm sound and stoping of alarm
    global breakss
    global runsnooze
    global snoozemt #snooze minute time
    global csnoozemt #change in snooze minute-time
    global hmsnooze #hour/minute snooze time
    global chmsnooze #change in hour/mnute snooze time
    global hsnooze
    global stopsnooze
    breakss = 0
    global i
    mixer.init() #initializing the audio player
    sound = mixer.Sound('rooster-1.wav')#audio file to wake up to

    while True:#while loop continuosuly plays ound until shake detector is triggerd 
        acceleration = sense.get_accelerometer_raw()
        x = acceleration['x']
        y = acceleration['y']
        z = acceleration['z']

        x = abs(x)
        y = abs(y)
        z = abs(z)
       
        
        #to stop snooze cycle
        if stopsnooze == 1:
            runsnooze = 0
            breakss = 1 #breakss (breakstop snooze) exits this while loop by using an if statement down below
            snoozemt = 0
            csnoozemt = 0
            hmsnooze = 0
            chmsnooze = 0
            hsnooze = 0
            stopsnooze = 0
            i=0
            print('stop snoozing')
            break
            
         
        if x > 1.05 or y > 1.05 or z > 1.05: #shake detector for snooze
          runsnooze += 1 #this variable will run snooze until it is reset by the stopping of the snooze cyclr
          breakss = 1
          i = 1
          
        while i == 1:
            if runsnooze >= 1:
                snoozeconversion()
            i = 0    
        if breakss == 1:
            breakss = 0 #re-setting break stop snooze
            break
                
        #----
        sound.play() #playing the sound
        sleep(3) #letting the sound run through with slight pause in-between
        
        
      



def window(): #controls tkinter window
    
    #Variable naming key
        #acs = alarm clock settings
        #hat = hour alarm time
        #mat = minute alarm time
        #s = scale
        #c = change
        #v = variable
        #m = minute
        #h = hour
    
    hat = 0 #0 is placeholder value
    mat = 0 #0 is placeholder value
    
    acs = Tk()

    def ch(): #called by button to get variable from scale
        global hat
        hat = shv.get() #getting data from the scale and setting it to hour alarm time
    def cm(): #called by button to get variable from scale
        global mat
        mat = smv.get() #getting data from the scale ans setting it to minute alarm time
        
    shv = DoubleVar()
    smv = DoubleVar()
    
    shat = Scale(acs, from_ = 0, to = 23, length=190, orient = HORIZONTAL, resolution=1, variable = shv) #shv = scale hour variable
    smat = Scale(acs, from_ = 0, to = 59, length=190, orient = HORIZONTAL, resolution=1, variable = smv) #smv = scale minute variable

    # this wil create a label widget for the scales
    l1 = Label(acs, text='Hour: (Integer between 0&23)')
    l2 = Label(acs, text='Minute: (Integer between 0&59')

    #getting data from scales through button click
    buttonh = Button(acs, text="Set hour", command=ch)
    buttonm = Button(acs, text="Set minute", command=cm)

    #starts the functionality of alarm clock
    disbutton = Button(acs, text="show clock", command=display) #display command shows the display and runs the actual clock

    #organizing the widget

    shat.grid(row = 2, column = 0, sticky = N, pady = 10)
    smat.grid(row = 4, column = 0, sticky = N, pady = 10)

    #grid method to arrange labels in respective 
    # rows and columns as specified
    l1.grid(row = 1, column = 0, sticky = N, pady = 10) 
    l2.grid(row = 3, column = 0, sticky = N, pady = 10)
    buttonh.grid(row = 2 , column = 1,pady = 10)
    buttonm.grid(row = 4 , column = 1,pady = 10)
    disbutton.grid(row = 5, column = 0, pady = 10)



    acs.mainloop() #closing the tkinter window

    sense.clear() #clearing the sense hat




def conversion():
    #declaring global variables
    global hat #hour alarm time
    global mat #minute alarm time
    global hmat #hour/minute time (this is in a format that can be compared to time.strftime(%H%M))
    global chmat #changed gour minute alarm time (used to make sure alarm doesnt run through more than it is supposed to)
    
    #correctingg data types
    hat = float(hat)
    hat = int(hat)
    hat = str(hat)
    mat = int(mat)
    #----
    
    if mat <= 9: #this if statement continues putting the minute tim in the correct format
        mat = "0"+ str(mat)
        print (mat)

    mat = str(mat)
    hmat = hat+':'+ mat #correct format
    
    #correcting data types
    mat = float(mat) 
    mat = int(mat)
    #----
    
    cmat = mat + 1
    if cmat <= 9: #this does the same thing as the if statement above with a different variable
        cmat = "0"+ str(cmat)
        print (cmat)
    cmat =str(cmat)
    chmat = hat+':'+cmat #correct format

    
    


def snoozeconversion(): #snooze conversion makes comparible snooze-time variables much like the regular conversion function
    #declaring global variables
    global hat #hour alarm time
    global mat #minute alarm time
    global hmat #hour/minute time (this is in a format that can be compared to time.strftime(%H%M))
    global chmat#changed gour minute alarm time (used to make sure alarm doesnt run through more than it is supposed to)
    global snoozemt #snooze minute time
    global csnoozemt #change in snooze minute-time
    global hmsnooze #hour/minute snooze time
    global chmsnooze #change in hour/mnute snooze time
    global hsnooze
    #----
    
    print("I ran")
    if runsnooze >= 2:
        snoozemt = int(snoozemt) + 2
    else:
        snoozemt = int(mat) + 2

    
    hat = str(hat)
    hsnooze = hat
    csnoozemt = int(snoozemt) + 1
    
    if snoozemt >= 60:
        snoozemt = "0"
        print (snoozemt)
        
    snoozemt = int(snoozemt)
    
    if snoozemt <= 9: #this if statement continues putting the minute tim in the correct format
        snoozemt = "0"+ str(snoozemt)
        print (snoozemt)
   
            
    snoozemt = str(snoozemt)
    hmsnooze = hsnooze+':'+ snoozemt #correct format
    
    snoozemt = int(snoozemt)
    
    
    if snoozemt >= 60:
        hsnooze = int(hsnooze) + 1
        print (hsnooze)
        
   
   
    hsnooze = int(hsnooze)
    
    if hsnooze >= 24:
        hsnooze = "00"
      
    csnoozemt = int(csnoozemt)
     
    hsnooze = str(hsnooze)
    csnoozemt = int(csnoozemt)

    
    if csnoozemt <= 9: #this does the same thing as the if statement above with a different variable
        csnoozemt = "0"+ str(csnoozemt)
        print (csnoozemt)
        
    csnoozemt = str(csnoozemt)
    

    print(hmsnooze)
#Code is executed below
window()


#-
#-
#-
#-
#-

#Code graveyard
"""
#snooze function:
if rawsnooze == 1:
            if rawsnooze >=2:
                snoozem = snoozem + 7
            p1 = int(snoozeh)
            p2 = int(snoozem)+7
            snooze = str(p1) + ':'+ str(p2)
            print(snooze)
            cp1 = int(snoozeh)
            cp2 = int(snoozem)+8
            csnooze = str(cp1) + ':' + str(cp2)
            print(csnooze)




"""

        
    


