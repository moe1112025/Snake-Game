🚩 Project Report: Snake PRO Edition
Developer: Moe Htet
Language: Python 3.x
Library: Pygame
---------------------------
1. Executive Summary
The "Snake: Moe Htet PRO Edition" is a modern take on the classic arcade game. It features a robust state management system, progressive difficulty scaling, and a refined input-handling logic to ensure a smooth and professional user experience.
----------------------------
2. Key Features
State Machine Architecture: Seamless transitions between the Main Menu, Gameplay, Pause, and Game Over states.
Progressive Difficulty: The game engine tracks the score and increases the clock.tick speed every 30 points to maintain a challenge.
Input Buffering (Direction Lock): A safety mechanism that prevents the snake from colliding with itself during rapid key presses.
Dynamic Visuals: Includes a head-differentiation system (distinct color and eyes) and a background grid for better spatial awareness.
-------------------------------
🧠 Technical Logic ExplanationA. The Movement Logic (Vectors)The snake doesn't actually "slide." It calculates a new position for its head based on a 2D vector.If moving RIGHT, it adds BLOCK_SIZE (20px) to the $X$ coordinate.The rest of the body follows by inserting the new head at index 0 and "popping" (removing) the last tail segment.
---------------------------------
B. Collision Matrix
The game runs a check every single frame:
Boundary Check: if head_x < 0 or head_x >= WIDTH...
Self-Collision Check: if head in snake_body...
Food Check: if head == food_pos... (If true, it skips the pop() function so the snake grows).

C. Resource Management (The Constants)
By separating constants (Colors, Directions, States) from the logic, the project follows the DRY (Don't Repeat Yourself) principle. This allows a developer to change the entire look of the game by editing just one section of the code.
-----------------------------------
🛠 Troubleshooting & Development Steps
During the development, several logical hurdles were cleared:
Food Overlap: Fixed by using a while loop to ensure food never spawns on a coordinate currently occupied by the snake_body.
The 180-Turn Bug: Solved by implementing a direction_lock boolean that resets only after the game state updates, preventing the snake from "folding" into itself.
Interface Stuck: Fixed by mapping the K_ESCAPE key to global state resets, ensuring the player is never trapped on a Game Over screen.
-----------------------------------------
"I built this using a State Machine approach. Instead of just having a game that runs, the code knows whether it's in 'Menu mode' or 'Play mode.' I also added a Direction Lock which is a professional touch to prevent the snake from dying due to fast typing. As you play, the game calculates your score and dynamically increases the speed, making it a true 'Pro Edition' experience." 
--

Make sure install "pip install pygame" in your terminal especiall Visual Studio Code Editor
