import os

import pygame
from pygame.locals import RLEACCEL
import random

base_path = os.getcwd()[:os.getcwd().find("Hangbird")]


def secret_word_generator():
    """Generates a secret word

    Returns:
        the_word (list): The secret word is divided into characters.
        hidden_word (list): The secret word that is hidden in '_' characters instead of letters.
    """

    with open(
        base_path + r"Hangbird game\words.txt", "r"
    ) as words_file:
        words = words_file.read().replace("\n", ",").split(",")
    the_word = random.choice([list(word) for word in words])
    hidden_word = list("_" * len(the_word))
    return the_word, hidden_word


class ColoredLetter(pygame.sprite.Sprite):
    """Creates letters and colors them

    Args:
        pygame (module): A set of Python modules designed for writing games
    """

    def __init__(self, letter, color, paint=True):
        """Creates letters and colors them (if paint==True)

        Args:
            letter (str): The letter that needs to be generated
            color (str): The color in which the letter is colored
            paint (bool, optional): Whether to color the letter - colors if 'True', doesn't color if 'False'. Defaults to True.
        """
        super().__init__()
        letter_file = (
            base_path + r"Hangbird game\sprites\letters\%s.png"
            % letter
        )
        self.surf = pygame.image.load(letter_file).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        if paint:
            search_color = pygame.Color(0, 0, 0, 255)
            set_of_colors = {
                "right green": (51, 204, 0),
                "wrong red": (220, 33, 20),
                "orange": (255, 100, 0),
                "yellow": (255, 180, 0),
                "cyan": (0, 180, 255),
                "blue": (0, 0, 255),
                "purple": (150, 0, 255),
                "pink": (235, 51, 235),
            }
            pygame.transform.threshold(
                self.surf,
                self.surf,
                search_color,
                (0, 0, 0, 255),
                set_of_colors[color],
                1,
            )


def update_message(
    message_group, message_content, message_class, general_group, color=None
):
    """Updates the message that is on the screen

    Args:
        message_group (pygame.sprite.Group): The pygame group of the message
        message_content (list): The message
        message_class (type): The class of the message
        general_group (pygame.sprite.Group): The general pygame group of the message (game_progression_objects or interacting_objects)
        color (None/str, optional): The color that the message letters should be colored in. Defaults to None.
    """
    for letter in message_group:
        letter.kill()
    for letter in message_content:
        if color != None:
            letter = message_class(letter, color)
        else:
            letter = message_class(letter)
        message_group.add(letter)
        general_group.add(letter)
