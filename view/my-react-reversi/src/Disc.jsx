function Disc(props) {

    const visible = props.visible;

    return(
        <div className="disc" visibility={visible ? "visible" : "hidden"}></div>
    );
}

export default Disc