import sys
import pygame
from constants import (
    SCREEN_WIDTH,
    SCREEN_HEIGHT,
    BUTTON_WIDTH,
    BUTTON_HEIGHT,
    BUTTON_COLOR,
    BUTTON_HOVER_COLOR,
    BUTTON_TEXT_COLOR,
    BUTTON_BORDER_RADIUS
)

def create_button(screen, text, x, y, width, height, color, hover_color, text_color, font, action=None):
    mouse_pos = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    button_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    is_hover = x < mouse_pos[0] < x + width and y < mouse_pos[1] < y + height

    if is_hover:
        pygame.draw.rect(button_surface, hover_color, (0, 0, width, height), 0, BUTTON_BORDER_RADIUS)
        pygame.draw.rect(button_surface, (255, 255, 255, 50), (0, 0, width, height), 2, BUTTON_BORDER_RADIUS)

        if click[0] == 1 and action is not None:
            return action
    else:
        pygame.draw.rect(button_surface, color, (0, 0, width, height), 0, BUTTON_BORDER_RADIUS)
        pygame.draw.rect(button_surface, (255, 255, 255, 30), (0, 0, width, height), 2, BUTTON_BORDER_RADIUS)

    text_surf = font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(width/2, height/2))
    button_surface.blit(text_surf, text_rect)
    screen.blit(button_surface, (x, y))

    return None

def show_controls_guide(screen, x, y, font):
    controls = [
        "CONTROLS:",
        "Arrow UP: Thrust forward",
        "Arrow LEFT/RIGHT: Rotate ship",
        "SPACE: Fire weapon",
    ]

    line_height = 30
    for i, line in enumerate(controls):
        if i == 0:
            text = font.render(line, True, (255, 255, 100))
        else:
            text = font.render(line, True, (200, 200, 200))

        screen.blit(text, (x - text.get_width() // 2, y + i * line_height))

    return (len(controls) * line_height) + 20

def show_start_menu(screen, bg_image, font):
    title_font = pygame.font.Font(None, 90)
    controls_font = pygame.font.Font(None, 30)

    while True:
        screen.blit(bg_image, (0, 0))
        title_text = title_font.render("ASTEROIDS", True, (255, 255, 255))
        title_x = SCREEN_WIDTH/2 - title_text.get_width()/2
        title_y = SCREEN_HEIGHT/4
        glow_text = title_font.render("ASTEROIDS", True, (100, 100, 255, 50))
        screen.blit(glow_text, (title_x + 3, title_y + 3))
        screen.blit(title_text, (title_x, title_y))
        controls_height = show_controls_guide(screen, SCREEN_WIDTH/2, title_y + title_text.get_height() + 30, controls_font)
        button_y = title_y + title_text.get_height() + 30 + controls_height

        start_action = create_button(
            screen, "START GAME",
            SCREEN_WIDTH/2 - BUTTON_WIDTH/2,
            button_y,
            BUTTON_WIDTH, BUTTON_HEIGHT,
            BUTTON_COLOR, BUTTON_HOVER_COLOR,
            BUTTON_TEXT_COLOR, font,
            "start"
        )

        exit_action = create_button(
            screen, "EXIT",
            SCREEN_WIDTH/2 - BUTTON_WIDTH/2,
            button_y + BUTTON_HEIGHT + 20,
            BUTTON_WIDTH, BUTTON_HEIGHT,
            BUTTON_COLOR, BUTTON_HOVER_COLOR,
            BUTTON_TEXT_COLOR, font,
            "exit"
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if start_action == "start":
            return
        elif exit_action == "exit":
            pygame.quit()
            sys.exit()

def show_game_over_screen(screen, bg_image, font, score):
    title_font = pygame.font.Font(None, 90)

    while True:
        screen.blit(bg_image, (0, 0))
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 120))
        screen.blit(overlay, (0, 0))
        gameover_text = title_font.render("GAME OVER", True, (255, 100, 100))
        gameover_x = SCREEN_WIDTH/2 - gameover_text.get_width()/2
        gameover_y = SCREEN_HEIGHT/4
        glow_text = title_font.render("GAME OVER", True, (150, 0, 0, 80))
        screen.blit(glow_text, (gameover_x + 3, gameover_y + 3))
        screen.blit(gameover_text, (gameover_x, gameover_y))
        score_text = font.render(f"FINAL SCORE: {score}", True, (220, 220, 220))
        screen.blit(score_text, (SCREEN_WIDTH/2 - score_text.get_width()/2, gameover_y + gameover_text.get_height() + 30))

        restart_action = create_button(
            screen, "PLAY AGAIN",
            SCREEN_WIDTH/2 - BUTTON_WIDTH/2,
            gameover_y + gameover_text.get_height() + 100,
            BUTTON_WIDTH, BUTTON_HEIGHT,
            BUTTON_COLOR, BUTTON_HOVER_COLOR,
            BUTTON_TEXT_COLOR, font,
            "restart"
        )

        exit_action = create_button(
            screen, "EXIT",
            SCREEN_WIDTH/2 - BUTTON_WIDTH/2,
            gameover_y + gameover_text.get_height() + 100 + BUTTON_HEIGHT + 20,
            BUTTON_WIDTH, BUTTON_HEIGHT,
            BUTTON_COLOR, BUTTON_HOVER_COLOR,
            BUTTON_TEXT_COLOR, font,
            "exit"
        )

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if restart_action == "restart":
            return True
        elif exit_action == "exit":
            pygame.quit()
            sys.exit()
