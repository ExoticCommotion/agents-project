# Devin Task Formatter Agent

The Devin Task Formatter Agent (DTFA) transforms natural language task descriptions into structured JSON task definitions suitable for automated processing and execution.

## Purpose

The Task Formatter Agent serves as a bridge between human-written task descriptions and machine-readable task definitions. It extracts key information from natural language descriptions and formats it according to a standardized schema, enabling:

- Consistent task representation across the system
- Automated validation of task requirements
- Clear communication of expectations between humans and AI agents
- Structured tracking of task progress and completion criteria

## Features

- Transforms natural language task descriptions into structured JSON
- Provides both CLI and API interfaces for integration
- Implements robust error handling and validation
- Returns detailed error information for troubleshooting
- Supports both synchronous and asynchronous processing

## Usage

### CLI Usage

The Task Formatter Agent can be used directly from the command line:

```bash
# Basic usage
uv run python -m backend.app.cli format-task "Create a Python module that does X and Y."

# Compact JSON output (no indentation)
uv run python -m backend.app.cli format-task "Fix bug in login form" --compact
```

#### CLI Options

- `task_description`: The natural language description of the task (required)
- `--pretty/--compact`: Format JSON output with indentation for readability (default: pretty)

### API Usage

The Task Formatter Agent is also available as a FastAPI endpoint:

```bash
# Start the API server
uv run python -m backend.app.main
```

#### Endpoint

- **URL**: `/format-task/`
- **Method**: POST
- **Request Body**:
  ```json
  {
    "task_description": "Create a Python module that does X and Y."
  }
  ```
- **Success Response**:
  ```json
  {
    "success": true,
    "data": {
      "title": "Python Module for X and Y",
      "goal": "Create a Python module that implements functionality X and Y",
      "input": "Requirements for X and Y functionality",
      "output": "A Python module with X and Y capabilities",
      "verify": ["Test X functionality", "Test Y functionality"],
      "notes": ["Consider edge cases for X", "Optimize Y for performance"]
    }
  }
  ```
- **Error Response**:
  ```json
  {
    "detail": {
      "success": false,
      "error": {
        "type": "validation_error",
        "message": "Task description is too short",
        "details": {
          "min_length": 10,
          "actual_length": 5
        }
      }
    }
  }
  ```

#### HTTP Status Codes

- `200 OK`: Successful task formatting
- `400 Bad Request`: Validation error (e.g., task description too short)
- `401 Unauthorized`: Authentication error (e.g., invalid API key)
- `429 Too Many Requests`: Rate limit exceeded
- `500 Internal Server Error`: Server or API error

## Output Format

The Task Formatter Agent produces JSON output with the following structure:

```json
{
  "title": "Brief task title",
  "goal": "What the feature or bug fix achieves",
  "input": "Input expectations (CLI args, API behavior, files touched)",
  "output": "Output expectations (stdout, files, etc.)",
  "verify": [
    "Test names, command output, or other pass/fail signals"
  ],
  "notes": [
    "Important hints, constraints, or potential pitfalls"
  ]
}
```

## Setup

### Prerequisites

- Python 3.10+
- OpenAI API key with access to GPT-4o

### Environment Variables

The Task Formatter Agent requires the following environment variables:

- `OPENAI_API_KEY`: Your OpenAI API key

You can set these variables in your environment:

```bash
export OPENAI_API_KEY="your-api-key"
```

Or create a `.env` file in the project root:

```
OPENAI_API_KEY=your-api-key
```

### Installation

The Task Formatter Agent is included in the agents-project repository. To set up the project:

1. Clone the repository
2. Run `make reset` to set up the virtual environment and install dependencies
3. Verify the installation with `make check`

## Error Handling

The Task Formatter Agent provides detailed error information for troubleshooting:

- **Validation Errors**: Issues with the input task description (e.g., too short, too long)
- **API Errors**: Issues with the OpenAI API (e.g., rate limits, authentication)
- **Parsing Errors**: Issues with parsing the JSON response from the agent

Each error includes:
- Error type
- Error message
- Detailed information for debugging

## Development

When extending or modifying the Task Formatter Agent:

1. Run tests with `make test`
2. Validate changes with `make check` and `make verify`
3. Follow the project's code style and documentation standards
