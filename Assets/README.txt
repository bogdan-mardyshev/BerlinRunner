# Berlin Runner - Pygame Project
Student Name: Bogdan Mardyshev
Matriculation Number: 100007202
 1. Game Concept
"Berlin Runner" is an endless runner game inspired by the daily life in Berlin. The player controls a character running U-Bahn tunnels and S-Bahn platforms. The goal is to survive as long as possible while dodging obstacles and dealing with ticket controllers.
Unique Mechanic: The "Pfand" (Deposit) System.
- The player collects bottles (+5ÿ).
- Hitting obstacles (Scooters, Trash cans, Dove) causes an instant game over.
- Hitting a  Controller (Fahrscheinkontrolle) checks the player's wallet.
    - If the player has collected at least 60ÿ, the fine is paid automatically, and the game continues.
    - If the player has less than 60ÿ, it's "Game Over" (Schwarzfahren).
 2. How to Run the Game
1. Ensure Python 3.x and Pygame are installed:
   pip install pygame
2. Make sure the 'Assets' folder is in the same directory as the scripts.
3. Run the main file: python main.py
Controls:
- SPACE / UP Arrow: Jump
- DOWN Arrow: Crouch (to dodge flying doves)
-SPACE to Start/Restart
 3. Implementation & Custom Classes
I implemented  6 custom classes to manage game entities:
1. Player Class:
   - Handles physics (gravity, jumping velocity).
   - Manages animations (running, crouching).
- Handles input and sound effects.
2. Enemy Class (The Controller):
   - Features a unique behavior: moves with the background but accelerates towards the player when triggered.
   - Interacts with the global money  variable to determine survival.
3. Bottle Class (Collectible):
   - Adds value to the `money` score when collected.
   - Can spawn at different heights.
4. Dove Class (Flying Obstacle):
   - Has a flying animation.
   - Moves faster than the background (parallax effect).
5. Trash & Scooter Classes:
   - Static ground obstacles with randomized spawn positions.
4. Additional Features
- Infinite Scrolling World: The background loops seamlessly.
- Biome Switching: The game transitions dynamically between the "U-Bahn Tunnel" and "S -Bahn platform" based on the score.(Switch after 330 point)
- Audio System:Background techno music and sound effects for actions (jump, collect, hit).
