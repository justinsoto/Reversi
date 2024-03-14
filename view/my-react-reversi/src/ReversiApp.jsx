import Title from "./Title";
import Game from "./Game";
import React, { useState } from "react";
import axios from "axios";

function ReversiApp() {
    const [size, setSize] = useState(8);
    getBoardSize();

    function getBoardSize() {
        axios.get(baseURL + '/board-size')
            .then(response => {
                setSize(response.data['size']);
            })
    }

    return (
        <>
            <Title />
            <Game size={size} />
        </>
    );
}

export default ReversiApp
export const baseURL = 'http://127.0.0.1:5000'
