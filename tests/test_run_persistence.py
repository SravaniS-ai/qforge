import json

from qforge.runs.persistence import (
    load_run_result,
    save_run_result,
)
from qforge.runs.service import execute_test_run
from qforge.scenarios.qf_001 import QF_001


def test_save_run_result_to_json(tmp_path):
    """
    Verify that a complete QForge TestRunResult can be persisted
    as JSON and that the stored data matches the original run.

    tmp_path is provided automatically by pytest and gives this
    test its own temporary directory.
    """

    # Execute a real QForge scenario so we are persisting the
    # same TestRunResult object used by the platform.
    run_result = execute_test_run(
        scenario=QF_001,
    )

    # Save into pytest's temporary directory instead of the real
    # project results/ folder. This keeps tests isolated and avoids
    # leaving generated files behind after the test suite runs.
    output_file = save_run_result(
        run_result=run_result,
        results_dir=str(tmp_path),
    )

    # Persistence should create a real JSON file.
    assert output_file.exists()

    # The filename should be based on the unique run identifier.
    assert output_file.name == f"{run_result.run_id}.json"

    # Read the stored JSON back from disk so we can verify that
    # persistence did not lose or modify important run data.
    saved_data = json.loads(
        output_file.read_text(
            encoding="utf-8",
        )
    )

    assert saved_data["run_id"] == run_result.run_id
    assert saved_data["scenario_id"] == "QF-001"
    assert saved_data["status"] == "PASS"

    # Verify nested execution data was also serialized correctly.
    assert saved_data["agent_result"]["status"] == "CONFIRMED"

    # Verify QForge's structured evaluation survived persistence.
    assert saved_data["evaluation"]["status"] == "PASS"

    # Lifecycle metadata should also be present in the stored record.
    assert "started_at" in saved_data
    assert "finished_at" in saved_data
    assert "duration_ms" in saved_data

def test_saved_run_can_be_loaded(tmp_path):
    """
    Verify the complete persistence round trip:

    TestRunResult
        -> JSON
        -> TestRunResult
    """

    # Create a real QForge run.
    original_run = execute_test_run(
        scenario=QF_001,
    )

    # Persist the run to an isolated temporary directory.
    output_file = save_run_result(
        run_result=original_run,
        results_dir=str(tmp_path),
    )

    # Load the persisted JSON back into the domain model.
    loaded_run = load_run_result(
        file_path=output_file,
    )

    # Identity should survive persistence.
    assert loaded_run.run_id == original_run.run_id
    assert loaded_run.scenario_id == original_run.scenario_id

    # The observed SUT behavior should survive persistence.
    assert (
        loaded_run.agent_result.status
        == original_run.agent_result.status
    )

    # QForge's judgment should also survive persistence.
    assert (
        loaded_run.evaluation.status
        == original_run.evaluation.status
    )

    assert loaded_run.status == original_run.status

    # Pydantic should reconstruct timestamps as datetime values,
    # not leave them as raw JSON strings.
    assert loaded_run.started_at == original_run.started_at
    assert loaded_run.finished_at == original_run.finished_at