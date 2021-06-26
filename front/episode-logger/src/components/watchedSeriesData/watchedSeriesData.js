import React, { useState } from "react";

import SaveIcon from "@material-ui/icons/Save";
import IconButton from "@material-ui/core/IconButton";
import ErrorIcon from "@material-ui/icons/Error";
import ErrorOutlineIcon from "@material-ui/icons/ErrorOutline";

import Checkbox from "@material-ui/core/Checkbox";

import Grid from "@material-ui/core/Grid";

const WatchedSeriesData = (props) => {
  const { name, air_date, watched, episode } = props.episodeData;
  const [checked, setChecked] = useState(watched);
  const [change, setChange] = useState(false);

  const handleChange = (event) => {
    setChecked(event.target.checked);
    setChange(true);
  };

  return (
    <div>
      <Grid
        container
        spacing={3}
        style={{
          display: "flex",
          flexWrap: "nowrap",
          alignItems: "center",
        }}
      >
        <Grid item xs={4}>
          <div>{name}</div>
        </Grid>
        <Grid item xs={1}>
          <div>{episode}</div>
        </Grid>
        <Grid item xs={4}>
          <div>{air_date}</div>
        </Grid>
        <Grid item xs={1}>
          <div>{watched}</div>
        </Grid>
        <Grid item xs={1}>
          <div>
            <Checkbox checked={checked} onChange={handleChange} />
          </div>
        </Grid>
        <Grid item xs={1}>
          <div>
            <IconButton>
              <SaveIcon />
            </IconButton>
          </div>
        </Grid>
        <Grid item xs={1}>
          <div>{change ? <ErrorIcon /> : <ErrorOutlineIcon />}</div>
        </Grid>
      </Grid>
    </div>
  );
};

export default WatchedSeriesData;
