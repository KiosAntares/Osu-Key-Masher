import pygame
from pynput.keyboard import Key, Listener
import win32api
import win32con
import win32gui
import sys
import configparser

screen = None

transparent = (10,10,10)
size = ()
framerate = 60

keys = {
}

frames = {
    'left':  None,
    'right':  None,
    0:      transparent,
        }


def parse_cfg():
    global transparent
    global size
    global framerate
    global keys

    # get resolution components
    config = configparser.ConfigParser()
    config.read('config.cfg')
    sizex = int(config['PROGRAM']['resolution_x'])
    sizey = int(config['PROGRAM']['resolution_y'])
    size = (sizex, sizey)

    # get transparency colour for chroma key
    rgb = config['PROGRAM']['transparency_rgb'].lstrip('#')
    transparent = tuple(int(rgb[i:i+2], 16) for i in (0,2,4))

    # get framerate
    framerate = int(config['PROGRAM']['target_framerate'])

    # setup keys
    for key in config['KEYS']:
        keys[f"'{config['KEYS'][key]}'"] = key


def on_press(key):
    pos = (0,0)
    global screen
    if str(key) in keys:
        screen.fill(transparent)
        screen.blit(frames[keys[str(key)]], pos)
        pygame.display.update()

def on_release(key):
    pos = (0,0)
    global screen
    screen.fill(transparent)
    screen.blit(frames[0], pos)
    pygame.display.update()
 
# define a main function
def main():
    global screen
    global size

    # load up configs
    parse_cfg()

    print('Program starting...')
    print('Settings are:')
    print(f'\tResolution: {size[0]}x{size[1]}')
    print(f'\tFramerate is: {framerate}')
    print(f'\tTransparency chroma RGB is: RGB{transparent}')
    print('Keys are:')
    for key in keys:
        print(f'\t{keys[key]}:{key}')

    # initialize the pygame module
    pygame.init()

    #preload and scale images
    pic = pygame.image.load('images/left.png')
    frames['left'] = pygame.transform.scale(pic, size)
    pic = pygame.image.load('images/right.png')
    frames['right'] = pygame.transform.scale(pic, size)
    pic = pygame.image.load('images/none.png')
    frames[0] = pygame.transform.scale(pic, size)

    
    # create a surface on screen that has the defined size
    screen =  pygame.display.set_mode(size)
    screen.fill(transparent)  # Transparent background
    pygame.display.update()

    # make background transparent for compositing in windows
    hwnd = pygame.display.get_wm_info()["window"]
    win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE,
                       win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE) | win32con.WS_EX_LAYERED)
    win32gui.SetLayeredWindowAttributes(hwnd, win32api.RGB(*transparent), 0, win32con.LWA_COLORKEY)

    on_release(None)

    #Add and start key listener
    listener = Listener(on_press=on_press, on_release=on_release)
    listener.start()

    #Make limiting clock
    clock = pygame.time.Clock()
   

    # define a variable to control the main loop
    running = True
     
    # main loop
    while running:
        # event handling, gets all event from the event queue
        for event in pygame.event.get():
            # only do something if the event is of type QUIT
            if event.type == pygame.QUIT:
                # change the value to False, to exit the main loop
                pygame.quit()
                sys.exit()

        clock.tick(framerate)

    listener.join()
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()
