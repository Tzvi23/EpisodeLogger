import React from "react";
import { connect } from "react-redux";
import PleaseLogInButton from "../../components/pleaseLogIn/PleaseLogIn";

import TextField from "@material-ui/core/TextField";
import { makeStyles } from "@material-ui/core/styles";

import Checkbox from "@material-ui/core/Checkbox";
import FormControlLabel from "@material-ui/core/FormControlLabel";

import Button from "@material-ui/core/Button";

import cssClasses from "./AddSeries.module.css";

const useStyles = makeStyles((theme) => ({
  root: {
    "& .MuiTextField-root": {
      margin: theme.spacing(1),
    },
  },
}));

const AddSeries = (props) => {
  const classes = useStyles();
  const [state, setState] = React.useState({
    checkedB: true,
  });

  const handleChange = (event) => {
    setState({ ...state, [event.target.name]: event.target.checked });
  };

  const addSeriesScreenConten = (
    <div className={cssClasses.card}>
      <form className={classes.root} noValidate autoComplete="off">
        <div className={cssClasses.giveSpace}>
          <TextField required id="seriesName" label="Enter Series Name" />
        </div>
        <div className={cssClasses.giveSpace}>
          <TextField required id="permaLink" label="Enter Perma-link" />
        </div>
        <div className={cssClasses.giveSpace}>
          <FormControlLabel
            control={
              <Checkbox
                checked={state.checkedB}
                onChange={handleChange}
                name="checkedB"
                color="primary"
              />
            }
            label="Mark all epsiodes as watched"
          />
        </div>
        <div className={cssClasses.giveSpace}>
          <Button variant="contained">Add Series</Button>
        </div>
      </form>
      <div className={cssClasses.giveSpace}>
        <Button variant="contained">Go to EpisodeDate.com</Button>
      </div>
    </div>
  );

  return (
    <div>
      {props.userName !== "Guest" ? (
        addSeriesScreenConten
      ) : (
        <PleaseLogInButton setScreenName={props.setScreenName} />
      )}
    </div>
  );
};

// Redux configuration
const mapStateToProps = (state) => {
  return {
    userName: state.userName,
    password: state.password,
  };
};

export default connect(mapStateToProps)(AddSeries);
