import pygame
from pygame import *
import sys

pygame.init()
pygame.mixer.init()

Current_state = 'start_menu'
Is_Victory = False
NextRound = False
RUNNING = True
clock = pygame.time.Clock()
FPS = 60

player_Score = 0
Stage_name = None

# Window
Width, Height = 800, 600
screen = display.set_mode((Width, Height))

from dataloader import *

player_last_fire = 0
enemy_last_spawn = 0

# Font Loading
GameTitle_text = pygame.font.Font('Assets/Fonts/RetroFont.ttf', 70)
ScoreBoard = pygame.font.Font('Assets/Fonts/RetroFont.ttf', 22)
Menu_gui = pygame.font.Font('Assets/Fonts/RetroFont.ttf', 37)
StageNumber_text = pygame.font.Font('Assets/Fonts/RetroFont.ttf', 75)
MissionName_text = pygame.font.Font('Assets/Fonts/RetroFont.ttf', 60)

while RUNNING:

    clock.tick(FPS)
    now = pygame.time.get_ticks()

# Input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False
            break

        if event.type == pygame.KEYDOWN:
            if Current_state == 'game':
                if event.key == pygame.K_SPACE and now - player_last_fire > projectile['cooldown']:
                    player_last_fire = now
                    play_sfx = pygame.mixer.Sound(projectile['sound'])
                    play_sfx.set_volume(0.4)
                    play_sfx.play()
                    projectile_hitbox = pygame.Rect(player['x_pos'], player['y_pos'], projectile['rect_width'], projectile['rect_height'])
                    projectile_hitbox.center = player['rect'].center
                    projectile['list'].append(projectile_hitbox)
            
            if event.key == pygame.K_RETURN and Current_state == 'start_menu':
                Current_state = 'loading'

# Game State
    if Current_state == 'game':
        pygame.display.set_caption(f"{GameTitle} {Version}   FPS: {int(clock.get_fps())}")

        Stage_name = type(current_stage).__name__.replace("_", " ")

        if current_music != current_stage.backgroundMusic:
            current_music = current_stage.backgroundMusic
            pygame.mixer.music.load(current_music)
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1)

    # Player Movement
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a] and player['rect'].left > -10:
            player['x_pos'] -= player['speed']

        if keys[pygame.K_d] and player['rect'].right < Width + 10:
            player['x_pos'] += player['speed']

        player['rect'].centerx = player['x_pos']

    # Stage 1 to 2
        if isinstance(current_stage, Stage_1):
            if player_Score == current_stage.milestone_score:
                Is_Victory = True
                Current_state = None
                if NextRound:
                    current_stage = Stage_2()
                    current_music = current_stage.backgroundMusic
                    current_bg = current_stage.Background()

    # Projectile Movement
        for projectile_rect in projectile['list']:
            projectile_rect.y -= projectile['speed']
            if projectile_rect.y < -10:
                projectile['list'].remove(projectile_rect)

    # Projectile Collision
        for projectile_rect in projectile['list']:
            for enemy_rect in enemy['list']:
                if projectile_rect.colliderect(enemy_rect):
                    player_Score += 1
                    play_sfx = pygame.mixer.Sound(enemy['explosion'])
                    play_sfx.set_volume(0.4)
                    play_sfx.play()
                    enemy['list'].remove(enemy_rect)
                    projectile['list'].remove(projectile_rect)

    # Enemy Spawning
        if now - enemy_last_spawn >= enemy['spawn_cd']:
            enemy_last_spawn = now
            enemy_hitbox = pygame.Rect(random.randint(15, 720), enemy['spawn_y'], enemy['rect_width'], enemy['rect_height'])
            enemy['list'].append(enemy_hitbox)

    # Enemy Movements
        for hitbox in enemy['list']:
            hitbox.y -= enemy['speed']
            if hitbox.y > enemy['despawn']:
                enemy['list'].remove(hitbox)

    # Layers
        screen.blit(current_bg, (0, 0))

        # Projectile
        for projectile_rect in projectile['list']:
            sprite_rect = projectile['sprite'].get_rect(center=projectile_rect.center)
            screen.blit(projectile['sprite'], sprite_rect)

        # Enemy
        for hitbox in enemy['list']:
            sprite_rect = enemy['sprite'].get_rect(center=hitbox.center)
            screen.blit(enemy['sprite'], sprite_rect)

        # Score Board
        ScoreCount = ScoreBoard.render(f"Score: {player_Score}", True, "White")
        StageCount = ScoreBoard.render(f"Stage: {Stage_name}", True, "White")
        screen.blit(ScoreCount, (22, 10))
        screen.blit(StageCount, (22, 36))

        # Player
        screen.blit(player['character'], player['rect'])

        pygame.display.flip()

# Start Menu State
    elif Current_state == 'start_menu':
        pygame.display.set_caption(f"{GameTitle} {Version}")
        gui['Start_show'] = True

    # Play Background Music
        if current_music != start_menu.backgroundMusic:
            current_music = start_menu.backgroundMusic
            pygame.mixer.music.load(current_music)
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1)

    # Game Title
        Title = GameTitle_text.render(f"{GameTitle}", True, 'White')
        screen.blit(Title, (screen.get_width()//2 - 250, screen.get_height()//2 - 100))

    # Start GUI
        if gui['Start_show']:
            Start_gui = Menu_gui.render("PRESS ENTER TO START", True, 'White')
            Start_gui_rect = Start_gui.get_rect(center=gui['Start'].center)
            screen.blit(Start_gui, Start_gui_rect)

            if now - gui['Last_flicker'] >= gui['Flicker_delay']:
                gui['Last_flicker'] = now
                gui['Flicker'] = not gui['Flicker']

            if gui['Flicker']:
                pygame.draw.rect(screen, 'White', gui['Start'], 2)
            else:
                pygame.draw.rect(screen, 'Black', gui['Start'], 2)

# Loading State
    elif Current_state == 'loading':
        pygame.display.set_caption(f"{GameTitle} {Version}    Loading...")
        screen.fill('Black')

    # Draw The Bar
        fill_width = int(gui['ProgressBar_Width'] * (gui['Loading_progress']/100))
        filled_bar = gui['Loading'].x + 10, gui['Loading'].y + 10, fill_width, gui['Loading'].height - 20
        
        if gui['Loading_progress'] <= 99.5:
            gui['Loading_progress'] += 0.5
        else:
            pygame.time.wait(3000)
            Current_state = 'FirstRound'
            current_stage.RoundWait = pygame.time.get_ticks() + 3000

        pygame.draw.rect(screen, 'White', filled_bar)
        pygame.draw.rect(screen, 'White', gui['Loading'], 2)

# Mission Call State
    elif Current_state == 'FirstRound':
        pygame.display.set_caption(f"{GameTitle} {Version}")
        pygame.mixer.music.stop()
        RoundStartSound = pygame.mixer.Sound('Assets/SFX/roundstart_sfx.mp3')

        Stage_name = type(current_stage).__name__.replace("_", " ")

        screen.fill('Black')
        StageNumber = StageNumber_text.render(f"{Stage_name}", True, 'White')
        MissionName = MissionName_text.render(f"{current_stage.mission_name}", True, 'White')

        screen.blit(StageNumber, (screen.get_width() // 2 - 120, screen.get_height() // 2 - 100))
        screen.blit(MissionName, (screen.get_width() // 2 - 300, screen.get_height() // 2))

        RoundStartSound.set_volume(0.5)
        channel = RoundStartSound.play()

        if now >= current_stage.RoundWait:
            channel = None
            Current_state = 'game'

    elif Is_Victory:
        screen.fill("Black")
        

    pygame.display.flip()
        
pygame.quit()
sys.exit()

# Line 79