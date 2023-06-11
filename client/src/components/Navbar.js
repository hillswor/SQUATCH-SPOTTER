import React, { useState } from "react";
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav>
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/test">Test Page</Link>
        </li>
        <li>
          <Link to="/report">Report Sighting</Link>
        </li>
        <li>
          <Link to="/sightings">Sightings</Link>
        </li>
        <li>
          <Link to="/login">Login</Link>
        </li>
        <li>
          <Link to="/signup">Sign Up</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Navbar;
