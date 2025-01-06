# Lai.debug: Your AI Debugger
Lai.debug (pronounced ladybug), incorporates debuggers with LLMs by utilizing prompt engineering in order to help developers fix bugs. It uses Python for the core library, Flask web framework for the API and JavaScript Object Notation (JSON) for communication along with deuggers such as or Python Debugger (PDB).

This demo currently only supports python files as source files and `gemini-1.5-flash` as a model.
## Dependencies
These programs are required to run this project:
* `node 22.11.0`
* `python 3.12.7`

## Installation
Run `git clone https://github.com/ArdaOzcan/laidebug-demo/`

## Setup
You will need to install the python requirements in order to use this projects.

Navigate to the root directory of the project `laidebug-demo/`.

### For Windows:
Run the `setup_windows.bat` file.

### For MacOS/Linux:
Run `chmod +x setup.sh` to make `setup.sh` executable.
Run the `setup.sh` file in your terminal.

You are now ready to use Lai.debug!

## Usage
### API Key
You will have to get a free API key for `gemini-1.5-flash` from [here](https://aistudio.google.com/apikey) in order to use Lai.debug.
After getting the key, insert it in `laidebug-demo/example_client/client.js` if you would like to use the example.

There are two ways to use this program. You can either use laidebug_engine as a CLI tool or start a HTTP server using the laidebug_api and create requests with a client of your choice.
1. **CLI**
   
   In order to use Lai.debug in your terminal, navigate to the engine directory `laidebug-demo/laidebug_engine` and activate the virtual environment with `source bin/activate` if you are on MacOS/Linux and `.\Scripts\active` if you are on Windows.

   After that, you can simply run `python -m laidebug_engine --help`. The command line arguments are like this: `python -m laidebug_engine FILE_PATH FUNCTION_NAME MODEL_NAME API_KEY`
2. **JSON-RPC**

  You can also run the laidebug_api HTTP server, which will be calling the function from the laidebug_engine using Remote Procedure Calling (RPC) over JSON.
  
  You can start the server by navigating to the api folder `laidebug-demo/laidebug_api` and running the command `python -m flask --app main run`.
  This will start a server running on `http://localhost:5000`. You can now send requests in JSON format. We can use the example client to test the server.
  Navigate to `laidebug-demo/example_client` and (you should have a valid API_KEY at this point) run `node client.js`.
  The example client sends this request to the server:
  ```json
{
  "method": "debugFunction",
  "params": [
    "def add(x, y):\n    sum = 0\n    for n in [x, y]:\n        sum += n\n    return sum\nif __name__ == \"__main__\":\n    add(35, 40)",
    "add",
    "gemini-1.5-flash",
    "API_KEY"
  ],
  "id": 1
}
  ```
  The servers response is:
  ```json
{
  "id": 1,
  "result": "The function `add` correctly sums the values of the variables `x` and `y`.  There is no unexpected behavior reported in the provided trace.  The function initializes `sum` to 0, iterates through the list `[x, y]`, adding each element to `sum`, and finally returns the correct sum (75).\n"
}
  ```

You can change the content of the `example.py` file and the function name parameter, the second parameter, in `client.js` to play with it.

## How does it Work?
The Lai.debug Engine runs the given python file and records local variables of the given function for each executed line. An example prompt generated by the engine looks like this:
```
Your task is to analyze function 'add' and report any unexpected behaviour.
The full function consists of the given lines of code:

-> Local variables currently are:
'x': 35
'y': 40
-> Line 3 will be executed.
-> Line content is:
    sum = 0
-> Local variables currently are:
'x': 35
'y': 40
'sum': 0
-> Line 4 will be executed.
-> Line content is:
    for n in [x, y]:
-> Local variables currently are:
'x': 35
'y': 40
'sum': 0
'n': 35
-> Line 5 will be executed.
-> Line content is:
        sum += n
-> Local variables currently are:
'x': 35
'y': 40
'sum': 35
'n': 35
-> Line 4 will be executed.
-> Line content is:
    for n in [x, y]:
-> Local variables currently are:
'x': 35
'y': 40
'sum': 35
'n': 40
-> Line 5 will be executed.
-> Line content is:
        sum += n
-> Local variables currently are:
'x': 35
'y': 40
'sum': 75
'n': 40
-> Line 4 will be executed.
-> Line content is:
    for n in [x, y]:
-> Local variables currently are:
'x': 35
'y': 40
'sum': 75
'n': 40
-> Line 7 will be executed.
-> Line content is:
    return sum
The function has ended.
```