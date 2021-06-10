import React from "react";

import SideDrawer from "../sideDrawer/SideDrawer.js";
import classes from "./toolbar.module.css";

const toolbar = (props) => {

  return (
    <div className={classes.header_toolbar}>
        <SideDrawer />
      <div className={classes.current_title}>
        Props title
      </div>
      <div className={classes.logIn}>
        <div className={classes.current_user}>
          Current user: {props.username}
        </div>
      </div>
    </div>
  );
};

export default toolbar;