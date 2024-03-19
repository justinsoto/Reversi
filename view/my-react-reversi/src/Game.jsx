import Board from "./Board";
import { useEffect, useState } from "react";
import axios from "axios";
import { baseURL } from "./ReversiApp";

function Game(props) {
    const size = props.size;
    const [player1Score, setPlayer1Score] = useState(0)
    const [player2Score, setPlayer2Score] = useState(0)
    const [currentPlayer, setCurrentPlayer] = useState(null)
    const [message, setMessage] = useState("")
    const [aiEnabled, setAIEnabled] = useState(null)

    const refresh = () => {
        updatePlayerScores()
        updateCurrentPlayer()
        updateMessage()
        updateAIStatus()
    }

    refresh()

    function updateCurrentPlayer() {
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

    function updateMessage() {
        axios.get(baseURL + '/message')
            .then(response => setMessage(response.data))
    }

    function updateAIStatus() {
        axios.get(baseURL + '/AI-status')
            .then(response => setAIEnabled(response.data['AI']))
    }

    function passTurn() {
        axios.get(baseURL + '/pass-turn')
        refresh()
    }

    function resetGame() {
        axios.get(baseURL + '/reset')
        refresh()
    }

    function toggleAI() {
        axios.get(baseURL + '/toggle-AI')
        resetGame()
    }

    return (
        <div className="game" onClick={refresh}>
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

