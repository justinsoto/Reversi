import { useNavigate } from "react-router-dom";
import { baseURL } from "./ReversiApp";

export default function UserRow(props) {
    const username = props.username
    const navigate = useNavigate()

    function playAgainstUser(username) {
        baseURL.get(`/play-user/${username}`)
        navigate('/game')
    }

    return (
        <div className="user-row">
            <h2>{username}</h2>
            <button onClick={() => playAgainstUser(username)}>Play</button>
        </div>
    );

}