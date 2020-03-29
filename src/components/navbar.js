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
            <NavbarBrand className="mr-3">Github Dating</NavbarBrand>
            {!props.loggedIn 
              ? <a href=""><NavbarText className="mr-2">Login</NavbarText></a>
              : <NavbarText className="mr-2">Howdy, {props.username}!</NavbarText>
            }
        </Nav>
    </Navbar>
  );
}

export default MyNavbar;