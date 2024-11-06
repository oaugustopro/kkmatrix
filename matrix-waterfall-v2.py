#!/usr/bin/env python
import curses
import random
import time
import sys

# Define a color map for easy lookup
COLOR_MAP = {
    "red": curses.COLOR_RED,
    "blue": curses.COLOR_BLUE,
    "yellow": curses.COLOR_YELLOW,
    "green": curses.COLOR_GREEN,
    "grey": curses.COLOR_WHITE,
    "cyan": curses.COLOR_CYAN,
    "magenta": curses.COLOR_MAGENTA,
}

def generate_random_string(length=10):
    return ''.join(random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ') for _ in range(length))

def draw_waterfall(win, height, width, empty_columns, n, color_pair, freeze=False, freeze_rect=None):
    for i in range(width):
        for j in range(1, height):  # Start from 1 to leave the top line for revealed characters
            if freeze and freeze_rect and (freeze_rect[0] <= i <= freeze_rect[2]) and (freeze_rect[1] <= j <= freeze_rect[3]):
                continue  # Skip drawing in the rectangle area
            if i % n in empty_columns:
                char = ' '  # Empty space for columns with revealed characters
            else:
                char = random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
            try:
                win.addstr(j, i, char, curses.color_pair(color_pair))
            except curses.error:
                pass  # Ignore errors if the character cannot be added

def draw_rectangle(win, start_x, start_y, width, height, color_pair):
    # Draw horizontal lines
    for x in range(start_x, start_x + width):
        win.addch(start_y, x, curses.ACS_HLINE, curses.color_pair(color_pair))
        win.addch(start_y + height, x, curses.ACS_HLINE, curses.color_pair(color_pair))

    # Draw vertical lines
    for y in range(start_y, start_y + height + 1):
        win.addch(y, start_x, curses.ACS_VLINE, curses.color_pair(color_pair))
        win.addch(y, start_x + width - 1, curses.ACS_VLINE, curses.color_pair(color_pair))

    # Draw corners
    win.addch(start_y, start_x, curses.ACS_ULCORNER, curses.color_pair(color_pair))
    win.addch(start_y, start_x + width - 1, curses.ACS_URCORNER, curses.color_pair(color_pair))
    win.addch(start_y + height, start_x, curses.ACS_LLCORNER, curses.color_pair(color_pair))
    win.addch(start_y + height, start_x + width - 1, curses.ACS_LRCORNER, curses.color_pair(color_pair))

def display_system_failure(win, height, width, color_pair):
    message = "System Failure"
    msg_width = len(message) + 2  # Space for the message
    msg_height = 2
    start_x = width // 2 - msg_width // 2
    start_y = height // 2 - 1
    draw_rectangle(win, start_x, start_y, msg_width, msg_height, color_pair)
    win.addstr(start_y + msg_height // 2, start_x + 1, message, curses.color_pair(color_pair))
    return (start_x, start_y, start_x + msg_width, start_y + msg_height)

def display_string(win, random_string, revealed_chars, color_pair):
    for i, char in enumerate(random_string):
        if i in revealed_chars:
            try:
                win.addstr(0, i, char, curses.color_pair(color_pair))
            except curses.error:
                pass

def main(win, input_string=None, freeze_halfway=False, color_name="green"):
    try:
        curses.start_color()
        curses.curs_set(0)  # Hide cursor

        # Set up color based on input
        if color_name in COLOR_MAP:
            curses.init_pair(1, COLOR_MAP[color_name], curses.COLOR_BLACK)
        else:
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Default to green if unknown color

        color_pair = 1
        height, width = win.getmaxyx()
        random_string = input_string if input_string else generate_random_string(min(width, 10))
        n = len(random_string)
        revealed_chars = set()
        last_reveal_time = time.time()
        freeze_time = None if not freeze_halfway else time.time() + len(random_string) // 2

        while True:
            current_time = time.time()
            freeze_now = freeze_halfway and freeze_time and current_time >= freeze_time

            if freeze_now:
                freeze_rect = display_system_failure(win, height, width, color_pair)
                draw_waterfall(win, height, width, revealed_chars, n, color_pair, freeze=True, freeze_rect=freeze_rect)
                display_string(win, random_string, revealed_chars, color_pair)  # Display string at the top left
                win.refresh()
                win.getch()  # Wait for a key press to exit
                break

            if len(revealed_chars) < n and current_time - last_reveal_time >= 1:
                revealed_chars.add(len(revealed_chars))
                last_reveal_time = current_time

            draw_waterfall(win, height, width, revealed_chars, n, color_pair)
            display_string(win, random_string, revealed_chars, color_pair)  # Display string at the top left
            win.refresh()
            time.sleep(0.01)  # Rapid change of other characters

    except curses.error as e:
        print("Curses error:", e)

if __name__ == "__main__":
    freeze_halfway = '-n' in sys.argv
    input_string = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] != '-n' else None
    color_name = sys.argv[2].lower() if len(sys.argv) > 2 else "green"  # Get color from arguments
    curses.wrapper(main, input_string, freeze_halfway, color_name)
