import React, { useState } from "react";
import { connect } from "react-redux";
import PleaseLogInButton from "../../components/pleaseLogIn/PleaseLogIn";

import TextField from "@material-ui/core/TextField";

import Checkbox from "@material-ui/core/Checkbox";
import FormControlLabel from "@material-ui/core/FormControlLabel";

// Back drop imports
import { makeStyles } from "@material-ui/core/styles";
import CircularProgress from "@material-ui/core/CircularProgress";
import Backdrop from "@material-ui/core/Backdrop";

import Button from "@material-ui/core/Button";

import cssClasses from "./AddSeries.module.css";

const useStyles = makeStyles((theme) => ({
  backdrop: {
    zIndex: theme.zIndex.drawer + 1,
    color: "#fff",
  },
}));

const AddSeries = (props) => {
  const classes = useStyles();
  const [checkBox, setCheckBox] = useState({
    checkedB: true,
  });
  const [seriesName, setSeriesName] = useState("");
  const [permalink, setPermalink] = useState("");
  const [failed, setFailed] = useState(false);
  const [success, setSuccess] = useState(false);
  const [loading, setLoading] = useState(false);

  // Bind Check box change
  const handleChange = (event) => {
    setCheckBox({ ...checkBox, [event.target.name]: event.target.checked });
  };

  // Bind series name field change
  const seriesNameHandleChange = (event) => {
    setSeriesName(event.target.value);
  };

  // Bind permalink field change
  const permalinkHandleChange = (event) => {
    setPermalink(event.target.value);
  };

  const addSeriesButtonFunc = () => {
    // Check form data
    const values = ["", "Please fill value", "Please fill vaild value"];
    if (values.includes(seriesName) || values.includes(permalink)) {
      if (seriesName === "") setSeriesName("Please fill value");
      if (permalink === "") setPermalink("Please fill vaild value");
      return;
    }

    setLoading(true);

    const formData = {
      userName: props.userName,
      seriesName: seriesName,
      seriesPermalink: permalink,
      watched: checkBox.checkedB,
    };

    const bodyData = {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(formData),
    };

    fetch("/addSeries", bodyData).then((response) => {
      console.log(response);
      if (response.ok) {
        setFailed(false);
        setSuccess(true);
      } else if (response.status === 406) {
        setFailed(true);
        setSuccess(false);
      }
      setLoading(false);
    });
  };

  const badRequest = (
    <div className={cssClasses.errorCard}>Failed to add series</div>
  );

  const goodRequest = (
    <div className={cssClasses.successCard}>Added series successfully</div>
  );

  const loadingBackDrop = (
    <div>
      <Backdrop className={classes.backdrop} open={loading}>
        <CircularProgress color="inherit" />
      </Backdrop>
    </div>
  );

  const addSeriesScreenConten = (
    <div>
      <div className={cssClasses.card}>
        <div className={cssClasses.giveSpace}>
          <TextField
            required
            id="seriesName"
            label="Enter Series Name"
            value={seriesName}
            onChange={seriesNameHandleChange}
          />
        </div>
        <div className={cssClasses.giveSpace}>
          <TextField
            required
            id="permaLink"
            label="Enter Perma-link"
            value={permalink}
            onChange={permalinkHandleChange}
          />
        </div>
        <div className={cssClasses.giveSpace}>
          <FormControlLabel
            control={
              <Checkbox
                checked={checkBox.checkedB}
                onChange={handleChange}
                name="checkedB"
                color="primary"
              />
            }
            label="Mark all epsiodes as watched"
          />
        </div>
        <div className={cssClasses.giveSpace}>
          <Button variant="contained" onClick={addSeriesButtonFunc}>
            Add Series
          </Button>
        </div>
        <div className={cssClasses.giveSpace}>
          <Button
            variant="contained"
            target="_blank"
            href="https://www.episodate.com/"
          >
            Go to EpisodeDate.com
          </Button>
        </div>
      </div>
      {failed ? badRequest : null}
      {success ? goodRequest : null}
    </div>
  );

  return (
    <div>
      {props.userName !== "Guest" ? (
        loading ? (
          loadingBackDrop
        ) : (
          addSeriesScreenConten
        )
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
