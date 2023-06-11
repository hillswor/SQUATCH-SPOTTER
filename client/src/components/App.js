import React, { useState, useEffect, useCallback } from "react";
import { Switch, Route } from "react-router-dom";
import Navbar from "./Navbar";
import Home from "./Home";
import Report from "./Report";
import Signup from "./Signup";
import Login from "./Login";
import MyAccount from "./MyAccount";

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [user, setUser] = useState(null);

  const setUserAndLogin = useCallback((user) => {
    setUser(user);
    setLoggedIn(true);
  }, []);

  const toggleLoggedIn = useCallback(() => {
    setLoggedIn((prevState) => !prevState);
  }, []);

  useEffect(() => {
    fetch("http://127.0.0.1:5555/check-session")
      .then((response) => response.json())
      .then((data) => {
        if (data.id) {
          setLoggedIn(true);
          setUser(data);
        } else {
          setLoggedIn(false);
          setUser(null);
        }
      })
      .catch((error) => {
        console.error("Error checking user session: ", error);
      });
  }, []);

  return (
    <div>
      <Navbar loggedIn={loggedIn} toggleLoggedIn={toggleLoggedIn} />
      <Switch>
        <Route exact path="/report">
          <Report />
        </Route>
        <Route exact path="/signup">
          <Signup setUserAndLogin={setUserAndLogin} />
        </Route>
        <Route exact path="/login">
          <Login setUserAndLogin={setUserAndLogin} />
        </Route>
        <Route path="/users/:id">
          <MyAccount />
        </Route>
        <Route exact path="/">
          <Home />
        </Route>
      </Switch>
    </div>
  );
}

export default App;
