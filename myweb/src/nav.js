// import logo from './logo.svg';
import './nav.css'
import {
    Link
} from "react-router-dom";
function nav() {
    return (
        <div id="navBar">
            <div className="logo">Mohak</div>
            <div className="mainMenu">
                <Link to="/"> <div className="menuItem hover-underline-animation">Home</div></Link>
                <Link to="/aboutme"> <div className="menuItem hover-underline-animation">About Me</div></Link>
                <Link to="/mywork"> <div className="menuItem hover-underline-animation">My Work</div></Link>
                <Link to="/blog"> <div className="menuItem hover-underline-animation">Blog</div></Link>
                <Link to="/contactme"> <div className="menuItem hover-underline-animation">Contact Me</div></Link>
            </div>
            <div className="hamburger" id="toggleButton">
                <span className="bar"></span>
                <span className="bar"></span>
                <span className="bar"></span>
            </div>
        </div>
    );
}

export default nav;

