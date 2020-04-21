import pygame
import os

#Initializes pygame and the joystick capabilities.
pygame.init()
pygame.joystick.init()

#Main loop.
run = True
while run:
    os.system('cls')
    #Quit when 'x' is pressed if there is a pygame window open.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = True

    #Finds joysticks (gamepads) that are connected to the computer.
    #Can find Playstation 4, XBox One, and Switch Pro Controllers, but will only
    #display values for the Playstation 4 controller.
    for i in range(pygame.joystick.get_count()):
        gamepad = pygame.joystick.Joystick(i)
        gamepad.init()

        #Finds number of axes on the gamepad. Displays values of axes.
        #Triggers count as axes as well. Value ranges from -1 to 1.
        axes = gamepad.get_numaxes()
        for i in range(axes):
            axis = gamepad.get_axis(i)
            print(axis)

        #Finds number of buttons on gamepad. Displays values of buttons (0 or 1).
        buttons = gamepad.get_numbuttons()
        for i in range(buttons):
            button = gamepad.get_button(i)
            print(button)

        #Finds number of hats(D-Pads). Displays values of hats.
        hats = gamepad.get_numhats()
        for i in range(hats):
            hat = gamepad.get_hat(i)
            print(hat)
    print('Exit with Ctrl + C for now')
