import React from "react";
import { connect } from "react-redux";
import PleaseLogInButton from "../components/pleaseLogIn/PleaseLogIn";

import WatchedSeriesCard from "../components/watchedSeriesCard/WatchedSeriesCard";

const Watched = (props) => {
  console.log(props.userData);

  const watchedScreenContent = (
    <div
      style={{ display: "flex", flexFlow: "wrap", justifyContent: "center" }}
    >
      {Object.keys(props.userData).map((series, i) => {
        if (props.userData[series].visible === true)
          return (
            <WatchedSeriesCard
              seriesName={props.userData[series].name}
              seriesImg={props.userData[series].data["image_thumbnail_path"]}
              done={props.userData[series].nextEpisode === null}
              key={i}
            />
          );
        else return null;
      })}
    </div>
  );

  return (
    <div>
      {props.userName !== "Guest" ? (
        watchedScreenContent
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
    userData: state.userData,
  };
};

export default connect(mapStateToProps)(Watched);
