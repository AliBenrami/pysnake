import pygame
from pygame import Rect
from sys import exit
from math import sqrt, ceil
from random import randint
pygame.init()


diplaysize = width, height = (800, 800)

display = pygame.display.set_mode(diplaysize)
clock = pygame.time.Clock()

playercolor = (0, 0, 0)
applecolor = (227, 61, 45)
font = pygame.font.Font('freesansbold.ttf', 32)

grid = []
gridDim = gridwidth, gridheight = (21, 21)


numberofgrides = (gridheight * gridwidth)

areaofdisplay = width * height

gridtodisplayration = 3/4

z = int(sqrt( ((areaofdisplay)/(numberofgrides)) * (gridtodisplayration) ))

gridarea = numberofgrides * (z ** 2)

for x in range(int(gridwidth)):
    grid.append([])
    for y in range(int(gridheight)):
        objdim = Rect(x * (z)+ (1/2) * (width - (gridwidth * z)), y * (z) + (1/2) * (height - (gridheight * z)), z-1, z-1)
        grid[x].append(objdim)

def input(inputstr:str):
    return pygame.key.get_pressed()[pygame.key.key_code(inputstr)]

ApplesAte = 0

playerpos = [ceil(gridwidth/2), ceil(gridheight/2)]

snakelist = [playerpos]

ApplePos = [randint(0, gridwidth-1), randint(0, gridheight-1)]


playerdir = ["up"]

gamestate = ["start"]

debugtext = open("info", "a")
debugtext.flush()

gameoversize = (200, 100)
gameoverbuttonrect = Rect(Rect((width/2) - (gameoversize[0]/2), height/2 - (gameoversize[1]/2), gameoversize[0], gameoversize[1]))

def blitztext(x, y, txt):
    text = font.render(txt, True, (255, 0, 0))
 
    textRect = text.get_rect()

    textRect.centerx = x
    textRect.centery = y

    display.blit(text, textRect)

def gameover():
    playerdir[0] = "None"
    gamestate[0] = "gameover"

def movement():
    if not gamestate[0] == "gameover":
        if input("W") and playerdir[0] != "down":
            playerdir[0] = "up"
            return
        if input("S") and playerdir[0] != "up":
            playerdir[0] = "down"
            return
        if input("D") and playerdir[0] != "left":
            playerdir[0] = "right"
            return
        if input("A") and playerdir[0] != "right":
            playerdir[0] = "left"
            return

def moveplayer():
    templist = [0, 0]
    if playerdir[0] == "up":
        templist[1] -= 1
    elif playerdir[0] == "down":
        templist[1] += 1
    elif playerdir[0] == "right":
        templist[0] += 1
    elif playerdir[0] == "left":
        templist[0] -= 1
    return templist

done = False 
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
    if input("escape"):
        done = True

    display.fill((3, 198, 252))


    for x in range(len(grid)):
        for y in range(len(grid[x])):
            objectcolor = (255, 255, 255)
            sqrDim = grid[x][y]

            
            if playerpos in snakelist[1:] and len(snakelist) > 4:
                gameover()
            if snakelist[0][0] in [len(grid)+1, -1] or snakelist[0][1] in [len(grid[x])+1, -1] :
                gameover()

            for i in snakelist:
                if i[0] == (x) and i[1] == (y):
                    objectcolor = playercolor

            if (x) == ApplePos[0] and (y) == ApplePos[1]:
                objectcolor = applecolor
            
            if playerpos == ApplePos:
                ApplesAte += 1
                ApplePos = [randint(0, gridwidth-1), randint(0, gridheight-1)]
                while ApplePos in snakelist:
                    ApplePos = [randint(0, gridwidth-1), randint(0, gridheight-1)]
                

                roc2 = [0, 0]
                if len(snakelist) > 2:
                    roc2 = [snakelist[len(snakelist)-2][0] - snakelist[len(snakelist)-1][0], snakelist[len(snakelist)-2][1] - snakelist[len(snakelist)-1][1]]
                
                
                backdir = "None"
                if roc2[0] == 1:
                    backdir = "right"
                elif roc2[0] == -1:
                    backdir = "left"
                elif roc2[1] == 1:
                    backdir = "down"
                elif roc2[1] == -1:
                    backdir = "up"
                
                
                if backdir == "None":
                    backdir = playerdir[0]



                if backdir == "up":
                    snakelist.append([snakelist[len(snakelist)-1][0], snakelist[len(snakelist)-1][1]-1])
                elif backdir == "down":
                    snakelist.append([snakelist[len(snakelist)-1][0], snakelist[len(snakelist)-1][1]+1])
                elif backdir == "right":
                    snakelist.append([snakelist[len(snakelist)-1][0]+1, snakelist[len(snakelist)-1][1]])
                elif backdir == "left":
                    snakelist.append([snakelist[len(snakelist)-1][0]-1, snakelist[len(snakelist)-1][1]])
                else:
                    print("error could not spawn tail")
            pygame.draw.rect(display, objectcolor, sqrDim)
            pass

    if gamestate[0] == "gameover":
        pygame.draw.rect(display, (103, 125, 183), gameoverbuttonrect)
        blitztext(gameoverbuttonrect.centerx, gameoverbuttonrect.centery, "restart")
        blitztext(gameoverbuttonrect.centerx, gameoverbuttonrect.centery - 10 * (z), "gameover")
        if gameoverbuttonrect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]) and pygame.mouse.get_pressed()[0]:
            ApplesAte = 0
            playerpos = [ceil(gridwidth/2), ceil(gridheight/2)]
            snakelist = [playerpos]
            ApplePos = [randint(0, gridwidth-1), randint(0, gridheight-1)]
            playerdir = ["up"]
            gamestate = ["start"]

    snakelist.pop()
    
    movement()
    roc = moveplayer()

    snakelist.insert(0, [playerpos[0] + roc[0], playerpos[1] + roc[1]])

    playerpos = [playerpos[0] + roc[0], playerpos[1] + roc[1]]

    blitztext(40, 40, str(int( clock.get_fps() * 1000 )/1000))
    pygame.display.update()
    clock.tick(10)
    
debugtext.close()
pygame.quit()
exit(0)
