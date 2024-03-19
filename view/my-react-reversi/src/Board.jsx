import Row from "./Row";
import { useEffect, useState } from "react";
import axios from "axios";
import { baseURL } from "./ReversiApp";

function Board(props) {
    const rows = []
    const size = props.size
    const [board, setBoard] = useState([[] * size])

    const updateBoard = () => {
        axios.get(baseURL + '/board')
            .then(response => setBoard(response.data['board']))
    }

    updateBoard()
    for (let row = 0; row < size; row++) {
        rows.push(<Row key={row} index={row} length={size} 
                        state={board[row] ? board[row] : "Empty"}/>);
    }

    return (
        <div className="board">
            {rows}
        </div>
    );
}

export default Board