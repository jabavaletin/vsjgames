import pygame
from pyexpat.errors import messages

import colors
from colors import log_action


class Ability:
    def __init__(self, name, performer, function, target_amount, target_type, max_cooldown, cooldown,
                 description="TEST"):
        self.name = name
        self.performer = performer
        self.function = function
        self.max_cooldown = max_cooldown
        self.cooldown = cooldown
        self.target_type = target_type
        self.target_amount = target_amount
        self.description = description

    def get_available_targets(self, mode, current_player):
        allies = list()
        enemies = list()
        if (mode == 2):
            allies = [0, 1]
            enemies = [2, 3]
        else:
            allies = [0, 1, 2]
            enemies = [3, 4, 5]
        if (current_player == 0):
            pass
        else:
            allies, enemies = enemies, allies

        if (self.target_type == "self only"):
            return [self.performer]
        if (self.target_type == "enemy"):
            return enemies
        else:
            return allies

    def use_ability(self, targets):
        self.function(targets, self.performer)
        self.cooldown = self.max_cooldown


print()


# ФУНКЦИИ
def cause_damage(target, performer, damage, poisoning=0, ignore_invincible=False):
    if (target.invincible == True and ignore_invincible == False):
        message = f"{target.name} is invincible, damage reduces to 0!"
        return
    else:
        if (poisoning != 0):
            target.poisoned = poisoning
        target.health -= damage
        if (target.health <= 0):
            if (target.patience > 0):
                target.health = 1
            elif target.lyudmurik_summon == 0:
                Lyudmurik.abilities[0].performer = performer
                target = Lyudmurik
                message = "Lyudmurik replaces Gobzavr"
                colors.log_action(message)
            else:
                target.health = 0
                target.dead = True


def heal(target, performer, healing_power):
    if (target.poisoned > 0):
        target.poisoned = 0
    else:
        target.health += healing_power
        if (target.health > target.max_health):
            target.health = target.max_health
        if (target.health > 0):
            target.dead = False


def test_ability_func_single_enemy(targets, performer):
    damage = 20
    for target in targets:
        cause_damage(target, performer, damage, 0, False)
    message = f"{fighters[performer].name} uses test ability for enemy {targets[0].name}"
    colors.log_action(message)


def test_ability_func_single_ally(targets, performer):
    healing_power = 10
    for target in targets:
        heal(target, performer, healing_power)
    message = f"{fighters[performer].name} uses test ability for enemy {targets[0].name}"
    colors.log_action(message)


def punch_of_lion_func(targets, performer):
    damage = 15
    for target in targets:
        cause_damage(target, performer, damage, 0, False)
    message = f"{fighters[performer].name} beats {targets[0].name} with punch of lion. HYCH HYCH HYCH!!!"
    colors.log_action(message)


def rags_func(targets, performer):
    for target in targets:
        target.invincible = 1
    message = f"Vanomas lays down on rags, making himself invincible."
    colors.log_action(message)


def beer_earthquake_func(targets, performer):
    damage = 40
    for target in targets:
        cause_damage(target, performer, damage, 0, False)
    message = f"Vanomas uses beer earthquake, causing Heavy damage for all enemies!!!"
    colors.log_action(message)


def test_ability_func_massive_enemies(targets, performer):
    damage = 10
    for target in targets:
        cause_damage(target, performer, damage, 0, False)
    message = f"{fighters[performer].name} uses mass ability for all enemies"
    colors.log_action(message)


def test_ability_func_massive_allies(targets, performer):
    healing_power = 10
    for target in targets:
        heal(target, performer, healing_power)
    message = f"{fighters[performer].name} uses mass ability for all allies"
    colors.log_action(message)


def patience_func(targets, performer):
    for target in targets:
        target.patience = 2
    message = f"ozon671 TERPIT!!!"
    colors.log_action(message)


def wall_crushing_func(targets, performer):
    damage = 70
    for target in targets:
        cause_damage(target, performer, damage, 0, True)
    message = f"ozon671games beat {targets[0].name} like a wall"
    colors.log_action(message)


def brepsi_func(targets, performer):
    for target in targets:
        heal(target, performer, 5)
    message = f"{targets[0].name} opened the can given by ozon671games. PFFFFFF CHKKKKKKK MMM... What a delicous taste of Brepsi! Oh!"
    colors.log_action(message)


def poisonous_breath_func(targets, performer):
    damage = 0
    for target in targets:
        cause_damage(target, performer, damage, 2)
    message = f"Saveliev breathes in {targets[0].name} face, applying the poison!"
    colors.log_action(message)


def ebatoria_func(targets, performer):
    damage = 20
    for target in targets:
        cause_damage(target, performer, damage, 3)
    message = f"Saveliev attacks all enemies with heavy damage. I'm so fucked up about this Ebatoria!"
    colors.log_action(message)


def mayonnaise_mask_func(targets, performer):
    healing_power = 30
    for target in targets:
        heal(target, performer, healing_power)
    message = f"Saveliev uses mayonaise mask, healing himself."
    colors.log_action(message)


def mormyshka_func(targets, performer):
    damage = 0
    for target in targets:
        cause_damage(target, performer, 0, 1)
        for i in target.abilities:
            if (i.name != 'Mormyshka'):
                i.cooldown -= 1
    message = f"Simonov drinks mormyshka!"
    colors.log_action(message)


def curtain_tear_func(targets, performer):
    damage = 20
    for target in targets:
        cause_damage(target, performer, damage)
    message = f"Simonov tears curtain just over the {targets[0].name}!, inflicting {damage} damage"
    colors.log_action(message)


def door_knocking_func(targets, performer):
    damage = 20
    for target in targets:
        cause_damage(target, performer, damage, 0, True)
    target.invincible = 0
    message = (f"Simonov knocking in the door. {targets[0].name}, this is Sergey.")
    colors.log_action(message)


def wardrobe_func(targets, performer):
    for target in targets:
        target.invincible = 1
    message = (f"Tolyan uses wardrobe to hide {targets[0].name}.")
    colors.log_action(message)


def pikkolini_func(targets, performer):
    healing_power = 30
    for target in targets:
        heal(target, performer, healing_power)
    message = f"Tolyan heals allies with pikkolini"
    colors.log_action(message)


def dance_func(targets, performer):
    damage = 5
    for target in targets:
        cause_damage(target, performer, damage)
    message = f"Tolyan performes strange dance, causing {damage} damage for all enemies."
    colors.log_action(message)


def spit_func(targets, performer):
    damage = 10
    for target in targets:
        cause_damage(target, performer, damage, 1)
    message = f"Gobzavr spits in {targets[0].name}'s mounth, causing {damage} damage and inflicting poison."
    colors.log_action(message)


def trousers_func(targets, performer):
    for target in targets:
        target.lyudmurik_summoning = 0
    message = f"Gobzavr picks up Lyudmurik's trousers to summon her!"
    colors.log_action(message)


def anekdot_func(targets, performer):
    damage = 10
    for target in targets:
        cause_damage(target, performer, damage, 0, True)
    message = f"Lyudmurik tells an anecdot, inflicting {damage} to {targets[0].name}."
    colors.log_action(message)


# Vanomas's abilities
punch_of_lion = Ability("PUNCH OF LION", 0, punch_of_lion_func, "single", "enemy", 0, 0,
                        "HYCH HYCH HYCH!!! Single-target attack")
rags = Ability("RAGS", 0, rags_func, "single", "self only", 4, 0,
               "Laying on rags making Vanomas invincible")
beer_earthquake = Ability("BEER EARTHQUAKE", 0, beer_earthquake_func, "massive", "enemy", 5, 0,
                          "Heavy massive damage from beer cans")
# ozon671games' abilities
patience = Ability("Patience", 0, patience_func, "single", "self only", 5, 2,
                   "HP cannot be less then 1 for next 2 turns")
wall_crushing = Ability("Wall crushing", 0, wall_crushing_func, "single", "enemy", 4, 4,
                        "Furious strike. Ignore invincible")
brepsi = Ability("Brepsi", 0, brepsi_func, "single", "ally", 0, 0,
                 "Heal 5 hp for chosen ally. ")
# Saveliev's abilities
mayonnaise_mask = Ability("Mayonaise mask", 0, mayonnaise_mask_func, "single", "self only", 1, 0)
ebatoria = Ability("Ebatoria", 0, ebatoria_func, "massive", "enemy", 3, 3)
poisonous_breath = Ability("Poisonous breath", 0, poisonous_breath_func, "single", "enemy", 0, 0)

# Simonov's abilities
mormyshka = Ability("Mormyshka", 0, mormyshka_func, "single", "self only", 1, 1,
                    "Strong poison. Reduces cooldown, but dangerous.")
door_knocking = Ability("Door knocking", 0, door_knocking_func, "single", "enemy", 3, 3,
                        "Weak attack, but ignores invincible.")
curtain_tear = Ability("Curtain tear", 0, curtain_tear_func, "single", "enemy", 0, 0,
                       "Single attack")

# Tolyan's abilities
pikkolini = Ability("Pikkolini", 0, pikkolini_func, "massive", "ally", 3, 3,
                    "Massive heal")
dance = Ability("Dance", 0, dance_func, "single", "enemy", 0, 0,
                "Weal attack for single enemy")
wardrobe = Ability("Wardrobe", 0, wardrobe_func, "single", "ally", 1, 1,
                   "Making one ally invincible for 1 turn")

# Gobzavr's abilities
spit = Ability("Spit", 0, spit_func, "single", "enemy", 0, 0,
               "single attack, poisonous")
trousers = Ability("Trousers", 0, trousers_func, "single", "self only", 1000, 0,
                   "summoning Lyudmurik. In 3 turns, if Gobzavr dies, Lyudmurik will replace him")

# Lydmurik abilities
anekdot = Ability("Anekdot", 0, anekdot_func, "single", "enemy", 0, 0,
                  "Single attack. Weak, but ignore invincible.")

# Test abilities
test_ally_ability = Ability("TEST SINGLE ABILITY FOR ENEMY", 0, test_ability_func_single_enemy, "single", "enemy", 0, 0)
test_enemy_ability = Ability("TEST SINGLE ABILITY FOR ALLY", 0, test_ability_func_single_ally, "single", "ally", 2, 0)
test_massive_ally_ability = Ability("TEST MASSIVE ABILITY FOR ALLIES", 0, test_ability_func_massive_allies,
                                    "massive", "ally", 2, 0)
test_massive_enemy_ability = Ability("TEST MASSIVE ABILITY FOR ENEMIES", 0, test_ability_func_massive_enemies,
                                     "massive", "enemy", 3, 0)


class Fighter:
    def __init__(self, name, color, max_health, pos, abilities, normal_sprite, ability_sprite, dead_sprite, player=-1,
                 index=-1):
        self.name = name  # name
        self.index = index  # index in main.game.battle_fighter
        self.player = player  # index of player
        self.max_health = max_health  # NUFF SAID
        self.health = self.max_health  # NUFF SAID
        self.dead = False
        self.color = color  # NUFF SAID
        self.pos = pos  # Position for drawing
        self.abilities = abilities  # list of abilities (ability-type)
        self.size = 80  # size for drawing
        self.selected = False
        self.target = False
        self.is_selected = False
        self.cooldowns = ()
        self.poisoned = 0
        self.invincible = 0
        self.patience = 0
        self.lyudmurik_summon = -1

        # sprites
        self.normal_sprite = self.load_and_scale_sprite(normal_sprite)
        self.ability_sprite = self.load_and_scale_sprite(ability_sprite)
        self.dead_sprite = self.load_and_scale_sprite(dead_sprite)

    def load_and_scale_sprite(self, sprite_path):

        if sprite_path:
            sprite = pygame.image.load(sprite_path)
            if sprite.get_width() > self.size or sprite.get_height() > self.size:
                scale_factor = min(self.size / sprite.get_width(), self.size / sprite.get_height())
                new_size = (int(sprite.get_width() * scale_factor), int(sprite.get_height() * scale_factor))
                sprite = pygame.transform.scale(sprite, new_size)
            return sprite
        return None

    def draw(self, surface):
        border_width = 5
        border_color = colors.RED if self.target else \
            colors.GREEN if self.selected else \
                colors.YELLOW if self.is_selected else colors.LIGHT_GRAY

        pygame.draw.rect(surface, border_color,
                         (self.pos[0] - border_width, self.pos[1] - border_width,
                          self.size + 2 * border_width, self.size + 2 * border_width),
                         border_width)

        if self.dead and self.dead_sprite:
            sprite = self.dead_sprite
        elif self.selected and self.ability_sprite:
            sprite = self.ability_sprite
        else:
            sprite = self.normal_sprite if self.normal_sprite else None

        if sprite:
            sprite_rect = sprite.get_rect(center=(self.pos[0] + self.size // 2, self.pos[1] + self.size // 2))
            surface.blit(sprite, sprite_rect)
        else:
            pygame.draw.rect(surface, self.color, (*self.pos, self.size, self.size))

        text = colors.font.render(f"{self.name} ({self.health} HP)", True, colors.WHITE)
        surface.blit(text, (self.pos[0] - 10, self.pos[1] - 30))

        pygame.draw.rect(surface, colors.LIGHT_GRAY, (self.pos[0], self.pos[1] + self.size + 5, self.size, 5))
        pygame.draw.rect(surface, colors.GREEN, (self.pos[0], self.pos[1] + self.size + 5,
                                                 self.size * (self.health / self.max_health), 5))

        status_y_offset = self.pos[1] + self.size + 20
        if self.poisoned > 0:
            text = colors.font.render(f"Poisoned {self.poisoned}", True, colors.GREEN)
            surface.blit(text, (self.pos[0], status_y_offset))
            status_y_offset += 20

        if self.invincible > 0:
            text = colors.font.render(f"Invincible {self.invincible}", True, colors.CYAN)
            surface.blit(text, (self.pos[0], status_y_offset))
            status_y_offset += 20

        if self.patience > 0:
            text = colors.font.render(f"Patience {self.patience}", True, colors.YELLOW)
            surface.blit(text, (self.pos[0], status_y_offset))
            status_y_offset += 20

        if (self.dead == True):
            text = colors.font.render("Dead", True, colors.PURPLE)
            surface.blit(text, (self.pos[0], status_y_offset))

    def check_conditions(self):
        if (self.poisoned > 0):
            self.poisoned -= 1
            self.health -= 15
        for i in self.abilities:
            i.cooldown -= 1
            i.cooldown = max(i.cooldown, 0)
        if (self.health <= 0):
            self.dead = True
            self.health = 0
        if (self.patience > 0):
            self.patience -= 1
        if (self.lyudmurik_summon > 0):
            self.lyudmurik_summon -= 1
        if (self.invincible > 0):
            self.invincible -= 1


fighters = [
    Fighter("VANOMAS", colors.YELLOW, 100, 0,
            [punch_of_lion, rags, beer_earthquake],
            'sprites/vanomas_normal.jpg', 'sprites/vanomas_ability.jpg', 'sprites/vanomas_dead.jpg'),

    Fighter("ozon671games", colors.BLUE, 120, 1,
            [brepsi, patience, wall_crushing],
            'sprites/ozon671games_normal.jpg', 'sprites/ozon671games_ability.jpg', 'sprites/ozon671games_dead.jpg'),

    Fighter("Saviliev", colors.RED, 150, 2,
            [poisonous_breath, mayonnaise_mask, ebatoria],
            'sprites/saveliev_normal.jpg', 'sprites/saveliev_ability.jpg', 'sprites/saveliev_dead.jpg'),

    Fighter("Simonov", colors.WHITE, 100, 3,
            [mormyshka, curtain_tear, door_knocking],
            'sprites/simonov_normal.jpg', 'sprites/simonov_ability.jpg', 'sprites/simonov_dead.jpg'),

    Fighter("Tolyan", colors.CYAN, 90, 4,
            [dance, pikkolini, wardrobe],
            'sprites/tolyan_normal.jpg', 'sprites/tolyan_ability.jpg', 'sprites/tolyan_dead.jpg'),

    Fighter("Gobzavr", colors.PURPLE, 80, 5,
            [spit, trousers],
            'sprites/gobzavr_normal.jpg', 'sprites/gobzavr_ability.jpg', 'sprites/gobzavr_dead.jpg')]

Lyudmurik = Fighter("Lyudmurik", colors.BLUE, 50, 6,
                    [anekdot],
                    'sprites/gobzavr_normal.jpg', 'sprites/gobzavr_ability.jpg', 'sprites/gobzavr_dead.jpg')

fighters[0].abilities[0].performer = 0
fighters[0].abilities[1].performer = 0
fighters[0].abilities[2].performer = 0

fighters[1].abilities[0].performer = 1
fighters[1].abilities[1].performer = 1
fighters[1].abilities[2].performer = 1

fighters[2].abilities[0].performer = 2
fighters[2].abilities[1].performer = 2
fighters[2].abilities[2].performer = 2

fighters[3].abilities[0].performer = 3
fighters[3].abilities[1].performer = 3
fighters[3].abilities[2].performer = 3

fighters[4].abilities[0].performer = 4
fighters[4].abilities[1].performer = 4
fighters[4].abilities[2].performer = 4

fighters[5].abilities[0].performer = 5
fighters[5].abilities[1].performer = 5
