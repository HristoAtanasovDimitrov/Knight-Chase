# Knight-Chase

A 2D digital version of the logic-based board game "Knight Chase" built with Python and Pygame.

## Rules
- **Board:** 8x8 grid.
- **Players:** Two players (Player A and Player B) starting in opposite corners.
- **Modes:** Play either Player vs Player (PvP) or Player vs Computer (PvE).
- **Movement:** Like a Knight in Chess (an "L" shape). Click on the highlighted spots to move. In PvE mode, the computer will move automatically after your turn.
- **Trail Mechanic:** Left squares are "burnt" (turn dark grey with orange accents) and cannot be landed on again.
- **Goals:**
  - **Capture:** Land directly on the opponent's square.
  - **Trap:** The opponent has no legal moves left on the board due to "burnt" squares or edge boundaries.
- **Restart:** When the game is over, press `SPACE` to go back to the menu and play again.

## Setup
1. Make sure you have Python installed.
2. Install dependencies (specifically `pygame`):
   ```bash
   pip install -r requirements.txt
   ```
3. Run the game:
   ```bash
   python main.py
   ```
