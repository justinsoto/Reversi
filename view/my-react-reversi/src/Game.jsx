import Board from "./Board";
import { useState } from "react";
import axios from "axios";
import { baseURL } from "./ReversiApp";

function Game(props) {

    const size = props.size;
    const [player1Score, setPlayer1Score] = useState(0)
    const [player2Score, setPlayer2Score] = useState(0)
    const [message, setMessage] = useState("")
    const [currentPlayer, setCurrentPlayer] = useState(null)
    const [aiEnabled, setAIEnabled] = useState(null)

    updatePlayerScores()
    updateMessage()
    updateAI()


    if (aiEnabled && currentPlayer === "Player 2") {
        axios.get(baseURL + '/trigger-AI')
    }

    function getCurrentPlayer() {
        axios.get(baseURL + '/current-player')
            .then(response => setCurrentPlayer(response.data))
    }

    function updatePlayerScores() {
        axios.get(baseURL + '/scores')
            .then(response => {
                setPlayer1Score(response.data['player1']);
                setPlayer2Score(response.data['player2']);
            })
    }

    function passTurn() {
        axios.get(baseURL + '/pass-turn')
        getCurrentPlayer()
    }

    function resetGame() {
        axios.get(baseURL + '/reset')
    }

    function updateMessage() {
        axios.get(baseURL + '/message')
            .then(response => setMessage(response.data))
    }

    function toggleAI() {
        axios.get(baseURL + '/toggle-AI')
        updateAI()
        resetGame()
    }

    function updateAI() {
        axios.get(baseURL + '/AI-enabled')
            .then(response => setAIEnabled(response.data['AI']))
    }

    return (
        <div className="game" onClick={updatePlayerScores}>
            <button
                className="new-game-button"
                onClick={resetGame}>
                New Game
            </button>

            <div className="score-container">
                <div className="score-label">Player 2</div>
                <div className="player2-score">{player2Score}</div>
            </div>

            <Board size={size} />

            <div className="message">{message}</div>

            <div className="score-container">
                <div className="player1-score">{player1Score}</div>
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
                {aiEnabled ? "Multiplayer" : "Play AI"}
            </button>
        </div>
    );
}

export default Game
