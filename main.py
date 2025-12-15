import pygame  # import library
import sys
import os
from settings import *  # import settings from settings.py
from sprites import Player, Enemy, Trash, Scooter, Dove, Bottle
import random

money = 0
death_cause = None

# Initialize Pygame and Audio Mixer
pygame.init()
pygame.mixer.init()

# Font settings
test_font = pygame.font.Font(None, 50)
start_time = 0
high_score = 0
pygame.font.init()

# Setup Screen (VSYNC enabled for smooth movement)
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.SCALED, vsync=1)
pygame.display.set_caption(TITLE)
clock = pygame.time.Clock()

# add player
player = Player()
player_group = pygame.sprite.GroupSingle()
player_group.add(player)

# Ground settings
FLOOR_HEIGHT = 60
BG_HEIGHT = HEIGHT - FLOOR_HEIGHT

# Load background images
bg_image1 = pygame.image.load(os.path.join("Assets", "background.png")).convert()  # add background
bg_image1 = pygame.transform.scale(bg_image1, (WIDTH, BG_HEIGHT))  # Cconvert bg size

bg_image2 = pygame.image.load(os.path.join("Assets", "background2.png")).convert()  # add background
bg_image2 = pygame.transform.scale(bg_image2, (WIDTH, BG_HEIGHT))  # Cconvert bg size

bg_image3 = pygame.image.load(os.path.join("Assets", "background3.png")).convert()  # add background
bg_image3 = pygame.transform.scale(bg_image3, (WIDTH, BG_HEIGHT))  # Cconvert bg size

bg_width = bg_image1.get_width()
bg_imgs_list = [bg_image1, bg_image1, bg_image1]

scroll = 0
tiles = 3

floor_image = pygame.image.load(os.path.join("Assets", "floor.png")).convert()  # add floor
floor_image = pygame.transform.scale(floor_image, (WIDTH, FLOOR_HEIGHT))  # floor size

#add Sprite Groups
bottle_group = pygame.sprite.Group()  # Bottles(coins)
obstacle_group = pygame.sprite.Group()  # Enemies and Obstacles
# Custom Event for Spawning Obstacles
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, 1500) #Trigger every 1.5 seconds


def display_score():
    """Calculates and displays the current score based on time."""
    current_time = int(pygame.time.get_ticks() / 100) - start_time
    score_surf = test_font.render(f'Score: {current_time}', False, (255, 255, 255))
    score_rect = score_surf.get_rect(topright=(WIDTH - 180, 5))
    screen.blit(score_surf, score_rect)
    return current_time


def display_high_score(high_score):
    """Displays the best score saved in the session."""
    high_score_surf = test_font.render(f'Best: {high_score}', False, (255, 215, 0))
    high_score_rect = high_score_surf.get_rect(topright=(WIDTH - 20, 5))
    screen.blit(high_score_surf, high_score_rect)


def draw_window(game_active, score, high_score, money, death_cause, bg_imgs_list, bg_rects, floor_rects):
    """Main rendering function. Handles Game, Menu, and Game Over screens."""
    # 1. Draw Scrolling Backgrounds
    for i in range(3):
        screen.blit(bg_imgs_list[i], bg_rects[i])
        screen.blit(floor_image, floor_rects[i])
    #2. Draw all the characters
    if game_active:
        player_group.draw(screen)
        obstacle_group.draw(screen)
        bottle_group.draw(screen)

        display_score()
        display_high_score(high_score)
        # Draw UI (Money)
        money_surf = test_font.render(f'Pfand: {money}€', False, (138, 226, 52))  # Зеленый цвет
        screen.blit(money_surf, (20, 10))
    # 3. State: Menu or GAME OVER
    else:
        # Screen of Death
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))

        #Main menu
        if death_cause is None:
            # Название игры
            title = test_font.render("BERLIN RUNNER", True, (255, 215, 0))  # Золотой цвет
            title_rect = title.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50))
            screen.blit(title, title_rect)

            # Инструкция
            instr = test_font.render("Press SPACE to Start", True, (255, 255, 255))
            instr_rect = instr.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 50))
            screen.blit(instr, instr_rect)

            # Draw player preview
            if player_group.sprite:
                menu_player = pygame.transform.scale(player_group.sprite.run_frames[0], (150, 220))
                screen.blit(menu_player, (WIDTH // 2 - 75, HEIGHT // 2 - 300))

        #Gave over logic
        else:
            msg = test_font.render("GAME OVER", True, (255, 255, 255))
            msg_rect = msg.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 50))
            screen.blit(msg, msg_rect)
            #Show specific death message
            if death_cause == 'controller':
                title_text = "SCHWARZFAHREN!" # Caught without ticket
                color = (50, 100, 255)  # Blue

            else:
                title_text = "WASTED" # Hit an obstacle
                color = (255, 50, 50)  # Red

            title_surf = test_font.render(title_text, True, color)
            title_rect = title_surf.get_rect(center=(WIDTH / 2, HEIGHT / 2 - 80))
            screen.blit(title_surf, title_rect)
            # Show stats

        # score logic
            score_msg = test_font.render(f"Score: {score}", True, (255, 255, 255))
            score_msg_rect = score_msg.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 0))
            screen.blit(score_msg, score_msg_rect)
        # high score logic
            high_score_msg = test_font.render(f"High Score: {high_score}", True, (255, 215, 0))
            high_score_rect = high_score_msg.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 60))
            screen.blit(high_score_msg, high_score_rect)
            #Collected bottles(coins)
            money_msg = test_font.render(f"Collected: {money}€", True, (138, 226, 52))
            screen.blit(money_msg, money_msg.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 23)))

        # Instruction
            info = test_font.render("Press SPACE to run", True, (200, 200, 200))
            info_rect = info.get_rect(center=(WIDTH / 2, HEIGHT / 2 + 120))
            screen.blit(info, info_rect)


def main():
    global start_time, money, death_cause
    run = True
    high_score = 0
    game_active = False # Start in Menu state
    score = 0
    money = 0
    death_cause = None
    game_speed = 5
    """Audio setup """
    if os.path.exists(os.path.join("Assets", "bg_music.mp3")):
        pygame.mixer.music.load(os.path.join("Assets", "bg_music.mp3"))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)  # Loop indefinitely

        # 2. Sound of coins
    coin_sound = None
    if os.path.exists(os.path.join("Assets", "coin.wav")):
        coin_sound = pygame.mixer.Sound(os.path.join("Assets", "coin.wav"))
        coin_sound.set_volume(0.6)
        #3. Hit sound
    hit_sound = None
    if os.path.exists(os.path.join("Assets", "hit.wav")):
        hit_sound = pygame.mixer.Sound(os.path.join("Assets", "hit.wav"))
        hit_sound.set_volume(0.6)
        # 4. Cashbox sound(When you pay to CONTROLLER)
    cashbox_sound = None
    if os.path.exists(os.path.join("Assets", "cashbox.wav")):
        cashbox_sound = pygame.mixer.Sound(os.path.join("Assets", "cashbox.wav"))
        cashbox_sound.set_volume(0.6)
    #Background lists for infinite scrolling
    bg_imgs_list = [bg_image1, bg_image1, bg_image1]
    bg_rects = []
    floor_rects = []
    # Initialize background positions
    for i in range(3):
        bg_rects.append(bg_image1.get_rect(topleft=(i * bg_width, 0)))
        floor_rects.append(floor_image.get_rect(topleft=(i * bg_width, HEIGHT - FLOOR_HEIGHT)))

    #Main Game Loop
    while run:
        clock.tick(FPS)  # control speed of game
        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if game_active:
                # Spawn obstacles randomly
                if event.type == obstacle_timer:
                    spawn_list = ['trash', 'trash', 'trash', 'scooter', 'scooter', 'bottle', 'bottle', 'dove', 'enemy']
                    choice = random.choice(spawn_list)
                    if choice == 'trash':
                        obstacle_group.add(Trash())
                    elif choice == 'scooter':
                        obstacle_group.add(Scooter())
                    elif choice == 'bottle':
                        bottle_group.add(Bottle())
                    elif choice == 'enemy':
                        obstacle_group.add(Enemy())  # Add Kontroleur
                    else:
                        obstacle_group.add(Dove())
            # Handle Restart / Start
            else:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    game_active = True
                    obstacle_group.empty()  # Removing old enemies
                    bottle_group.empty()
                    player.rect.midbottom = (100, HEIGHT - 60)  # Returning the player
                    player.gravity = 0
                    start_time = int(pygame.time.get_ticks() / 100)  # Resetting time
                    death_cause = None
                    game_speed = 5
                    # Restart music if stopped
                    if not pygame.mixer.music.get_busy():
                        pygame.mixer.music.play(-1)

                    # Reset background
                    bg_imgs_list = [bg_image1, bg_image1, bg_image1]
                    bg_rects = []
                    floor_rects = []
                    for i in range(3):
                        bg_rects.append(bg_image1.get_rect(topleft=(i * bg_width, 0)))
                        floor_rects.append(floor_image.get_rect(topleft=(i * bg_width, HEIGHT - FLOOR_HEIGHT)))
        # Game Logic Update
        if game_active:
            score = int(pygame.time.get_ticks() / 100) - start_time
            if score > high_score:
                high_score = score

            # Increase game speed over time
            game_speed += 0.005
            if game_speed > 15:  # Limiter
                game_speed = 15

            obstacle_group.update(int(game_speed))
            player_group.update()
            bottle_group.update(int(game_speed))
            # Move backgrounds
            for i in range(3):
                bg_rects[i].x -= int(game_speed)
                floor_rects[i].x -= int(game_speed)
            #  Infinity scrolling & biome switching logic
            if bg_rects[0].right < 0:
                bg_rects.pop(0) #Remove leftmost background
                floor_rects.pop(0)
                # We remember what is leaving
                last_img = bg_imgs_list[-1]
                bg_imgs_list.pop(0) # Remove corresponding image

                new_x = bg_rects[-1].right # Calculate new position
                # Determine next biome (Tunnel or Street) based on score
                target_phase = (score // 300) % 2
                next_bg = bg_image1  #Default: Tunnel

                if target_phase == 1:  # Target: Street
                    if last_img == bg_image1:
                        # There was a Tunnel -> We put a TRANSITION
                        next_bg = bg_image3
                    elif last_img == bg_image3:
                        next_bg = bg_image2 # Street
                    else:
                        next_bg = bg_image2

                else:  # Target: Tunnel
                    # If you were on the street, just enter the tunnel
                    next_bg = bg_image1

                bg_imgs_list.append(next_bg)
                bg_rects.append(next_bg.get_rect(topleft=(new_x, 0)))
                floor_rects.append(floor_image.get_rect(topleft=(new_x, HEIGHT - FLOOR_HEIGHT)))
            #Colission detection
            collision_list = pygame.sprite.spritecollide(player, obstacle_group, False, pygame.sprite.collide_mask)

            if collision_list:
                obstacle = collision_list[0]  # Who did we crash into?

                # 1. If it's CONTROLLER (Enemy)
                if isinstance(obstacle, Enemy):
                    if money >= 60:
                        money -= 60   # Pay Fine
                        obstacle.kill()  # Remove Controller
                        if cashbox_sound: cashbox_sound.play()
                    else:
                        # Game Over: No Money
                        game_active = False
                        death_cause = 'controller'
                        pygame.mixer.music.stop()
                        if hit_sound: hit_sound.play()

                # Case 2: Hit Obstacle (Trash, Scooter, Dove)
                else:
                    game_active = False  # Immediate death, no way to buy your way out
                    death_cause = 'obstacle'
                    pygame.mixer.music.stop()
                    if hit_sound: hit_sound.play()

                # 2. Collision with BOTTLES (coins)
            if pygame.sprite.spritecollide(player, bottle_group, True):# True means "remove the bottle after touching it"
                money += 5
                if coin_sound: coin_sound.play()

        # Render Frame
        draw_window(game_active, score, high_score, money, death_cause, bg_imgs_list, bg_rects, floor_rects)
        pygame.display.flip()
    #Quit
    pygame.quit()  # checking if window close
    sys.exit()


if __name__ == '__main__':
    main()
