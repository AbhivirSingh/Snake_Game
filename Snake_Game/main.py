import pygame, sys
import time
import random
from button import Button



# Window size
window_x, window_y = 1280, 720



# Initialising pygame
pygame.init()

# Initialise game window
game_window = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption("Menu")



BG = pygame.image.load("assets/Back.jpg")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("assets/font.ttf", size)

def play():
    
    snake_speed = 15

    # defining colors
    global black, white, red, green, blue, purple
    black = pygame.Color(0, 0, 0)
    white = pygame.Color(255, 255, 255)
    red = pygame.Color(255, 0, 0)
    green = pygame.Color(124, 255, 138)
    blue = pygame.Color(0, 0, 255)
    purple = pygame.Color(138, 43, 226)

    # FPS (frames per second) controller
    fps = pygame.time.Clock()

    # defining snake default position
    snake_position = [100, 50]

    # defining first 2 blocks of snake body
    snake_body = [[100, 50],[90, 50],[80, 50],[70, 50],[60, 50],[50, 50]]

    # fruit position
    fruit_position = [random.randrange(1, (window_x//10)) * 10,random.randrange(1, (window_y//10)) * 10]
    fruit_spawn = True

    # setting default snake direction towards right
    direction = 'RIGHT'
    change_to = direction

    # initial score
    global score,moves
    score, moves = 0, 0

    while True:
        PLAY_MOUSE_POS = pygame.mouse.get_pos()
        game_window.fill(BColor)

        # handling key events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    change_to = 'UP'
                    moves+=1
                if event.key == pygame.K_DOWN:
                    change_to = 'DOWN'
                    moves+=1
                if event.key == pygame.K_LEFT:
                    change_to = 'LEFT'
                    moves+=1
                if event.key == pygame.K_RIGHT:
                    change_to = 'RIGHT'
                    moves+=1


        # If two keys pressed simultaneously we don't want snake to move into two directions simultaneously
        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'
        # Moving the snake
        if direction == 'UP':
            snake_position[1] -= 10
        if direction == 'DOWN':
            snake_position[1] += 10
        if direction == 'LEFT':
            snake_position[0] -= 10
        if direction == 'RIGHT':
            snake_position[0] += 10
        
        # Snake body growing mechanism if fruits and snakes collide then scores will be incremented by 10
        snake_body.insert(0, list(snake_position))
        if snake_position[0] == fruit_position[0] and snake_position[1] == fruit_position[1]:
            file="assets/snake-hissing-6092.mp3"
            pygame.mixer.music.load(file)
            pygame.mixer.music.play()
            score+=10
            fruit_spawn = False
            moves=0
        else:
            snake_body.pop()

        if not fruit_spawn:
            fruit_position = [random.randrange(1, (window_x//10)) * 10,random.randrange(1, (window_y//10)) * 10]

        fruit_spawn = True
        game_window.fill(BColor)

        for pos in snake_body:
            pygame.draw.rect(game_window, SnakeColor, pygame.Rect(pos[0], pos[1], 10, 10))
            pygame.draw.rect(game_window, FoodColor, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))

        # Game Over conditions
        if snake_position[0] < 0 or snake_position[0] > window_x-10:
            game_over()
            time.sleep(3)
        if snake_position[1] < 0 or snake_position[1] > window_y-10:
            game_over()
            time.sleep(3)
        
        # Limitations in snake movement
        if moves==10:
            game_over()
            time.sleep(3)
            
        
        # Changing Highscore
        hscore=get_highscore()
        if hscore<score:
            edit_highscore(score)

        # Touching the snake body
        for block in snake_body[1:]:
            if snake_position[0] == block[0] and snake_position[1] == block[1]:
                game_over()
                time.sleep(3)

        # displaying score continuously
        show_score(1, purple, 'times new roman', 30)

        # displaying level continuously
        show_level(1, purple, 'times new roman', 30)

        # displaying moves continuously
        show_moves(1, purple, 'times new roman', 30)

        # displaying highscore()
        show_highscore(1, purple, 'times new roman', 30)

        # Refresh game screen
        pygame.display.update()

        # Frame Per Second /Refresh Rate
        fps.tick(snake_speed*(1+(score/50)))

# displaying Score function
def show_score(choice, color, font, size):

	# creating font object
    # score_font
	score_font = pygame.font.SysFont(font, size)
	
	# create the display surface object
	# score_surface
	score_surface = score_font.render('                   Score : ' + str(score), True, color)
	
	# create a rectangular object for the text
	# surface object
	score_rect = score_surface.get_rect()
	
	# displaying text
	game_window.blit(score_surface, score_rect)

# displaying Moves function
def show_moves(choice, color, font, size):

	# creating font object
    # moves_font
	moves_font = pygame.font.SysFont(font, size)
	
	# create the display surface object
	# moves_surface
	moves_surface = moves_font.render('                                       Moves : ' + str(moves), True, color)
	
	# create a rectangular object for the text
	# surface object
	moves_rect = moves_surface.get_rect()
	
	# displaying text
	game_window.blit(moves_surface, moves_rect)

# displaying Level function
def show_level(choice, color, font, size):

	# creating font object
    # level_font
	level_font = pygame.font.SysFont(font, size)
	
	# create the display surface object
	# level_surface
	level_surface = level_font.render('Level : ' + str(int((((score+10)/10)+2)/3)), True, color)
	
	# create a rectangular object for the text
	# surface object
	level_rect = level_surface.get_rect()
	
	# displaying text
	game_window.blit(level_surface, level_rect)

# displaying Level function
def show_highscore(choice, color, font, size):

	# creating font object
    # level_font
	highscore_font = pygame.font.SysFont(font, size)
	
	# create the display surface object
	# level_surface
	highscore_surface = highscore_font.render('                                                              Highscore : ' + str(get_highscore()), True, color)
	
	# create a rectangular object for the text
	# surface object
	highscore_rect = highscore_surface.get_rect()
	
	# displaying text
	game_window.blit(highscore_surface, highscore_rect)

# To get the current highscore
def get_highscore():
    f=open("highscore.txt","r")
    a=f.read()
    f.close()
    return int(a)

# To write new highscore
def edit_highscore(score):
    f=open("highscore.txt","w")
    f.write(str(score))
    f.close()

# game over function
def game_over():
	# creating font object my_font
	my_font = pygame.font.SysFont('times new roman', 50)
	
	
	# creating a text surface on which text
	# will be drawn
	game_over_surface = my_font.render('Your Score is : ' + str(score), True, red)
	
	# create a rectangular object for the text
	# surface object
	game_over_rect = game_over_surface.get_rect()
	
	# setting position of the text
	game_over_rect.midtop = (window_x/2, window_y/4)
	
	# blit will draw the text on screen
	game_window.blit(game_over_surface, game_over_rect)
	pygame.display.flip()


	file="assets/2G7CF5V-gamers-fail-game.mp3"
	pygame.mixer.music.load(file)
	pygame.mixer.music.play()
    
	while True:
            game_window.blit(BG, (0, 0))
            
            MENU_MOUSE_POS = pygame.mouse.get_pos()
            
            MENU_TEXT = get_font(100).render("MAIN MENU", True, "#00ff00")
            MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))
            
            PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
            QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

            game_window.blit(MENU_TEXT, MENU_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
                button.changeColor(MENU_MOUSE_POS)
                button.update(game_window)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        play()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        options()
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        pygame.quit()
                        sys.exit()
            pygame.display.update()

def options():
    global BColor, SnakeColor, FoodColor
    purple = pygame.Color(138, 43, 226)
    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()

        game_window.fill("White")

        OPTIONS_1 = Button(image=pygame.image.load("assets/Theme1.png"), pos=(340, 360), text_input="Theme 1", font=get_font(55), base_color="purple", hovering_color="White")
        OPTIONS_2 = Button(image=pygame.image.load("assets/Theme2.png"), pos=(940, 360), text_input="Theme 2", font=get_font(55), base_color="purple", hovering_color="White")

        OPTIONS_BACK = Button(image=None, pos=(640, 660), text_input="BACK", font=get_font(75), base_color="Black", hovering_color="Green")

        for button in [OPTIONS_1, OPTIONS_2, OPTIONS_BACK]:
                button.changeColor(OPTIONS_MOUSE_POS)
                button.update(game_window)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()
                if OPTIONS_1.checkForInput(OPTIONS_MOUSE_POS):
                    BColor, SnakeColor, FoodColor = pygame.Color(255, 255, 0), pygame.Color(255, 0, 0), pygame.Color(0, 255, 0)
                    play()
                if OPTIONS_2.checkForInput(OPTIONS_MOUSE_POS):
                    BColor, SnakeColor, FoodColor = pygame.Color(159, 226, 191), pygame.Color(193, 84, 193), pygame.Color(255, 0, 0)
                    play()

        pygame.display.update()

def main_menu():
    global BColor, SnakeColor, FoodColor
    BColor, SnakeColor, FoodColor = pygame.Color(255, 255, 0), pygame.Color(255, 0, 0), pygame.Color(0, 255, 0)

    while True:
        game_window.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#00ff00")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("assets/Play Rect.png"), pos=(640, 250), 
                            text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("assets/Options Rect.png"), pos=(640, 400), 
                            text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("assets/Quit Rect.png"), pos=(640, 550), 
                            text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        game_window.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(game_window)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
