import pygame

class Character_1:

    def MainPlayer(self):
        player = {}
        player['character'] = pygame.image.load("Assets/Player_Character/Character_1.png").convert_alpha()
        player['character'] = pygame.transform.scale(player['character'], (150, 150))
        player['x_pos'] = 800 // 2
        player['y_pos'] = 520
        player['rect'] = player['character'].get_rect(center=(player['x_pos'], player['y_pos']))
        player['speed'] = 6
        return player

    def create_projectile(self):
        projectile = {}
        projectile['sprite'] = pygame.image.load("Assets/Player_Character/Projectile_1.png").convert_alpha()
        projectile['sprite'] = pygame.transform.scale(projectile['sprite'], (150, 150))
        projectile['sound'] = 'Assets/SFX/launch_sfx1.mp3'
        projectile['rect_width'] = 22
        projectile['rect_height'] = 26
        projectile['cooldown'] = 300
        projectile['speed'] = 6
        projectile['list'] = []
        return projectile

