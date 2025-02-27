import pygame
import sys

import colors
import fighters

WIDTH, HEIGHT = 1000, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("VSJ Battles")


def wrap_text(text, max_width):
    # split
    words = text.split(' ')
    lines = []
    current_line = ''

    for word in words:
        # Проверяем, не превышает ли текущая строка максимальную ширину
        if colors.font.size(current_line + ' ' + word)[0] <= max_width:
            current_line += ' ' + word
        else:
            lines.append(current_line.strip())
            current_line = word

    if current_line:
        lines.append(current_line.strip())

    return lines


class GameState:
    MAIN_MENU = 0
    SELECT_MODE = 1
    SELECT_FIGHTERS = 2
    BATTLE = 3
    ABILITY_SELECT = 4
    TARGET_SELECT = 5
    GAME_OVER = 6


class Game:
    def __init__(self):
        self.state = GameState.MAIN_MENU
        self.players = [[], []]
        self.current_player = 0
        self.selected = []
        self.battle_fighters = []
        self.current_turn = 0
        self.log = []
        self.available_targets = []
        self.ability_number = None
        self.winner = None
        self.hover_index = 0
        self.selection_grid = [[0, 1, 2], [3, 4, 5]]
        self.mode = 2
        self.mode_hover = 0
        self.confirm_highlight = False
        self.fighters_data = fighters.fighters

    def reset_selections(self):
        for f in self.battle_fighters:
            f.selected = False
            f.target = False
            f.is_selected = False

    def check_winner(self):

        p1_alive = any(f.dead == False for f in self.players[0])
        p2_alive = any(f.dead == False for f in self.players[1])

        if not p1_alive:
            return 2
        if not p2_alive:
            return 1
        return None


    def draw_main_menu(self):
        screen.fill(colors.DARK_GRAY)
        text = colors.title_font.render("MAIN MENU", True, colors.WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 100))

        pygame.draw.rect(screen, colors.GREEN, (WIDTH // 2 - 100, HEIGHT // 2 - 25, 200, 50))
        text = colors.font.render("Start Game", True, colors.WHITE)
        screen.blit(text, (WIDTH // 2 - 70, HEIGHT // 2 - 15))

        hint_text = colors.hint_font.render("Press ENTER to start", True, colors.LIGHT_GRAY)
        screen.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT - 100))

    def draw_select_mode(self):
        screen.fill(colors.DARK_GRAY)
        text = colors.title_font.render("Select Game Mode", True, colors.WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 100))

        color_2 = colors.GREEN if self.mode_hover == 0 else colors.LIGHT_GRAY
        pygame.draw.rect(screen, color_2, (WIDTH // 2 - 150, 250, 300, 60))
        text = colors.font.render("2 Fighters", True, colors.WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 270))

        color_3 = colors.GREEN if self.mode_hover == 1 else colors.LIGHT_GRAY
        pygame.draw.rect(screen, color_3, (WIDTH // 2 - 150, 350, 300, 60))
        text = colors.font.render("3 Fighters", True, colors.WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 370))

        hint_text = colors.hint_font.render("Use UP/DOWN to choose, ENTER to confirm", True, colors.LIGHT_GRAY)
        screen.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT - 100))

    def draw_selection(self):
        screen.fill(colors.DARK_GRAY)
        text = colors.title_font.render(f"Player {self.current_player + 1}: Choose {self.mode} Fighters", True,
                                        colors.WHITE)
        screen.blit(text, (50, 50))

        for i, fighter in enumerate(self.fighters_data):
            row = i // 3
            col = i % 3
            fighter.pos = (50 + col * 350, 150 + row * 300)
            fighter.is_selected = fighter in self.selected
            fighter.draw(screen)

            if fighter in self.selected:
                pygame.draw.rect(screen, colors.YELLOW, (fighter.pos[0] - 8, fighter.pos[1] - 8,
                                                         fighter.size + 16, fighter.size + 16), 5)

            if self.selection_grid[row][col] == self.hover_index:
                pygame.draw.rect(screen, colors.GREEN, (fighter.pos[0] - 8, fighter.pos[1] - 8,
                                                        fighter.size + 16, fighter.size + 16), 5)

        text = colors.font.render("Selected: " + ", ".join([f.name for f in self.selected]), True, colors.WHITE)
        screen.blit(text, (50, HEIGHT - 100))

        hint_text = colors.hint_font.render("Use ARROWS to navigate, ENTER to select", True, colors.LIGHT_GRAY)
        screen.blit(hint_text, (50, HEIGHT - 10))

    def draw_battle(self):
        screen.fill(colors.DARK_GRAY)
        player_num = (self.current_turn // self.mode) + 1
        fighter = self.battle_fighters[self.current_turn]
        text = colors.title_font.render(f"Player {player_num}'s Turn: {fighter.name}", True, colors.WHITE)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 20))

        # allies
        for i, fighter in enumerate(self.players[0]):
            fighter.pos = (200 + i * (WIDTH // (self.mode + 1)), HEIGHT - 200)
            fighter.draw(screen)

        # enemies
        for i, fighter in enumerate(self.players[1]):
            fighter.pos = (200 + i * (WIDTH // (self.mode + 1)), 100)
            fighter.draw(screen)

        # Лог
        y = HEIGHT - 160
        for entry in self.log[-5:]:
            text = colors.font.render(entry, True, colors.WHITE)
            screen.blit(text, (60, y))
            y += 30

        hint_text = colors.hint_font.render("Press ENTER to choose ability", True, colors.LIGHT_GRAY)
        screen.blit(hint_text, (50, HEIGHT - 100))

    def draw_ability_select(self):
        screen.fill(colors.DARK_GRAY)
        fighter = self.battle_fighters[self.current_turn]

        # Заголовок
        text = colors.title_font.render(f"Choose Ability for {fighter.name}:", True, colors.WHITE)
        screen.blit(text, (50, 50))

        # Отрисовка списка способностей
        for i in range(len(fighter.abilities)):
            ability = fighter.abilities[i]
            bg_color = colors.GREEN if i == self.hover_index else colors.LIGHT_GRAY
            pygame.draw.rect(screen, bg_color, (100, 150 + i * 80, 800, 60))

            # Отображение названия способности и кулдауна
            cooldown_text = f"{ability.name} (Cooldown: {ability.cooldown}/{ability.max_cooldown})"
            text = colors.font.render(cooldown_text, True, colors.WHITE)
            screen.blit(text, (120, 170 + i * 80))

        # Отображение описания выбранной способности
        if fighter.abilities:
            selected_ability = fighter.abilities[self.hover_index]
            description_text = selected_ability.description
            description_lines = wrap_text(description_text, 500)  # Перенос текста на несколько строк

            # Отображение описания
            y_offset = 500
            for line in description_lines:
                text = colors.font.render(line, True, colors.WHITE)
                screen.blit(text, (100, y_offset))
                y_offset += 30

        hint_text = colors.hint_font.render("Use UP/DOWN to choose, ENTER to confirm", True, colors.LIGHT_GRAY)
        screen.blit(hint_text, (100, HEIGHT - 100))

    def draw_target_select(self):
        screen.fill(colors.DARK_GRAY)
        attacker = self.battle_fighters[self.current_turn]
        current_ability = attacker.abilities[self.ability_number]

        # Заголовок
        text = colors.title_font.render(f"Choose Target for {attacker.name}:", True, colors.WHITE)
        screen.blit(text, (50, 10))

        # Описание способности
        description_text = current_ability.description
        description_lines = wrap_text(description_text, 900)
        y_offset = 350
        for line in description_lines:
            text = colors.font.render(line, True, colors.WHITE)
            screen.blit(text, (50, y_offset))
            y_offset += 25

        # Информация о типе и количестве целей
        target_info = f"Type: {current_ability.target_type}, Targets: {current_ability.target_amount}"
        text = colors.font.render(target_info, True, colors.CYAN)
        screen.blit(text, (50, y_offset))
        y_offset += 30

        # Бойцы текущего игрока внизу
        for i, fighter in enumerate(self.players[0]):
            fighter.pos = (200 + i * (WIDTH // (self.mode + 1)), HEIGHT - 250)
            fighter.draw(screen)

        # Бойцы противника сверху
        for i, fighter in enumerate(self.players[1]):
            fighter.pos = (200 + i * (WIDTH // (self.mode + 1)), 200)
            fighter.draw(screen)

        # Подсветка стрелкой
        if self.available_targets:
            target_index = self.available_targets[self.hover_index % len(self.available_targets)]
            target = self.battle_fighters[target_index]
            arrow_color = colors.RED if self.confirm_highlight else colors.YELLOW

            # Позиция стрелки
            if target in self.players[0]:  # Боец внизу
                arrow_x = target.pos[0] + target.size // 2
                arrow_y = target.pos[1] - 30
            else:  # Боец сверху
                arrow_x = target.pos[0] + target.size // 2
                arrow_y = target.pos[1] + target.size + 10

            # Отрисовка стрелки
            pygame.draw.polygon(screen, arrow_color, [
                (arrow_x, arrow_y),
                (arrow_x - 10, arrow_y - 20),
                (arrow_x + 10, arrow_y - 20)
            ])

        # Подсказка
        hint_text = colors.hint_font.render("LEFT/RIGHT to choose, ENTER to confirm", True, colors.LIGHT_GRAY)
        screen.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT - 40))

    def draw_game_over(self):
        screen.fill(colors.DARK_GRAY)
        text = colors.title_font.render(f"PLAYER {self.winner} WINS!", True,
                                        colors.GREEN if self.winner == 1 else colors.RED)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 - 50))

        hint_text = colors.hint_font.render("Press ESC to exit", True, colors.LIGHT_GRAY)
        screen.blit(hint_text, (WIDTH // 2 - hint_text.get_width() // 2, HEIGHT // 2 + 50))


# Инициализация игры
game = Game()
clock = pygame.time.Clock()

# Главный цикл
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if game.state == GameState.MAIN_MENU:
                pygame.mixer.music.load('soundtrack.wav')
                pygame.mixer.music.play(-1)
                if event.key == pygame.K_RETURN:
                    game.state = GameState.SELECT_MODE
                    colors.log_action("Game started")

            elif game.state == GameState.SELECT_MODE:
                if event.key == pygame.K_UP:
                    game.mode_hover = (game.mode_hover - 1) % 2
                elif event.key == pygame.K_DOWN:
                    game.mode_hover = (game.mode_hover + 1) % 2
                elif event.key == pygame.K_RETURN:
                    game.mode = 2 if game.mode_hover == 0 else 3
                    game.state = GameState.SELECT_FIGHTERS
                    colors.log_action(f"Selected mode: {game.mode} fighters")

            elif game.state == GameState.SELECT_FIGHTERS:
                if event.key == pygame.K_UP:
                    game.hover_index = (game.hover_index - 3) % 6
                elif event.key == pygame.K_DOWN:
                    game.hover_index = (game.hover_index + 3) % 6
                elif event.key == pygame.K_LEFT:
                    game.hover_index = (game.hover_index - 1) % 6
                elif event.key == pygame.K_RIGHT:
                    game.hover_index = (game.hover_index + 1) % 6
                elif event.key == pygame.K_RETURN:
                    selected_fighter = game.fighters_data[game.hover_index]
                    if len(game.selected) < game.mode and selected_fighter not in game.selected:
                        game.selected.append(selected_fighter)
                        game.fighters_data[game.hover_index] = selected_fighter
                        game.fighters_data[game.hover_index].player = game.current_player
                        game.fighters_data[game.hover_index].index = game.hover_index
                        colors.log_action(f"Player {game.current_player + 1} selected {selected_fighter.name}")

                if len(game.selected) == game.mode:
                    game.players[game.current_player] = game.selected.copy()
                    game.selected.clear()
                    game.current_player += 1
                    if game.current_player == 2:
                        game.state = GameState.BATTLE
                        game.battle_fighters = game.players[0] + game.players[1]
                        for i in range(len(game.battle_fighters)):
                            game.battle_fighters[i].index = i
                        game.reset_selections()
                        colors.log_action("Battle started")

            elif game.state == GameState.BATTLE:
                for i in game.battle_fighters:
                    i.draw(screen)
                if event.key == pygame.K_RETURN:
                    current_fighter = game.battle_fighters[game.current_turn]
                    game.current_player = current_fighter.player
                    current_fighter.check_conditions()
                    if (current_fighter.dead == True):
                        game.current_turn += 1
                    for ability in current_fighter.abilities:
                        ability.performer = game.current_turn
                    if current_fighter.dead == False:
                        game.reset_selections()
                        game.draw_battle()
                        game.state = GameState.ABILITY_SELECT
                        game.hover_index = 0

            elif game.state == GameState.ABILITY_SELECT:
                for i in game.battle_fighters:
                    i.draw(screen)
                if event.key == pygame.K_UP:
                    game.hover_index = (game.hover_index - 1) % 3
                elif event.key == pygame.K_DOWN:
                    game.hover_index = (game.hover_index + 1) % 3
                elif event.key == pygame.K_RETURN:
                    game.ability_number = game.hover_index
                    current_ability = current_fighter.abilities[game.ability_number]
                    if (current_ability.cooldown > 0):
                        hint_text = colors.hint_font.render("Invalid Ability: cooldown", True, colors.RED)
                        screen.blit(hint_text, (50, HEIGHT - 10))
                        game.draw_ability_select()


                    elif (current_ability.cooldown == 0):
                        game.state = GameState.TARGET_SELECT
                        game.hover_index = 0


            elif game.state == GameState.TARGET_SELECT:
                game.available_targets = current_ability.get_available_targets(game.mode, game.current_player)
                if (current_ability.target_amount == "massive" or current_ability.target_amount == "self only"):
                    targets = [game.battle_fighters[i] for i in game.available_targets]
                    if (event.key == pygame.K_RETURN):
                        current_ability.use_ability(targets)
                        game.winner = game.check_winner()
                        if game.winner:
                            game.state = GameState.GAME_OVER
                        else:
                            game.current_turn = (game.current_turn + 1) % (game.mode * 2)
                            while game.battle_fighters[game.current_turn].health <= 0:
                                game.current_turn = (game.current_turn + 1) % (game.mode * 2)
                            game.state = GameState.BATTLE
                else:
                    if event.key == pygame.K_LEFT:
                        game.hover_index = (game.hover_index - 1) % len(game.available_targets)
                    elif event.key == pygame.K_RIGHT:
                        game.hover_index = (game.hover_index + 1) % len(game.available_targets)
                    elif event.key == pygame.K_RETURN:

                        if game.available_targets:
                            game.confirm_highlight = True
                            game.draw_target_select()
                            pygame.display.flip()
                            pygame.time.delay(150)
                            game.confirm_highlight = False

                            target_index = game.available_targets[game.hover_index]
                            target = game.battle_fighters[target_index]
                            current_ability.use_ability([target])
                            game.winner = game.check_winner()
                            if game.winner:
                                game.state = GameState.GAME_OVER
                            else:
                                game.current_turn = (game.current_turn + 1) % (game.mode * 2)
                                while game.battle_fighters[game.current_turn].health <= 0:
                                    game.current_turn = (game.current_turn + 1) % (game.mode * 2)
                                game.state = GameState.BATTLE


            elif game.state == GameState.GAME_OVER:
                if event.key == pygame.K_ESCAPE:
                    running = False

    screen.fill(colors.DARK_GRAY)

    if game.state == GameState.MAIN_MENU:
        game.draw_main_menu()
    elif game.state == GameState.SELECT_MODE:
        game.draw_select_mode()
    elif game.state == GameState.SELECT_FIGHTERS:
        game.draw_selection()
    elif game.state == GameState.BATTLE:
        game.draw_battle()
    elif game.state == GameState.ABILITY_SELECT:
        game.draw_ability_select()
    elif game.state == GameState.TARGET_SELECT:
        game.draw_target_select()
    elif game.state == GameState.GAME_OVER:
        game.draw_game_over()

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
