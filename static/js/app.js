const url = "http://127.0.0.1:5000/api/v1.0/names";

// Promise Pending
const dataPromise = d3.json(url);
console.log("Data Promise: ", dataPromise);

// Fetch the JSON data and console log it
d3.json(url).then(function (data) {
  console.log(data);
});
