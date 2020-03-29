import React, {useState, useEffect} from 'react';
import logo from './logo.svg';
import './App.css';

import {
  Row,
  Col,
  Container
} from "reactstrap";
import GithubButton from 'react-github-login-button'


import Navbar from "./components/navbar";
import ProfCard from "./components/profile_card";
import MyProfile from "./components/my_profile";

function Login() {
  return(
    <div className="text-center centercontainer">
      <div className="center text-center">
        <h1>Please log in with Github to continue</h1>
        <a href="http://localhost:5000/login">
          <GithubButton style={{marginLeft: "25px"}}/>
        </a>
      </div>
    </div>
  )
}

function App() {

  const [isLoggedIn, setLoggedIn] = useState(false);
  const [username, setUsername] = useState("")
  const [user, setUser] = useState({});

  useEffect(() => {
    async function fetchData() {
      var resp = await fetch('/currentuser');
      var user = await resp.json();
      console.log(user)
      setLoggedIn(user["loggedIn"]);
      if(user["name"]){
        setUsername(user["name"])
      }
      console.log("HELLO!")
      console.log(user["name"])
      setUser(user);
    }

    fetchData();
  }, []);

  return (
    <div className="App">
      <Navbar loggedIn={isLoggedIn} username={username}/>
      <Container fluid={true} className="container" style={{maxWidth: "100vw", flex: 1}}>
        <Row className="height-full">
          <Col xs="3" className="sidebar">Hello</Col>
          <Col xs="auto" style={{flex: 1}} className="centercontainer">

              <div className="center maincard" style={{height: "70%", width: "80%", marginBottom: "3vh"}}>

                {!isLoggedIn && <Login />}
                {isLoggedIn && user.onboarded && <ProfCard githubId={"23515048"} />}
                {isLoggedIn && !user.onboarded && <MyProfile githubId={"23515048"} /> }

              </div>

          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default App;
