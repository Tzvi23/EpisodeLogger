import React, { useState } from "react";
import { connect } from 'react-redux';

import SideDrawer from "../sideDrawer/SideDrawer.js";
import classes from "./toolbar.module.css";


import ProfileMenu from '../proflieMenuButton';

const Toolbar = (props) => {
  const [screenName, setScreenName] = useState('Log In');


  return (
    <div className={classes.header_toolbar}>
        <SideDrawer screenName={setScreenName}/>
      <div className={classes.current_title}>
        {screenName}
      </div>
        <div className={classes.current_user}>
          <div>{props.userName}</div>
          <ProfileMenu curUsrName={props.userName} screenName={setScreenName}/>
        </div>
    </div>
  );
};

// Redux configuration
const mapStateToProps = (state) => {
  return {
    userName: state.userName,
    password: state.password
  };
};

export default connect(mapStateToProps)(Toolbar);