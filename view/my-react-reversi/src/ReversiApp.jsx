import Title from "./Title";
import Game from "./Game";
import React, { useEffect, useState } from "react";
import axios from "axios";

function ReversiApp() {
    const [size, setSize] = useState(8);

    useEffect(() => {
        baseURL.get('/board-size').then(response => setSize(response.data['size']))
    }, [])

    return (
        <>
            <Title />
            <Game size={size} />
        </>
    );
}

export default ReversiApp
export const baseURL = axios.create({
    baseURL: 'http://127.0.0.1:5000',
    timeout: 1000,
    headers: { 'X-Custom-Header': 'foobar' }
});
