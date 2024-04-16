import Board from "./Board";
import { useEffect, useState } from "react";
import { baseURL } from "./ReversiApp";
import { Link } from "react-router-dom";
import Title from "./Title";

function Game(props) {
    const size = props.size
    const [gameState, setGameState] = useState(null)

    useEffect(() => {
        async function updateGameState() {
            const response = await baseURL.get('/game-state')
            setGameState({
                ...gameState,
                currentPlayer: response.data.currentPlayer,
                scores: response.data.scores,
                message: response.data.message,
                aiStatus: response.data.aiStatus,
                board: response.data.board
            })
        }
        updateGameState()
    }, [gameState])

    async function passTurn() {
        const response = await baseURL.get('pass-turn')
        console.log(response.data)
        baseURL.get('/trigger-ai')
    }

    async function resetGame() {
        const response = await baseURL.get('/reset')
        console.log(response.data)
    }

    async function toggleAI() {
        const response = await baseURL.get('/toggle-ai')
        console.log(response.data)
    }

    async function triggerAI() {
        const response = await baseURL.get('/trigger-ai')
        console.log(response.data)
    }

    if (!size | !gameState) { return <p>Loading...</p> }

    return (
        <>
        <Title />
        <div className="game">
            <Link to={'/'}>
                <button>Home</button>
            </Link>
            
            <button
                className="new-game-button"
                onClick={resetGame}>
                New Game
            </button>

            <div className="score-container">
                <div className="score-label">Player 2</div>
                <div className="player2-score">{gameState.scores.player2}</div>
            </div>

            <Board size={size} state={gameState.board} />

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
        </>
    );
}

export default Game

