import Title from "./Title";
import Game from "./Game";

function ReversiApp() {

    document.title = "Reversi";

    return (
        <>
            <Title />
            <Game size={8}/>
        </>

    );
}

export default ReversiApp