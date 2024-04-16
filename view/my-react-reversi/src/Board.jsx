import Row from "./Row";
import { useEffect, useState } from "react";
import { baseURL } from "./ReversiApp";

function Board(props) {
    const board = props.state

    if (!board) { return <p>Loading...</p> }

    return (
        <div className="board">
            {board.map((row, idx) => <Row key={idx} index={idx} state={board[idx]} />)}
        </div>
    );
}

export default Board