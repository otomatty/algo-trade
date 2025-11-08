"""
JSON I/O utilities for communication with Rust commands.
"""
import json
import sys
from typing import Any, Dict


def read_json_input() -> Dict[str, Any]:
    """
    Read JSON input from stdin.
    Used when Python script is called from Rust command.
    """
    try:
        input_data = sys.stdin.read()
        if not input_data:
            return {}
        return json.loads(input_data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON input: {e}")


def write_json_output(data: Any) -> None:
    """
    Write JSON output to stdout.
    Used to send results back to Rust command.
    """
    json.dump(data, sys.stdout, ensure_ascii=False, indent=2)
    sys.stdout.flush()


def json_response(success: bool, data: Any = None, error: str = None) -> Dict[str, Any]:
    """
    Create a standardized JSON response.
    """
    response = {"success": success}
    if data is not None:
        response["data"] = data
    if error is not None:
        response["error"] = error
    return response

