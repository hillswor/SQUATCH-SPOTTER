import React, { useEffect, useState } from "react";
import SightingsCard from "./SightingsCard";

function Home() {
  const [sightings, setSightings] = useState([]);

  useEffect(() => {
    fetch("http://127.0.0.1:5555/sightings")
      .then((response) => response.json())
      .then((data) => setSightings(data));
  }, []);

  return (
    <div className="grid grid-cols-1 gap-10 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 p-16 mt-20">
      {sightings.map((sighting) => (
        <SightingsCard
          key={sighting.id}
          sighting={sighting}
          comments={sighting.comments}
        />
      ))}
    </div>
  );
}

export default Home;
