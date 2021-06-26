import React from "react";
import { connect } from "react-redux";

import { useParams } from "react-router-dom";

const WatchedData = (props) => {
  const params = useParams();

  console.log(params);
  console.log(props.userData);

  return <div>Series Data</div>;
};

// Redux configuration
const mapStateToProps = (state) => {
  return {
    userName: state.userName,
    userData: state.userData,
  };
};

export default connect(mapStateToProps)(WatchedData);
