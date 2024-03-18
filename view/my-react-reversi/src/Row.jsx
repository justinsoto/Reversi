import Cell from "./Cell"

function Row(props) {
    const cells = []
    const index = props.index
    const rowLength = props.length
    // const rowState = props.state

    for (let i = 0; i < rowLength; i++) {
        cells.push(<Cell key={i} row={index} index={i} />)
    }

    return (
        <div className="row">
            {cells}
        </div>
    );
}

export default Row