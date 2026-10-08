"""
GameEngine: owns the paddle, ball, and bricks.

Starter version: single brick type, no lives yet, no score/combo yet.
Ball-brick collision also has a known bug (see game/collision.py) that
Task 1 asks you to fix. If the ball falls below the paddle, it just
resets to the starting position with no consequence - that's what
Task 2 builds on.
"""

import pygame

from game.paddle import Paddle
from game.ball import Ball
from game.brick import Brick
from game.collision import handle_ball_brick_collision
from game.renderer import WIDTH, HEIGHT


BRICK_ROWS = 4
BRICK_COLS = 8
BRICK_WIDTH = 68
BRICK_HEIGHT = 22
BRICK_GAP = 6
BRICK_TOP_MARGIN = 50


class GameEngine:
    def __init__(self):
        self.paddle = Paddle(x=WIDTH / 2, y=HEIGHT - 30)
        self.ball = Ball(x=WIDTH / 2, y=HEIGHT - 50)
        self.bricks = self._build_bricks()

        # Task 2: lives system
        self.lives = 3
        self.game_over = False

    def _build_bricks(self):
        bricks = []

        total_width = (
            BRICK_COLS * (BRICK_WIDTH + BRICK_GAP)
            - BRICK_GAP
        )

        start_x = (WIDTH - total_width) / 2

        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):

                x = start_x + col * (BRICK_WIDTH + BRICK_GAP)
                y = BRICK_TOP_MARGIN + row * (
                    BRICK_HEIGHT + BRICK_GAP
                )

                # Task 3:
                # Row 0 -> Unbreakable
                # Row 1 -> Strong
                # Rows 2-3 -> Normal
                if row == 0:
                    brick_type = Brick.UNBREAKABLE

                elif row == 1:
                    brick_type = Brick.STRONG

                else:
                    brick_type = Brick.NORMAL

                bricks.append(
                    Brick(
                        x,
                        y,
                        BRICK_WIDTH,
                        BRICK_HEIGHT,
                        brick_type
                    )
                )

        return bricks

    def _reset_ball(self):
        self.ball = Ball(
            x=WIDTH / 2,
            y=HEIGHT - 50
        )

    def restart(self):
        """Restart the game after Game Over."""

        self.paddle = Paddle(
            x=WIDTH / 2,
            y=HEIGHT - 30
        )

        self.ball = Ball(
            x=WIDTH / 2,
            y=HEIGHT - 50
        )

        self.bricks = self._build_bricks()

        self.lives = 3
        self.game_over = False

    def handle_input(self, keys_pressed):

        # Don't move paddle after Game Over
        if self.game_over:
            return

        dx = 0

        if keys_pressed[pygame.K_LEFT]:
            dx -= self.paddle.speed

        if keys_pressed[pygame.K_RIGHT]:
            dx += self.paddle.speed

        self.paddle.move(dx, WIDTH)

    def handle_keydown(self, key):

        # Press R to restart after Game Over
        if self.game_over and key == pygame.K_r:
            self.restart()

    def update(self):

        # Stop updating the game after Game Over
        if self.game_over:
            return

        self.ball.update()

        self.ball.bounce_off_walls(WIDTH)

        # -------------------------------------------------
        # Ball-paddle collision
        # -------------------------------------------------

        if (
            self.ball.get_rect().colliderect(
                self.paddle.get_rect()
            )
            and self.ball.vy > 0
        ):
            self.ball.bounce_off_paddle(
                self.paddle.get_rect()
            )

        # -------------------------------------------------
        # Ball-brick collision
        # -------------------------------------------------

        for brick in self.bricks:

            if handle_ball_brick_collision(
                self.ball,
                brick
            ):

                # -----------------------------------------
                # Unbreakable brick
                # -----------------------------------------

                if brick.brick_type == Brick.UNBREAKABLE:
                    # It can be hit but is never destroyed.
                    break

                # -----------------------------------------
                # Normal / Strong brick
                # -----------------------------------------

                brick.hits_remaining -= 1

                # Remove brick when all hits are used.
                if brick.hits_remaining <= 0:
                    self.bricks.remove(brick)

                break

        # -------------------------------------------------
        # Ball falls below the screen
        # -------------------------------------------------

        if self.ball.is_below(HEIGHT):

            self.lives -= 1

            if self.lives <= 0:
                self.game_over = True

            else:
                self._reset_ball()

    def draw(self, surface, font):

        from game import renderer

        renderer.draw_scene(
            surface,
            self.paddle,
            self.ball,
            self.bricks
        )

        # -------------------------------------------------
        # Bricks remaining
        # -------------------------------------------------

        renderer.draw_text(
            surface,
            font,
            f"Bricks left: {len(self.bricks)}",
            (10, 10)
        )

        # -------------------------------------------------
        # Lives
        # -------------------------------------------------

        renderer.draw_text(
            surface,
            font,
            f"Lives: {self.lives}",
            (10, 35)
        )

        # -------------------------------------------------
        # Game Over
        # -------------------------------------------------

        if self.game_over:

            renderer.draw_text(
                surface,
                font,
                "GAME OVER - Press R to Restart",
                (WIDTH // 2 - 170, HEIGHT // 2)
            )