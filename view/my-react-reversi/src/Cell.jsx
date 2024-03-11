import { useState } from "react";
import Disc from "./Disc";

function Cell() {

    const [cellState, setCellState] = useState(false);

    function changeCellState() {
        setCellState(!cellState);
        console.log(cellState);
    }

    return (
        <div className="cell" onClick={changeCellState}>
            {cellState ? <Disc className="disc" /> : null}
        </div>
    );
}

export default Cell