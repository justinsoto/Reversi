import Board from "./Board";
import { useState } from "react";
import axios from "axios";


function Game(props) {

    const size = props.size;
    const [player1Score, setPlayer1Score] = useState(0);
    const [player2Score, setPlayer2Score] = useState(0);

    const baseURL = 'http://127.0.0.1:5000';
    getPlayerScores();

    function getPlayerScores() {
        console.log();
        axios.get(baseURL + '/scores')
            .then(response => {
                setPlayer1Score(response.data['player1']);
                setPlayer2Score(response.data['player2']);
            })
    }

    return (
        <div className="game">
            <div className="score-container">
                <div className="score-label">Player 2</div>
                <div className="player2-score">{player2Score}</div>
            </div>

            <Board size={size} />

            <div className="score-container">
                <div className="player1-score">{player1Score}</div>
                <div className="score-label">Player 1</div>
            </div>

            <button className="pass-button">Pass</button>
        </div>
    );
}

export default Game