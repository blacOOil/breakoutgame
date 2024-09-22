import pygame, random
import os
from pygame import mixer
from src.constants import *

pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.init()

music_channel = mixer.Channel(0)
music_channel.set_volume(0.2)

from src.Dependency import *

class GameMain:
    def __init__(self):
        self.max_frame_rate = 60
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))

        self.bg_image = pygame.image.load("./graphics/background.png")
        self.bg_image = pygame.transform.scale(self.bg_image, (WIDTH + 5, HEIGHT + 5))

        self.num_dup_images = math.ceil(WIDTH / self.bg_image.get_width()) + 1
        self.scroll = 0
        self.scroll_bg = False

        # Add a variable to track the scroll direction (1 for right, -1 for left)
        self.scroll_direction = 1

        self.bg_music = pygame.mixer.Sound('sounds/music.wav')

        g_state_manager.SetScreen(self.screen)

        states = {
            'start': StartState(),
            'play': PlayState(),
            'serve': ServeState(),
            'game-over': GameOverState(),
            'victory': VictoryState(),
            'high-scores': HighScoreState(),
            'enter-high-score': EnterHighScoreState(),
            'paddle-select': PaddleSelectState()
        }
        g_state_manager.SetStates(states)

        # Initialize the countdown timer (in seconds)
        self.timer_duration = 41
        self.start_time = None

    def LoadHighScores(self):
        if not os.path.exists(RANK_FILE_NAME):
            with open(RANK_FILE_NAME, "w") as fp:
                for i in range(10, 0, -1):
                    scores = "AAA\n" + str(i * 10) + "\n"
                    fp.write(scores)
                fp.close()

        file = open(RANK_FILE_NAME, "r+")
        all_lines = file.readlines()
        scores = []

        name_flip = True
        counter = 0
        for i in range(10):
            scores.append({
                'name': '',
                'score': 0
            })

        for line in all_lines:
            if name_flip:
                scores[counter]['name'] = line[:-1]
            else:
                scores[counter]['score'] = int(line[:-1])
                counter += 1

            name_flip = not name_flip

        return scores

    def RenderBackground(self):
        # Scroll the background based on the scroll direction
        i = 0
        while i < self.num_dup_images:
            main.screen.blit(self.bg_image, (self.bg_image.get_width() * i + self.scroll, 0))
            i += 1

        # Update scroll based on the direction (positive for right, negative for left)
        self.scroll += 6 * self.scroll_direction

        # Reverse the direction when reaching the edge
        if self.scroll >= 0:
            self.scroll_direction = -1  # Scroll to the left
        elif self.scroll <= -self.bg_image.get_width():
            self.scroll_direction = 1  # Scroll to the right

    def RenderTimer(self, remaining_time):
        font = pygame.font.SysFont(None, 74)
        timer_text = font.render(str(remaining_time), True, (255, 0, 0))
        timer_rect = timer_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(timer_text, timer_rect)

    def PlayGame(self):
        self.bg_music.play(-1)
        clock = pygame.time.Clock()
        g_state_manager.Change('start', {
            'high_scores': self.LoadHighScores(),
        })

        # Randomize brick creation
        bricks = []
        for x in range(0, WIDTH, 100):
            # Random chance to place a brick
            if random.random() > 0.3:  # 70% chance to place a brick
                bricks.append(Brick(x, 100))

        # Set the start time for the countdown
        self.start_time = pygame.time.get_ticks()  # Get start time in milliseconds

        while True:
            pygame.display.set_caption("Breakout game running with {:d} FPS".format(int(clock.get_fps())))
            dt = clock.tick(self.max_frame_rate) / 1000.0

            # Input handling
            events = pygame.event.get()

            # Update game state
            g_state_manager.update(dt, events)

            # Get the remaining time
            elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Convert to seconds
            remaining_time = int(self.timer_duration - elapsed_time)

            # If time is up, end the game
            if remaining_time <= 0:
                print("Game Over! Time's up.")
                break

            # Update and render each brick
            for brick in bricks:
                brick.update(dt)
                brick.render(self.screen)

            # Render the background with scrolling
            self.RenderBackground()

            # Render the timer
            self.RenderTimer(remaining_time)

            # Render the game state
            g_state_manager.render()

            # Update the display
            pygame.display.update()


if __name__ == '__main__':
    main = GameMain()
    main.PlayGame()
