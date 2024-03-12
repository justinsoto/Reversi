import Title from "./Title";
import Game from "./Game";
import React, { Component } from "react";
import axios from "axios";

export default function ReversiApp() {

    document.title = "Reversi";
    fetchAPI();

    function fetchAPI() {
        axios.get('http://127.0.0.1:5000/hello')
            .then(response => console.log(response.data))
    }

    return (
        <>
            <Title />
            <Game size={8} />
        </>
    );
}
