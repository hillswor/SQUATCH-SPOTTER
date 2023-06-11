import React from "react";

function SightingsCard({ sighting, comments }) {
  return (
    <div className="bg-stone-200 shadow-inherit overflow-hidden sm:rounded-lg max-w-lg mx-auto">
      <div className="px-4 py-5 sm:px-6">
        <h3 className="text-lg leading-6 font-medium text-green-800">
          {sighting.location.name}
        </h3>
        <h4 className="text-sm leading-6 font-medium text-green-600">
          {new Date(sighting.sighting_date).toDateString()}
        </h4>
        <p className="mt-1 max-w-2xl text-sm text-green-1000">
          {sighting.description}
        </p>
      </div>
    </div>
  );
}

export default SightingsCard;
