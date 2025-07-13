import threading
from gdi import (
    TunnelEffect, 
    ErrorIcons, 
    SuperMelt, 
    VoidEffect, 
    HellEffect, 
    PanScreen, 
    InvertEffect, 
    SinesEffect, 
    RotateTunnel, 
    RandomImage, 
    Smelt, 
    SwipeScreen, 
    RasterHorizontal)

###
stop_event = threading.Event()  
###

def starttunnel():
    effect = TunnelEffect(stop_event=stop_event)
    thread = threading.Thread(target=effect.run)
    thread.start()
    return thread

def starticonscursor():
    effect = ErrorIcons(stop_event=stop_event)
    thread = threading.Thread(target=effect.run)
    thread.start()
    return thread

def startmelt():
    effect = SuperMelt(stop_event=stop_event)
    thread = threading.Thread(target=effect.run)
    thread.start()
    return thread

def startvoid():
    effect = VoidEffect(stop_event=stop_event)
    thread = threading.Thread(target=effect.run)
    thread.start()
    return thread

def starterrors():
    effect = ErrorIcons(stop_event=stop_event)
    thread = threading.Thread(target=effect.run)
    thread.start()
    return thread

def starthell():
    effect = HellEffect(stop_event=stop_event)
    thread = threading.Thread(target=effect.run)
    thread.start()
    return thread

def startpanscreen():
    effect = PanScreen(stop_event=stop_event)
    thread = threading.Thread(target=effect.run)
    thread.start()
    return thread

def startinvert():
    effect = InvertEffect(stop_event=stop_event)
    thread = threading.Thread(target=effect.run)
    thread.start()
    return thread

def startsines():
    effect = SinesEffect(stop_event=stop_event)
    thread = threading.Thread(target=effect.run)
    thread.start()
    return thread

def startrottun():
    effect = RotateTunnel(stop_event=stop_event)
    thread = threading.Thread(target=effect.run)
    thread.start()
    return thread

def startdrawimages():
    image_paths = ["image1.png", "image2.png"]  
    effect = RandomImage(image_paths=image_paths, stop_event=stop_event)
    thread = threading.Thread(target=effect.run)
    thread.start()
    return thread

def startsmelt():
    effect = Smelt(stop_event=stop_event)
    thread = threading.Thread(target=effect.run)
    thread.start()
    return thread

def startswipescreen():
    effect = SwipeScreen(stop_event=stop_event)
    thread = threading.Thread(target=effect.run)
    thread.start()
    return thread

def startrastagHori():
    effect = RasterHorizontal(stop_event=stop_event)
    thread = threading.Thread(target=effect.run)
    thread.start()
    return thread


