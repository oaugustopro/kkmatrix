#!/usr/bin/env python
import curses
import random
import time
import sys

# Define color mappings for easy lookup
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

def draw_waterfall(win, height, width, empty_columns, color_pair):
    for i in range(width):
        for j in range(1, height):  # Start from 1 to leave the top line for revealed characters
            if i in empty_columns:
                char = ' '  # Empty space for columns with revealed characters
            else:
                char = random.choice('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
            try:
                win.addstr(j, i, char, curses.color_pair(color_pair))
            except curses.error:
                pass  # Ignore errors if the character cannot be added

def calculate_positions(width, length):
    step = max(1, width // length)
    return [i * step for i in range(length)]

def main(win, input_string=None, color_name="green"):
    try:
        curses.start_color()
        curses.curs_set(0)  # Hide cursor

        # Initialize color pairs with a default color
        if color_name in COLOR_MAP:
            curses.init_pair(1, COLOR_MAP[color_name], curses.COLOR_BLACK)
        else:
            # Fallback to green if an unknown color is provided
            curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)

        color_pair = 1  # Use color pair 1 for text
        height, width = win.getmaxyx()
        random_string = input_string if input_string else generate_random_string(min(width // 10, 10))
        revealed_chars = set()
        char_positions = calculate_positions(width, len(random_string))

        start_time = time.time()
        revealed_count = 0

        while True:
            current_time = time.time()

            if revealed_count < len(random_string) and current_time - start_time >= 1:
                x = char_positions[revealed_count]
                try:
                    win.addstr(0, x, random_string[revealed_count], curses.color_pair(color_pair))
                    revealed_chars.add(x)
                    revealed_count += 1
                    start_time = current_time
                except curses.error:
                    pass

            draw_waterfall(win, height, width, revealed_chars, color_pair)
            win.refresh()

            if revealed_count >= len(random_string):
                time.sleep(5)  # Continue waterfall for 5 seconds
                break
            else:
                time.sleep(0.05)  # Rapid change of other characters

        # Clear the screen and display the final string blinking
        win.clear()
        win.addstr(0, 0, random_string, curses.color_pair(color_pair) | curses.A_BLINK)
        win.refresh()
        win.getch()  # Wait for a key press to exit

    except curses.error as e:
        print("Curses error:", e)

if __name__ == "__main__":
    input_string = sys.argv[1] if len(sys.argv) > 1 else None
    color_name = sys.argv[2].lower() if len(sys.argv) > 2 else "green"  # Get color from arguments
    curses.wrapper(main, input_string, color_name)
