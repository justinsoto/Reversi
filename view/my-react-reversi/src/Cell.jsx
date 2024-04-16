import axios from "axios";
import { baseURL } from "./ReversiApp";

function Cell(props) {
    const cellState = props.state
    const rowIndex = props.row
    const colIndex = props.col
    let disc = renderDisc()

    function renderDisc() {
        if (cellState === 'Player 1') {
            return <div className="black-disc" />
        }
        else if (cellState === 'Player 2') {
            return <div className="white-disc" />
        }
        else if (cellState === "Legal") {
            return <div className="legal-space" onClick={executeMove} />;
        }
        else {
            return null
        }
    }

    async function executeMove() {
        // Calls the Flask server to execute a move in the game model
        let response = await baseURL.get(`/execute-move/${rowIndex}/${colIndex}`)
        console.log(response.data)

        // Calls the Flask server to trigger the AI to make a move in the game model
        response = await baseURL.get('/trigger-ai')
        console.log(response.data)
    }

    return (
        <div className="cell">
            {disc}
        </div>
    );
}

export default Cell