# Minesweeper Game

## Overview

This project is a simple implementation of the classic Minesweeper game using Python and Tkinter. The game generates a grid where players must uncover squares without hitting bombs. Players can flag squares suspected of containing bombs and win by uncovering all non-bomb squares.

## Features

Graphical user interface using Tkinter.

Configurable grid size and number of bombs.

Left-click to uncover a square.

Right-click (or middle-click) to place or remove a flag.

Auto-reveal of empty squares.

Bomb indicators with different colors.

Win/Loss notification messages.

## Installation

### Prerequisites

Ensure you have Python installed (Python 3.x recommended).

Install Tkinter if not already available (typically included with Python).

### Steps

Clone or download the repository.

Navigate to the project directory.

Run the script using:

python minesweeper.py

## How to Play

A Minesweeper grid will appear.

Left-click a square to reveal it:

If it's a bomb, you lose.

If it's an empty space, adjacent squares may be revealed.

If it's a numbered square, it indicates how many bombs are adjacent.

Right-click (or middle-click) to place/remove a flag on a suspected bomb.

The game ends when:

You successfully flag all bombs and uncover all other squares (Win).

You uncover a bomb (Lose).

## Configuration

You can customize the grid size and number of bombs by modifying the script's function call:

play_minesweeper(width, height, bombAmount)

For example:

play_minesweeper(12, 10, 15)

sets up a 12x10 grid with 15 bombs.

## License

This project is open-source and free to use. Modify and improve as needed!
