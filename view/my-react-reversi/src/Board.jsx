import Row from "./Row";
import { useState } from "react";
import axios from "axios";
import { baseURL } from "./ReversiApp";

function Board(props) {
    const rows = []
    const size = props.size
    const [board, setBoard] = useState([[]*size])


    for (let row = 0; row < size; row++) {
        rows.push(<Row key={row} index={row} size={size} />);
    }

    return (
        <div className="board">
            {rows}
        </div>
    );
}

export default Board