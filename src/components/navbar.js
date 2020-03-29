import React, { useState } from 'react';
import {
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  NavbarText
} from 'reactstrap';

import styled from 'styled-components';

import WordMark from '../img/wordmark.png'

const Navtext = styled.span`
    margin-right: 32px;
    text-align: left;
    letter-spacing: 0;
    color: #FFFFFF;
    opacity: 1;
`;

const MyNavbar = (props) => {

  return (
    <Navbar dark style={{display: "block"}}>
        <Nav className="justify-content-between py-2">
            <NavbarBrand className="mr-3"><img src={WordMark} style={{height:"44px"}}/></NavbarBrand>
            {!props.loggedIn 
              ? <a href="http://localhost:5000/login"><NavbarText className="mr-2">Login</NavbarText></a>
              : <NavbarText className="mr-2">Howdy, {props.username}!</NavbarText>
            }
        </Nav>
    </Navbar>
  );
}

export default MyNavbar;