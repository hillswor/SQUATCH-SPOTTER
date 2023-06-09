import { Switch, Route } from "react-router-dom";

import Navbar from "./Navbar";
import Login from "./Login";

function App() {
  return (
    <div>
      <Navbar />
      <Switch>
        <Route path="/login">
          <Login />
        </Route>
      </Switch>
    </div>
  );
}

export default App;
