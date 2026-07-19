import pygame
import random

class StartMenu:
    backgroundMusic = 'Assets/bgMusic/menu_music.mp3'

    def GUI(self):
        gui = {}

    # Start
        gui['Start'] = pygame.Rect(0, 0, 390, 50)
        gui['Start'].center = (800 // 2, 420)
        gui['Flicker'] = False
        gui['Last_flicker'] = 0
        gui['Flicker_delay'] = 300

    # Loading Bar
        gui['Loading'] = pygame.Rect(0, 0, 400, 50)
        gui['Loading'].center = (800 // 2, 500)
        gui['ProgressBar_Width'] = 380
        gui['Loading_progress'] = 5
        return gui

class Stage_1:
    backgroundMusic = 'Assets/bgMusic/stage1.mp3'
    mission_name = 'Mission 1: The Beginning'
    RoundWait = None

    def Background(self):
        background = pygame.image.load("Assets/Backgrounds/level1_bg.png").convert_alpha()
        background = pygame.transform.scale(background, (800, 600))
        return background

    def Enemies(self):
        enemy = {}
        enemy['sprite'] = pygame.image.load("Assets/Enemies/LowRanked_1.png").convert_alpha()
        enemy['sprite'] = pygame.transform.rotate(enemy['sprite'], 180)
        enemy['sprite'] = pygame.transform.scale(enemy['sprite'], (225, 175))
        enemy['explosion'] = 'Assets/SFX/explosion_sfx1.mp3'
        enemy['rect_width'] = 80
        enemy['rect_height'] = 10
        enemy['spawn_y'] = 0
        enemy['despawn'] = 480
        enemy['speed'] = -1
        enemy['spawn_cd'] = 1500
        enemy['list'] = []
        return enemy
    
    milestone_score = 3

class Stage_2:
    backgroundMusic = 'Assets/bgMusic/stage2.mp3'

    def Background(self):
        background = pygame.image.load("Assets/Backgrounds/level2_bg.png").convert_alpha()
        background = pygame.transform.scale(background, (800, 600))
        return background
    
    def Enemies(self):
        pass