import { useEffect, useState } from "react";
import { baseURL } from "../ReversiApp";
import UserRow from "../UserRow";
import { useNavigate } from "react-router-dom";

export default function UserTable() {
    const [userList, setUserList] = useState([])
    const navigate = useNavigate()

    useEffect(() => {
        baseURL.get('/users')
            .then(res => {
                setUserList(res.data.users)
            })
    }, [])

    function playAgainstAI() {
        baseURL.get('/play-ai')
        navigate('/game')
    }

    return (
        <>
            <div className="user-top-row">
                <button onClick={playAgainstAI}>Play AI</button>
            </div>

            {userList && userList.map((user, idx) => <UserRow key={idx} username={user} />)}
        </>
    );
}

