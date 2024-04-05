import Row from "./Row";
import { useEffect, useState } from "react";
import { baseURL } from "./ReversiApp";

function Board(props) {
    const rows = []
    const size = props.size
    // const [board, setBoard] = useState(null)
    const board = props.state

    // useEffect(() => {
    //     baseURL.get('/board')
    //         .then(response => setBoard(response.data.board))
    // }, [board])

    if (!board) { return <p>Loading...</p>}

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