const API_KEY = "";

const fileContent = `
def add(x, y):
    sum = 0
    for n in [x, y]:
        sum += n

    return sum


if __name__ == "__main__":
    add(35, 40)
`;


fetch("http://localhost:5000", {
  method: "POST",
  body: JSON.stringify({
    method: "debugFunction",
    params: [fileContent, "adr", "gemini-1.5-flash", API_KEY],
    id: 1,
  }),
  headers: {
    "Content-type": "application/json; charset=UTF-8"
  }
})
  .then((response) => response.json())
  .then((json) => console.log(json));

