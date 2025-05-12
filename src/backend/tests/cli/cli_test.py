import asyncio
import json
import os
import re
import subprocess
import sys
from unittest.mock import patch

import pytest

from backend.app.utils.logger import get_logger

logger = get_logger(__name__)

# --- Constants ---
OUTPUT_DIR = "outputs"
ENTRYPOINT = "src/backend/app/cli.py"


def extract_json_from_output(output: str) -> dict:
    """Extract JSON from CLI output that may contain log messages."""
    start = output.find('{')
    end = output.rfind('}')
    
    if start == -1 or end == -1 or start > end:
        raise ValueError(f"No JSON found in output: {output}")
    
    json_str = output[start:end+1]
    
    json_str = re.sub(r'[\x00-\x1F\x7F]', '', json_str)
    
    try:
        return json.loads(json_str)
    except json.JSONDecodeError:
        for line in output.split('\n'):
            line = line.strip()
            if line.startswith('{') and line.endswith('}'):
                try:
                    return json.loads(line)
                except json.JSONDecodeError:
                    continue
        
        raise ValueError(f"Could not parse JSON from output: {output}")


async def test_greet_command() -> None:
    """Test the greet command."""
    logger.info("=== Testing greet command ===")

    result = subprocess.run(
        [sys.executable, ENTRYPOINT, "greet", "Test User", "--excited"],
        capture_output=True,
        text=True,
    )

    logger.info("CLI output:\n%s", result.stdout)
    assert result.returncode == 0, "CLI did not exit cleanly"
    assert "hello, test user!" in result.stdout.lower(), "Expected greeting not found"

    logger.info("✅ Greet command test passed.")


@pytest.mark.asyncio
async def test_format_task_command() -> None:
    """Test the format-task command."""
    logger.info("=== Testing format-task command ===")

    result = subprocess.run(
        [sys.executable, ENTRYPOINT, "format-task", "Create a test module"],
        capture_output=True,
        text=True,
    )

    logger.info("CLI output:\n%s", result.stdout)
    assert result.returncode == 0, "CLI did not exit cleanly"
    
    output_json = extract_json_from_output(result.stdout)
    assert "title" in output_json, "Title field missing"
    assert "goal" in output_json, "Goal field missing"
    assert "input" in output_json, "Input field missing"
    assert "output" in output_json, "Output field missing"
    assert "verify" in output_json, "Verify field missing"
    assert "notes" in output_json, "Notes field missing"
    
    assert isinstance(output_json["title"], str), "Title should be a string"
    assert isinstance(output_json["goal"], str), "Goal should be a string"
    assert isinstance(output_json["verify"], list), "Verify should be a list"
    assert isinstance(output_json["notes"], list), "Notes should be a list"

    logger.info("✅ Format-task command test passed.")


@pytest.mark.asyncio
async def test_format_task_compact_flag() -> None:
    """Test the format-task command with compact flag."""
    logger.info("=== Testing format-task command with compact flag ===")

    result = subprocess.run(
        [sys.executable, ENTRYPOINT, "format-task", "Create a test module", "--compact"],
        capture_output=True,
        text=True,
    )

    logger.info("CLI output:\n%s", result.stdout)
    assert result.returncode == 0, "CLI did not exit cleanly"
    
    output_json = extract_json_from_output(result.stdout)
    assert "title" in output_json, "Title field missing"
    assert "goal" in output_json, "Goal field missing"
    
    pretty_result = subprocess.run(
        [sys.executable, ENTRYPOINT, "format-task", "Create a test module", "--pretty"],
        capture_output=True,
        text=True,
    )
    
    logger.info("Pretty CLI output:\n%s", pretty_result.stdout)
    assert pretty_result.returncode == 0, "Pretty CLI did not exit cleanly"
    
    pretty_output_json = extract_json_from_output(pretty_result.stdout)
    
    assert len(result.stdout) < len(pretty_result.stdout), \
        "Compact output should be shorter than pretty output"

    logger.info("✅ Format-task command with compact flag test passed.")


@pytest.mark.asyncio
async def test_format_task_error_handling() -> None:
    """Test error handling in the format-task command."""
    logger.info("=== Testing format-task command error handling ===")

    result = subprocess.run(
        [sys.executable, ENTRYPOINT, "format-task", ""],
        capture_output=True,
        text=True,
    )
    
    logger.info(f"CLI stdout:\n{result.stdout}")
    logger.info(f"CLI stderr:\n{result.stderr}")
    
    combined_output = result.stdout.lower() + result.stderr.lower()
    assert "error" in combined_output or result.returncode != 0, \
        "CLI should display an error message or exit with non-zero code"

    logger.info("✅ Format-task command error handling test passed.")


if __name__ == "__main__":
    asyncio.run(test_greet_command())
    asyncio.run(test_format_task_command())
    asyncio.run(test_format_task_compact_flag())
    asyncio.run(test_format_task_error_handling())
