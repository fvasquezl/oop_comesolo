# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a Python implementation of "Comesolo" (Peg Solitaire), a single-player board game. The game uses a triangular board where the goal is to eliminate pegs by jumping over them until only one peg remains.

## Running the Application

```bash
python main.py
```

The game prompts for an initial position (1-15) to remove, then automatically plays random valid moves until no moves remain.

## Architecture

The codebase consists of three classes in `main.py`:

- **Board**: Manages the triangular game board state. Uses a 1D list to represent the 15-cell triangle (5 rows). Cells contain "1" (peg present) or "0" (empty).

- **Rules**: Generates valid jump rules for the triangular board. Calculates all possible moves by identifying sub-triangles of depth 3 and creating bidirectional jump rules (origin -> delete -> destination).

- **Comesolo**: Main game controller. Orchestrates board creation, validates moves against rules, and executes random valid moves.

## Board Indexing

The triangular board positions are numbered 0-14 in row-major order:
```
        0
      1   2
    3   4   5
  6   7   8   9
10  11  12  13  14
```

## Key Implementation Details

- Jump rules are pre-computed as a dictionary mapping origin positions to lists of [delete, destination] pairs
- Valid moves require: origin has peg ("1"), middle position has peg ("1"), destination is empty ("0")
- The `make_move` method is implemented as a property that executes one random move and returns True/False for continuation
