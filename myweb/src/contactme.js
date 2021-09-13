import './App.css'
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faFacebook, faLinkedin, faTwitter, faInstagram, faGithub, fab, faInstagramSquare } from "@fortawesome/free-brands-svg-icons";
import { library } from '@fortawesome/fontawesome-svg-core';
library.add(faFacebook, faLinkedin, faInstagram, faTwitter, faGithub, fab)
function contactme() {
    return (
        <div className="section gridCenter" style={{"top":"4rem"}}>
            <div className="flexRow w-100">
                <div className="flexColumn h-100">
                    <div className="contactInfo">
                        <div>
                            <p>me@mohak.com</p>
                            <p>Address - <br /> CryoStation 001,<br /> 24.5795245,80.733008<br />
                                Planet AEX012 <br />
                                Andromeda Galaxy
                            </p>
                        </div>
                    </div>
                    <div className="flexRow socialMedia ">
                        {/* <a className="fab fa-facebook media animated fadeInUp" aria-hidden="true"></a>
                        <a href="https://www.twitter.com/mohakagrawal89 " className="fab fa-twitter media animated fadeInUp"
                            target="_blank" aria-hidden="true" rel="noreferrer" ></a>
                        <a href="https://www.linkedin.com/in/agr-mohak" className="fab fa-linkedin media animated fadeInUp"
                            target="_blank" aria-hidden="true" rel="noreferrer" ></a>
                        <a href="https://www.instagram.com/mohak.agr" className="fab fa-instagram media animated fadeInUp"
                            target="_blank" aria-hidden="true" rel="noreferrer" ></a> */}
                        <div className="media"> <FontAwesomeIcon icon={faFacebook} /></div>
                        <a href="https://www.linkedin.com/in/agr-mohak"  target="_blank"rel="noreferrer"><div className="media"> <FontAwesomeIcon icon={faLinkedin} /></div></a>
                        <a href="https://www.instagram.com/mohak.agr" target="_blank"rel="noreferrer"><div className="media"> <FontAwesomeIcon icon={faInstagramSquare} /></div></a>
                        <a href="https://www.twitter.com/mohakagrawal89 " target="_blank"rel="noreferrer"><div className="media"> <FontAwesomeIcon icon={faTwitter} /></div></a>
                        <a href="https://www.github.com/Mohak89" target="_blank"rel="noreferrer"><div className="media"> <FontAwesomeIcon icon={faGithub} /></div></a>
                    </div>
                </div>
                <div className="form h-100">
                    <p>Drop me a message</p>
                    <div className="name">
                        <input type="text" placeholder="First Name" autoComplete="false" />
                        <input type="text" placeholder="Last Name" autoComplete="false"/>
                    </div>
                    <input type="text" placeholder="Mobile" />
                    <input type="email" placeholder="name@company.com" />
                    <textarea name="" id="" cols="30" rows="5" placeholder="Message"></textarea>
                    <button id="send" className="w-25 gridCenter">Send</button>
                </div>
            </div>
        </div>
    )
}
export default contactme;