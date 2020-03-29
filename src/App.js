import React from 'react';
import logo from './logo.svg';
import './App.css';

import {
  Row,
  Col,
  Container
} from "reactstrap";

import Navbar from "./components/navbar"

function App() {
  return (
    <div className="App">
      <Navbar />
      <Container fluid={true} className="container" style={{maxWidth: "100vw", flex: 1}}>
        <Row className="height-full">
          <Col xs="3" className="sidebar">Hello</Col>
          <Col xs="auto" style={{flex: 1}}>

              This zone is for the cards and stuff.

          </Col>
        </Row>
      </Container>
    </div>
  );
}

export default App;
