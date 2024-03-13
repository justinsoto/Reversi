import Title from "./Title";
import Game from "./Game";
import React, { useState } from "react";
import axios from "axios";

export default function ReversiApp() {

    document.title = "Reversi";

    const [size, setSize] = useState(8);

    const baseURL = 'http://127.0.0.1:5000';
    fetchAPI();

    function fetchAPI() {
        axios.get(baseURL + '/game-size')
            .then(response => setSize(s => s = response.data))
    }

    return (
        <>
            <Title />
            <Game size={size} />
        </>
    );
}
