# Reversi Game Implementation

# Table of Contents
- [Introduction](#introduction)
- [Setup](#setup)
  - [Prerequisites](#prerequisites)
  - [Installing Dependencies](#installing-dependencies)
  - [Running the Application](#running-the-application)
- [Usage](#usage)
  - [Console Gameplay Instructions](#console-gameplay-instructions)
  - [Web Gameplay Instructions](#web-gameplay-instructions)
- [Architecture](#architecture)
    - [Explanation of our MVC Architecture](#explanation-of-our-mvc-architecture)
    - [Explanation of some important files](#explanation-of-some-important-files)
    - [Explanation of some important directories](#explanation-of-some-important-directories)
- [Acknowledgements](#acknowledgements)
- [Misc.](#misc)

## Introduction
This README provides information on the setup and usage for the Reversi game implementation, which supports both web and console (CLI) interfaces. The game features MVC architecture, AI opponents, database integration for scorekeeping, and a React-based web UI.

## Setup

### Prerequisites
- Python 3.x
- Flask (for web interface)
- MySQL (for database functionality)
- Node.js and npm (for React web interface)

### Installing Dependencies
#### Python Dependencies
```bash
pip install flask flask-cors mysql-connector-python
```

#### React Dependencies
Navigate to the `view/my-react-reversi` directory and run:
```bash
npm install
```

#### Firebase Dependencies
```bash
npm install firebase
```


### Running the Application
#### Console Interface (Command-Line Interface)
```bash
python main.py
```
This command starts the console version of the game.

#### Web/GUI Interface
Start the Flask backend server:
```bash
python app.py
```
Then, launch the React front end in a separate terminal:
```bash
cd view/my-react-reversi
npm run dev
```

## Usage
### Console Gameplay (Command-line Interface)
The console interface of the Reversi game presents a text-based version of the game board and interacts with the user through the console for making moves, displaying the game state, and managing game flow.

### Console Gameplay Instructions
1. **Starting the Game:** Run `python main.py` from the command line to start the game in console mode. The game initializes and displays the initial state of the game board on your command line.

2. **Viewing the Game Board:** The console displays the game board using symbols to represent different players. Each cell on the board is shown in a grid format, with pieces represented by specific symbols (e.g., X and O for the two players).

3. **Making a Move:** The game will prompt the player to enter their move. Moves are typically entered as coordinates corresponding to the board's grid (e.g., row and column), but the exact format can vary. Follow the on-screen instructions for inputting your move.

4. **Game Progression:** After each move, the game board updates and displays the new state. The game automatically checks for legal moves, captures opponent pieces according to Reversi rules, and updates the players' scores.

5. **Ending the Game:** The game concludes either when no legal moves remain for both players or if the game is manually terminated (e.g., by pressing `Ctrl+C` on macOS or Windows). Upon completion, the console displays the final scores and declares the winner.


6. **Additional Features:** Playing against an AI opponent. The first on-screen instruction asks if you would like to play against the AI opponnent.

### Tips for Playing
- Pay attention to the game's instructions for entering moves. Incorrect input formats throw errors.

### Web Gameplay Instructions
1. **Launching the Game:**
   - Start the Flask backend by running `python app.py` from the command line. This will initiate the server to handle game logic and state management, typically `http://127.0.0.1:5000`.
   - Open a new terminal window and navigate to the `view/my-react-reversi` directory. Run `npm run dev` to launch the React development server. Your default web browser should automatically open to the game's URL, typically `http://localhost:5173`.

2. **Navigating the Interface:**
   - The React front end will present a user-friendly web interface for the Reversi game. The main page should display the game board and current game status, including which player's turn it is and the current scores.

3. **Making Moves:**
   - Players make moves by clicking on the game board where they wish to place their piece, according to Reversi rules. The game will automatically update the board, flip any captured pieces, and switch turns between players.

4. **Game Progression:**
   - The web interface will continuously update to reflect the current state of the game, including available moves. Players can proceed with their turns, with the game logic ensuring all moves are valid according to the rules of Reversi.

5. **Ending the Game:**
   - The game concludes when no legal moves are available for either player. The web page will display the final scores and announce the winner: ![Endgame screenshot of Reversi showing Player 2's victory with options to 'New Game' or 'Pass.'](https://github.com/justinsoto/Reversi/blob/main/assets/reversi-endgame-player2-win.png?raw=true)



6. **Additional Features:**
   - Ability to start a new game 
   - Playing against an AI opponent
   - The ability to log in
   - The ability to pass your turn the oppononent player
   - Pick your board size
        - **Note:** In Reversi, board sizes vary from $4 \times 4$ to $12 \times 12$, with $8 \times 8$ being standard for competitive play, where $N \times N$ boards must use even numbers to ensure balanced gameplay and strategic depth (especially for the AI).




### Tips for Playing
- Explore the UI to fully understand all available features and gameplay options.
- The visual cues on the board help plan your moves effectively, so you know where you can place your tile for a legal move.

## Architecture
MVC architecture, and the role of key components:
- **Model**: Game logic, player management, AI, and database interactions.
- **View**: Console and web (React) interfaces.
- **Controller**: Handling user input and connecting the model with the view.


## Acknowledgements
Inspiration for the game's development came from several sources, to help our understanding and implementation of Reversi:

- [CardGames.io Reversi](https://cardgames.io/reversi/): This site provided insights into user interface design and gameplay flow.
  
- [Wikipedia: Reversi](https://en.wikipedia.org/wiki/Reversi): The  history and rules described on Wikipedia offered an understanding of Reversi, contributing to our game's implementation.
  
- [Reversi Strategy Video](https://youtu.be/zFrlu3E18BA?si=txmLHLvpIMgSu8lu): A helpful video on Reversi gameplay and strategy.

- Integrating Python APIs with a React front-end, using Flask: [Building a Python API and Fetching it in React: A Step-by-Step Guide](https://python.plainenglish.io/building-a-python-api-and-fetching-it-in-react-a-step-by-step-guide-5024ba4ed9dd)

## Misc.
Updated Class Diagram:
![UpdatedClassDiagram](https://github.com/justinsoto/Reversi/assets/107148168/cb21d382-a7ff-4062-8dd8-687fec32e47a)

### Explanation of some important directories:
The Reversi game implementation are organized into various directories and files. Here's a brief overview of the structure:

- **Root Files and Directories:**
  - `app.py`: The Flask application.
  - `main.py`: The main script for the CLI version of the game.
  - `scores.txt`: A file to store game scores.

- **Directories for MVC Architecture:**
  - `model`: Contains the data structure and logic of the game.
  - `view`: Holds files related to the game's user interface presentation, such as the react application.
  - `controller`: Contains logic to handle the interaction between the model and view.

- **Other Directories:**
    - `server`: Holds files for server-side logic, for online gameplay or data management (TBA)
    - `database`: Include's files for database interaction, storing game states, scores, or user accounts.
    - The `my-react-reversi` directory contains the React application. `src` directory contains the main JavaScript (JSX) files defining the components and logic for the game's UI. The `public` directory contains static assets. Vite is used as the build tool for the React application( based off the configuration and package files like `package.json` and `vite.config.js`)


### Explanation of some important files:
- **`app.py`**: This file sets up a Flask application to serve as the backend, as the game has a web interface component. It imports models and controllers, initializes a game instance, and defines routes for web requests. The presence of our routes indicate endpoints for web interaction for starting the game, fetching game state, sending messages, and more.

- **`main.py`**: This file is the console-based version of the game, initializing the game model, a console view, and a game controller before starting the game. There is some additional functionality we want to implement soon, such as database connection and user management.
### Explanation of our MVC Architecture:
### Model
- `board.py`: Handles the game board's structure and logic.
- `game.py`: Central game logic, managing game state, rules, and progression.
- `ai.py`: Artificial Intelligence for the game.
- `player.py` and `player_color.py`: Manages player information, such as player identifiers, like black and white pieces in Reversi.
- `db_management`: A directory containing files for database interactions, such as storing scores or game states.

### View
- `console_board_view.py` & `console_game_view.py`: Console-based views for the game board and overall game interface.
- `game_view.py` & `board_view.py`: Used to define interfaces and view implementations.
- `my-react-reversi`: A directory for the React-based web interface for the game, aligning with the web server functionality in `app.py`.

### Controller
- `controller.py`: The controller that handles inputs and connecting the model to the console view.
- `gui_controller.py`: A GUI-specific controller, interfacing between the model and the web-based (React) view.