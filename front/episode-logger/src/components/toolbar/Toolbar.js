import React from "react";
import { connect } from 'react-redux';

import SideDrawer from "../sideDrawer/SideDrawer.js";
import classes from "./toolbar.module.css";


import ProfileMenu from '../proflieMenuButton';

const toolbar = (props) => {

  return (
    <div className={classes.header_toolbar}>
        <SideDrawer />
      <div className={classes.current_title}>
        Props title
      </div>
        <div className={classes.current_user}>
          <div>{props.userName}</div>
          <ProfileMenu curUsrName={props.userName}/>
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

export default connect(mapStateToProps)(toolbar);