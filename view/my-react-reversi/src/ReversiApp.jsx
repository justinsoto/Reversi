import Title from "./Title";
import Game from "./Game";
import React, { useState } from "react";
import axios from "axios";

export default function ReversiApp() {
    const baseURL = 'http://127.0.0.1:5000';

    document.title = "Reversi";

    const size1 = () => {
        axios.get(baseURL + '/board-size')
            .then(response => size1 = response.data['size']);
    }
    const [size, setSize] = useState(8);


    fetchAPI();

    function fetchAPI() {
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
