import React from 'react';
import { connect } from 'react-redux';
import * as actionTypes from '../store/actions';

import NextEpisodeCard from '../components/nextEpisodeCard/NextEpisodeCard';
import PleaseLogInButton from '../components/pleaseLogIn/PleaseLogIn';



const NextEpisode = (props) => {

  const getUserDataCall = () => {
    const userName = { username: props.userName }
    let body = {
          method: "POST",
          headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(userName)
    }
  
    fetch("/getUserData", body).then(
        (response) => response.json()
        .then(data => {
          console.log(data);
          props.loadUserData(data);
        })
    );
  };


  // Send request for the logged user to get Series data from the mongo DB
  if(props.userName !== 'Guest' && JSON.stringify(props.userData) === '{}'){
    getUserDataCall();
  }

  

  const nextEpisodeScreenVis = (
    <div>
      <h1>Next Episode screen </h1> 
      <div style={{display: 'flex'}}>
      {Object.keys(props.userData).map((series, i) => {
      console.log(props.userData[series])
      if(props.userData[series].visible === true)
      return <NextEpisodeCard seriesData={props.userData[series]} key={i}/>
    })}
      </div>
    </div>
  );

    return (
        <div>
        { props.userName !== 'Guest' ? nextEpisodeScreenVis : <PleaseLogInButton setScreenName={props.setScreenName}/>}
        </div>
    )
};

// Redux configuration
const mapStateToProps = (state) => {
    return {
      userName: state.userName,
      password: state.password,
      userData: state.userData
    };
  };

// Define function action to update store
const mapDispathToProps = (dispatch) => {
  return {
      loadUserData: (dataFetched) =>
      dispatch({
          type: actionTypes.LOAD_DATA,
          userData: dataFetched
      })
  };
};

export default connect(mapStateToProps, mapDispathToProps)(NextEpisode);