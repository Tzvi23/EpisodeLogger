import React, { useState } from 'react';
import { connect } from 'react-redux';
import { Redirect } from 'react-router-dom';

import * as actionTypes from '../../store/actions';
import classes from "./Login.module.css";

import FormControl from '@material-ui/core/FormControl';
import InputLabel from '@material-ui/core/InputLabel';
import Input from '@material-ui/core/Input';
import InputAdornment from '@material-ui/core/InputAdornment';
import AccountCircle from '@material-ui/icons/AccountCircle';
import IconButton from '@material-ui/core/IconButton';
import Visibility from '@material-ui/icons/Visibility';
import VisibilityOff from '@material-ui/icons/VisibilityOff';
import Button from '@material-ui/core/Button';


const Login = (props) => {
    const [values, setValues] = useState({
        userName: '',
        password: '',
        showPassword: false,
      });
    const [redirect, setRedirect] = useState(false);
    const [notAuth, setNotAuth] = useState(false);

    //Password input functions
    const handleChange = (prop) => (event) => {
        setValues({ ...values, [prop]: event.target.value });
    };

    const handleClickShowPassword = () => {
        setValues({ ...values, showPassword: !values.showPassword });
      };
    
    const handleMouseDownPassword = (event) => {
        event.preventDefault();
    };

    // Log In request with username and password data
    const logIn = () => {
        const cred = { ...values };
        delete cred.showPassword;

        let bodyData = {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(cred)
        }

        fetch('/login', bodyData)
        .then(response => {
            if (response.ok){
                props.onLogin(cred.userName, '');
                setNotAuth(false);
                setRedirect(true);
            }
            else {
                setNotAuth(true);
            }
        });
    };

    const badUser = (
        <div className={classes.errorCard}>
                Bad User name or password
        </div>
    );

    // const testServer = () => {
    //     fetch("/getDataTest").then(
    //         (response) => response.json().then(data => console.log(data))
    //     );
    // };

    return (
        <div>
        {redirect ? <Redirect to="/nextEpisode"/> : null }
            <div className={classes.card}>
                {/* User Name Input */}
                <FormControl >
                    <InputLabel htmlFor="input-userName">User Name</InputLabel>
                    <Input
                    id="input-userName"
                    onChange={handleChange('userName')}
                    startAdornment={
                        <InputAdornment position="start">
                            <AccountCircle />
                        </InputAdornment>
                    }
                    />
                </FormControl>
            {/* Password Input */}
                <FormControl >
                    <InputLabel htmlFor="standard-adornment-password">Password</InputLabel>
                    <Input
                        id="standard-adornment-password"
                        type={values.showPassword ? 'text' : 'password'}
                        value={values.password}
                        onChange={handleChange('password')}
                        endAdornment={
                        <InputAdornment position="end">
                            <IconButton
                            aria-label="toggle password visibility"
                            onClick={handleClickShowPassword}
                            onMouseDown={handleMouseDownPassword}
                            >
                            {values.showPassword ? <Visibility /> : <VisibilityOff />}
                            </IconButton>
                        </InputAdornment>
                        }
                    />
                </FormControl>
                {/* Login Button */}
                <Button variant="contained" onClick={logIn}>Log In</Button>
            </div>
            {notAuth ? badUser : null}
        </div>
    );
};


// Redux definition
// Add store state to props
const mapStateToProps = (state) => {
    return {
        userName: state.userName,
        password: state.password
    };
};

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

export default connect(mapStateToProps, mapDispathToProps)(Login);