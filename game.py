import sys

import pygame
from pygame.locals import *
import numpy as np
import torch

import othello
from model import FNN
from env import MODEL_PATH

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN_BLACK = (0, 50, 0)
GREEN = (10, 180, 30)
GREEN_SHADOW = (10, 100, 10)
BLUE_BLACK = (0, 0, 70)
YELLOW = (255, 200, 0)
PURPLE = (150, 0, 255)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1000, 850))
        pygame.display.set_caption("Othello AI")

        self.model = FNN()
        self.model.load_state_dict(torch.load(MODEL_PATH)["model_state_dict"])
        self.model.eval()
        print("model loaded")

        self.black_player = othello.Othello(color=othello.OthelloPiece.Black)
        self.white_player = othello.Othello(color=othello.OthelloPiece.White)
        self.clock = pygame.time.Clock()
        self.player_color = "black"
        self.player_turn = True

        self.black_player.initial_board()
        self.white_player.initial_board()

    def render_splash(self):
        frame_count = 0
        splash_image = pygame.image.load("assets/othello_logo.png").convert_alpha()
        splash_image.set_alpha(0)
        image_size = splash_image.get_size()

        while frame_count < 30 * 5:
            self.screen.fill(BLACK)
            if frame_count < 50:
                splash_image.set_alpha(frame_count * 5)
            elif frame_count < 120:
                splash_image.set_alpha(255)
            else:
                splash_image.set_alpha((150 - frame_count) * 8)

            self.screen.blit(
                splash_image, ((1000 - image_size[0]) / 2, (850 - image_size[1]) / 2)
            )
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            frame_count += 1
            self.clock.tick(30)

    def render_ready(self):
        text_1 = pygame.font.SysFont("Noto Sans CJK JP", 50).render(
            "Select your piece color.", True, WHITE
        )
        text_2 = pygame.font.SysFont("Noto Sans CJK JP", 40).render(
            "Black: Press B", True, WHITE
        )
        text_3 = pygame.font.SysFont("Noto Sans CJK JP", 40).render(
            "White: Press W", True, WHITE
        )
        text_4 = pygame.font.SysFont("Noto Sans CJK JP", 40).render(
            "Quit: Press ESC", True, WHITE
        )

        while True:
            self.screen.fill(BLACK)
            self.render_bg_pattern()
            render_surf(self.screen, text_1, 1 / 2, 100)
            render_surf(self.screen, text_2, 1 / 4, 600)
            render_surf(self.screen, text_3, 3 / 4, 600)
            render_surf(self.screen, text_4, 1 / 2, 740)
            pygame.draw.rect(
                self.screen, GREEN, Rect(100, 300, 300, 300), border_radius=10
            )
            pygame.draw.rect(
                self.screen, GREEN, Rect(600, 300, 300, 300), border_radius=10
            )
            pygame.draw.circle(self.screen, GREEN_SHADOW, (260, 460), 98)
            pygame.draw.circle(self.screen, BLACK, (250, 450), 100)
            pygame.draw.circle(self.screen, GREEN_SHADOW, (760, 460), 98)
            pygame.draw.circle(self.screen, WHITE, (750, 450), 100)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == K_b:
                        self.player_color = "black"
                        self.player_turn = True
                        return
                    elif event.key == K_w:
                        self.player_color = "white"
                        self.player_turn = False
                        return
                    else:
                        pass
            self.clock.tick(30)

    def render_color_selected(self):
        frame_count = 0
        text_1 = pygame.font.SysFont("Noto Sans CJK JP", 50).render(
            f"Your color is {self.player_color}. Good Luck !", True, WHITE
        )

        while frame_count < 30 * 2:
            self.screen.fill(BLACK)
            self.render_bg_pattern()
            render_surf(self.screen, text_1, 1 / 2, 100)
            pygame.draw.rect(
                self.screen, GREEN, Rect(350, 300, 300, 300), border_radius=10
            )
            pygame.draw.circle(self.screen, GREEN_SHADOW, (510, 460), 98)
            if self.player_color == "black":
                pygame.draw.circle(self.screen, BLACK, (500, 450), 100)
            else:
                pygame.draw.circle(self.screen, WHITE, (500, 450), 100)

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()

            frame_count += 1
            self.clock.tick(30)
            # TODO

    def render_match_start(self):
        frame_count = 0
        self.black_player.initial_board()
        self.white_player.initial_board()

        while frame_count < 30 * 4:
            self.screen.fill((0, 0, 0))
            self.render_bg_pattern()
            self.render_field()
            self.render_pieces()

            if frame_count < 30:
                text = pygame.font.SysFont("Noto Sans CJK JP", 100).render(
                    "3", True, YELLOW
                )
            elif frame_count < 60:
                text = pygame.font.SysFont("Noto Sans CJK JP", 100).render(
                    "2", True, YELLOW
                )
            elif frame_count < 90:
                text = pygame.font.SysFont("Noto Sans CJK JP", 100).render(
                    "1", True, YELLOW
                )
            else:
                text = pygame.font.SysFont("Noto Sans CJK JP", 100).render(
                    "start !", True, YELLOW
                )
            render_surf(self.screen, text, 1 / 2, 350)

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
            frame_count += 1
            self.clock.tick(30)

    def render_match(self):
        text_pass_ai = pygame.font.SysFont("Noto Sans CJK JP", 100).render(
            "AI pass", True, PURPLE
        )
        text_pass_player = pygame.font.SysFont("Noto Sans CJK JP", 100).render(
            "You pass", True, PURPLE
        )
        text_thinking1 = pygame.font.SysFont("Noto Sans CJK JP", 50).render(
            "thinking.", True, YELLOW
        )
        text_thinking2 = pygame.font.SysFont("Noto Sans CJK JP", 50).render(
            " thinking..", True, YELLOW
        )
        text_thinking3 = pygame.font.SysFont("Noto Sans CJK JP", 50).render(
            "  thinking...", True, YELLOW
        )
        frame_count = 0
        if self.player_turn:
            animation = "player_turn"  # ["player_turn", "pass", "ai_turn", "end"]
        else:
            animation = "ai_turn"

        while True:
            self.screen.fill(BLACK)
            self.render_bg_pattern()
            self.render_field()
            self.render_pieces()

            # check game set
            black_put_pos = self.black_player.search_putable_pos()
            white_put_pos = self.white_player.search_putable_pos()
            if len(black_put_pos) == 0 and len(white_put_pos) == 0:
                break

            # check pass
            if self.player_turn:
                if self.player_color == "black":
                    pos = black_put_pos
                else:
                    pos = white_put_pos
                if len(pos) == 0:
                    animation = "pass"
                    self.player_turn = not self.player_turn
            else:
                if self.player_color == "black":
                    pos = white_put_pos
                else:
                    pos = black_put_pos
                if len(pos) == 0:
                    animation = "pass"
                    self.player_turn = not self.player_turn

            if animation == "player_turn":
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            sys.exit()
                    elif event.type == MOUSEBUTTONDOWN:
                        x, y = self._get_click_square(pygame.mouse.get_pos())
                        if not othello.out_of_board(x, y):
                            if self.player_color == "black":
                                dirs = self.black_player.can_put(x, y)
                                if len(dirs) > 0:
                                    self.black_player.put(
                                        x, y, othello.OthelloPiece.Black, dirs
                                    )
                                    self.white_player.put(
                                        x, y, othello.OthelloPiece.Black, dirs
                                    )
                                    self.player_turn = not self.player_turn
                                    animation = "ai_turn"
                            else:
                                dirs = self.white_player.can_put(x, y)
                                if len(dirs) > 0:
                                    self.black_player.put(
                                        x, y, othello.OthelloPiece.White, dirs
                                    )
                                    self.white_player.put(
                                        x, y, othello.OthelloPiece.White, dirs
                                    )
                                    self.player_turn = not self.player_turn
                                    animation = "ai_turn"

            elif animation == "ai_turn":
                if frame_count < 20:
                    pass
                elif frame_count < 25:
                    render_surf(self.screen, text_thinking1, 1 / 2, 375)
                elif frame_count < 30:
                    render_surf(self.screen, text_thinking2, 1 / 2, 375)
                elif frame_count < 35:
                    render_surf(self.screen, text_thinking3, 1 / 2, 375)
                elif frame_count < 40:
                    render_surf(self.screen, text_thinking1, 1 / 2, 375)
                elif frame_count < 45:
                    render_surf(self.screen, text_thinking2, 1 / 2, 375)
                elif frame_count < 50:
                    render_surf(self.screen, text_thinking3, 1 / 2, 375)
                elif frame_count == 50:
                    x, y = self._get_predict()
                    if self.player_color == "black":
                        dirs = self.white_player.can_put(x, y)
                        self.black_player.put(x, y, othello.OthelloPiece.White, dirs)
                        self.white_player.put(x, y, othello.OthelloPiece.White, dirs)
                    else:
                        dirs = self.black_player.can_put(x, y)
                        self.black_player.put(x, y, othello.OthelloPiece.Black, dirs)
                        self.white_player.put(x, y, othello.OthelloPiece.Black, dirs)
                elif frame_count < 60:
                    pass
                elif frame_count == 60:
                    self.player_turn = not self.player_turn
                    animation = "player_turn"
                    frame_count = 0
                    continue
                frame_count += 1
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            sys.exit()

            elif animation == "pass":
                if self.player_turn:
                    if frame_count < 15:
                        text_pass_ai.set_alpha(17 * frame_count)
                    elif frame_count < 45:
                        text_pass_ai.set_alpha(255)
                    else:
                        text_pass_ai.set_alpha(17 * (60 - frame_count))
                    render_surf(self.screen, text_pass_ai, 1 / 2, 350)
                    if frame_count == 60:
                        frame_count = 0
                        animation = "player_turn"
                else:
                    if frame_count < 15:
                        text_pass_player.set_alpha(17 * frame_count)
                    elif frame_count < 45:
                        text_pass_player.set_alpha(255)
                    else:
                        text_pass_player.set_alpha(17 * (60 - frame_count))
                    render_surf(self.screen, text_pass_player, 1 / 2, 350)
                    if frame_count == 60:
                        frame_count = 0
                        animation = "ai_turn"
                frame_count += 1

                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == QUIT:
                        pygame.quit()
                        sys.exit()
                    elif event.type == KEYDOWN:
                        if event.key == K_ESCAPE:
                            pygame.quit()
                            sys.exit()

            self.clock.tick(30)

    def render_match_end(self):
        frame_count = 0
        while True:
            self.render_bg_pattern()
            self.render_field()
            self.render_pieces()

            if frame_count <= 30:
                text_end = pygame.font.SysFont(
                    "Noto Sans CJK JP", 130 - frame_count
                ).render("Game End", True, YELLOW)
                text_end.set_alpha(frame_count * 8.5)

            render_surf(self.screen, text_end, 1 / 2, 350)
            if frame_count >= 60:
                text_guide = pygame.font.SysFont("Noto Sans CJK JP", 50).render(
                    "Show Result: Press SPACE", True, YELLOW
                )
                render_surf(self.screen, text_guide, 1 / 2, 500)
                frame_count == 60
            frame_count += 1
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == K_SPACE:
                        return
            self.clock.tick(30)

    def render_result(self):
        winner = self.black_player.judge_winner()
        if winner == othello.OthelloPiece.Black:
            text_res = pygame.font.SysFont("Noto Sans CJK JP", 70).render(
                "Winner : Black", True, YELLOW
            )
        elif winner == othello.OthelloPiece.White:
            text_res = pygame.font.SysFont("Noto Sans CJK JP", 70).render(
                "Winner : White", True, YELLOW
            )
        else:
            text_res = pygame.font.SysFont("Noto Sans CJK JP", 70).render(
                "Judge : Draw", True, PURPLE
            )
        text_guide = pygame.font.SysFont("Noto Sans CJK JP", 50).render(
            "New Game: Press N", True, WHITE
        )
        while True:
            self.screen.fill(BLACK)
            self.render_bg_pattern()
            render_surf(self.screen, text_res, 1 / 2, 100)
            render_surf(self.screen, text_guide, 1 / 2, 700)
            pygame.draw.rect(
                self.screen, GREEN, Rect(350, 300, 300, 300), border_radius=10
            )
            if winner == othello.OthelloPiece.Black:
                pygame.draw.circle(self.screen, GREEN_SHADOW, (510, 460), 98)
                pygame.draw.circle(self.screen, BLACK, (500, 450), 100)
            elif winner == othello.OthelloPiece.White:
                pygame.draw.circle(self.screen, GREEN_SHADOW, (510, 460), 100)
                pygame.draw.circle(self.screen, WHITE, (500, 450), 100)
            else:
                pass

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    elif event.key == K_n:
                        return
            self.clock.tick(30)

    def render_pieces(self):
        for y in range(8):
            for x in range(8):
                if self.black_player.current_board[y][x] == self.black_player.self_num:
                    pygame.draw.circle(
                        self.screen, GREEN_SHADOW, (100 * x + 155, 100 * y + 80), 39
                    )
                    pygame.draw.circle(
                        self.screen, BLACK, (100 * x + 150, 100 * y + 75), 40
                    )
                elif (
                    self.black_player.current_board[y][x] == self.black_player.opnt_num
                ):
                    pygame.draw.circle(
                        self.screen, GREEN_SHADOW, (100 * x + 155, 100 * y + 80), 39
                    )
                    pygame.draw.circle(
                        self.screen, WHITE, (100 * x + 150, 100 * y + 75), 40
                    )
                else:
                    pass

    def render_field(self):
        pygame.draw.rect(self.screen, GREEN, Rect(100, 25, 800, 800), border_radius=7)
        for i in range(1, 8):
            pygame.draw.line(
                self.screen,
                GREEN_BLACK,
                (100 * i + 100, 25),
                (100 * i + 100, 825),
                width=3,
            )
            pygame.draw.line(
                self.screen,
                GREEN_BLACK,
                (100, 100 * i + 25),
                (900, 100 * i + 25),
                width=3,
            )

    def render_bg_pattern(self):
        for y in range(17):
            for x in range(20):
                if (x + y) % 2 == 0:
                    pygame.draw.rect(self.screen, BLACK, Rect(x * 50, y * 50, 50, 50))
                else:
                    pygame.draw.rect(
                        self.screen, BLUE_BLACK, Rect(x * 50, y * 50, 50, 50)
                    )

    def _get_click_square(self, pos: tuple[int, int]) -> tuple[int, int]:
        x, y = pos
        x -= 100
        y -= 25
        x = int(x / 100)
        y = int(y / 100)
        return x, y

    def _get_predict(self) -> tuple[int, int]:
        if self.player_color == "black":
            res = self.model(
                torch.Tensor(
                    [
                        np.array(
                            self.white_player.current_board, dtype=np.float32
                        ).transpose()
                    ]
                )
            )[0]
            while True:
                x = res.argmax() % 8
                y = int(res.argmax() / 8)
                dirs = self.white_player.can_put(x, y)
                if len(dirs) > 0:
                    break
                else:
                    res[y * 8 + x] = 0
            return x, y
        else:
            res = self.model(
                torch.Tensor(
                    [
                        np.array(
                            self.black_player.current_board, dtype=np.float32
                        ).transpose()
                    ]
                )
            )[0]
            while True:
                x = res.argmax() % 8
                y = int(res.argmax() / 8)
                dirs = self.black_player.can_put(x, y)
                if len(dirs) > 0:
                    break
                else:
                    res[y * 8 + x] = 0
            return x, y


def render_surf(screen: pygame.Surface, surf: pygame.Surface, x_pos: float, y: int):
    text_width = surf.get_size()[0]
    x = 1000 * x_pos - text_width / 2
    screen.blit(surf, (x, y))


def main():
    game = Game()
    game.render_splash()
    while True:
        game.render_ready()
        game.render_color_selected()
        game.render_match_start()
        game.render_match()
        game.render_match_end()
        game.render_result()


if __name__ == "__main__":
    main()
