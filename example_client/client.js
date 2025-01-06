fetch("http://localhost:5000", {
  method: "POST",
  body: "something",
  headers: {
    "Content-type": "application/json; charset=UTF-8"
  }
})
  .then((response) => response.json())
  .then((json) => console.log(json));

