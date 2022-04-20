import pygame, sys ,random

# !ACT
def draw_floor():
    screen.blit(floor,(floor_x_pos,650))
    screen.blit(floor,(floor_x_pos + 432,650))
def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bot_pipe = pipe_surface.get_rect(midtop = (550,random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop = (550,random_pipe_pos-650))
    return bot_pipe,top_pipe
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >=600 :
            screen.blit(pipe_surface, pipe)
        else :
            flip_pipe = pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe, pipe)
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            music_die.play()
            return False
    if(bird_rect.top <= -75 or bird_rect.bottom >= 650):
        music_die.play()
        return False
    return True
def rotate_bird(bird1):
    new_bird = pygame.transform.rotozoom(bird1, -bird_movement*3, 1)
    return new_bird
def bird_animation():
    new_bird = bird_list[bird_index]
    new_bird_rect = new_bird.get_rect(center = (100 , bird_rect.centery))
    return new_bird,new_bird_rect
def score_display():
        score_surface = game_font.render(str(int(score)), True, (255,255,255))
        score_rect = score_surface.get_rect(center = (400,70))
        screen.blit(score_surface,score_rect)

        score_max_surface = game_font.render('High Score:'+str(int(score_max)), True, (255,255,255))
        score_max_rect = score_max_surface.get_rect(center = (300,120))
        screen.blit(score_max_surface,score_max_rect)

# !DATA
pygame.mixer.pre_init()
pygame.init()
screen = pygame.display.set_mode((432,768))
clock = pygame.time.Clock()
gravity = 0.20
bird_movement = 0
game_act = True
game_font = pygame.font.Font('04B_19.TTF', 40)
score = 0
score_max = 0
# background
background = pygame.image.load('assets/background-night.png').convert()
background = pygame.transform.scale2x(background)
# sàn
floor = pygame.image.load('assets/floor.png').convert()
floor = pygame.transform.scale2x(floor)
floor_x_pos = 0
# bird
bird_mid = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
bird_down = pygame.image.load('assets/yellowbird-downflap.png').convert_alpha()
bird_up = pygame.image.load('assets/yellowbird-upflap.png').convert_alpha() 

bird_list = [bird_down,bird_mid,bird_up]
bird_index = 0
bird = bird_list[bird_index]
bird = pygame.transform.scale2x(bird)
bird_rect=bird.get_rect(center = (100,384))

#tạo timer cho bird 
birdflap = pygame.USEREVENT + 1
pygame.time.set_timer(birdflap, 100)
#vật cản 
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface = pygame.transform.scale2x(pipe_surface)
pipe_height = [200,300,400]
#timer
spawn_pipe = pygame.USEREVENT
pygame.time.set_timer(spawn_pipe, 1200)
pipe_list = []
#màn hình kết thúc
game_start = pygame.image.load('assets/message.png').convert_alpha()
game_start = pygame.transform.scale2x(game_start)
game_start_rect = game_start.get_rect(center = (216,384))
game_over = pygame.image.load('assets/gameover.png').convert_alpha()
game_over_rect = game_over.get_rect(center = (216,384))
#music
music_flap = pygame.mixer.Sound('sound/sfx_wing.wav')
music_die = pygame.mixer.Sound('sound/sfx_die.wav')
music_point = pygame.mixer.Sound('sound/sfx_point.wav')
time_point = 100
# !GAME
while True:

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_act:
                print('fly')
                bird_movement = 0
                bird_movement = -11
                music_flap.play()
            if event.key == pygame.K_SPACE and game_act == False:
                game_act = True
                pipe_list.clear()
                bird_rect.center = (100,384)
                bird_movement=0
        if event.type == spawn_pipe:
            pipe_list.extend(create_pipe())
            print(create_pipe())
        if event.type == birdflap:
            bird_index += 1
            bird_index %= 3
        bird,bird_rect = bird_animation()
    # background
    screen.blit(background,(0,0))
    if game_act:
        # bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird)
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird, bird_rect) 
        game_act = check_collision(pipe_list)
        # vật cản
        pipe_list = move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score += 0.01
        time_point -= 1
        if time_point == 0:
            music_point.play()
            time_point = 100
        # music_point.play()
        score_max = max(score,score_max)
        score_display()
    else :
        score_max_surface = game_font.render('High Score:'+str(int(score_max)), True, (255,255,255))
        score_max_rect = score_max_surface.get_rect(center = (216,630))
        screen.blit(score_max_surface,score_max_rect)
        screen.blit(game_start,game_start_rect)
        score = 0

    # floor
    floor_x_pos -= 1
    draw_floor()
    if(floor_x_pos <= -432):
        floor_x_pos=0

    pygame.display.update()
    clock.tick(120)

