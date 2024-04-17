import Title from "./Title";
import Game from "./pages/Game";
import React, { useEffect, useState } from "react";
import axios from "axios";
import { createBrowserRouter, RouterProvider } from "react-router-dom";
import Login from "./pages/Login";
import UserTable from "./pages/UserTable";

export default function ReversiApp() {

    const size = () => {
        baseURL.get('/board-size')
            .then(res => { return res.data.size })
    }

    const router = createBrowserRouter([
        {path: '/', element: <Login />},
        {path: '/users', element: <UserTable />},
        {path: '/game', element: <Game size={size} />}
    ])

    return (
        <>
            <RouterProvider router={router} />
        </>
    );
}

export const baseURL = axios.create({
    baseURL: 'http://127.0.0.1:5000',
    timeout: 1000,
    headers: { 'X-Custom-Header': 'foobar' }
});
