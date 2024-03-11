import Board from "./Board";

function Game(props) {

    const size = props.size;

    return (
        <div className="game">
            <div className="score-container">
                <div className="score-label">Player 2</div>
                <div className="player2-score">0</div>
            </div>

            <Board size={size} />

            <div className="score-container">
                <div className="player1-score">0</div>
                <div className="score-label">Player 1</div>
            </div>

            <button className="pass-button">Pass</button>
        </div>
    );
}

export default Game