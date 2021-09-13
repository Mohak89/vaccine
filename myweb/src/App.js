import './App.css';
import './nav.css';
import '@fortawesome/fontawesome-svg-core'
import React from "react";
import contact from './contactme'
import {
  BrowserRouter as Router,
  Switch,
  Route,
  Link
} from "react-router-dom";

function App() {
  return (
    <Router>
      <div id="navBar">
        <div className="logo">Mohak</div>
        <div className="mainMenu">
          <Link to="/">  <div className="menuItem hover-underline-animation">Home</div></Link>
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
      <Switch>
        <Route path="/aboutme">
          <Aboutme />
        </Route>
        <Route path="/mywork">
          <Mywork />
          <Route path="/blog">
            <blog />
          </Route>
        </Route>
        <Route path="/contactme">
          <Contactme />
        </Route>
        <Route path="/">
          <Home />
        </Route>
      </Switch>
    </Router>

  );
}
function Home() {
  return <h2>Home</h2>;
}

function Aboutme() {
  return <h2>About</h2>;
}

function Mywork() {
  return <h2>mywork</h2>;
}
function Contactme() {
  return contact();
}


export default App;
