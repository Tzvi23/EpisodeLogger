import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Card from '@material-ui/core/Card';
import CardActions from '@material-ui/core/CardActions';
import CardContent from '@material-ui/core/CardContent';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import Grid from '@material-ui/core/Grid'

const useStyles = makeStyles({
  root: {
    minWidth: 275,
    margin: '10px',
    background: '#949392',
    borderColor: '#ff860d'
  },
  title: {
    fontSize: 14,
  },
  pos: {
    marginBottom: 12,
  },
  daysCard: {
      display:'flex',
      justifyContent:'center',
      width: '50px',
      height: '50px',
      backgroundColor: 'white',
      borderRadius: '0.25rem',
      boxShadow: '0 20px 40px -14px rgba(0, 0, 0, 0.25)'
  },
  cneter: {
      display: 'flex',
      justifyContent: 'center',
  }
});

export default function NextEpisodeCard(props) {
  const classes = useStyles();
  console.log(props.seriesData)

  return (
    
    <Card className={classes.root}>
        <Grid container spacing={2} justify='center'>
        <Grid item xs={8}>
      <CardContent >
        <Typography variant="h6" >
          {props.seriesData.name}
        </Typography>
        <Typography >
          Season: {props.seriesData.nextEpisode.season}
        </Typography>
        <Typography >
          Episode: {props.seriesData.nextEpisode.episode}
        </Typography>
        <Typography >
          Air date: {props.seriesData.nextEpisode.air_date}
        </Typography>
        <Typography >
            {props.seriesData.nextEpisode.episode_name}
        </Typography>
        </CardContent>
        </Grid>
        <Grid item xs={4}>
        <CardContent className={classes.cneter}>
        <div className={classes.daysCard}>
        {props.seriesData.nextEpisode.days}
        </div>
      </CardContent>
        
      <CardActions>
        <Button size="small">Learn More</Button>
      </CardActions>
      </Grid>
      
      </Grid>
    </Card>
    
  );
}
