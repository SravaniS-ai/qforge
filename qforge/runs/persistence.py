from pathlib import Path

from qforge.runs.models import TestRunResult


def save_run_result(
    run_result: TestRunResult,
    results_dir: str = "results",
) -> Path:
    """
    Persist one complete QForge TestRunResult as a JSON file.

    Each run is stored using its unique run_id so that multiple
    executions of the same scenario remain separate records.

    Example:
        RUN-A1B2C3D4.json
    """

    # Ensure the results directory exists before writing the file.
    #
    # parents=True allows nested directories if we add them later.
    # exist_ok=True avoids errors when the folder already exists.
    output_directory = Path(results_dir)
    output_directory.mkdir(
        parents=True,
        exist_ok=True,
    )

    # Use the unique run ID as the filename.
    output_file = output_directory / f"{run_result.run_id}.json"

    # Pydantic handles conversion of nested models and datetime
    # values into JSON-compatible output.
    json_content = run_result.model_dump_json(
        indent=2,
    )

    output_file.write_text(
        json_content,
        encoding="utf-8",
    )

    return output_file
def load_run_result(
    file_path: str | Path,
) -> TestRunResult:
    """
    Load a previously persisted QForge run from JSON.

    This reconstructs the saved JSON back into the same
    TestRunResult model used by the execution platform.
    """

    input_file = Path(file_path)

    # Read the persisted JSON exactly as text.
    json_content = input_file.read_text(
        encoding="utf-8",
    )

    # Pydantic reconstructs the complete nested object:
    #
    # TestRunResult
    # ├── RebookingResult
    # └── EvaluationResult
    #
    # including datetime fields.
    return TestRunResult.model_validate_json(
        json_content
    )