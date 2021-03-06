import React from 'react';
import { connect } from 'react-redux';
import PleaseLogInButton from '../components/pleaseLogIn/PleaseLogIn';

const RemoveSeries = (props) => {

    return (
        <div>
        { props.userName !== 'Guest' ? <h1>Remove Screen </h1> : <PleaseLogInButton setScreenName={props.setScreenName}/>}
        </div>
    )
};

// Redux configuration
const mapStateToProps = (state) => {
    return {
      userName: state.userName,
      password: state.password
    };
  };

export default connect(mapStateToProps)(RemoveSeries);