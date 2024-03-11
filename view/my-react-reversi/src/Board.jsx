import Row from "./Row";

function Board(props) {

    const rows = []
    const size = props.size

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