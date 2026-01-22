# slop-agent-101
An AI agent built with Google's Gemini API, for the purpose of following a [Boot.Dev course](https://www.boot.dev/courses/build-ai-agent-python).

The agent is designed with the capability of running python scripts to find .py files within
subdirectories, read their contents, write to them, and run them.

For security purposes, the agent is given constraints designed to keep it from looking anywhere 
but the directory defined by the `WORKING_DIR` constant within `config.py`.


## Usage

Don't.

## Usage (okay, fine)
I say "don't" because running AI agents on your local machine, especially your daily driver, is dangerous,
especially when said agents have capabilities like read, write, and execute permissions.
Even if the agent is given constraints (as in this project), agentic AI can be manipulated, and the outcome
of using it may be unpredictable.

However, I am a fan of completeness, so here's an official `usage` section. If you'd like to run this agent
(or _any_ AI agent, for that matter) for any reason whatsoever, I recommend doing so in a containerized or 
virtual environment.

### Step 1:
Clone the repo:
```
git clone https://github.com/bntrtm/slop-agent-101.git
```

### Step 2:
In `.env` file, set the `GEMINI_API_KEY` environment variable to whatever key [Google AI Studio](https://aistudio.google.com/api-keys) 
gives you after generating an API key for a new project.

### Step 3:
Configure the agent with `config.py`:
```
MAX_CHARS = 10000 # maximum character count to output before truncating, when reading a file
WORKING_DIR = "./calculator" # directory to work within
LOOP_ITER_MAX = 5 # number of iterations for the agent to loop over before giving up on a response
```

### Step 4:
Run the agent with: `uv main.py (user_prompt_here)`.
You can experiment with the default working directory by changing the `precedence` of the `+` operator within
the included `calculator.py` script to `3` instead of `1`, and then asking the agent to fix the bug:
```
uv main.py "Fix the bug: 3 + 7 * 2 shouldn't be 20."
```
For more robust output, you can use the `--verbose` flag when running the script:
```
uv main.py "Fix the bug: 3 + 7 * 2 shouldn't be 20." --verbose
```
