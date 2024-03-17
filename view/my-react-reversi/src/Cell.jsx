import { useState } from "react";
import Disc from "./Disc";
import axios from "axios";
import { baseURL } from "./ReversiApp";

function Cell(props) {

    const [cellState, setCellState] = useState(null);
    // const cellState = props.state
    const rowIndex = props.row
    const colIndex = props.index
    let disc = renderDisc()
    changeCellState()
    
    function changeCellState() {
        axios.get(baseURL + '/cell-state/'+ rowIndex + '/' + colIndex)
            .then(response => setCellState(response.data))
    }

    function renderDisc() {
        if (cellState === 'Player 1') {
            return <div className="black-disc" />
        }
        else if (cellState === 'Player 2') {
            return <div className="white-disc" />
        }
        else if (cellState === "Legal") {
            return <div className="legal-space" onClick={executeMove}/>;
        }
        else {
            return null
        }
    }

    function executeMove() {
        axios.get(baseURL + '/execute-move/'+ rowIndex + '/' + colIndex)
    }

    return (
        <div className="cell">
            {disc}
        </div>
    );
}

export default Cell