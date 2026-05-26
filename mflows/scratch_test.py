"""
scratch_test.py — Flow tests for the DAG parser + LLM fallback system.

Run with:
    pytest scratch_test.py -v

Covers:
    1. Valid linear DAG
    2. Valid branching DAG
    3. Cycle detection
    4. Missing action (hard fail — no LLM repair)
    5. Malformed depends syntax (repairable)
    6. Duplicate step ids
    7. Invalid arrow syntax (hard fail)
    8. Provider disabled state
    9. LLM timeout handling
   10. Parser hard fail behavior (no partial acceptance)
"""

import pytest
from unittest.mock import patch, MagicMock

from app.parsers.dsl_parser import parse_dsl
from app.parsers.dag_validator import validate_dag
from app.parsers.dag_orchestrator import parse_dag_workflow
from app.llm.provider_health import (
    record_provider_error,
    is_provider_healthy,
    reset_provider,
    PROVIDER_STATE,
)


# ─────────────────────────────────────────────
# HELPERS
# ─────────────────────────────────────────────

def clear_provider_state():
    PROVIDER_STATE.clear()


# ─────────────────────────────────────────────
# 1. VALID LINEAR DAG
# ─────────────────────────────────────────────

def test_valid_linear_dag_parse():
    dsl = """
@1: payment_due -> send_reminder
@2 @depends(@1): payment_due -> escalate_case
@3 @depends(@2): payment_due -> close_case
"""
    result = parse_dsl(dsl)

    assert result["success"] is True
    assert len(result["steps"]) == 3
    assert result["errors"] == []

    assert result["steps"][0]["id"] == "1"
    assert result["steps"][0]["trigger"] == "payment_due"
    assert result["steps"][0]["action"] == "send_reminder"
    assert result["steps"][0]["depends_on"] == []

    assert result["steps"][1]["depends_on"] == ["1"]
    assert result["steps"][2]["depends_on"] == ["2"]


def test_valid_linear_dag_validation():
    steps = [
        {"id": "1", "trigger": "payment_due", "action": "send_reminder", "depends_on": []},
        {"id": "2", "trigger": "payment_due", "action": "escalate_case", "depends_on": ["1"]},
        {"id": "3", "trigger": "payment_due", "action": "close_case", "depends_on": ["2"]},
    ]
    result = validate_dag(steps)

    assert result["is_valid"] is True
    assert result["errors"] == []


def test_valid_linear_dag_full_flow():
    dsl = """
@1: payment_due -> send_reminder
@2 @depends(@1): payment_due -> escalate_case
"""
    with patch("app.parsers.dag_orchestrator.cache_store") as mock_cache:
        mock_cache.__contains__ = MagicMock(return_value=False)
        mock_cache.__setitem__ = MagicMock()

        result = parse_dag_workflow(dsl)

    assert result["success"] is True
    assert len(result["steps"]) == 2
    assert result["validation"]["is_valid"] is True
    assert result["validation"]["errors"] == []
    assert result["source"] == "deterministic"


# ─────────────────────────────────────────────
# 2. VALID BRANCHING DAG
# ─────────────────────────────────────────────

def test_valid_branching_dag():
    dsl = """
@1: payment_due -> send_reminder
@2 @depends(@1): payment_due -> escalate_case
@3 @depends(@1): payment_due -> notify_manager
"""
    result = parse_dsl(dsl)

    assert result["success"] is True
    assert len(result["steps"]) == 3

    # Both step 2 and 3 depend on step 1 — branching
    assert result["steps"][1]["depends_on"] == ["1"]
    assert result["steps"][2]["depends_on"] == ["1"]


def test_valid_branching_dag_validation():
    steps = [
        {"id": "1", "trigger": "payment_due", "action": "send_reminder", "depends_on": []},
        {"id": "2", "trigger": "payment_due", "action": "escalate_case", "depends_on": ["1"]},
        {"id": "3", "trigger": "payment_due", "action": "notify_manager", "depends_on": ["1"]},
    ]
    result = validate_dag(steps)

    assert result["is_valid"] is True


def test_multi_dependency_step():
    dsl = """
@1: payment_due -> send_reminder
@2: payment_due -> notify_manager
@3 @depends(@1,@2): payment_due -> close_case
"""
    result = parse_dsl(dsl)

    assert result["success"] is True
    assert result["steps"][2]["depends_on"] == ["1", "2"]


# ─────────────────────────────────────────────
# 3. CYCLE DETECTION
# ─────────────────────────────────────────────

def test_direct_cycle_detected():
    # 1 → 2 → 1 is a cycle
    steps = [
        {"id": "1", "trigger": "payment_due", "action": "send_reminder", "depends_on": ["2"]},
        {"id": "2", "trigger": "payment_due", "action": "escalate_case", "depends_on": ["1"]},
    ]
    result = validate_dag(steps)

    assert result["is_valid"] is False
    assert "dag_has_cycle" in result["errors"]


def test_self_cycle_detected():
    # step depends on itself
    steps = [
        {"id": "1", "trigger": "payment_due", "action": "send_reminder", "depends_on": ["1"]},
    ]
    result = validate_dag(steps)

    assert result["is_valid"] is False
    assert "dag_has_cycle" in result["errors"]


def test_three_node_cycle_detected():
    steps = [
        {"id": "1", "trigger": "payment_due", "action": "send_reminder", "depends_on": ["3"]},
        {"id": "2", "trigger": "payment_due", "action": "escalate_case", "depends_on": ["1"]},
        {"id": "3", "trigger": "payment_due", "action": "close_case", "depends_on": ["2"]},
    ]
    result = validate_dag(steps)

    assert result["is_valid"] is False
    assert "dag_has_cycle" in result["errors"]


def test_no_cycle_in_valid_dag():
    steps = [
        {"id": "1", "trigger": "payment_due", "action": "send_reminder", "depends_on": []},
        {"id": "2", "trigger": "payment_due", "action": "escalate_case", "depends_on": ["1"]},
        {"id": "3", "trigger": "payment_due", "action": "close_case", "depends_on": ["2"]},
    ]
    result = validate_dag(steps)

    assert result["is_valid"] is True
    assert "dag_has_cycle" not in result["errors"]


# ─────────────────────────────────────────────
# 4. MISSING ACTION — hard fail, no LLM repair
# ─────────────────────────────────────────────

def test_missing_action_is_hard_fail():
    # action is not in ALLOWED_ACTIONS — semantic failure
    steps = [
        {"id": "1", "trigger": "payment_due", "action": None, "depends_on": []},
    ]
    result = validate_dag(steps)

    assert result["is_valid"] is False
    assert any("action_required" in e for e in result["errors"])


def test_invalid_action_name_is_hard_fail():
    steps = [
        {"id": "1", "trigger": "payment_due", "action": "approve_loan", "depends_on": []},
    ]
    result = validate_dag(steps)

    assert result["is_valid"] is False
    assert any("invalid_action" in e for e in result["errors"])


def test_missing_action_does_not_trigger_llm_repair():
    """
    Semantic validation failure must never trigger LLM repair.
    The orchestrator must return hard fail immediately.
    """
    dsl = """
@1: payment_due -> send_reminder
@2 @depends(@1): payment_due -> approve_loan
"""
    with patch("app.parsers.dag_orchestrator.repair_dsl_with_llm") as mock_repair:
        result = parse_dag_workflow(dsl)

    # LLM repair must NOT have been called
    mock_repair.assert_not_called()
    assert result["success"] is False
    assert result["validation"]["is_valid"] is False


# ─────────────────────────────────────────────
# 5. MALFORMED DEPENDS — repairable
# ─────────────────────────────────────────────

def test_malformed_depends_is_repairable():
    # Has arrow but malformed depends — structurally repairable
    dsl = "payment_due -> send_reminder"  # missing @id: prefix

    result = parse_dsl(dsl)

    assert result["success"] is False
    assert result["repairable"] is True


def test_ambiguous_syntax_no_arrow_is_not_repairable():
    # Old ambiguous format — no arrow — hard fail
    dsl = "@1: payment_due validate_payment"

    result = parse_dsl(dsl)

    assert result["success"] is False
    assert result["repairable"] is False
    assert any("invalid_syntax_no_arrow" in e for e in result["errors"])


def test_repairable_triggers_llm_repair():
    dsl = "payment_due -> send_reminder"  # missing @id: — repairable

    repaired_dsl = "@1: payment_due -> send_reminder"

    with patch("app.parsers.dag_orchestrator.repair_dsl_with_llm") as mock_repair, \
         patch("app.parsers.dag_orchestrator.cache_store") as mock_cache:

        mock_cache.__contains__ = MagicMock(return_value=False)
        mock_cache.__setitem__ = MagicMock()
        mock_repair.return_value = {"success": True, "repaired_text": repaired_dsl}

        result = parse_dag_workflow(dsl)

    mock_repair.assert_called_once()
    assert result["success"] is True
    assert result["source"] == "llm_repair"


# ─────────────────────────────────────────────
# 6. DUPLICATE STEP IDS
# ─────────────────────────────────────────────

def test_duplicate_step_ids_fail():
    steps = [
        {"id": "1", "trigger": "payment_due", "action": "send_reminder", "depends_on": []},
        {"id": "1", "trigger": "payment_due", "action": "escalate_case", "depends_on": []},
    ]
    result = validate_dag(steps)

    assert result["is_valid"] is False
    assert any("duplicate_step_id" in e for e in result["errors"])


def test_duplicate_step_ids_in_dsl():
    dsl = """
@1: payment_due -> send_reminder
@1: payment_due -> escalate_case
"""
    parse_result = parse_dsl(dsl)
    # DSL parser succeeds (both lines are valid syntax)
    # Validator catches the duplicate
    if parse_result["success"]:
        validation = validate_dag(parse_result["steps"])
        assert validation["is_valid"] is False
        assert any("duplicate_step_id" in e for e in validation["errors"])


# ─────────────────────────────────────────────
# 7. INVALID ARROW SYNTAX — hard fail
# ─────────────────────────────────────────────

def test_no_arrow_is_hard_fail():
    dsl = "@1: payment_due validate_payment"

    result = parse_dsl(dsl)

    assert result["success"] is False
    assert result["repairable"] is False


def test_no_arrow_does_not_trigger_llm():
    dsl = "@1: payment_due validate_payment"

    with patch("app.parsers.dag_orchestrator.repair_dsl_with_llm") as mock_repair, \
         patch("app.parsers.dag_orchestrator.cache_store") as mock_cache:

        mock_cache.__contains__ = MagicMock(return_value=False)
        mock_cache.__setitem__ = MagicMock()

        result = parse_dag_workflow(dsl)

    mock_repair.assert_not_called()
    assert result["success"] is False


def test_empty_input_is_hard_fail():
    result = parse_dsl("")

    # No steps parsed
    assert result["success"] is False or result["steps"] == []


# ─────────────────────────────────────────────
# 8. PROVIDER DISABLED STATE
# ─────────────────────────────────────────────

def test_fatal_error_disables_provider():
    clear_provider_state()

    record_provider_error("gemini", "API_KEY_INVALID: key not valid")

    assert is_provider_healthy("gemini") is False


def test_non_fatal_error_does_not_disable_provider():
    clear_provider_state()

    record_provider_error("gemini", "timeout")

    assert is_provider_healthy("gemini") is True


def test_disabled_provider_reenables_after_cooldown():
    import time
    clear_provider_state()

    # Disable with 1 second cooldown
    record_provider_error("gemini", "API_KEY_INVALID", cooldown_seconds=1)
    assert is_provider_healthy("gemini") is False

    time.sleep(1.1)

    # Should be re-enabled now
    assert is_provider_healthy("gemini") is True


def test_manual_reset_reenables_provider():
    clear_provider_state()

    record_provider_error("ollama", "API_KEY_INVALID")
    assert is_provider_healthy("ollama") is False

    reset_provider("ollama")
    assert is_provider_healthy("ollama") is True


def test_unknown_provider_is_healthy():
    clear_provider_state()
    assert is_provider_healthy("some_new_provider") is True


# ─────────────────────────────────────────────
# 9. LLM TIMEOUT HANDLING
# ─────────────────────────────────────────────

def test_llm_repair_timeout_returns_hard_fail():
    dsl = "payment_due -> send_reminder"  # repairable

    with patch("app.parsers.dag_orchestrator.repair_dsl_with_llm") as mock_repair, \
         patch("app.parsers.dag_orchestrator.cache_store") as mock_cache:

        mock_cache.__contains__ = MagicMock(return_value=False)
        mock_cache.__setitem__ = MagicMock()
        # Simulate LLM timeout
        mock_repair.return_value = {"success": False, "error": "timeout"}

        result = parse_dag_workflow(dsl)

    assert result["success"] is False
    assert any("llm_repair_failed" in e for e in result["validation"]["errors"])


def test_llm_repair_returns_invalid_dsl_is_hard_fail():
    dsl = "payment_due -> send_reminder"  # repairable

    with patch("app.parsers.dag_orchestrator.repair_dsl_with_llm") as mock_repair, \
         patch("app.parsers.dag_orchestrator.cache_store") as mock_cache:

        mock_cache.__contains__ = MagicMock(return_value=False)
        mock_cache.__setitem__ = MagicMock()
        # LLM returns something still invalid
        mock_repair.return_value = {
            "success": True,
            "repaired_text": "@1: payment_due validate_payment",  # still no arrow
        }

        result = parse_dag_workflow(dsl)

    assert result["success"] is False


# ─────────────────────────────────────────────
# 10. PARSER HARD FAIL — no partial acceptance
# ─────────────────────────────────────────────

def test_invalid_workflow_never_returns_success_true():
    """
    Core contract: success=True must NEVER appear with validation errors.
    """
    dsl = "@1: payment_due validate_payment"  # no arrow

    with patch("app.parsers.dag_orchestrator.cache_store") as mock_cache:
        mock_cache.__contains__ = MagicMock(return_value=False)
        mock_cache.__setitem__ = MagicMock()

        result = parse_dag_workflow(dsl)

    # Contract: if success is False, steps must be empty
    assert result["success"] is False
    assert result["steps"] == []
    assert result["validation"]["is_valid"] is False
    assert len(result["validation"]["errors"]) > 0


def test_valid_workflow_never_returns_errors():
    """
    Core contract: success=True must have empty errors list.
    """
    dsl = "@1: payment_due -> send_reminder"

    with patch("app.parsers.dag_orchestrator.cache_store") as mock_cache:
        mock_cache.__contains__ = MagicMock(return_value=False)
        mock_cache.__setitem__ = MagicMock()

        result = parse_dag_workflow(dsl)

    assert result["success"] is True
    assert result["validation"]["is_valid"] is True
    assert result["validation"]["errors"] == []
    assert len(result["steps"]) > 0


def test_unknown_dependency_is_hard_fail():
    steps = [
        {"id": "1", "trigger": "payment_due", "action": "send_reminder", "depends_on": ["99"]},
    ]
    result = validate_dag(steps)

    assert result["is_valid"] is False
    assert any("unknown_dependency" in e for e in result["errors"])


def test_empty_dag_is_hard_fail():
    result = validate_dag([])

    assert result["is_valid"] is False
    assert "dag_has_no_steps" in result["errors"]


def test_comments_and_empty_lines_ignored():
    dsl = """
# This is a comment
@1: payment_due -> send_reminder

# Another comment
@2 @depends(@1): payment_due -> escalate_case
"""
    result = parse_dsl(dsl)

    assert result["success"] is True
    assert len(result["steps"]) == 2


def test_whitespace_tolerance():
    dsl = "@1  :  payment_due  ->  send_reminder"

    result = parse_dsl(dsl)

    assert result["success"] is True
    assert result["steps"][0]["trigger"] == "payment_due"
    assert result["steps"][0]["action"] == "send_reminder"
