import time
from machine import Pin, Timer
import utime
from picographics import PicoGraphics, DISPLAY_INKY_PACK
from pimoroni import Button
from retrieve_file import retrieveTextAsList

graphics = PicoGraphics(DISPLAY_INKY_PACK)
WIDTH, HEIGHT = graphics.get_bounds()

button_a = machine.Pin(12, machine.Pin.IN, pull=machine.Pin.PULL_UP)
button_b = machine.Pin(13, machine.Pin.IN, pull=machine.Pin.PULL_UP)
button_c = machine.Pin(14, machine.Pin.IN, pull=machine.Pin.PULL_UP)

DEBOUNCE_TIME = 500
timer = Timer(-1)
button_pressed = False


list, page_count = retrieveTextAsList('pyramus_monologue.txt')



print(list)
curr_page = 1


def displayNav():
    '''
    adds navigation symbols next to buttons
    '''
    graphics.set_pen(3)
    graphics.rectangle(WIDTH - 30, 15, 30, 18) #for the A button, a box to house the up arrow
    graphics.rectangle(WIDTH - 30, HEIGHT - 30, 30, 18) # for the C button, a box to house the down arrow
    
    graphics.set_pen(16)
    graphics.text("/\\", WIDTH - 22, 17, scale = 2) #this creates an arrow pointing up near the A button
    graphics.text('\\/', WIDTH - 22, HEIGHT - 28, scale = 2) #this creates an arrow pointing down near the B button

def displayPageCount(p = 1):
    graphics.set_pen(16)
    graphics.rectangle(WIDTH - 30, int(HEIGHT/2) - 10, 30, 20)
    graphics.set_pen(0)
    graphics.text(str(p)+'/'+str(page_count), WIDTH - 30, int(HEIGHT/2) - 10, wordwrap= 30, scale = 2)


def updatePage(p):
    graphics.set_update_speed(3)
    text = list[p - 1]
    
    graphics.set_pen(16) 
    graphics.clear()
    displayNav()
    graphics.update() #clear first so less shadow from previous page
    
    
    displayPageCount(p)
    graphics.set_pen(0)
    graphics.text(text, 10, 10, wordwrap=WIDTH - 40, scale = 2)
    graphics.update()
    print(text)
    
def activateButton(pin):
    '''
    handles what the button presses do, after checking its not a debounce
    button A: scrolls up
    button B: goes back to start
    button C: scrolls down
    '''
    global curr_page
    inc = 0
    if pin == button_a:
        if curr_page <= 1: return
        curr_page -= 1
    if pin == button_b:
        curr_page = 1
    if pin == button_c:
        if curr_page >= len(list): return
        curr_page += 1
    
    time.sleep(1)
    updatePage(curr_page)
    
    print("current page = "+str(curr_page) )

def debounceCheck(t, pin): #checks that button has not been pressed in a row, currently less than 0.5 s away from the last press
    global button_pressed
    if not button_pressed: return
    
    print("Button pressed!")
    activateButton(pin)
    button_pressed = False 

def button(pin): #when button is pressed
    global button_pressed
    button_pressed = True
    timer.init(mode=Timer.ONE_SHOT, period=DEBOUNCE_TIME, callback=lambda t: debounceCheck(t, pin))

def setup(): #set up screen with nav buttons and text!
    graphics.set_pen(16)
    graphics.clear()
    displayNav()
    updatePage(1)


setup()

button_a.irq(trigger=machine.Pin.IRQ_FALLING, handler=button )
button_b.irq(trigger=machine.Pin.IRQ_FALLING, handler=button )
button_c.irq(trigger=machine.Pin.IRQ_FALLING, handler=button )

