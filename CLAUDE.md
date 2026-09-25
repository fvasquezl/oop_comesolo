# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Comesolo is a Python implementation of triangular Peg Solitaire (also known as "Cracker Barrel puzzle"). The game uses a triangular board where pieces can jump over adjacent pieces to remove them, with the goal of leaving as few pieces as possible.

This project also doubles as an OOP study exercise: `main.py` is mid-refactor, moving from a flat-index representation to a coordinate/bitmask-based one, as a way to practice composition, dependency injection, and Python typing.

## Running the Application

```bash
python main.py
```

`main.py` currently runs the **new, in-progress implementation** (see Architecture below): it builds a `TriangleGeometry`, a `BoardN`, and a `RulesN`, and prints the generated rules. The original game loop (`Comesolo(5).solve()`) is commented out at the bottom of the file and not currently wired to `__main__`.

## Architecture

`main.py` currently contains two implementations side by side.

### Legacy implementation (kept as reference, wrapped in a `"""..."""` block)

Three classes plus a solver:

- **Board**: manages the triangular board state as a flat list. Cells are indexed 0-14 for a 5-row triangle, where "1" = peg present, "0" = empty hole. `print_cells()` renders the board with ANSI coloring.
- **Rules**: generates all valid jump rules for the triangle. Uses a sub-triangle approach where each 3-row sub-triangle defines 6 possible jumps (3 directions × 2 ways). Rules are stored as `{origin: [[delete, destination], ...]}`.
- **BFSSolver**: BFS + bitmask solver that finds *all* optimal solutions (fewest pegs remaining) for a given `Board`/`Rules` pair.
- **Comesolo**: main game controller. Combines `Board`, `Rules`, and `BFSSolver` — asks for the initial position to remove, then `solve()` finds all optimal solutions and plays one at random.

This block is intentionally kept, not dead code — the new implementation's formulas (e.g. sub-triangle jump generation) are being ported from it.

### New implementation (in progress)

- **TriangleGeometry**: pure triangle geometry, independent of any board/game state. Given `rows` (and `subtriange_len`), computes `total_cells` and `subtriangles_no`, and converts between flat index and `(fila, columna)` coordinates via `index_to_coord`/`coord_to_index` (verified mutually inverse). `get_subtriangles()` returns the flat-index triples for each sub-triangle side (origin, jumped-over, destination) — verified to match the legacy `Rules` sub-triangle formula exactly.
- **BoardN**: receives a `TriangleGeometry` instance through its constructor (dependency injection) rather than owning its own `rows`. Holds board state as a single `int` bitmask (`self.pegs`, one bit per cell) plus a `self.coords: dict[(i, j), "0"/"1"]` rebuilt from the bitmask on demand for display. `print_board()` groups `coords` by row with `itertools.groupby`. `play()` asks the player for a 1-indexed position and clears that bit.
- **RulesN**: receives only a `TriangleGeometry` (deliberately *not* `BoardN`'s state) — rules depend solely on geometry, never on which cells currently hold a peg. `generate_rules()` is in progress: turning each sub-triangle side into a forward + reverse jump rule.

Design intent: rules/geometry stay decoupled from the board's runtime peg state (mirrors the legacy `Rules`/`Board` split), and shared calculations (like index↔coordinate conversion) live in one place (`TriangleGeometry`) instead of being duplicated across classes.

Not yet done: `RulesN.generate_rules()` doesn't yet produce an origin-keyed dict like the legacy `Rules.rules`; there's no solver ported to the new bitmask representation; `BoardN.play()` only removes the first piece, with no move-execution loop yet.

## Board Indexing

The triangular board is stored/numbered as a flat list with positions:
```
        0
      1   2
    3   4   5
  6   7   8   9
10  11  12  13  14
```
Both the legacy `Board` and the new `TriangleGeometry.index_to_coord`/`coord_to_index` use this same numbering.

## Language

Code comments and user prompts are in Spanish.
