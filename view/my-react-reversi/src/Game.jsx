import Board from "./Board";
import { useEffect, useState } from "react";
import axios from "axios";
import { baseURL } from "./ReversiApp";

function Game(props) {
    const size = props.size;
    const [gameState, setGameState] = useState(null)

    useEffect(() => updateGameState(), [gameState])

    function updateGameState() {
        baseURL.get('/game-state')
            .then(response => {
                setGameState({
                    ...gameState,
                    scores: response.data.scores,
                    message: response.data.message,
                    aiStatus: response.data.aiStatus
                })
            })
    }

    function passTurn() {
        baseURL.get('pass-turn')
    }

    function resetGame() {
        baseURL.get('/reset')
    }

    function toggleAI() {
        baseURL.get('/toggle-ai')
    }

    if (!gameState) { return <p>Loading...</p> }

    return (
        <div className="game" onClick={updateGameState}>
            <button
                className="new-game-button"
                onClick={resetGame}>
                New Game
            </button>

            <div className="score-container">
                <div className="score-label">Player 2</div>
                <div className="player2-score">{gameState.scores.player2}</div>
            </div>

            <Board size={size} />

            <div className="message">{gameState.message}</div>

            <div className="score-container">
                <div className="player1-score">{gameState.scores.player1}</div>
                <div className="score-label">Player 1</div>
            </div>

            <button
                className="pass-button"
                onClick={passTurn}>
                Pass
            </button>

            <button
                className="multiplayer-button"
                onClick={toggleAI}>
                {gameState.aiStatus ? "Multiplayer" : "Play AI"}
            </button>
        </div>
    );
}

export default Game

