import pygame
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
import random

from useful_functions import *

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
game_display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.display.set_caption("Hangbird")
Icon = pygame.image.load(
    r"c:\Users\ofir1\OneDrive\שולחן העבודה\Hangbird game\sprites\hangman phases\phase 6.png"
)
pygame.display.set_icon(Icon)

bg_image = pygame.image.load(
    r"c:\Users\ofir1\OneDrive\שולחן העבודה\Hangbird game\sprites\green fields.png"
)

the_word, hidden_word = secret_word_generator()
wrong_letters_list = []

pygame.mixer.init()
pygame.init()


class Player(pygame.sprite.Sprite):
    """Creates the player entity and updates his movement

    Args:
        pygame (module): A set of Python modules designed for writing games
    """

    def __init__(self):
        """Creates the player entity"""
        super().__init__()
        self.surf = pygame.image.load(
            r"c:\Users\ofir1\OneDrive\שולחן העבודה\Hangbird game\sprites\Hbird7.png"
        ).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        """Updates player movement

        Args:
            pressed_keys (ScancodeWrapper): The keys pressed to move the player
        """
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH


class Obstacle(pygame.sprite.Sprite):
    """The obstacles that stand in the way

    Args:
        pygame (module): A set of Python modules designed for writing games
    """

    # The distance between the middle of the gap between the two obstacles and the middle of an obstacle
    SPACE_TO_OBSTACLE = 360
    gap_center = (SCREEN_WIDTH + 400, random.randint(172, SCREEN_HEIGHT - 172))

    def __init__(self, obstacle_position):
        """Creates the obstacles"""
        super().__init__()
        self.surf = pygame.image.load(
            r"c:\Users\ofir1\OneDrive\שולחן העבודה\Hangbird game\sprites\obstacles\%s.png"
            % obstacle_position
        ).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)

    def update(self):
        """Moves the obstacle and kills it when it leaves the screen."""
        self.rect.move_ip(-5, 0)
        if self.rect.right <= 0:
            self.kill()


class LowerObstacle(Obstacle):
    """The lower obstacle that stands in the way

    Args:
        Obstacle (type): The obstacles that stand in the way
    """

    def __init__(self):
        """Creates the lower obstacle"""
        super().__init__("lower")
        self.rect = self.surf.get_rect(
            # Moves the center of the obstacle away from the center of the gap by 360 units (SPACE_TO_OBSTACLE)
            center=tuple(
                map(
                    lambda a, b: a + b,
                    Obstacle.gap_center,
                    (0, Obstacle.SPACE_TO_OBSTACLE),
                )
            )
        )

    def update(self):
        """Moves the lower obstacle and kills it when it leaves the screen."""
        super().update()


class UpperObstacle(Obstacle):
    """The upper obstacle that stands in the way

    Args:
        Obstacle (type): The obstacles that stand in the way
    """

    def __init__(self):
        """Creates the upper obstacle"""
        super().__init__("upper")
        self.rect = self.surf.get_rect(
            # Moves the center of the obstacle away from the center of the gap by 360 units (SPACE_TO_OBSTACLE)
            center=tuple(
                map(
                    lambda a, b: a - b,
                    Obstacle.gap_center,
                    (0, Obstacle.SPACE_TO_OBSTACLE),
                )
            )
        )

        Obstacle.gap_center = (
            SCREEN_WIDTH + 400,
            random.randint(75, SCREEN_HEIGHT - 75),
        )

    def update(self):
        """Moves the upper obstacle and kills it when it leaves the screen."""
        super().update()


class Letter(ColoredLetter):
    """The letters that need to be collected

    Args:
        ColoredLetter (type): Creates letters and colors them
    """

    wrong_letter_sound = pygame.mixer.Sound(
        r"c:\Users\ofir1\OneDrive\שולחן העבודה\Hangbird game\music\wrong letter + collision.mp3"
    )
    correct_letter_sound = pygame.mixer.Sound(
        r"c:\Users\ofir1\OneDrive\שולחן העבודה\Hangbird game\music\correct letter + powerup.mp3"
    )
    the_abc = [
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "H",
        "I",
        "J",
        "K",
        "L",
        "M",
        "N",
        "O",
        "P",
        "Q",
        "R",
        "S",
        "T",
        "U",
        "V",
        "W",
        "X",
        "Y",
        "Z",
    ]
    vowel_letters = ["A", "E", "I", "O", "U"]
    letter_center = (
        random.randint(SCREEN_WIDTH + 120, SCREEN_WIDTH + 230),
        random.randint(60, SCREEN_HEIGHT - 60),
    )

    def __init__(self):
        """Creates the letters"""
        if len(Letter.vowel_letters) > 0:
            # At start, the chance of a vowel letter is 25/84 (29.76%)
            self.random_letter = random.choice(
                random.choice(
                    [
                        Letter.vowel_letters,
                    ]
                    + [Letter.the_abc] * 4
                )
            )
        else:
            self.random_letter = random.choice(Letter.the_abc)
        random_color = random.choice(
            ["orange", "yellow", "cyan", "blue", "purple", "pink"]
        )
        super().__init__(self.random_letter, random_color)
        self.rect = self.surf.get_rect(center=Letter.letter_center)

    def update(self):
        """Moves the letters and updates the results according to the letters collected."""
        self.rect.move_ip(-5, 0)
        if (self.rect.right <= 0) or (self.random_letter not in Letter.the_abc):
            self.kill()
        if pygame.sprite.collide_rect(player, self):
            self.kill()
            if self.random_letter in the_word:
                self.correct_letter_sound.play()
                # Saves the indexes of the letter in the secret word
                right_letter_indexes = [
                    char[0]
                    for char in enumerate(the_word)
                    if self.random_letter == char[1]
                ]
                # Copies the indexes of the hidden word to the secret word
                for index in right_letter_indexes:
                    hidden_word[index] = self.random_letter
                # Updates the hidden word
                HiddenLetter.hidden_letter_horizontal_ip = (
                    SCREEN_WIDTH / 2 - (len(the_word) - 1) * 20
                )
                update_message(
                    hidden_letters,
                    hidden_word,
                    HiddenLetter,
                    game_progression_objects,
                    "right green",
                )
            else:
                self.wrong_letter_sound.play()
                hangman.update()
                wrong_letters_list.append(self.random_letter)
                WrongLetter.wrong_letter_index = 1
                update_message(
                    wrong_letters,
                    wrong_letters_list,
                    WrongLetter,
                    game_progression_objects,
                )
            # Removes the letter from the letters list ('the_abc') and the vowel letters list
            Letter.the_abc.remove(self.random_letter)
            if self.random_letter in Letter.vowel_letters:
                Letter.vowel_letters.remove(self.random_letter)
        Letter.letter_center = (
            random.randint(SCREEN_WIDTH + 120, SCREEN_WIDTH + 230),
            random.randint(60, SCREEN_HEIGHT - 60),
        )


class Hangman(pygame.sprite.Sprite):
    """Creates the hangman who testifies to the amount of mistakes

    Args:
        pygame (module): A set of Python modules designed for writing games
    """

    phase_num = 0

    def __init__(self):
        """Creates the Hangman"""
        super().__init__()
        self.surf = pygame.image.load(
            r"c:\Users\ofir1\OneDrive\שולחן העבודה\Hangbird game\sprites\hangman phases\phase %s.png"
            % Hangman.phase_num
        ).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(bottomleft=(0, SCREEN_HEIGHT - 10))

    def update(self):
        """Updating the Hangman"""
        if Hangman.phase_num < 6:
            Hangman.phase_num += 1
            self.__init__()


class HiddenLetter(ColoredLetter):
    """The letters that were discovered in the hidden word

    Args:
        ColoredLetter (type): Creates letters and colors them
    """

    hidden_letter_horizontal_ip = SCREEN_WIDTH / 2 - (len(the_word) - 1) * 20

    def __init__(self, letter="_", color=None, paint=True):
        """Creates the letters of the hidden word gradually as the player progresses

        Args:
            letter (str, optional): The revealed letter. Defaults to '_'.
            color (str, optional): The color of the revealed letter - 'right green' if found by the player, 'wrong red' if revealed when the player lost. Defaults to None.
            paint (bool, optional): Colors the letter when True, does not color it when False (False only when letter = '_'). Defaults to True.
        """
        if letter == "_":
            paint = False
        super().__init__(letter, color, paint)
        self.rect = self.surf.get_rect(
            center=(HiddenLetter.hidden_letter_horizontal_ip, 90)
        )
        HiddenLetter.hidden_letter_horizontal_ip += 40


class WrongLetter(ColoredLetter):
    """The letters that are not in the word

    Args:
        ColoredLetter (type): Creates letters and colors them
    """

    wrong_letter_left_ip = 120
    wrong_letter_top_ip = SCREEN_HEIGHT - 140
    wrong_letter_index = 1

    def __init__(self, letter):
        """Displays the wrong letters.

        Args:
            letter (str): The wrong letter the player took
        """
        super().__init__(letter, "wrong red")
        if WrongLetter.wrong_letter_index == 1:
            WrongLetter.wrong_letter_left_ip = 120
            WrongLetter.wrong_letter_top_ip = SCREEN_HEIGHT - 140
        elif WrongLetter.wrong_letter_index % 2 == 0:
            WrongLetter.wrong_letter_top_ip = SCREEN_HEIGHT - 80
        else:
            WrongLetter.wrong_letter_left_ip += 60
            WrongLetter.wrong_letter_top_ip = SCREEN_HEIGHT - 140
        WrongLetter.wrong_letter_index += 1
        self.rect = self.surf.get_rect(
            topleft=(WrongLetter.wrong_letter_left_ip, WrongLetter.wrong_letter_top_ip)
        )


class EndGameMessage(ColoredLetter):
    """The message displayed at the end of the game ('YOU WIN!' or 'GAME OVER!')

    Args:
        ColoredLetter (type): Creates letters and colors them
    """

    letter_index = 0

    def __init__(self, letter, color, message_length):
        """Creates the end game message

        Args:
            letter (str): The letter that is part of the endgame message
            color (str): The color of the letter - 'right green' if it is part of the message 'YOU WIN!', or 'wrong red' if it is part of the message 'GAME OVER!'
            message_length (int): The length of the message
        """
        if letter == " ":
            letter = "..."
        super().__init__(letter, color)
        horizontal_ip = (
            SCREEN_WIDTH / 2
            - (message_length - 1) * 20
            + EndGameMessage.letter_index * 40
        )
        self.rect = self.surf.get_rect(center=(horizontal_ip, 170))
        EndGameMessage.letter_index += 1

    def update():
        if hidden_word == the_word:
            for char in "YOU WIN!":
                char = EndGameMessage(char, "right green", len("YOU WIN!"))
                game_progression_objects.add(char)
            print("\nYOU WIN!")
        elif (Hangman.phase_num == 6) or (Heart.active_hearts == 0):
            for char in "GAME OVER!":
                char = EndGameMessage(char, "wrong red", len("GAME OVER!"))
                game_progression_objects.add(char)
            for hidden_letter in hidden_letters:
                hidden_letter.kill()
            HiddenLetter.hidden_letter_horizontal_ip = (
                SCREEN_WIDTH / 2 - (len(the_word) - 1) * 20
            )

            for correct_letter in the_word:
                if correct_letter in hidden_word:
                    correct_letter = HiddenLetter(correct_letter, "right green")
                else:
                    correct_letter = HiddenLetter(correct_letter, "wrong red")
                hidden_letters.add(correct_letter)
                game_progression_objects.add(correct_letter)
            print("\nGAME OVER!")


class Powerup(pygame.sprite.Sprite):
    """Gives the player an advantage in the game

    Args:
        pygame (module): A set of Python modules designed for writing games
    """

    powerup_sound = pygame.mixer.Sound(
        r"c:\Users\ofir1\OneDrive\שולחן העבודה\Hangbird game\music\correct letter + powerup.mp3"
    )
    powerup_center = (
        random.randint(SCREEN_WIDTH + 120, SCREEN_WIDTH + 230),
        random.randint(60, SCREEN_HEIGHT - 60),
    )

    def __init__(self, powerup):
        """Creates the powerup

        Args:
            powerup (str): The name of the powerup that needs to be created
        """
        super().__init__()
        self.surf = pygame.image.load(
            r"c:\Users\ofir1\OneDrive\שולחן העבודה\Hangbird game\sprites\powerups\%s.png"
            % powerup
        ).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=Powerup.powerup_center)

    def update(self):
        """Moves the powerup and kills it when it leaves the screen or when the game ends"""
        self.rect.move_ip(-5, 0)
        if self.rect.right <= 0:
            self.kill()
        if pygame.sprite.collide_rect(player, self):
            self.powerup_sound.play()
            self.kill()
        Powerup.powerup_center = (
            random.randint(SCREEN_WIDTH + 120, SCREEN_WIDTH + 230),
            random.randint(60, SCREEN_HEIGHT - 60),
        )


class ExtraGuess(Powerup):
    """Moves the hangman state back one step, giving the player another guess.

    Args:
        Powerup (type): Gives the player an advantage in the game
    """

    def __init__(self):
        """Creates the 'Extra Guess' powerup"""
        super().__init__("extra guess")

    def update(self):
        """Gives the player another guess"""
        super().update()
        if (pygame.sprite.collide_rect(player, self)) and (Hangman.phase_num > 0):
            Hangman.phase_num -= 1
            hangman.__init__()


class LetterReveal(Powerup):
    """Reveals a letter from the hidden word to the player

    Args:
        Powerup (type): Gives the player an advantage in the game
    """

    def __init__(self):
        """Creates the 'Letter Reveal' powerup"""
        super().__init__("letter reveal")

    def update(self):
        """Reveals a letter from the hidden word"""
        super().update()
        if pygame.sprite.collide_rect(player, self):
            # Searches for an index in the hidden word that is missing a letter
            i = random.choice(range(len(hidden_word)))
            while (hidden_word[i] != "_") and ("_" in hidden_word):
                i = random.choice(range(len(hidden_word)))
            # Copies the correct letter to the hidden word.
            right_letter_indexes = [
                char[0] for char in enumerate(the_word) if the_word[i] == char[1]
            ]
            for index in right_letter_indexes:
                the_letter = the_word[i]
                hidden_word[index] = the_letter
            HiddenLetter.hidden_letter_horizontal_ip = (
                SCREEN_WIDTH / 2 - (len(the_word) - 1) * 20
            )
            update_message(
                hidden_letters,
                hidden_word,
                HiddenLetter,
                game_progression_objects,
                "right green",
            )

            Letter.the_abc.remove(the_letter)
            if the_letter in Letter.vowel_letters:
                Letter.vowel_letters.remove(the_letter)


class ExtraLife(Powerup):
    """Gives the player an extra life

    Args:
        Powerup (type): Gives the player an advantage in the game
    """

    def __init__(self):
        """Creates the 'Extra Life' powerup"""
        super().__init__("extra life")

    def update(self):
        """Gives an extra life"""
        super().update()
        if pygame.sprite.collide_rect(player, self):
            Heart.active_hearts += 1
            Heart.heart_horizontal_ip = SCREEN_WIDTH - 40
            for i in range(Heart.active_hearts):
                heart = Heart()
                hearts.add(heart)
                game_progression_objects.add(heart)


class Heart(pygame.sprite.Sprite):
    """One of the three hearts at the game's start. Additional hearts can be obtained by collecting the 'Extra Life' powerup, and if the player loses all the hearts, they lose and the game is over.

    Args:
        pygame (module): A set of Python modules designed for writing games
    """

    heart_horizontal_ip = SCREEN_WIDTH - 40
    active_hearts = 3

    def __init__(self):
        """Creates the heart"""
        super().__init__()
        self.surf = pygame.image.load(
            r"c:\Users\ofir1\OneDrive\שולחן העבודה\Hangbird game\sprites\heart.png"
        ).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(center=(Heart.heart_horizontal_ip, 40))
        Heart.heart_horizontal_ip -= 60


def restart(command):
    """Kills all objects except the player and game progress objects. Does additional things as per the command

    Args:
        command (str): The command that corresponds to the game state ('COLLISION' when the player collides with an obstacle, and 'END GAME' when the game ends)
    """
    if command == "COLLISION":
        if game_on:
            collision_sound = pygame.mixer.Sound(
                r"c:\Users\ofir1\OneDrive\שולחן העבודה\Hangbird game\music\wrong letter + collision.mp3"
            )
            collision_sound.play()
        for obstacle in obstacles:
            obstacle.kill()
        player.rect.topleft = (0, 0)
        Heart.active_hearts -= 1
    if command == "END GAME":
        Heart.active_hearts = 0
    for letter in letters:
        letter.kill()
    for powerup in powerups:
        powerup.kill()
    for heart in hearts:
        heart.kill()
    Heart.heart_horizontal_ip = SCREEN_WIDTH - 40
    for i in range(Heart.active_hearts):
        heart = Heart()
        hearts.add(heart)
        game_progression_objects.add(heart)


screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADD_OBSTACLE = pygame.USEREVENT + 1
pygame.time.set_timer(ADD_OBSTACLE, 2000)
ADD_LETTER = pygame.USEREVENT + 2
pygame.time.set_timer(ADD_LETTER, 2000)

player = Player()
hangman = Hangman()
obstacles = pygame.sprite.Group()
letters = pygame.sprite.Group()
powerups = pygame.sprite.Group()
hidden_letters = pygame.sprite.Group()
wrong_letters = pygame.sprite.Group()
hearts = pygame.sprite.Group()
game_progression_objects = pygame.sprite.Group()
game_progression_objects.add(hangman)
interacting_objects = pygame.sprite.Group()
interacting_objects.add(player)

for hidden_letter in hidden_word:
    hidden_letter = HiddenLetter()
    hidden_letters.add(hidden_letter)
    game_progression_objects.add(hidden_letter)

for i in range(3):
    heart = Heart()
    hearts.add(heart)
    game_progression_objects.add(heart)

clock = pygame.time.Clock()
powerup_timer = 1

game_on, game_over_restart = (
    (
        (Hangman.phase_num < 6)
        and (hidden_word != the_word)
        and (Heart.active_hearts > 0)
    ),
    (True),
)

pygame.mixer.music.load(
    r"c:\Users\ofir1\OneDrive\שולחן העבודה\Hangbird game\music\background music.wav"
)
pygame.mixer.music.play(loops=-1)

running = True
print("\nWelcome to the flight on the Hbird7 aircraft.")
print("Please fasten your seatbelts and enjoy the flight.")

while running:
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT:
            running = False
        elif event.type == ADD_OBSTACLE:
            new_lower_obstacle, new_upper_obstacle = LowerObstacle(), UpperObstacle()
            obstacles.add(new_lower_obstacle, new_upper_obstacle)
            interacting_objects.add(new_lower_obstacle, new_upper_obstacle)
        elif (event.type == ADD_LETTER) and game_on:
            if powerup_timer % 15 == 0:
                new_powerup = random.choice([ExtraGuess(), LetterReveal(), ExtraLife()])
                powerups.add(new_powerup)
                interacting_objects.add(new_powerup)
            else:
                new_letter = Letter()
                letters.add(new_letter)
                interacting_objects.add(new_letter)
            powerup_timer += 1

    screen.fill((255, 255, 255))
    game_display.blit(bg_image, (0, 0))

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    obstacles.update()
    letters.update()
    powerups.update()

    for entity in interacting_objects:
        screen.blit(entity.surf, entity.rect)
    for entity in game_progression_objects:
        screen.blit(entity.surf, entity.rect)
    game_on = (
        (Hangman.phase_num < 6)
        and (hidden_word != the_word)
        and (Heart.active_hearts > 0)
    )
    pygame.display.update()

    if not (game_on) and game_over_restart:
        restart("END GAME")
        EndGameMessage.update()
        game_over_restart = False
    if pygame.sprite.spritecollideany(player, obstacles):
        restart("COLLISION")

    pygame.display.flip()

    clock.tick(45)

pygame.mixer.music.stop()
pygame.mixer.quit()
pygame.quit()