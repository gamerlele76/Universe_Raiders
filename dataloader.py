from Data.StateData import *
from Data.PlayerData import *

# Game Version
GameTitle = "UniverseRaiders"
Version = "a.1.0"

# Load StartMenu Data
start_menu = StartMenu()
gui = start_menu.GUI()

# Stage Data
current_stage = Stage_1()
current_bg = current_stage.Background()
current_music = None

# Player Data
current_char = Character_1()
player = current_char.MainPlayer()
projectile = current_char.create_projectile()

# Enemy Data
enemy = current_stage.Enemies()