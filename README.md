# Techno

**Techno** is an AI-powered API agent built for [RSRoute](https://github.com/ItzRustam/rsroute).

It uses tool calling to understand natural-language requests, interact with APIs, work with files, search the web when necessary, and return structured results.

Techno is designed as a lightweight, self-hosted alternative for experimenting with **Agentic AI + API workflows** without depending on a paid AI agent platform.

### CLI
```bash
python3 main.py
```

### Streamlit UI
```bash
streamlit run agent_with_ui.py
```

## Features

* Natural-language API tasks
* GET and POST API requests
* AI-powered tool calling
* Multiple tools in a single task
* API response inspection
* File creation and reading
* Web search
* Structured `APIResult` responses
* Configurable maximum tool calls
* Persistent conversation during a Streamlit session
* Streamlit chat interface
* Postman-style API result view
* Table and raw JSON result tabs
* Visible tool execution logs
* Google Gemini model support
* Local development through Python

## How It Works

Techno uses a manual agent loop rather than a high-level agent executor.

```text
User
 │
 ▼
Techno
 │
 ├── Tool call
 │      │
 │      ▼
 │   Tool result
 │      │
 │      ▼
 │   Techno
 │
 ├── Another tool call
 │      │
 │      ▼
 │   Tool result
 │
 ▼
Structured APIResult
```

For example, a request such as:

```text
Send a POST request to
http://0.0.0.0:8000/v1/gemini/chat
with the required parameters.
```

can cause Techno to:

```text
Natural language request
        ↓
    call_api
        ↓
   API response
        ↓
    Techno reads result
        ↓
    APIResult
```

For more complex tasks, Techno can chain tools:

```text
call_api
   ↓
inspect response
   ↓
create_file
   ↓
final result
```

## Available Tools

### `call_api`

Makes HTTP requests to API endpoints.

Currently supports:

* `GET`
* `POST`

Example request:

```text
Get http://0.0.0.0:8000/
```

Techno can determine the required tool arguments and execute the request.

### `create_file`

Creates a file with supplied content.

Example:

```text
Create info.csv with age and height data.
```

### `read_file`

Reads an existing file from the agent workspace.

### `find_file`

Finds files available in the workspace.

### `web_search`

Performs a web search when additional information is required.

Techno is instructed to avoid unnecessary tool calls and prefer the shortest valid path to completing a task.

## Structured Output

Techno uses a Pydantic model for its final response:

```python
class APIResult(BaseModel):
    status: str
    summary: str
    api_result: Dict[Any, Any]
```

The final response contains:

* `status` — whether the operation succeeded or failed
* `summary` — a concise description of what happened
* `api_result` — the actual API/tool result

The final model response is parsed using `PydanticOutputParser`.

## Streamlit Interface

Techno includes a Streamlit interface designed around API-agent workflows.

The interface provides:

### Tool execution

Every tool call is displayed:

```text
⚙ Tool: call_api

url
http://0.0.0.0:8000/v1/gemini/chat

method
post

✓ Tool result received
```

This makes Techno's agentic behavior observable instead of hiding tool execution.

### Status

The final status is displayed separately in a compact box.

```text
STATUS

✓ success

Successfully completed the API request.
```

### API Result

Results are displayed using two tabs:

```text
Table | JSON
```

**Table** provides a human-readable key/value representation.

**JSON** provides the raw structured result.

## Installation

Clone the repository:

```bash
git clone <repository-url>
cd rsroute-agent
```

Create a virtual environment:

```bash
python3 -m venv .venv
```

Activate it:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file:

```env
MODEL=gemini-3.5-flash-lite
GOOGLE_API_KEY=your_google_api_key
MAX_TOOL_USE=10
```

`MODEL` determines which Gemini model Techno uses.

`GOOGLE_API_KEY` is required by the Google Generative AI integration.

`MAX_TOOL_USE` limits the number of tool calls Techno can make for a single request.

## Running Techno

### Terminal version

The original agent can be run with:

```bash
python3 main.py
```

### Streamlit version

Run:

```bash
streamlit run app.py
```

Streamlit will start a local web application where you can interact with Techno through a chat interface.

## Example

### Create a CSV

```text
You:
Make a file named info.csv and create two columns:
age and height. Add 10 lines where height generally
increases with age.
```

Techno can call:

```text
create_file
```

and produce the requested file.

### API → File workflow

```text
You:
Make a GET request to http://0.0.0.0:8000/
and write the output to root_output.csv.
```

Techno can perform:

```text
call_api
    ↓
inspect response
    ↓
create_file
```

### API request

```text
You:
Send a POST request to
http://0.0.0.0:8000/v1/gemini/chat
with my API parameters.
```

Techno can construct the tool call, execute the request, inspect the response, and return an `APIResult`.