//profile card component to be put in the main card
//represents SOMEONE ELSE'S profile

import React, {useEffect, useState} from "react";
import ghPinnedRepos from 'gh-pinned-repos';

import {
    Row,
    Col,
    Container
  } from "reactstrap";

const RepoBox = (props) => {
    return(
        <div className="repobox my-2 py-2 px-2">
            <a href={`https://github.com/${props.owner}/${props.repo}`} target="_blank"><div className="reponame">{props.owner}/{props.repo}</div></a>
            <div className="mt-1">{props.description}</div>
        </div>
    )
}

const ProfileCard = (props) => {

    const [profile, setProfile] = useState({});
    const [featured, setFeatured] = useState([]);

    useEffect(() => {
        async function fetchData() {
          var resp = await fetch(`https://api.github.com/user/${props.githubId}`);
          var user = await resp.json();

          setProfile({
              name: user.name,
              org: user.company,
              site: user.blog,
              location: user.location,
              avatar: user.avatar_url,
              bio: user.bio
          }) //these values will be null if they don't exist -- just make sure to handle that

          var pinned = await (await fetch(`https://gh-pinned-repos.now.sh/?username=${user.login}`)).json(); //we'll rely on this random site for now lmao
          //TODO: move to something more robust
          console.log(pinned)
          setFeatured(pinned.slice(0,3));
          
          console.log(user)

        }
    
        fetchData();
      }, []);

    return (
        <div className="my-2 mx-2">
            <Row>
                <Col xs="5" style={{wordWrap: "break-word"}}>
                    <div className="mt-5 mx-3 ml-5">
                        <img src={profile.avatar} className="profileimage"/>
                        
                        <div className="mt-2">
                            <span className="profilecardname">Matt Katz</span>
                        </div>

                        <div className="mt-2">
                            <div className="profilesmalldetails my-1">{profile.location}</div>
                            <div className="profilesmalldetails my-1">{profile.site}</div>
                            <div className="profilesmalldetails my-1">{profile.org}</div>
                        </div>

                        <div className="mt-2">
                            {profile.bio}
                        </div>
                    </div>
                </Col>
                <Col>
                    <div className="mt-5 mx-2 ml-1"> 
                        <span className="profilesmalldetails" style={{fontWeight: 700}}> Pinned </span>
                        {
                            featured.map((repo, index) =>
                                <RepoBox owner={repo.owner} repo={repo.repo} description={repo.description}/>
                            )
                        }
                    </div>
                </Col>
            </Row>
        </div>
    )

}

export default ProfileCard;