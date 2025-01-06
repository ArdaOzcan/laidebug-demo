// Your API key goes here
const API_KEY = "";

const fs = require('fs');
const fileContent = fs.readFileSync('./example.py', 'utf8');

fetch("http://localhost:5000", {
  method: "POST",
  body: JSON.stringify({
    method: "debugFunction",
    params: [fileContent, "power", "gemini-1.5-flash", API_KEY],
    id: 1,
  }),
  headers: {
    "Content-type": "application/json; charset=UTF-8"
  }
})
  .then((response) => response.json())
  .then((json) => console.log(json));

