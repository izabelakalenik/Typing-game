import sys
import editdistance
import pygame

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


def calculate_accuracy(user_input, expected_input):
    return round((1 - editdistance.eval(user_input, expected_input) / len(expected_input)) * 100, 2)


def read_sentences_from_file(file_path):
    sentences_list = []
    with open(file_path, 'r') as file:
        text = file.read()
        sentence_delimiters = ['.', '!', '?']
        for delimiter in sentence_delimiters:
            sentences_list.extend(text.split(delimiter))
        sentences_list = [sentence.strip() for sentence in sentences_list if sentence.strip()]
    return sentences_list


class TypingGame:
    def __init__(self):
        self.running = False
        pygame.init()

        # Set up the screen
        self.WIDTH = 900
        self.HEIGHT = 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Typing Game")

        # Game variables
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 40)
        self.text_file = './texts/lorem_ipsum.txt'
        self.sentences = read_sentences_from_file(self.text_file)
        self.sentence_iterator = None
        self.current_sentence = None
        self.user_text = ""
        self.total_user_input = []
        self.total_expected_input = []
        self.i = 0

    def display_accuracy(self):
        accuracy = calculate_accuracy(self.total_user_input, self.total_expected_input)
        accuracy_text = self.font.render(f"Accuracy: {accuracy} %", True, WHITE)
        self.screen.blit(accuracy_text, (10, 10))

    def display_user_input(self):
        user_text_render = self.font.render(self.user_text, True, WHITE)
        user_text_rect = user_text_render.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 + 50))
        self.screen.blit(user_text_render, user_text_rect)

    def display_current_sentence(self):
        sentence_text = self.font.render(self.current_sentence, True, WHITE)
        sentence_rect = sentence_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT // 2 - 50))
        letter_x = sentence_rect.left  # Starting x-coordinate

        for i, letter in enumerate(self.current_sentence):
            letter_width = self.font.size(letter)[0]  # Width of the current letter

            if i < len(self.user_text):
                if self.user_text[i] == letter:
                    letter_color = GREEN  # Green for correct letter
                else:
                    letter_color = RED # Red for incorrect letter
            else:
                letter_color = WHITE

            letter_surface = self.font.render(letter, True, letter_color)
            letter_rect = letter_surface.get_rect(topleft=(letter_x, sentence_rect.bottom))

            self.screen.blit(letter_surface, letter_rect)

            letter_x += letter_width  # Update x-coordinate for the next letter

    def display_restart(self):
        restart_text = self.font.render('RESTART GAME', True, RED)
        restart_rect = restart_text.get_rect(center=(self.WIDTH // 2, self.HEIGHT - 50))
        self.screen.blit(restart_text, restart_rect)

    def restart_game(self):
        self.sentence_iterator = iter(self.sentences)
        self.current_sentence = next(self.sentence_iterator)
        self.user_text = ""
        self.total_user_input = []
        self.total_expected_input = []
        self.i = 0

    def run(self):
        self.running = True
        self.restart_game()
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self.user_text += event.unicode

            self.screen.fill(BLACK)

            self.display_current_sentence()
            self.display_user_input()

            if len(self.user_text) == len(self.current_sentence):
                self.total_user_input += self.user_text
                self.total_expected_input += self.current_sentence
                self.current_sentence = next(self.sentence_iterator)
                self.user_text = ""
                self.i += 1

            if self.i == 2:
                self.display_accuracy()
                self.display_restart()

            pygame.display.update()

        pygame.quit()


if __name__ == '__main__':
    game = TypingGame()
    game.run()
