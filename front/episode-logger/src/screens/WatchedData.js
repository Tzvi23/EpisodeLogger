import React from "react";
import { connect } from "react-redux";

import { useParams } from "react-router-dom";

import { makeStyles } from "@material-ui/core/styles";
import Accordion from "@material-ui/core/Accordion";
import AccordionSummary from "@material-ui/core/AccordionSummary";
import AccordionDetails from "@material-ui/core/AccordionDetails";
import Typography from "@material-ui/core/Typography";
import ExpandMoreIcon from "@material-ui/icons/ExpandMore";

import WatchedSeriesData from "../components/watchedSeriesData/watchedSeriesData";

const useStyles = makeStyles((theme) => ({
  root: {
    width: "60%",
  },
  heading: {
    fontSize: theme.typography.pxToRem(15),
    fontWeight: theme.typography.fontWeightRegular,
  },
}));

const WatchedData = (props) => {
  const params = useParams();
  const classes = useStyles();

  // Get specific data using the url params
  const localData = props.userData[params.seriesname].DF_episodes_json_dict;
  console.log(localData);
  return (
    <div className={classes.root}>
      {Object.keys(localData).map((season, i) => {
        return (
          <Accordion key={i}>
            <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel1a-content"
              id="panel1a-header"
            >
              <Typography className={classes.heading}>
                Season: {season}
              </Typography>
            </AccordionSummary>
            <AccordionDetails
              style={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
              }}
            >
              {Object.keys(localData[season]).map((episode, y) => {
                return (
                  <WatchedSeriesData
                    episodeData={{
                      ...localData[season][episode],
                      episode: episode,
                    }}
                    key={y}
                  />
                );
              })}
            </AccordionDetails>
          </Accordion>
        );
      })}
    </div>
  );
};

// Redux configuration
const mapStateToProps = (state) => {
  return {
    userName: state.userName,
    userData: state.userData,
  };
};

export default connect(mapStateToProps)(WatchedData);
