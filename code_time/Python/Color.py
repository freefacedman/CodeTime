"""
Enhanced Encoded Message Visualizer
-----------------------------------
A Pygame application that allows users to encode messages into a color-coded grid.
Features:
- Resizable borderless window with customizable grid size.
- Color legend displayed at the bottom of the window.
- Help overlay integrated with the legend.
- Option to save the encoded message as an image without the legend.
- Export and import color legends for secure message sharing.
- Dynamic color map generation based on a password seed.
- Toggle between different background themes.
- Zoom in and out of the grid for better readability.
- Help overlay with available controls and final notes.
"""

import sys
import string
import random
import math
import pyperclip
import pygame

# Initialize Pygame and its font module
pygame.init()
pygame.font.init()

# Define background themes
THEMES = {
    "light": (255, 255, 255),
    "pastel": (245, 230, 255)
}

# Default color legend for encoding
DEFAULT_LEGEND = {
    "A": (255, 0, 0),    "B": (0, 0, 255),    "C": (255, 255, 0),    "D": (240, 225, 48),
    "E": (0, 0, 0),      "F": (34, 139, 34),  "G": (128, 128, 128),  "H": (210, 180, 140),
    "I": (75, 0, 130),   "J": (165, 42, 42),  "K": (255, 235, 205),  "L": (50, 205, 50),
    "M": (255, 0, 255),  "N": (165, 42, 42),  "O": (230, 190, 255),  "P": (128, 0, 128),
    "Q": (218, 112, 214),"R": (255, 0, 0),    "S": (192, 192, 192),  "T": (0, 128, 128),
    "U": (100, 149, 237),"V": (238, 130, 238),"W": (123, 191, 123),  "X": (0, 123, 104),
    "Y": (255, 255, 0),  "Z": (57, 255, 20),
}

# Special characters that require unique drawings
SPECIALS = {",", "-", "#", "!", "."}

# Initialize clock
clock = pygame.time.Clock()

def generate_color_map(password=""):
    """
    Generates a randomized color map based on a password seed.

    Args:
        password (str): Seed for randomization to ensure reproducibility.

    Returns:
        dict: Mapping of uppercase letters to RGB color tuples.
    """
    letters = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    random.seed(password)
    random.shuffle(letters)
    color_map = {}
    for letter in letters:
        r = 100 + random.randint(0, 155)
        g = 100 + random.randint(0, 155)
        b = 100 + random.randint(0, 155)
        color_map[letter] = (r, g, b)
    return color_map

def export_legend_to_file(color_map, filepath):
    """
    Exports the color legend to a text file.

    Args:
        color_map (dict): Mapping of letters to RGB colors.
        filepath (str): Path to the output file.
    """
    try:
        with open(filepath, "w", encoding='utf-8') as f:
            for k, v in color_map.items():
                f.write(f"{k}:{v[0]},{v[1]},{v[2]}\n")
    except Exception as e:
        print(f"Error exporting legend: {e}")

def parse_legend_file(filepath):
    """
    Parses a legend file and returns the color map.

    Args:
        filepath (str): Path to the legend file.

    Returns:
        dict or None: Mapping of letters to RGB colors, or None if parsing fails.
    """
    legend = {}
    try:
        with open(filepath, "r", encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or ":" not in line:
                    continue
                letter, rgb_str = line.split(":")
                r, g, b = rgb_str.split(",")
                legend[letter.upper()] = (int(r), int(g), int(b))
    except Exception as e:
        print(f"Error parsing legend file: {e}")
        legend = None
    return legend

def draw_special_char(ch, x, y, sz):
    """
    Draws special characters with unique designs.

    Args:
        ch (str): The special character to draw.
        x (int): X-coordinate of the top-left corner of the grid cell.
        y (int): Y-coordinate of the top-left corner of the grid cell.
        sz (int): Size of the grid cell.
    """
    if ch == ",":
        pygame.draw.arc(screen, (0,0,0), (x, y+sz-15, sz, 15), 0, math.pi, 2)
    elif ch == "-":
        pygame.draw.line(screen, (0,0,0), (x, y+sz//2), (x+sz, y+sz//2), 2)
    elif ch == "#":
        t = 2
        pygame.draw.line(screen, (0,0,0), (x+t, y+t), (x+sz-t, y+t), t)
        pygame.draw.line(screen, (0,0,0), (x+t, y+sz//4), (x+sz-t, y+sz//4), t)
        pygame.draw.line(screen, (0,0,0), (x+t, y+sz//2), (x+sz-t, y+sz//2), t)
        pygame.draw.line(screen, (0,0,0), (x+t, y+3*(sz//4)), (x+sz-t, y+3*(sz//4)), t)
    elif ch == "!":
        pygame.draw.line(screen, (0,0,0), (x+sz//2, y+sz//2), (x+sz//2, y+sz-2), 2)
    elif ch == ".":
        pygame.draw.circle(screen, (0,0,0), (x+sz//2, y+sz-2), 2)

def draw_encoded_message(msg, color_map, grid_size, theme_bg, message_surface):
    """
    Draws the encoded message on the provided surface.

    Args:
        msg (str): The message to encode.
        color_map (dict): Mapping of letters to RGB colors.
        grid_size (int): Size of each grid cell.
        theme_bg (tuple): Background color tuple.
        message_surface (pygame.Surface): Surface to draw the message on.
    """
    w, h = message_surface.get_size()
    message_surface.fill(theme_bg)
    cols = max(1, w // grid_size)
    offset_y = 0
    for i, ch in enumerate(msg):
        up_ch = ch.upper()
        c = color_map.get(up_ch, (255,255,255))
        x = (i % cols) * grid_size
        y = (i // cols) * grid_size + offset_y
        if y > h - grid_size:
            break
        pygame.draw.rect(message_surface, (255,255,255), (x, y, grid_size, grid_size))
        if ch in SPECIALS:
            draw_special_char(ch, x, y, grid_size)
        elif ch != " " and ch not in string.punctuation:
            pygame.draw.rect(message_surface, c, (x, y, grid_size, grid_size))
        if ch.isupper():
            pygame.draw.rect(message_surface, (0,0,0), (x, y, grid_size, grid_size), 3)

def draw_legend(color_map, grid_size, legend_surface):
    """
    Draws the color legend at the bottom of the window.

    Args:
        color_map (dict): Mapping of letters to RGB colors.
        grid_size (int): Size of each grid cell.
        legend_surface (pygame.Surface): Surface to draw the legend on.
    """
    legend_surface.fill((200, 200, 200))  # Grey background for legend
    padding = 10
    box_size = 20
    font_size = 20
    font = pygame.font.SysFont(None, font_size)
    x, y = padding, padding
    max_width, max_height = legend_surface.get_size()
    for letter, color in sorted(color_map.items()):
        if x + box_size + 30 > max_width:
            x = padding
            y += box_size + padding
        pygame.draw.rect(legend_surface, color, (x, y, box_size, box_size))
        text_surface = font.render(letter, True, (0,0,0))
        legend_surface.blit(text_surface, (x + box_size + 5, y))
        x += box_size + 30

def save_screen_as_image(message_surface, filename="encoded_message.png"):
    """
    Saves the encoded message surface as an image file.

    Args:
        message_surface (pygame.Surface): Surface containing the encoded message.
        filename (str): Name of the file to save the image as.
    """
    try:
        pygame.image.save(message_surface, filename)
        print(f"Screen saved as {filename}")
    except Exception as e:
        print(f"Error saving screen: {e}")

def main():
    """
    Main function to run the Encoded Message Visualizer.
    """
    global screen
    pygame.display.set_caption("Enhanced Encoded Message Visualizer")
    default_width, default_height = 1280, 720
    screen = pygame.display.set_mode((default_width, default_height), pygame.RESIZABLE | pygame.NOFRAME)  # pylint: disable=no-member

    base_font = pygame.font.SysFont(None, 36)
    clock = pygame.time.Clock()
    running = True
    input_box = pygame.Rect(50, 50, 300, 40)
    col_inactive = pygame.Color("lightskyblue3")
    col_active = pygame.Color("dodgerblue2")
    box_color = col_inactive
    text_input = ""
    active = False
    input_done = True
    grid_size = 20
    theme_choice = "light"
    current_legend = DEFAULT_LEGEND.copy()
    dynamic_legend = False
    msg_displayed = ""
    show_help = True

    # Initialize message_surface
    w, h = screen.get_size()
    legend_height = 100
    message_height = h - legend_height - 100  # 100 reserved for input box and padding
    message_surface = pygame.Surface((w, message_height))  # pylint: disable=no-member

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # pylint: disable=no-member
                running = False
            elif event.type == pygame.KEYDOWN:  # pylint: disable=no-member
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif active:
                    if event.key == pygame.K_RETURN:
                        msg_displayed = text_input
                        draw_encoded_message(msg_displayed, current_legend, grid_size, THEMES[theme_choice], message_surface)
                        active = False
                        input_done = True
                    elif event.key == pygame.K_BACKSPACE:
                        text_input = text_input[:-1]
                    elif event.key == pygame.K_v and (event.mod & pygame.KMOD_CTRL):
                        try:
                            text_input += pyperclip.paste()
                        except Exception as e:
                            print(f"Error pasting text: {e}")
                    else:
                        text_input += event.unicode
                else:
                    if event.key == pygame.K_s:
                        save_screen_as_image(message_surface)
                    elif event.key == pygame.K_l:
                        export_legend_to_file(current_legend, "legend.txt")
                    elif event.key == pygame.K_r:
                        loaded = parse_legend_file("legend.txt")
                        if loaded:
                            current_legend = loaded
                            draw_encoded_message(msg_displayed, current_legend, grid_size, THEMES[theme_choice], message_surface)
                    elif event.key == pygame.K_t:
                        theme_choice = "pastel" if theme_choice == "light" else "light"
                        draw_encoded_message(msg_displayed, current_legend, grid_size, THEMES[theme_choice], message_surface)
                    elif event.key == pygame.K_g:
                        dynamic_legend = not dynamic_legend
                        if dynamic_legend:
                            password = "seeded"
                            current_legend = generate_color_map(password)
                        else:
                            current_legend = DEFAULT_LEGEND.copy()
                        draw_encoded_message(msg_displayed, current_legend, grid_size, THEMES[theme_choice], message_surface)
                    elif event.key in (pygame.K_PLUS, pygame.K_EQUALS):
                        grid_size += 2
                        if grid_size > 100:
                            grid_size = 100
                        draw_encoded_message(msg_displayed, current_legend, grid_size, THEMES[theme_choice], message_surface)
                    elif event.key == pygame.K_MINUS:
                        grid_size -= 2
                        if grid_size < 5:
                            grid_size = 5
                        draw_encoded_message(msg_displayed, current_legend, grid_size, THEMES[theme_choice], message_surface)
                    elif event.key == pygame.K_h:
                        show_help = not show_help
            elif event.type == pygame.MOUSEBUTTONDOWN:  # pylint: disable=no-member
                if input_box.collidepoint(event.pos) and input_done:
                    active = True
                    input_done = False
                else:
                    active = False
                box_color = col_active if active else col_inactive
            elif event.type == pygame.VIDEORESIZE:  # pylint: disable=no-member
                # Reassign screen with the new size
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE | pygame.NOFRAME)  # pylint: disable=no-member
                # Recreate message_surface with updated size
                w, h = screen.get_size()
                legend_height = 100
                message_height = h - legend_height - 100  # 100 reserved for input box and padding
                message_surface = pygame.Surface((w, message_height))  # pylint: disable=no-member
                # Redraw the message
                draw_encoded_message(msg_displayed, current_legend, grid_size, THEMES[theme_choice], message_surface)

        # Handle dynamic resizing outside of event loop
        w, h = screen.get_size()
        legend_height = 100
        message_height = h - legend_height - 100  # 100 reserved for input box and padding
        if message_surface.get_size() != (w, message_height):
            message_surface = pygame.Surface((w, message_height))  # pylint: disable=no-member
            draw_encoded_message(msg_displayed, current_legend, grid_size, THEMES[theme_choice], message_surface)

        # Blit the message_surface to the screen
        screen.blit(message_surface, (0, 100))  # 100 reserved for input box and padding

        # Draw the legend at the bottom
        legend_surface = pygame.Surface((w, legend_height))  # pylint: disable=no-member
        draw_legend(current_legend, grid_size, legend_surface)
        screen.blit(legend_surface, (0, h - legend_height))

        # Draw the input box
        screen.fill(THEMES[theme_choice], (input_box.x, input_box.y, input_box.w, input_box.h))
        txt_surface = base_font.render(text_input, True, box_color)
        input_box.w = max(300, txt_surface.get_width() + 20)
        screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
        pygame.draw.rect(screen, box_color, input_box, 2)

        # Draw the help overlay with final notes
        if show_help:
            help_lines = [
                "Controls:",
                "Type a message and press ENTER to encode.",
                "[S] Save as Image    [L] Export Legend    [R] Load Legend",
                "[T] Toggle Theme     [G] Toggle Random Legend  [H] Hide/Show Help",
                "[+/-] Zoom Grid      [ESC] Quit",
                "",
                "Final Notes:",
                "Legend Export and Import:",
                "Ensure that when sharing encoded messages, you also securely share the corresponding legend.txt file to allow the recipient to decode the message.",
                "",
                "Custom Password for Color Map:",
                "To enhance security, consider allowing users to input a custom password for generating the color map, ensuring that only those with the password can decode the message.",
                "",
                "Error Handling:",
                "The script includes basic error handling for file operations. For a more robust application, consider adding more detailed error messages or recovery options.",
                "",
                "Further Enhancements:",
                "You can continue to build upon this script by adding features such as:",
                "- Animated Encoding: Animate the drawing of the message for a more engaging visual.",
                "- Multiple Legends: Support multiple legends for different parts of the message.",
                "- Encryption Keys: Integrate more complex encryption mechanisms for enhanced security."
            ]
            font_size = 18
            help_font = pygame.font.SysFont(None, font_size)
            y_offset = 0
            for line in help_lines:
                if y_offset + 20 > legend_height:
                    break  # Prevent overflow
                help_surface = help_font.render(line, True, (50, 50, 50))
                screen.blit(help_surface, (50, 60 + y_offset))  # Positioned near the input box
                y_offset += 20

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
