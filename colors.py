from datetime import datetime

import pygame
#ЭТУ ХУЙНЮ НАДО ПЕРЕИМЕНОВАТЬ

# ЦВЕТА



DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (100, 100, 100)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
CYAN = (0, 255, 255)

COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, CYAN]
# НЕСКУЧНЫЕ ШРИФТЫ
pygame.init()
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 48)
hint_font = pygame.font.Font(None, 28)



#  LOG (ТИПА ТУДУ)
LOG_FILE = "battle_log.txt"
with open(LOG_FILE, "w") as f:
    f.write("Battle Log\n")
    f.write("=" * 50 + "\n")


def log_action(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] {message}\n")



