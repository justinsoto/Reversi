import { useEffect, useState } from "react";
import { baseURL } from "../ReversiApp";
import UserRow from "../UserRow";

export default function UserTable() {
    const [userList, setUserList] = useState([])

    useEffect(() => {
        baseURL.get('/users')
            .then(res => {
                setUserList(res.data.users)
            })
    }, [])

    function playAI() {
        
    }

    return (
        <>
            <div className="user-top-row">
                <button>Play AI</button>
            </div>

            <UserRow username={'user1'} />
            {userList && userList.map((user, idx) => <UserRow key={idx} username={user} />)}
        </>
    );
}

