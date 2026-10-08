"""
GameEngine: owns the paddle, ball, and bricks.

Implemented tasks:
Task 1 - Brick collision and destruction
Task 2 - 3 lives, Game Over, and restart
Task 3 - Normal, Strong, and Unbreakable bricks
Task 4 - Score and combo multiplier
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
        self.paddle = Paddle(
            x=WIDTH / 2,
            y=HEIGHT - 30
        )

        self.ball = Ball(
            x=WIDTH / 2,
            y=HEIGHT - 50
        )

        self.bricks = self._build_bricks()

        # Task 2: Lives
        self.lives = 3
        self.game_over = False

        # Task 4: Score and combo
        self.score = 0
        self.combo = 1

    def _build_bricks(self):
        bricks = []

        total_width = (
            BRICK_COLS * (BRICK_WIDTH + BRICK_GAP)
            - BRICK_GAP
        )

        start_x = (WIDTH - total_width) / 2

        for row in range(BRICK_ROWS):
            for col in range(BRICK_COLS):

                x = start_x + col * (
                    BRICK_WIDTH + BRICK_GAP
                )

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

        # Reset lives
        self.lives = 3
        self.game_over = False

        # Reset score and combo
        self.score = 0
        self.combo = 1

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

        # Stop updating after Game Over
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
                    # Unbreakable bricks don't affect score
                    # or combo.
                    break

                # -----------------------------------------
                # Reduce brick hits
                # -----------------------------------------

                brick.hits_remaining -= 1

                # -----------------------------------------
                # Brick destroyed
                # -----------------------------------------

                if brick.hits_remaining <= 0:

                    # Remove the brick
                    self.bricks.remove(brick)

                    # Task 4: scoring
                    if brick.brick_type == Brick.NORMAL:
                        base_points = 10

                    elif brick.brick_type == Brick.STRONG:
                        base_points = 30

                    else:
                        base_points = 10

                    # Apply combo multiplier
                    self.score += base_points * self.combo

                    # Increase combo for the next
                    # consecutive destroyed brick
                    self.combo += 1

                break

        # -------------------------------------------------
        # Ball falls below the screen
        # -------------------------------------------------

        if self.ball.is_below(HEIGHT):

            # Lose one life
            self.lives -= 1

            # Task 4: reset combo after missing
            self.combo = 1

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
        # Score
        # -------------------------------------------------

        renderer.draw_text(
            surface,
            font,
            f"Score: {self.score}",
            (10, 60)
        )

        # -------------------------------------------------
        # Combo
        # -------------------------------------------------

        renderer.draw_text(
            surface,
            font,
            f"Combo: x{self.combo}",
            (10, 85)
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