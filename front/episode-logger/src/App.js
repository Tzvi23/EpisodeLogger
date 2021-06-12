import './App.css';

import { Route, Switch, Redirect, BrowserRouter } from 'react-router-dom';
import { useState } from 'react';

import AddSeries from './screens/AddSeries';
import Login from './screens/Login/Login';
import NextEpisode from './screens/NextEpisode';
import RemoveSeries from './screens/RemoveSeries';
import Watched from './screens/Watched';
import UpdateSeries from './screens/UpdateSeries';

import Toolbar from './components/toolbar/Toolbar';

function App() {
  const [screenName, setScreenName] = useState('Log In');

  return (
    <div className="App">
      <BrowserRouter>
          <Toolbar setScreenName={setScreenName} curScreenName={screenName}/>
          <div id='mainCenter' style={{'display': 'flex','justifyContent': 'center', 'marginTop': '30px'}}>
          <Switch>
            <Route path="/" exact>
              <Redirect to="/login" />
            </Route>
            <Route path="/addSeries" >
              <AddSeries setScreenName={setScreenName}/>
            </Route>
            <Route path="/login">
              <Login setScreenName={setScreenName}/>
            </Route>
            <Route path="/nextEpisode">
              <NextEpisode setScreenName={setScreenName}/>
            </Route>
            <Route path="/removeSeries">
              <RemoveSeries setScreenName={setScreenName}/>
            </Route>
            <Route path="/watched">
              <Watched setScreenName={setScreenName}/>
            </Route>
            <Route path="/updateSeries">
              <UpdateSeries setScreenName={setScreenName}/>
            </Route>
          </Switch>
          </div>
        </BrowserRouter>
    </div>
  );
}

export default App;
