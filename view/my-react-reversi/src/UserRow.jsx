export default function UserRow(props) {
    const username = props.username

    return (
        <div className="user-row">
            <h2>{username}</h2>
            <button>Play</button>
        </div>
    );

}