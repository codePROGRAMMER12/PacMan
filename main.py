import pygame
from time import sleep
from random import choice

level = [
    "                            ",
    "                            ",
    "----------------------------",
    "-••••••••••••--••••••••••••-",
    "-•----•-----•--•-----•----•-",
    "-*----•-----•--•-----•----*-",
    "-••••••••••••••••••••••••••-",
    "-•----•--•--------•--•----•-",
    "-•----•--•--------•--•----•-",
    "-••••••--••••--••••--••••••-",
    "------•----- -- -----•------",
    "     -•--          --•-     ",
    "------•-- ---==--- --•------",
    "      •   --    --   •      ",
    "------•-- -------- --•------",
    "     -•--          --•-     ",
    "------•-- -------- --•------",
    "-••••••••••••--••••••••••••-",
    "-•----•--•--•--•--•--•----•-",
    "-•----•--•--•--•--•--•----•-",
    "-*••--•--•--•  •--•--•--••*-",
    "---•--•--•--------•--•--•---",
    "-••••••--••••--••••--••••••-",
    "-•----------•--•----------•-",
    "-••••••••••••••••••••••••••-",
    "----------------------------",
    "                            ",
    "                            ",
]

class Pacman(pygame.sprite.Sprite):
    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.filename = filename
        self.image = pygame.image.load(self.filename).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x
        self.y = y

class Ghost(pygame.sprite.Sprite):
    def __init__(self, x, y, filename, ghost_speed):
        pygame.sprite.Sprite.__init__(self)
        self.filename = filename
        self.image = pygame.image.load(self.filename).convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))
        self.ghost_speed = ghost_speed
        self.x = x
        self.y = y
        self.sleep_time = 0


def set_level():
    lst_level = []
    for i in level:
        lst_level.append(list(i))
    return lst_level

def make_coords_list():
    coords = []

    for i, row in enumerate(level):
        if i not in [0, 1, len(level) - 1, len(level) - 2]:
            for j, element in enumerate(row):
                if level[i][j] != "-":
                    coords.append((i * 20, j * 20))
    
    return coords

pygame.init()

screen = pygame.display.set_mode((20*28,20*29))
clock = pygame.time.Clock()

pygame.display.set_icon(pygame.image.load("images/icon.png"))
pygame.display.set_caption("Pac-Man")


BLACK = (0,0,0)
BLUE = (0,0,125)
WHITE = (125,125,125)
YELLOW = (125,125,0)
RED = (125,0,0)

FPS = 60

FONT = pygame.font.Font("CrackMan.TTF", 24)

LIFE_X = (10, 50, 90)

world = set_level()
flag = True
clock = pygame.time.Clock()

coords_list = make_coords_list()
isPlayIntro = True
sound = pygame.mixer.Sound('sounds/pacman_chomp.mp3')

PACMAN_X = 20*14
PACMAN_Y = 20*20

pacman = Pacman(x = PACMAN_X, y = PACMAN_Y, filename= 'images/pacman_right.png')
red_ghost = Ghost(x = 12 * 20, y = 13 * 20, filename= 'images/ghostred.png', ghost_speed=1)
red_prev_step = (red_ghost.y, red_ghost.x)
yellow_ghost = Ghost(x = 13 * 20, y = 13 * 20, filename= 'images/ghostyellow.png', ghost_speed=1)
yellow_prev_step = (yellow_ghost.y, yellow_ghost.x)
blue_ghost = Ghost(x = 14 * 20, y = 13 * 20, filename= 'images/ghostblue.png', ghost_speed=1)
blue_prev_step = (blue_ghost.y, blue_ghost.x)
green_ghost = Ghost(x = 15 * 20, y = 13 * 20, filename= 'images/ghostgreen.png', ghost_speed=1)
green_prev_step = (green_ghost.y, green_ghost.x)

count_of_balls = 0
count_of_lifes = 3

red_do_new_step = False
yellow_do_new_step = False
green_do_new_step = False
blue_do_new_step = False

def start_step(ghost: Ghost, pacman: Pacman, prev_step: tuple, do_new_step: bool):
    global count_of_lifes
    
    if ghost.y in range(11 * 20 + 1, 14 * 20) and ghost.x in range(12 * 20, 14 * 20):
        if ghost.x == 13 * 20:
            prev_step = (ghost.y, ghost.x)
            ghost.y -= ghost.ghost_speed
            return (ghost.y, ghost.x), prev_step, do_new_step
        prev_step = (ghost.y, ghost.x)
        ghost.x += ghost.ghost_speed
        return (ghost.y, ghost.x), prev_step, do_new_step
    
    elif ghost.y in range(11 * 20 + 1, 14 * 20) and ghost.x in range(14 * 20, 16 * 20):
        if ghost.x == 14 * 20 and ghost.y:
            prev_step = (ghost.y, ghost.x)
            ghost.y -= ghost.ghost_speed
            return (ghost.y, ghost.x), prev_step, do_new_step
        prev_step = (ghost.y, ghost.x)
        ghost.x -= ghost.ghost_speed
        return (ghost.y, ghost.x), prev_step, do_new_step
    
    elif ghost.y == 11 * 20 and (ghost.x == 13 * 20 or ghost.x == 14 * 20):
        prev_step = (ghost.y, ghost.x)
        ghost.x = choice([ghost.x - ghost.ghost_speed, ghost.x + ghost.ghost_speed])
        do_new_step = True
        return (ghost.y, ghost.x), prev_step, do_new_step
    return (ghost.y, ghost.x), prev_step, do_new_step

def true_steps(ghost: Ghost, prev_step: tuple):
    test = ghost_eq_pacman(ghost, pacman, prev_step)
    if test != ():
        ghost.y, ghost.x, prev_step = test[0][0],test[0][1],test[1]
        return (ghost.y, ghost.x), prev_step
    elif (ghost.y, ghost.x + ghost.ghost_speed) == prev_step:
        test = go_left(ghost, prev_step)
        ghost.y, ghost.x, prev_step = test[0][0], test[0][1], test[1]
    elif (ghost.y, ghost.x - ghost.ghost_speed) == prev_step:
        test = go_right(ghost, prev_step)
        ghost.y, ghost.x, prev_step = test[0][0], test[0][1], test[1]
    elif (ghost.y - ghost.ghost_speed, ghost.x) == prev_step:
        test = go_down(ghost, prev_step)
        ghost.y, ghost.x, prev_step = test[0][0], test[0][1], test[1]
    elif (ghost.y + ghost.ghost_speed, ghost.x) == prev_step:
        test = go_up(ghost, prev_step)
        ghost.y, ghost.x, prev_step = test[0][0], test[0][1], test[1]
    
    return (ghost.y, ghost.x), prev_step
    

def go_left(ghost: Ghost, prev_step: tuple):
    if ghost.x % 20 != 0:
        prev_step = (ghost.y, ghost.x)
        ghost.x -= ghost.ghost_speed
        return (ghost.y, ghost.x), prev_step
    else:
        test = search_neighbors(ghost, (prev_step[0], prev_step[1] - 4))
        ghost.y, ghost.x, prev_step = test[0][0], test[0][1], test[1]
        return (ghost.y, ghost.x), prev_step

def go_right(ghost: Ghost, prev_step: tuple):
    if ghost.x % 20 != 0:
        prev_step = (ghost.y, ghost.x)
        ghost.x += ghost.ghost_speed
        return (ghost.y, ghost.x), prev_step
    else:
        test = search_neighbors(ghost, (prev_step[0], prev_step[1] + 4))
        ghost.y, ghost.x, prev_step = test[0][0], test[0][1], test[1]
        return (ghost.y, ghost.x), prev_step

def go_down(ghost: Ghost, prev_step: tuple):
    if ghost.y % 20 != 0:
        prev_step = (ghost.y, ghost.x)
        ghost.y += ghost.ghost_speed
        return (ghost.y, ghost.x), prev_step
    else:
        test = search_neighbors(ghost, (prev_step[0] + 4, prev_step[1]))
        ghost.y, ghost.x, prev_step = test[0][0], test[0][1], test[1]
        return (ghost.y, ghost.x), prev_step

def go_up(ghost: Ghost, prev_step: tuple):
    if ghost.y % 20 != 0:
        prev_step = (ghost.y, ghost.x)
        ghost.y -= ghost.ghost_speed
        return (ghost.y, ghost.x), prev_step
    else:
        test = search_neighbors(ghost, (prev_step[0] - 4, prev_step[1]))
        ghost.y, ghost.x, prev_step = test[0][0], test[0][1], test[1]
        return (ghost.y, ghost.x), prev_step

def search_neighbors(ghost: Ghost, prev_step: tuple):
    global world
    true_neighbors = []
    ghost_up = ((ghost.y - 20) // 20, ghost.x // 20)
    ghost_down = ((ghost.y + 20) // 20, ghost.x // 20)
    ghost_left = (ghost.y // 20, (ghost.x - 20) // 20)
    ghost_right = (ghost.y // 20, (ghost.x + 20) // 20)
    if ghost_left[1] != -1 and ghost_right[1] != 28:
        neighbors = [ghost_up, ghost_down, ghost_left, ghost_right] 
    else:
        if ghost_left[1] == -1:
            return (ghost.y, 27*20), (ghost.y, 27*20 + 1)
        else:
            return (ghost.y, 20), (ghost.y, 19)
        
    for neighbor in neighbors:
        if neighbor == prev_step:
            pass
        else:
            if world[neighbor[0]][neighbor[1]] != "-":
                true_neighbors.append((neighbor[0] * 20, neighbor[1] * 20))
    try:
        test_neighbor = choice(true_neighbors)
    
        if test_neighbor == (ghost.y - 20, ghost.x):
            test_neighbor = (ghost.y - ghost.ghost_speed, ghost.x)
        elif test_neighbor == (ghost.y + 20, ghost.x):
            test_neighbor = (ghost.y + ghost.ghost_speed, ghost.x)
        elif test_neighbor == (ghost.y, ghost.x - 20):
            test_neighbor = (ghost.y, ghost.x - ghost.ghost_speed)
        elif test_neighbor == (ghost.y, ghost.x + 20):
            test_neighbor = (ghost.y, ghost.x + ghost.ghost_speed)

        prev_step = (ghost.y, ghost.x)

        return test_neighbor, prev_step
    except:
        return (ghost.y, ghost.x), prev_step


def ghost_eq_pacman(ghost: Ghost, pacman: Pacman, prev_step: tuple):
    global count_of_lifes
    if ghost.y == pacman.y and pacman.x == ghost.x: 
        count_of_lifes -= 1

        pacman.y = PACMAN_Y
        pacman.x = PACMAN_X
        test = search_neighbors(ghost, prev_step)
        ghost.y, ghost.x, prev_step, test[0][0], test[0][1], test[1]
        return (ghost.y, ghost.x), prev_step
    
    return ()

def scream():
    global pacman, red_ghost, blue_ghost, yellow_ghost, green_ghost, red_do_new_step, yellow_do_new_step, green_do_new_step, blue_do_new_step

    if pacman.y in range(red_ghost.y - 10, red_ghost.y + 11) and pacman.x in range(red_ghost.x - 10, red_ghost.x + 11):
        pygame.mixer.music.load('sounds/pacman_eatghost.wav')
        pygame.mixer.music.play()
        red_ghost.x, red_ghost.y = 12 * 20, 13 * 20
        red_ghost.image = pygame.image.load("images/ghostgogoaway.png").convert_alpha()
        red_ghost.sleep_time = 120
        red_do_new_step = False
    
    elif pacman.y in range(yellow_ghost.y - 10, yellow_ghost.y + 11) and pacman.x in range(yellow_ghost.x - 10, yellow_ghost.x + 11):
        pygame.mixer.music.load('sounds/pacman_eatghost.wav')
        pygame.mixer.music.play()
        yellow_ghost.x, yellow_ghost.y = 13 * 20, 13 * 20
        yellow_ghost.image = pygame.image.load("images/ghostgogoaway.png").convert_alpha()
        yellow_ghost.sleep_time = 120
        yellow_do_new_step = False
    
    elif pacman.y in range(blue_ghost.y - 10, blue_ghost.y + 11) and pacman.x in range(blue_ghost.x - 10, blue_ghost.x + 11):
        pygame.mixer.music.load('sounds/pacman_eatghost.wav')
        pygame.mixer.music.play()
        blue_ghost.x, blue_ghost.y = 14 * 20, 13 * 20
        blue_ghost.image = pygame.image.load("images/ghostgogoaway.png").convert_alpha()
        blue_ghost.sleep_time = 120
        blue_do_new_step = False
    
    elif pacman.y in range(green_ghost.y - 10, green_ghost.y + 11) and pacman.x in range(green_ghost.x - 10, green_ghost.x + 11):
        pygame.mixer.music.load('sounds/pacman_eatghost.wav')
        pygame.mixer.music.play()
        green_ghost.x, green_ghost.y = 15 * 20, 13 * 20
        green_ghost.image = pygame.image.load("images/ghostgogoaway.png").convert_alpha()
        green_ghost.sleep_time = 120
        green_do_new_step = False

while flag:
        if isPlayIntro == True:
            pygame.mixer.music.load('sounds/intro.wav')
            pygame.mixer.music.play()
            isPlayIntro = False
        else:
            main_x = 0
            main_y = 0
            screen.fill(BLACK)
            if red_ghost.sleep_time == 0:
                red_ghost.image = pygame.image.load("images/ghostred.png").convert_alpha()
                if red_do_new_step == False:
                    info = start_step(red_ghost, pacman, red_prev_step, red_do_new_step)
                    red_ghost.y, red_ghost.x, red_prev_step, red_do_new_step = info[0][0], info[0][1], info[1], info[2]
                else:
                    info = true_steps(red_ghost, red_prev_step)
                    red_ghost.y, red_ghost.x, red_prev_step = info[0][0], info[0][1], info[1]
            else:
                red_ghost.sleep_time -= 1

            if yellow_ghost.sleep_time == 0:
                yellow_ghost.image = pygame.image.load("images/ghostyellow.png").convert_alpha()
                if yellow_do_new_step == False:
                    info = start_step(yellow_ghost, pacman, yellow_prev_step, yellow_do_new_step)
                    yellow_ghost.y, yellow_ghost.x, yellow_prev_step, yellow_do_new_step = info[0][0], info[0][1], info[1], info[2]
                else:
                    info = true_steps(yellow_ghost, yellow_prev_step)
                    yellow_ghost.y, yellow_ghost.x, yellow_prev_step = info[0][0], info[0][1], info[1]
            else:
                yellow_ghost.sleep_time -= 1

            if blue_ghost.sleep_time == 0:
                blue_ghost.image = pygame.image.load("images/ghostblue.png").convert_alpha()
                if blue_do_new_step == False:
                    info = start_step(blue_ghost, pacman, blue_prev_step, blue_do_new_step)
                    blue_ghost.y, blue_ghost.x, blue_prev_step, blue_do_new_step = info[0][0], info[0][1], info[1], info[2]
                else:
                    info = true_steps(blue_ghost, blue_prev_step)
                    blue_ghost.y, blue_ghost.x, blue_prev_step = info[0][0], info[0][1], info[1]
            else:
                blue_ghost.sleep_time -= 1

            if green_ghost.sleep_time == 0:
                green_ghost.image = pygame.image.load("images/ghostgreen.png").convert_alpha()
                if green_do_new_step == False:
                    info = start_step(green_ghost, pacman, green_prev_step, green_do_new_step)
                    green_ghost.y, green_ghost.x, green_prev_step, green_do_new_step = info[0][0], info[0][1], info[1], info[2]
                else:
                    info = true_steps(green_ghost, green_prev_step)
                    green_ghost.y, green_ghost.x, green_prev_step = info[0][0], info[0][1], info[1]
            else:
                green_ghost.sleep_time -= 1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                elif event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_UP] or pygame.key.get_pressed()[pygame.K_w]:
                        pacman.image = pygame.image.load('images/pacman_up.png').convert_alpha()
                        scream()
                        pacman_test_y = (pacman.y - 20) // 20
                        pacman_test_x = pacman.x // 20 
                        if world[pacman_test_y][pacman_test_x] in "•* ":
                            if world[pacman_test_y][pacman_test_x] == "•":
                                count_of_balls += 10
                            elif world[pacman_test_y][pacman_test_x] == "*":
                                count_of_balls += 50
                            sound.play()
                            pacman.y -= 20
                            world[pacman_test_y][pacman_test_x] = " "

                    elif pygame.key.get_pressed()[pygame.K_DOWN] or pygame.key.get_pressed()[pygame.K_s]:
                        pacman.image = pygame.image.load('images/pacman_down.png').convert_alpha()
                        scream()
                        pacman_test_y = (pacman.y + 20) // 20
                        pacman_test_x = pacman.x // 20
                        if world[pacman_test_y][pacman_test_x] in "•* ":
                            if world[pacman_test_y][pacman_test_x] == "•":
                                count_of_balls += 10
                            elif world[pacman_test_y][pacman_test_x] == "*":
                                count_of_balls += 50
                            sound.play()
                            pacman.y += 20
                            world[pacman_test_y][pacman_test_x] = " "

                    elif pygame.key.get_pressed()[pygame.K_LEFT] or pygame.key.get_pressed()[pygame.K_a]:
                        pacman.image = pygame.image.load('images/pacman_left.png').convert_alpha()
                        scream()
                        pacman_test_y = pacman.y // 20
                        pacman_test_x = (pacman.x - 20) // 20
                        if pacman_test_x == -1:
                            pacman.x += 27 * 20
                        elif world[pacman_test_y][pacman_test_x] in "•* ":
                            if world[pacman_test_y][pacman_test_x] == "•":
                                count_of_balls += 10
                            elif world[pacman_test_y][pacman_test_x] == "*":
                                count_of_balls += 50
                            sound.play()
                            pacman.x -= 20
                            world[pacman_test_y][pacman_test_x] = " "

                    elif pygame.key.get_pressed()[pygame.K_RIGHT] or pygame.key.get_pressed()[pygame.K_d]:
                        pacman.image = pygame.image.load('images/pacman_right.png').convert_alpha()
                        scream()
                        pacman_test_y = pacman.y // 20
                        pacman_test_x = (pacman.x + 20) // 20
                        if pacman_test_x == 28:
                            pacman.x -= 27 * 20
                        elif world[pacman_test_y][pacman_test_x] in "•* ":
                            if world[pacman_test_y][pacman_test_x] == "•":
                                count_of_balls += 10
                            elif world[pacman_test_y][pacman_test_x] == "*":
                                count_of_balls += 50
                            sound.play()
                            pacman.x += 20
                            world[pacman_test_y][pacman_test_x] = " "
                            
            for row in world:
                for block in row:
                    if block == "-":
                        pygame.draw.rect(screen, BLUE, (main_x, main_y, 20, 20),border_radius=5)
                    elif block == "•":
                        pygame.draw.circle(screen,WHITE,(main_x + 10, main_y + 10), radius=5.0)
                    elif block == "*":
                        pygame.draw.circle(screen,YELLOW,(main_x + 10, main_y + 10), radius=10.0)
                    elif block == "=":
                        pygame.draw.line(screen,YELLOW,(main_x, main_y + 10), (main_x + 20, main_y + 10))
                    main_x += 20
                main_x = 0
                main_y += 20

            img = FONT.render(f"SCORE: {count_of_balls}", True, YELLOW)
            proig = FONT.render(f"You lost!!", True, YELLOW)
            vyig = FONT.render(f"You won!!", True, YELLOW)
            life = pygame.image.load('images/life.png').convert_alpha()

            screen.blit(pacman.image, (pacman.x,pacman.y))
            screen.blit(red_ghost.image, (red_ghost.x, red_ghost.y))
            screen.blit(yellow_ghost.image, (yellow_ghost.x, yellow_ghost.y))
            screen.blit(green_ghost.image, (green_ghost.x, green_ghost.y))
            screen.blit(blue_ghost.image, (blue_ghost.x, blue_ghost.y))
            screen.blit(img, (10,10))

            for i in range(count_of_lifes):
                screen.blit(life, (LIFE_X[i], 20 * 27 - 10))
            
            balls_in_world = [j for i in world for j in i if j in "*•"]
            
            if count_of_lifes != 0 and balls_in_world != []:
                pygame.display.update()
                clock.tick(FPS)
            
            elif count_of_lifes != 0 and balls_in_world == []:
                screen.blit(vyig, (10*20,13*20))
                pygame.display.update()
                sleep(1.5)
                pygame.quit()
            elif count_of_lifes == 0:
                screen.blit(proig, (10*20,13*20))
                pygame.mixer.music.load('sounds/pacman_death.wav')
                pygame.mixer.music.play()
                pygame.display.update()
                sleep(1.5)
                pygame.quit()
