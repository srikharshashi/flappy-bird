import pygame, sys, random
pygame.init()


def cr_pipe():
    h = random.randint(250, 380)
    bottom_pipe = pipe_surface.get_rect(midtop=(350, h))
    top_pipe = pipe_surface.get_rect(midbottom=(350, h - 100))
    return bottom_pipe, top_pipe


def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 3
    visible_pipes=[pipe for pipe in pipes if pipe.right>-50]
    return visible_pipes


def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= 500:
            SCREEN.blit(pipe_surface, pipe)
        else:
            flip_surface = pygame.transform.flip(pipe_surface, False, True)
            SCREEN.blit(flip_surface, pipe)


def check_coll(pipes):
    global can_score
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            can_score=True
            dead_sound.play()
            pygame.time.delay(300)
            return False

    if bird_rect.top <= 0 or bird_rect.bottom >= 488:
        can_score=True
        dead_sound.play()
        pygame.time.delay(300)
        return False
    return True


def score_display(game_state):
    if game_state == 1:
        score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(150, 50))
        SCREEN.blit(score_surface, score_rect)
    elif game_state == -1:
        score_surface = game_font.render(f'Score:{int(score)}', True, (255, 255, 255))
        score_rect = score_surface.get_rect(center=(150, 50))
        SCREEN.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High Score: {int(high_score)} ', True, (255, 255, 255))
        high_score_rect = score_surface.get_rect(center=(130, 460))
        SCREEN.blit(high_score_surface, high_score_rect)

        developer=game_font_2.render("Dev:Srikhar Shashi",True,(255,255,255))
        developer_rect=developer.get_rect(center=(50,10))
        SCREEN.blit(developer,developer_rect)


def update_score(score,high_score):
    if score >high_score:
            high_score=score
    return high_score
def pipe_score_check():
    global score
    global can_score
    if pipe_list:
        for pipe in pipe_list:
            if 135<pipe.centerx<140 and can_score:
                score+=1
                point_sound.play()
                can_score=False
            if pipe.centerx<0:
                can_score=True

# Essentials
SCREEN = pygame.display.set_mode((300, 600))
pygame.display.set_caption("Flappy-Bird-Pygame")
fpsclock = pygame.time.Clock()
fx = 0
bg = pygame.image.load('bg-r.png')
base = pygame.image.load('base.png')
game_font = pygame.font.Font('04B_19.TTF', 20)
game_font_2 = pygame.font.Font('04B_19.TTF', 10)
game_font_3 = pygame.font.Font('04B_19.TTF', 11)

message=pygame.image.load("text.png")
message_rect=message.get_rect(center=(150,250))
# Player Essentials
bird_surface = pygame.image.load('redbird-midflap.png')
bird_rect = bird_surface.get_rect(center=(150, 122))

# Game Variables
gravity = 0.25

bird_movement = 0
game_active = True
score = 0
can_score=True

# Pipe
pipe_surface = pygame.image.load("pipe-red.png").convert_alpha()
pipe_list = []
# """This is a user defined event"""
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

#Mixer
flap_sound=pygame.mixer.Sound("sfx_wing.wav")
dead_sound=pygame.mixer.Sound("sfx_hit.wav")
point_sound=pygame.mixer.Sound("sfx_point.wav")

high_score = 0
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            pygame.quit()
            sys.exit()
            high_score = 0
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE or event.key == pygame.K_UP or event.key == pygame.K_w:
                bird_movement = 0
                bird_movement -= 6
                flap_sound.play()
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (120, 200)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(cr_pipe())

    SCREEN.blit(bg, (0, 0))

    if game_active:

        # Bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        SCREEN.blit(bird_surface, bird_rect)
        game_active = check_coll(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)  # in Move_pipes the attribute .centerx is changed by -5
        draw_pipes(pipe_list)
        pipe_score_check()
        score_display(1)
    else:
        SCREEN.blit(message,message_rect)
        msg_surface = game_font_3.render((" Use Space to start and Jump through the obstacles"), True, (255, 255, 255))
        msg_rect = msg_surface.get_rect(center=(150, 390))
        SCREEN.blit(msg_surface, msg_rect)
        high_score = update_score(score,high_score)
        score_display(-1)


    # Bases
    SCREEN.blit(base, (fx, 488))
    SCREEN.blit(base, (fx + 300, 488))
    if fx < -300:
        fx = 0
    fx -= 1

    pygame.display.update()
    fpsclock.tick(60)
