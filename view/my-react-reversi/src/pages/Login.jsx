import { Link } from "react-router-dom"

export default function Login() {

    return (
        <div className="login-container">
            <div className="user-form">
                <label>Username:</label>
                <input type="text" /><br />
                <label>Password:</label>
                <input type="text" /><br />
            </div>

            <Link to={'/game'}>
                <button>Login</button>
            </Link>
            <Link to={'/game'}>
                <button>Register</button>
            </Link>
        </div>
    )
}

//main change needed here is to have the page return the username and password that are entered in the inputs whenever a button is clicked
