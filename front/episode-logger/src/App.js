import './App.css';

import { Route, Switch, Redirect, BrowserRouter } from 'react-router-dom';

import AddSeries from './screens/AddSeries';
import Login from './screens/Login/Login';
import NextEpisode from './screens/NextEpisode';
import RemoveSeries from './screens/RemoveSeries';
import Watched from './screens/Watched';
import UpdateSeries from './screens/UpdateSeries';

import Toolbar from './components/toolbar/Toolbar';

function App() {

  return (
    <div className="App">
      <BrowserRouter>
          <Toolbar/>
          <div id='mainCenter' style={{'display': 'flex','justifyContent': 'center', 'marginTop': '30px'}}>
          <Switch>
            <Route path="/" exact>
              <Redirect to="/login" />
            </Route>
            <Route path="/addSeries" >
              <AddSeries />
            </Route>
            <Route path="/login">
              <Login />
            </Route>
            <Route path="/nextEpisode">
              <NextEpisode />
            </Route>
            <Route path="/removeSeries">
              <RemoveSeries />
            </Route>
            <Route path="/watched">
              <Watched />
            </Route>
            <Route path="/updateSeries">
              <UpdateSeries />
            </Route>
          </Switch>
          </div>
        </BrowserRouter>
    </div>
  );
}

export default App;
