# kkmatrix
Show a matrix code like in the movie

# Waterfall Animation with System Failure Simulation

This repository contains two Python scripts that create a dynamic "waterfall" animation in a terminal using `curses`. The scripts simulate cascading characters with a gradually revealed string and feature an optional system failure message.

## Scripts

1. **waterfall.py**: This script animates a waterfall of random characters while revealing a specified string character by character at the top of the screen. The waterfall animation runs for 5 seconds after the string is fully revealed.

2. **waterfall_system_failure.py**: An enhanced version of the first script, with an optional system failure feature that freezes half of the animation screen with a "System Failure" message when triggered by a flag.

## Requirements

- Python 3.x
- `curses` library (available in Python’s standard library for Unix-based systems)

## Usage

### `waterfall.py`
Run `waterfall.py` with an optional input string argument. If no argument is provided, a random string is generated.

```bash
python waterfall.py [input_string]
```

## Example:

python waterfall.py "HELLO"

This displays "HELLO" at the top while characters cascade down the screen.

## waterfall_system_failure.py

Run waterfall_system_failure.py with optional arguments: -n to trigger the system failure halfway through the animation, and [input_string] to specify a custom string.

python waterfall_system_failure.py [-n] [input_string]

## Example

python waterfall_system_failure.py -n "ERROR"

The script freezes with a "System Failure" message halfway through the animation.

## Functions Overview

    generate_random_string(length): Generates a random string of specified length.
    draw_waterfall(win, height, width, empty_columns, ...): Draws cascading characters in the terminal.
    calculate_positions(width, length): Calculates character positions for string display.
    display_system_failure(win, height, width): Displays a "System Failure" message.
    display_string(win, random_string, revealed_chars): Shows the revealed string characters.

## Customization

You can adjust the delay times, waterfall characters, and visual effects within each script as needed. Feel free to explore the code for more custom configurations.

## License

This project is licensed under the MIT License. See the LICENSE file for details.
Contributing

Contributions are welcome! Please open an issue to discuss any changes or suggestions.

## Author

Created by oaugustopro.

Enjoy the animation, and feel free to customize the scripts!
