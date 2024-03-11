import Cell from "./Cell"

function Row(props) {
    const cells = []
    const index = props.index
    const rowLength = props.size

    for (let i = 0; i < rowLength; i++) {
        cells.push(<Cell key={i} index={i}/>)
    }

    return (
        <div className="row">
            {cells}
        </div>
    );
}

export default Row