import React from 'react';
import { Link } from 'react-router-dom';
import { connect } from 'react-redux';
import * as actionTypes from '../store/actions';

import Menu from '@material-ui/core/Menu';
import MenuItem from '@material-ui/core/MenuItem';
import Button from '@material-ui/core/Button';
import AccountCircleIcon from '@material-ui/icons/AccountCircle';

 const ProfileMenu = (props) => {
  const [anchorEl, setAnchorEl] = React.useState(null);

  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const logInFunc = (screenName) => {
    setAnchorEl(null);
    props.screenName(screenName);
  };

  const logOutFunc = () => {
    setAnchorEl(null);

    if (props.curUsrName !== 'Guest'){
        console.log('Log out Function!');
        props.screenName('Log In');
        props.onLogin('Guest', '');
    };
  };

  // Return to the menu button the correct MenuItem:
  // Guest = Navigate to Log In screen
  // Other = logged user will have the Log out button that will use the Log out function
  const logButton = () => {
      if (props.curUsrName === 'Guest'){
          return (
            <MenuItem component={Link}
            to={'/login'} 
            onClick={() => logInFunc("Log In")}>Log In</MenuItem>
          );
      }
      else return (<MenuItem 
                    component={Link}
                    to={'/login'} 
                    onClick={logOutFunc}>Log Out</MenuItem>);
  };

  return (
    <div>
        {/* The style values are for the size of background ripple effect of the Button element */}
      <Button style={{maxWidth: '30px', maxHeight: '30px', minWidth: '30px', minHeight: '30px'}}
      aria-controls="simple-menu" aria-haspopup="true" onClick={handleClick} size="small">
        <AccountCircleIcon style={{ fontSize: 32 }}/>
      </Button>
      <Menu
        id="simple-menu"
        anchorEl={anchorEl}
        keepMounted
        open={Boolean(anchorEl)}
        onClose={handleClose}
      >
          {logButton()}
      </Menu>
    </div>
  );
}

// Define function action to update store
const mapDispathToProps = (dispatch) => {
  return {
      onLogin: (usrName, usrPass) =>
      dispatch({
          type: actionTypes.USER_LOGIN,
          userName: usrName,
          password: usrPass
      })
  };
};

export default connect(null, mapDispathToProps)(ProfileMenu);