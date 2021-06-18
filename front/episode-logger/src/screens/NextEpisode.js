import React from 'react';
import { connect } from 'react-redux';
import * as actionTypes from '../store/actions';


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
  
    if(props.userName !== 'Guest' && JSON.stringify(props.userData) === '{}'){
      getUserDataCall();
    }

    return (
        <div>
        { props.userName !== 'Guest' ? <h1>Next Episode screen </h1> : <PleaseLogInButton setScreenName={props.setScreenName}/>}
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