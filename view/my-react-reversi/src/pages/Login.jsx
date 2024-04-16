import { Link, useNavigate } from "react-router-dom"
import { baseURL } from "../ReversiApp"
import { useState } from "react"

export default function Login() {

    const [username, setUsername] = useState("")
    const [password, setPassword] = useState("")
    const navigate = useNavigate()

    function login() {
        baseURL.get(`/login/${username}/${password}`)
        .then(res => {
            console.log(username)
            console.log(res.data)
            navigate('/game')
        })
    }

    function register() {
        baseURL.get(`/register/${username}/${password}`)
        .then(res => {
            console.log(username)
            console.log(res.data)
        })
        navigate('/game')
    }

    return (
        <div className="login-container">
            <div className="user-form">
                <label>Username:</label>
                <input type="text" onChange={(e) => {setUsername(e.target.value)}}/><br />
                <label>Password:</label>
                <input type="text" onChange={(e) => {setPassword(e.target.value)}}/><br />
            </div>

            <Link onClick={login}>
                <button>Login</button>
            </Link>
            <Link onClick={register}>
                <button>Register</button>
            </Link>
        </div>
    )
}

//main change needed here is to have the page return the username and password that are entered in the inputs whenever a button is clicked