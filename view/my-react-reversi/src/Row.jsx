import Cell from "./Cell"

function Row(props) {
    const rowState = props.state
    const rowIndex = props.index

    return (
        <div className="row">
            {rowState.map((cell, idx) => <Cell key={idx} row={rowIndex} col={idx} state={rowState[idx]} />)}
        </div>
    );
}

export default Row