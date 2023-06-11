import { Switch, Route } from "react-router-dom";

import Navbar from "./Navbar";
import Login from "./Login";
import Signup from "./Signup";
import Report from "./Report";
import SightingsContainer from "./SightingsContainer";
import Home from "./Home";

function App() {
  return (
    <div>
      <Navbar />
      <Switch>
        <Route exact path="/test">
          <div>Test Page</div>
        </Route>
        <Route exact path="/report">
          <Report />
        </Route>
        <Route exact path="/sightings">
          <SightingsContainer />
        </Route>
        <Route exact path="/signup">
          <Signup />
        </Route>
        <Route exact path="/login">
          <Login />
        </Route>
        <Route exact path="/">
          <Home />
        </Route>
      </Switch>
    </div>
  );
}

export default App;
