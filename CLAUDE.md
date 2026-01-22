# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Comesolo is a Python implementation of triangular Peg Solitaire (also known as "Cracker Barrel puzzle"). The game uses a triangular board where pieces can jump over adjacent pieces to remove them, with the goal of leaving as few pieces as possible.

## Running the Application

```bash
python main.py
```

The game prompts for an initial position to remove (1-15 for a 5-row board), then makes random valid moves.

## Architecture

The codebase consists of three classes in `main.py`:

- **Board**: Manages the triangular board state as a flat list. Cells are indexed 0-14 for a 5-row triangle, where "1" = peg present, "0" = empty hole. The `print_cells()` method renders the board with ANSI coloring.

- **Rules**: Generates all valid jump rules for the triangle. Uses a sub-triangle approach where each 3-row sub-triangle defines 6 possible jumps (3 directions × 2 ways). Rules are stored as `{origin: [[delete, destination], ...]}`.

- **Comesolo**: Main game controller that combines Board and Rules. The `make_move` property finds all valid moves and executes one randomly.

## Board Indexing

The triangular board is stored as a flat list with positions:
```
        0
      1   2
    3   4   5
  6   7   8   9
10  11  12  13  14
```

## Language

Code comments and user prompts are in Spanish.
