import pygame, sys
import random
from button import Button

pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Menu")

BG = pygame.image.load("menubackground.png")
won = pygame.mixer.Sound("won.wav")

def get_font(size):
    return pygame.font.Font("font.ttf", size)

def level1():
    pygame.time.delay(1000)
    WIDTH, HEIGHT = 1280, 720
    FPS = 60

    game_over_sound = pygame.mixer.Sound("game_over.wav")
    background_sound = pygame.mixer.Sound("background_sound.mp3")

    WHITE = (255, 255, 255)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Level - 1")

    background = pygame.image.load("background3.png")
    obstacle_image = pygame.image.load("blue.png")
    scaled_obstacle_image = pygame.transform.scale(obstacle_image, (48, 48))

    player_sprite_sheet = pygame.image.load("idle.png")
    vplayer_sprite_sheet = pygame.image.load("vidle.png")
    chainsaw_sprite_sheet = pygame.image.load("chainsaw.png")

    player_frames = []
    frame_index = 0
    animation_speed = 0.05

    vplayer_frames = []
    vframe_index = 0
    vanimation_speed = 0.05

    chainsaws_frames = []
    chainsaw_index = 0
    chainsaws_animation_speed = 0.05
    for i in range(11):
        frame = player_sprite_sheet.subsurface((i * 32, 0, 32, 32))
        scaled_frame = pygame.transform.scale2x(frame)
        player_frames.append(scaled_frame)

    for j in range(11):
        vframe = vplayer_sprite_sheet.subsurface((j * 32, 0, 32, 32))
        vscaled_frame = pygame.transform.scale(vframe, (vframe.get_width() * 12, vframe.get_height() * 12))
        vplayer_frames.append(vscaled_frame)

    for i in range(8):
        chainsaw_frame = chainsaw_sprite_sheet.subsurface((i * 38, 0, 38, 38))
        scaled_chainsaw = pygame.transform.scale2x(chainsaw_frame)
        chainsaws_frames.append(scaled_chainsaw)

    player_animation_timer = 0
    vplayer_animation_timer = 0

    player_rect = player_frames[0].get_rect()
    player_rect.topleft = (200, HEIGHT - player_rect.height - 50)
    original_player_speed = 3
    player_speed = original_player_speed
    jump_speed = 20
    gravity = 0.5
    player_jump = False
    on_the_ground = True

    chainsaw_chaser_speed = 3
    chainsaw_chaser_rect = chainsaws_frames[0].get_rect(topleft=(WIDTH, HEIGHT - chainsaws_frames[0].get_height() - 50))
    vplayer_rect = vplayer_frames[0].get_rect()
    vplayer_rect.topleft = (100 - 300, HEIGHT - vplayer_rect.height - 50)
    vplayer_speed = player_speed - 1

    obstacles = []
    current_x_position = player_rect.right + random.randint(100, 300)

    while current_x_position < WIDTH + 2000:
        obstacle_rect = scaled_obstacle_image.get_rect(
            topleft=(current_x_position, HEIGHT - scaled_obstacle_image.get_height() - 50))
        obstacles.append({"image": scaled_obstacle_image, "rect": obstacle_rect})
        current_x_position += random.randint(150, 250)
    total_level_distance = 1200
    completion_percentage = min((player_rect.right / total_level_distance) * 100, 100)

    chainsaws_animation_timer = pygame.time.get_ticks()

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 36)
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.mixer.Sound.play(background_sound)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += player_speed

        if keys[pygame.K_SPACE] and on_the_ground:
            player_jump = True
            on_the_ground = False
            jump_speed = 10

        if player_jump:
            player_rect.y -= jump_speed
            jump_speed -= gravity
            if player_rect.top >= HEIGHT - player_rect.height - 50:
                player_rect.y = HEIGHT - player_rect.height - 50
                on_the_ground = True
                player_jump = False

        if pygame.time.get_ticks() - player_animation_timer > animation_speed * 1000:
            player_animation_timer = pygame.time.get_ticks()
            frame_index = (frame_index + 1) % len(player_frames)

        player_collision_rect = player_rect.inflate(-10, -10)

        for obstacle in obstacles:
            obstacle["rect"].x -= (player_speed - 1)
            if obstacle["rect"].right <= 0:
                obstacle["rect"].x = WIDTH + random.randint(150, 250)
                obstacle["rect"].y =  HEIGHT -scaled_obstacle_image.get_height() - 50

        vplayer_rect.x += vplayer_speed
        if vplayer_rect.right >= WIDTH:
            vplayer_rect.x = 0 - vplayer_rect.width

        if pygame.time.get_ticks() - vplayer_animation_timer > vanimation_speed * 1000:
            vplayer_animation_timer = pygame.time.get_ticks()
            vframe_index = (vframe_index + 1) % len(vplayer_frames)

        collision_detected = False

        for obstacle in obstacles:
            player_collision_zone = player_collision_rect.inflate(-9, -9)
            obstacle_collision_zone = obstacle["rect"].inflate(-10, -9)

            if player_collision_zone.colliderect(obstacle_collision_zone):
                player_speed = 1
                collision_detected = True

        if player_rect.x > 1200:
            OPTIONS_TEXT = get_font(60).render("Level Completed!", True, "Yellow")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
            SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
            won.play()
            background_sound.stop()
            won.play()
            pygame.display.flip()
            pygame.time.delay(2000)
            main_menu()

        if not collision_detected:
            player_speed = original_player_speed

        player_collision_zone = player_collision_rect.inflate(-5, -5)
        vplayer_collision_zone = vplayer_rect.inflate(-111, -111)

        if player_collision_zone.colliderect(vplayer_collision_zone) and not game_over:
            game_over = True
            OPTIONS_TEXT = get_font(34).render("GAME OVER", True, "Red")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
            SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
            pygame.display.flip()
            background_sound.stop()
            game_over_sound.play()
            pygame.time.delay(2000)
            main_menu()

        screen.blit(background, (0, 0))

        for obstacle in obstacles:
            screen.blit(obstacle["image"], obstacle["rect"].topleft)

        player_surface = pygame.transform.flip(player_frames[frame_index], keys[pygame.K_LEFT], False)
        screen.blit(player_surface, player_rect.topleft)

        vplayer_surface = pygame.transform.flip(vplayer_frames[vframe_index], False, False)
        screen.blit(vplayer_surface, vplayer_rect.topleft)

        completion_percentage = min((player_rect.right / total_level_distance) * 100, 100)

        percentage_text = get_font(24).render(f"Completion: {completion_percentage:.2f}%", True, "White")
        screen.blit(percentage_text, (10, 10))

        chainsaw_chaser_rect.x -= chainsaw_chaser_speed
        if chainsaw_chaser_rect.right <= 0:
            chainsaw_chaser_rect.x = WIDTH
        if pygame.time.get_ticks() - chainsaws_animation_timer > chainsaws_animation_speed * 1000:
            chainsaws_animation_timer = pygame.time.get_ticks()
            chainsaw_index = (chainsaw_index + 1) % len(chainsaws_frames)
        chainsaw_chaser_collision_zone = chainsaw_chaser_rect.inflate(-9, -9)
        if chainsaw_chaser_collision_zone.colliderect(player_collision_rect):
            game_over = True
            OPTIONS_TEXT = get_font(34).render("GAME OVER", True, "Red")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
            SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
            pygame.display.flip()
            background_sound.stop()
            game_over_sound.play()
            pygame.time.delay(2000)
            main_menu()

        chainsaw_chaser_surface = chainsaws_frames[chainsaw_index]
        screen.blit(chainsaw_chaser_surface, chainsaw_chaser_rect.topleft)

        pygame.display.flip()
        clock.tick(FPS)

def optionsYES():
    SCREEN.fill("white")
    OPTIONS_TEXT = get_font(34).render("OH , I AM SORRY FOR YOU", True, "Black")
    OPTIONS_TEXT_SPACE = get_font(20).render("<SPACE>  jump", True, "Black")
    OPTIONS_TEXT_ARROWS = get_font(20).render("<arrows>  move", True, "Black")
    OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
    SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
    SCREEN.blit(OPTIONS_TEXT_SPACE, (640, 300))
    SCREEN.blit(OPTIONS_TEXT_ARROWS, (640, 330))

def options():
    show_additional_info = False

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("white")

        if not show_additional_info:
            OPTIONS_TEXT = get_font(30).render("REALLY HAVE YOU PLAYED IN YOUR FIFE", True, "Black")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
            SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
        else:
            optionsYES()

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="NO", font=get_font(75), base_color="Black", hovering_color="Green")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        OPTIONS_MENU = Button(image=None, pos=(640, 540),
                              text_input="MENU", font=get_font(75), base_color="Black", hovering_color="Green")
        OPTIONS_MENU.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_MENU.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    show_additional_info = not show_additional_info
                elif OPTIONS_MENU.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def levels():
    show_additional_info = False

    while True:
        OPTIONS_MOUSE_POS = pygame.mouse.get_pos()
        SCREEN.fill("white")

        OPTIONS_BACK2 = Button(image=None, pos=(640, 380),
                              text_input="LEVEL-1", font=get_font(75), base_color="Black", hovering_color="Green")
        OPTIONS_BACK2.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK2.update(SCREEN)

        OPTIONS_BACK = Button(image=None, pos=(640, 460),
                              text_input="LEVEL-2", font=get_font(75), base_color="Black", hovering_color="Green")
        OPTIONS_BACK.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_BACK.update(SCREEN)

        OPTIONS_MENU = Button(image=None, pos=(640, 540),
                              text_input="MENU", font=get_font(75), base_color="Black", hovering_color="Green")
        OPTIONS_MENU.changeColor(OPTIONS_MOUSE_POS)
        OPTIONS_MENU.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if OPTIONS_BACK2.checkForInput(OPTIONS_MOUSE_POS):
                    level1()
                elif OPTIONS_BACK.checkForInput(OPTIONS_MOUSE_POS):
                    level2()
                elif OPTIONS_MENU.checkForInput(OPTIONS_MOUSE_POS):
                    main_menu()

        pygame.display.update()

def level2():
    pygame.time.delay(500)

    WIDTH, HEIGHT = 1280, 720
    FPS = 60
    game_over_sound = pygame.mixer.Sound("game_over.wav")
    background_sound = pygame.mixer.Sound("background_sound.mp3")

    WHITE = (255, 255, 255)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Level - 2")

    background = pygame.image.load("level2background.jpg")
    background = pygame.transform.scale(background, (1280, 720))
    obstacle_image = pygame.image.load("obstacle2.png")
    scaled_obstacle_image = pygame.transform.scale(obstacle_image, (48, 48))

    player_sprite_sheet = pygame.image.load("idle.png")
    vplayer_sprite_sheet = pygame.image.load("v2idle.png")
    chainsaw_sprite_sheet = pygame.image.load("chainsaw.png")

    player_frames = []
    frame_index = 0
    animation_speed = 0.05

    vplayer_frames = []
    vframe_index = 0
    vanimation_speed = 0.05

    chainsaw_frames = []
    chainsaw_frame_index = 0
    chainsaw_animation_speed = 0.05

    for i in range(11):
        frame = player_sprite_sheet.subsurface((i * 32, 0, 32, 32))
        scaled_frame = pygame.transform.scale2x(frame)
        player_frames.append(scaled_frame)

    for j in range(11):
        vframe = vplayer_sprite_sheet.subsurface((j * 32, 0, 32, 32))
        vscaled_frame = pygame.transform.scale(vframe, (vframe.get_width() * 12, vframe.get_height() * 12))
        vplayer_frames.append(vscaled_frame)

    for i in range(8):
        chainsaw_frame = chainsaw_sprite_sheet.subsurface((i * 38, 0, 38, 38))
        scaled_chainsaw = pygame.transform.scale2x(chainsaw_frame)
        chainsaw_frames.append(scaled_chainsaw)

    player_animation_timer = 0
    vplayer_animation_timer = 0
    chainsaw_animation_timer = 0

    player_rect = player_frames[0].get_rect()
    player_rect.topleft = (200, HEIGHT - player_rect.height - 50)
    original_player_speed = 3
    player_speed = original_player_speed
    jump_speed = 10
    gravity = 0.5
    player_jump = False
    on_the_ground = True

    vplayer_rect = vplayer_frames[0].get_rect()
    vplayer_rect.topleft = (100 - 300, HEIGHT - vplayer_rect.height - 50)
    vplayer_speed = player_speed - 1

    chainsaw_chaser_speed = 3
    chainsaw_chaser_rect = chainsaw_frames[0].get_rect(topleft=(WIDTH, HEIGHT - chainsaw_frames[0].get_height() - 50))

    obstacles = []
    current_x_position = player_rect.right + random.randint(100, 300)

    while current_x_position < WIDTH + 2000:
        obstacle_rect = scaled_obstacle_image.get_rect(
            topleft=(current_x_position, HEIGHT - scaled_obstacle_image.get_height() - 50))
        obstacles.append({"image": scaled_obstacle_image, "rect": obstacle_rect})
        current_x_position += random.randint(150, 250)

    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 36)
    game_over = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.mixer.Sound.play(background_sound)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_rect.left > 0:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT] and player_rect.right < WIDTH:
            player_rect.x += player_speed

        if keys[pygame.K_SPACE] and on_the_ground:
            player_jump = True
            on_the_ground = False
            jump_speed = 10

        if player_jump:
            player_rect.y -= jump_speed
            jump_speed -= gravity
            if player_rect.top >= HEIGHT - player_rect.height - 50:
                player_rect.y = HEIGHT - player_rect.height - 50
                on_the_ground = True
                player_jump = False

        if pygame.time.get_ticks() - player_animation_timer > animation_speed * 1000:
            player_animation_timer = pygame.time.get_ticks()
            frame_index = (frame_index + 1) % len(player_frames)

        player_collision_rect = player_rect.inflate(-10, -10)

        for obstacle in obstacles:
            obstacle["rect"].x -= (player_speed - 1)
            if obstacle["rect"].right <= 0:
                obstacle["rect"].x = WIDTH + random.randint(150, 250)
                obstacle["rect"].y = HEIGHT - scaled_obstacle_image.get_height() - 50

        vplayer_rect.x += vplayer_speed
        if vplayer_rect.right >= WIDTH:
            vplayer_rect.x = 0 - vplayer_rect.width

        if pygame.time.get_ticks() - vplayer_animation_timer > vanimation_speed * 1000:
            vplayer_animation_timer = pygame.time.get_ticks()
            vframe_index = (vframe_index + 1) % len(vplayer_frames)

        collision_detected = False

        for obstacle in obstacles:
            player_collision_zone = player_collision_rect.inflate(-9, -9)
            obstacle_collision_zone = obstacle["rect"].inflate(-10, -9)

            if player_collision_zone.colliderect(obstacle_collision_zone):
                collision_detected = True

        chainsaw_collision_zone = chainsaw_chaser_rect.inflate(-5, -5)
        if player_collision_zone.colliderect(chainsaw_collision_zone):
            collision_detected = True

        if collision_detected:
            OPTIONS_TEXT = get_font(34).render("GAME OVER", True, "Red")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
            SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)

            background_sound.stop()
            game_over_sound.play()

            pygame.display.flip()
            pygame.time.delay(2000)

            main_menu()
        else:
            player_speed = original_player_speed

        player_collision_zone = player_collision_rect.inflate(-5, -5)
        vplayer_collision_zone = vplayer_rect.inflate(-111, -111)
        if player_rect.x > 1200:
            OPTIONS_TEXT = get_font(60).render("Level Completed!", True, "Yellow")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
            SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
            won.play()

            background_sound.stop()
            won.play()

            pygame.display.flip()
            pygame.time.delay(2000)

            main_menu()
        if player_collision_zone.colliderect(vplayer_collision_zone) and not game_over:
            game_over = True
            OPTIONS_TEXT = get_font(34).render("GAME OVER", True, "Red")
            OPTIONS_RECT = OPTIONS_TEXT.get_rect(center=(640, 260))
            SCREEN.blit(OPTIONS_TEXT, OPTIONS_RECT)
            pygame.display.flip()

            background_sound.stop()
            game_over_sound.play()

            pygame.time.delay(2000)
            main_menu()

        chainsaw_chaser_rect.x -= chainsaw_chaser_speed
        if chainsaw_chaser_rect.right <= 0:
            chainsaw_chaser_rect.x = WIDTH

        if pygame.time.get_ticks() - chainsaw_animation_timer > chainsaw_animation_speed * 1000:
            chainsaw_animation_timer = pygame.time.get_ticks()
            chainsaw_frame_index = (chainsaw_frame_index + 1) % len(chainsaw_frames)

        chainsaw_chaser_surface = chainsaw_frames[chainsaw_frame_index]
        screen.blit(chainsaw_chaser_surface, chainsaw_chaser_rect.topleft)

        screen.blit(background, (0, 0))

        for obstacle in obstacles:
            screen.blit(obstacle["image"], obstacle["rect"].topleft)

        player_surface = pygame.transform.flip(player_frames[frame_index], keys[pygame.K_LEFT], False)
        screen.blit(player_surface, player_rect.topleft)

        vplayer_surface = pygame.transform.flip(vplayer_frames[vframe_index], False, False)
        screen.blit(vplayer_surface, vplayer_rect.topleft)

        screen.blit(chainsaw_frames[chainsaw_frame_index], chainsaw_chaser_rect.topleft)

        total_level_distance = 1280
        player_distance = player_rect.x
        completion_percentage = (player_distance / total_level_distance) * 100
        completion_text = get_font(24).render(f"Completion: {completion_percentage:.2f}%", True, WHITE)

        screen.blit(completion_text, (20, 20))

        pygame.display.flip()

        clock.tick(FPS)

def main_menu():
    while True:
        SCREEN.blit(BG, (0, 0))

        MENU_MOUSE_POS = pygame.mouse.get_pos()

        MENU_TEXT = get_font(100).render("MAIN MENU", True, "#b68f40")
        MENU_RECT = MENU_TEXT.get_rect(center=(640, 100))

        PLAY_BUTTON = Button(image=pygame.image.load("Play Rect.png"), pos=(640, 250),
                             text_input="PLAY", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        OPTIONS_BUTTON = Button(image=pygame.image.load("Options Rect.png"), pos=(640, 400),
                                text_input="OPTIONS", font=get_font(75), base_color="#d7fcd4", hovering_color="White")
        QUIT_BUTTON = Button(image=pygame.image.load("Quit Rect.png"), pos=(640, 550),
                             text_input="QUIT", font=get_font(75), base_color="#d7fcd4", hovering_color="White")

        SCREEN.blit(MENU_TEXT, MENU_RECT)

        for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    levels()
                if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                    options()
                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()
