import React, { useState } from 'react';
import { Redirect } from 'react-router-dom'
import { makeStyles } from '@material-ui/core/styles';
import Button from '@material-ui/core/Button';

const useStyles = makeStyles((theme) => ({
  root: {
    '& > *': {
      margin: theme.spacing(1),
    },
  },
}));

export default function PleaseLogInButton(props) {
    const classes = useStyles();

    const [redirect, setRedirect] = useState(false);

    const forwardToLogin = () => {
        props.setScreenName("Log In");
        setRedirect(true);
    };


    return (
        <div className={classes.root}>
            { redirect ? <Redirect to="/login"/> : null}
            <Button variant="contained"
            onClick={forwardToLogin}>Please Log In</Button>
        </div>
    );
}
