import React, { useState } from 'react';
import { connect } from 'react-redux';
import * as actionTypes from '../store/actions';

import NextEpisodeCard from '../components/nextEpisodeCard/NextEpisodeCard';
import PleaseLogInButton from '../components/pleaseLogIn/PleaseLogIn';



const NextEpisode = (props) => {
  const [refresh, setRefresh] = useState(false);  // Responsible to refresh the data after episode marked as watched

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
          props.loadUserData(data);
        })
    );
  };

  // Seperate function only when refresh one.
  // Didnt merge with the function below to prevent ifinite state loop.
  if(refresh === true){
    getUserDataCall();
    setRefresh(false);
  }


  // Send request for the logged user to get Series data from the mongo DB
  // Actiavtes only when the user isn't Guest and no data present for the user.
  if(props.userName !== 'Guest' && JSON.stringify(props.userData) === '{}'){
    getUserDataCall();
  }

  const nextEpisodeScreenVis = (
    <div>
      <h1>Next Episode screen </h1> 
      <div style={{display: 'flex', flexFlow: 'wrap', justifyContent: 'center'}}>
      {Object.keys(props.userData).map((series, i) => {
      if(props.userData[series].visible === true)return <NextEpisodeCard seriesData={props.userData[series]} userName={props.userName} refresh={setRefresh} key={i}/>
      else return null
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