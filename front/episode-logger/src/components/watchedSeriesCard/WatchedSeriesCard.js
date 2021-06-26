import React from "react";
import { makeStyles } from "@material-ui/core/styles";
import Card from "@material-ui/core/Card";
import CardActionArea from "@material-ui/core/CardActionArea";
import CardContent from "@material-ui/core/CardContent";
import CardMedia from "@material-ui/core/CardMedia";
import Typography from "@material-ui/core/Typography";
import CheckCircleIcon from "@material-ui/icons/CheckCircle";

import { Link } from "react-router-dom";

const useStyles = makeStyles({
  root: {
    maxWidth: 345,
    minWidth: 200,
    margin: "20px",
  },
  media: {
    height: 250,
  },
});

export default function WatchedSeriesCard(props) {
  const classes = useStyles();

  return (
    <Card className={classes.root}>
      <CardActionArea component={Link} to={"/watched/" + props.seriesName}>
        <CardMedia
          className={classes.media}
          image={props.seriesImg}
          title={props.seriesName}
        />
        <CardContent>
          <Typography gutterBottom variant="h5" component="h2">
            {props.seriesName} &nbsp;
            {props.done ? <CheckCircleIcon /> : null}
          </Typography>
        </CardContent>
      </CardActionArea>
    </Card>
  );
}
