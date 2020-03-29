import React, {useEffect, useState} from "react";
import ghPinnedRepos from 'gh-pinned-repos';

import {ReactComponent as Heart} from "../img/heart.svg";
import {ReactComponent as X} from "../img/x.svg";

import {
    Row,
    Col,
    Container,
    ListGroup, 
    ListGroupItem 
  } from "reactstrap";

  import ProfCard from "./profile_card";

function Sidebar(props) {

    const [matches, setMatches] = useState([])

    useEffect(() => {
        async function fetchData() {
            var matches = await (await fetch('/matches')).json();
            setMatches(matches);
            console.log("fetched data");
        }

        fetchData();
        setInterval(fetchData, 30000);
    }, []);

    return (
        <div className="text-center">
            <h4 className="my-4">Matches</h4>

            {matches.length == 0 && <h6>None yet :)</h6>}
            {matches.length > 0 &&
                <ListGroup>
                    {
                        matches.map((match, index) =>
                            <ListGroupItem><a href={`https://github.com/${match.github_login}`}>{match.name}</a> - {match.other_disc}</ListGroupItem>
                        )
                    }
                </ListGroup>
            
            }
        </div>
    )

}

export default Sidebar;