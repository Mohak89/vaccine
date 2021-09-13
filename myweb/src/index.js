import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';

ReactDOM.render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
  document.getElementById('root')
);
var toggle_button = document.getElementById("toggleButton")

function toggle() {
  var classes = document.getElementsByClassName("mainMenu")[0].classList
  if (classes.contains("active")) {
    classes.remove("active")
    toggle_button.classList.remove("cross")
  } else {
    toggle_button.classList.add("cross")
    classes.add("active")
  }
}
toggle_button.addEventListener("click",toggle)

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
