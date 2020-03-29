import React, {useEffect, useState} from "react";
import ghPinnedRepos from 'gh-pinned-repos';

import {ReactComponent as Heart} from "../img/heart.svg";
import {ReactComponent as X} from "../img/x.svg";

import {
    Row,
    Col,
    Container
  } from "reactstrap";

  import ProfCard from "./profile_card";

const SwipeView = (props) => {

    const [pairs, setPairs] = useState([]);
    const [currIndex, setIndex] = useState(0);
    const [currMatch, setCM] = useState("");

    useEffect(() => {
        async function fetchData() {
          var resp = await fetch('/getpairs');
          var pairs = await resp.json();
          console.log(pairs);
          setPairs(pairs);
          setIndex(0);
          //setCM(pairs[0]);
        }
    
        fetchData();
      }, []);

    return (
        <div>
            {/* pairs[currIndex] && pairs[currIndex].hash */}
            {pairs.length == 0 && <span>Sorry! We couldn't find any potential matches for you right now.</span>}
            {pairs.length > 0 && currIndex >= pairs.length && <span>We've run out of potential matches for you. Check back soon!</span>}
            {pairs.length > 0 && currIndex < pairs.length && <ProfCard dummy={currIndex} onYes={() => _sendSwipe(pairs[currIndex].hash, true, currIndex, setIndex)} onNo={() => _sendSwipe(pairs[currIndex].hash, false, currIndex, setIndex)} githubId={pairs[currIndex].other} />}
        </div>
    )
}

async function _sendSwipe(hash, liked, currIndex, setIndex) {
    var like = "true"
    if(!liked) {
        like = "false"
    }

    setIndex(currIndex + 1)
    
    var resp = await (await fetch(`/swipe/${hash}/${like}`)).text();
    console.log(resp);
}

export default SwipeView;