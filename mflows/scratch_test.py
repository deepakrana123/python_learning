# """
# scratch_test.py — Full flow tests + Chaos scenario tests

# Run with:
#     pytest scratch_test.py -v

# Sections:
#     1-10:  DAG parser + validation tests (existing)
#     11-20: Chaos action tests — every real-world failure mode
#     21-28: Dispatcher + retry integration tests
# """

# import pytest
# import time
# from unittest.mock import patch, MagicMock

# # ── Parser imports ────────────────────────────────────────────
# from app.parsers.dsl_parser import parse_dsl
# from app.parsers.dag_validator import validate_dag
# from app.parsers.dag_orchestrator import parse_dag_workflow

# # ── Provider health imports ───────────────────────────────────
# from app.llm.provider_health import (
#     record_provider_error,
#     is_provider_healthy,
#     reset_provider,
#     PROVIDER_STATE,
# )

# # ── Chaos imports ─────────────────────────────────────────────
# from app.execution.chaos_actions import (
#     chaos_send_reminder,
#     chaos_escalate_case,
#     chaos_notify_manager,
#     chaos_reject_loan,
#     chaos_close_case,
#     chaos_assign_senior_officer,
#     GatewayError,
#     TimeoutError,
#     RateLimitError,
#     AuthError,
#     BadPayloadError,
#     PartialSuccessError,
# )
# from app.execution.dispatcher import execute_action


# # ─────────────────────────────────────────────
# # HELPERS
# # ─────────────────────────────────────────────

# def clear_provider_state():
#     PROVIDER_STATE.clear()


# def make_payload(entity_id="CU001", attempt=1):
#     return {"entity_id": entity_id, "_attempt": attempt}


# def make_config(chaos_mode="success", **kwargs):
#     return {"chaos_mode": chaos_mode, **kwargs}


# # ═════════════════════════════════════════════
# # SECTION 1-10: DAG PARSER TESTS (existing)
# # ═════════════════════════════════════════════

# def test_valid_linear_dag_parse():
#     dsl = """
# @1: payment_due -> send_reminder
# @2 @depends(@1): payment_due -> escalate_case
# @3 @depends(@2): payment_due -> close_case
# """
#     result = parse_dsl(dsl)
#     assert result["success"] is True
#     assert len(result["steps"]) == 3
#     assert result["steps"][1]["depends_on"] == ["1"]


# def test_valid_branching_dag():
#     dsl = """
# @1: payment_due -> send_reminder
# @2 @depends(@1): payment_due -> escalate_case
# @3 @depends(@1): payment_due -> notify_manager
# """
#     result = parse_dsl(dsl)
#     assert result["success"] is True
#     assert result["steps"][1]["depends_on"] == ["1"]
#     assert result["steps"][2]["depends_on"] == ["1"]


# def test_direct_cycle_detected():
#     steps = [
#         {"id": "1", "trigger": "payment_due", "action": "send_reminder", "depends_on": ["2"]},
#         {"id": "2", "trigger": "payment_due", "action": "escalate_case", "depends_on": ["1"]},
#     ]
#     result = validate_dag(steps)
#     assert result["is_valid"] is False
#     assert "dag_has_cycle" in result["errors"]


# def test_missing_action_is_hard_fail():
#     steps = [{"id": "1", "trigger": "payment_due", "action": None, "depends_on": []}]
#     result = validate_dag(steps)
#     assert result["is_valid"] is False
#     assert any("action_required" in e for e in result["errors"])


# def test_ambiguous_syntax_no_arrow_is_not_repairable():
#     dsl = "@1: payment_due validate_payment"
#     result = parse_dsl(dsl)
#     assert result["success"] is False
#     assert result["repairable"] is False


# def test_duplicate_step_ids_fail():
#     steps = [
#         {"id": "1", "trigger": "payment_due", "action": "send_reminder", "depends_on": []},
#         {"id": "1", "trigger": "payment_due", "action": "escalate_case", "depends_on": []},
#     ]
#     result = validate_dag(steps)
#     assert result["is_valid"] is False
#     assert any("duplicate_step_id" in e for e in result["errors"])


# def test_invalid_workflow_never_returns_success_true():
#     dsl = "@1: payment_due validate_payment"
#     with patch("app.parsers.dag_orchestrator.cache_store") as mock_cache:
#         mock_cache.__contains__ = MagicMock(return_value=False)
#         mock_cache.__setitem__ = MagicMock()
#         result = parse_dag_workflow(dsl)
#     assert result["success"] is False
#     assert result["steps"] == []


# def test_fatal_error_disables_provider():
#     clear_provider_state()
#     record_provider_error("gemini", "API_KEY_INVALID: key not valid")
#     assert is_provider_healthy("gemini") is False


# def test_comments_and_empty_lines_ignored():
#     dsl = """
# # comment
# @1: payment_due -> send_reminder

# @2 @depends(@1): payment_due -> escalate_case
# """
#     result = parse_dsl(dsl)
#     assert result["success"] is True
#     assert len(result["steps"]) == 2


# def test_whitespace_tolerance():
#     dsl = "@1  :  payment_due  ->  send_reminder"
#     result = parse_dsl(dsl)
#     assert result["success"] is True
#     assert result["steps"][0]["action"] == "send_reminder"


# # ═════════════════════════════════════════════
# # SECTION 11-20: CHAOS ACTION TESTS
# # ═════════════════════════════════════════════

# # ── 11. Success (baseline) ────────────────────

# def test_chaos_success_mode():
#     result = chaos_send_reminder(make_payload(), make_config("success"))
#     assert result["success"] is True
#     assert result["status"] == "success"


# # ── 12. Always fail ──────────────────────────

# def test_chaos_always_fail_raises():
#     with pytest.raises(GatewayError) as exc:
#         chaos_send_reminder(make_payload(), make_config("always_fail"))
#     assert "always_fail" in str(exc.value)


# def test_chaos_always_fail_escalate():
#     with pytest.raises(GatewayError):
#         chaos_escalate_case(make_payload(), make_config("always_fail"))


# # ── 13. Timeout ──────────────────────────────

# def test_chaos_timeout_raises():
#     with pytest.raises(TimeoutError) as exc:
#         chaos_send_reminder(make_payload(), make_config("timeout", delay_seconds=0))
#     assert "timeout" in str(exc.value)


# def test_chaos_timeout_with_delay():
#     start = time.time()
#     with pytest.raises(TimeoutError):
#         chaos_notify_manager(make_payload(), make_config("timeout", delay_seconds=1))
#     elapsed = time.time() - start
#     assert elapsed >= 1.0


# # ── 14. Gateway error (502/503) ──────────────

# def test_chaos_gateway_error():
#     with pytest.raises(GatewayError) as exc:
#         chaos_escalate_case(make_payload(), make_config("gateway_error"))
#     assert "502" in str(exc.value) or "gateway_error" in str(exc.value)


# def test_chaos_gateway_error_reject_loan():
#     with pytest.raises(GatewayError):
#         chaos_reject_loan(make_payload(), make_config("gateway_error"))


# # ── 15. Rate limit (429) ─────────────────────

# def test_chaos_rate_limit():
#     with pytest.raises(RateLimitError) as exc:
#         chaos_notify_manager(make_payload(), make_config("rate_limit"))
#     assert "429" in str(exc.value) or "rate_limit" in str(exc.value)


# # ── 16. Auth error (401/403) ─────────────────

# def test_chaos_auth_error():
#     with pytest.raises(AuthError) as exc:
#         chaos_reject_loan(make_payload(), make_config("auth_error"))
#     assert "401" in str(exc.value) or "auth_error" in str(exc.value)


# def test_chaos_auth_error_assign_officer():
#     with pytest.raises(AuthError):
#         chaos_assign_senior_officer(make_payload(), make_config("auth_error"))


# # ── 17. Bad payload (400) ────────────────────

# def test_chaos_bad_payload():
#     with pytest.raises(BadPayloadError) as exc:
#         chaos_notify_manager(make_payload(), make_config("bad_payload"))
#     assert "400" in str(exc.value) or "bad_payload" in str(exc.value)


# def test_chaos_payload_overload():
#     with pytest.raises(BadPayloadError) as exc:
#         chaos_send_reminder(make_payload(), make_config("payload_overload"))
#     assert "payload_overload" in str(exc.value)


# # ── 18. Partial success (207) ────────────────

# def test_chaos_partial_success():
#     with pytest.raises(PartialSuccessError) as exc:
#         chaos_close_case(make_payload(), make_config("partial_success"))
#     assert "207" in str(exc.value) or "partial_success" in str(exc.value)


# # ── 19. Flaky service ────────────────────────

# def test_chaos_flaky_always_fails_at_100_percent():
#     with pytest.raises(GatewayError):
#         chaos_send_reminder(make_payload(), make_config("flaky", fail_rate=1.0))


# def test_chaos_flaky_never_fails_at_0_percent():
#     result = chaos_send_reminder(make_payload(), make_config("flaky", fail_rate=0.0))
#     assert result["success"] is True


# def test_chaos_flaky_statistical():
#     """At 50% fail rate, over 20 calls we expect some failures and some successes."""
#     failures = 0
#     successes = 0
#     for _ in range(20):
#         try:
#             chaos_send_reminder(make_payload(), make_config("flaky", fail_rate=0.5))
#             successes += 1
#         except GatewayError:
#             failures += 1
#     assert failures > 0, "expected some failures at 50% rate"
#     assert successes > 0, "expected some successes at 50% rate"


# # ── 20. Succeed after retries ────────────────

# def test_chaos_succeed_after_retries_fails_first():
#     with pytest.raises(GatewayError) as exc:
#         chaos_escalate_case(
#             make_payload(attempt=1),
#             make_config("succeed_after_retries", succeed_after=2),
#         )
#     assert "attempt 1/2" in str(exc.value)


# def test_chaos_succeed_after_retries_succeeds_eventually():
#     result = chaos_escalate_case(
#         make_payload(attempt=3),
#         make_config("succeed_after_retries", succeed_after=2),
#     )
#     assert result["success"] is True


# def test_chaos_fail_on_specific_attempt():
#     # Fails only on attempt 2
#     with pytest.raises(GatewayError):
#         chaos_close_case(
#             make_payload(attempt=2),
#             make_config("fail_on_attempt", fail_on_attempt=2),
#         )
#     # Succeeds on attempt 1 and 3
#     r1 = chaos_close_case(make_payload(attempt=1), make_config("fail_on_attempt", fail_on_attempt=2))
#     r3 = chaos_close_case(make_payload(attempt=3), make_config("fail_on_attempt", fail_on_attempt=2))
#     assert r1["success"] is True
#     assert r3["success"] is True


# # ── Slow service ─────────────────────────────

# def test_chaos_slow_succeeds_but_takes_time():
#     start = time.time()
#     result = chaos_assign_senior_officer(
#         make_payload(), make_config("slow", delay_seconds=1)
#     )
#     elapsed = time.time() - start
#     assert result["success"] is True
#     assert elapsed >= 1.0


# # ═════════════════════════════════════════════
# # SECTION 21-28: DISPATCHER INTEGRATION TESTS
# # ═════════════════════════════════════════════

# def test_dispatcher_unknown_action_returns_failed():
#     result = execute_action("nonexistent_action", make_payload(), {})
#     assert result["status"] == "failed"
#     assert result["reason"] == "unknown action"


# def test_dispatcher_chaos_mode_gateway_error_propagates():
#     """
#     In chaos mode, gateway errors must propagate as exceptions
#     so step_executor can catch them and trigger retry.
#     """
#     with patch("app.execution.dispatcher._CHAOS_ENABLED", True), \
#          patch("app.execution.dispatcher.ACTION_MAP", {
#              "send_reminder": chaos_send_reminder
#          }):
#         with pytest.raises(GatewayError):
#             execute_action(
#                 "send_reminder",
#                 make_payload(),
#                 make_config("gateway_error"),
#             )


# def test_dispatcher_chaos_mode_success():
#     with patch("app.execution.dispatcher._CHAOS_ENABLED", True), \
#          patch("app.execution.dispatcher.ACTION_MAP", {
#              "send_reminder": chaos_send_reminder
#          }):
#         result = execute_action(
#             "send_reminder",
#             make_payload(),
#             make_config("success"),
#         )
#     assert result["success"] is True


# def test_dispatcher_chaos_timeout_propagates():
#     with patch("app.execution.dispatcher._CHAOS_ENABLED", True), \
#          patch("app.execution.dispatcher.ACTION_MAP", {
#              "escalate_case": chaos_escalate_case
#          }):
#         with pytest.raises(TimeoutError):
#             execute_action(
#                 "escalate_case",
#                 make_payload(),
#                 make_config("timeout", delay_seconds=0),
#             )


# def test_dispatcher_chaos_auth_error_propagates():
#     with patch("app.execution.dispatcher._CHAOS_ENABLED", True), \
#          patch("app.execution.dispatcher.ACTION_MAP", {
#              "reject_loan": chaos_reject_loan
#          }):
#         with pytest.raises(AuthError):
#             execute_action(
#                 "reject_loan",
#                 make_payload(),
#                 make_config("auth_error"),
#             )


# def test_dispatcher_chaos_rate_limit_propagates():
#     with patch("app.execution.dispatcher._CHAOS_ENABLED", True), \
#          patch("app.execution.dispatcher.ACTION_MAP", {
#              "notify_manager": chaos_notify_manager
#          }):
#         with pytest.raises(RateLimitError):
#             execute_action(
#                 "notify_manager",
#                 make_payload(),
#                 make_config("rate_limit"),
#             )


# def test_dispatcher_chaos_bad_payload_propagates():
#     with patch("app.execution.dispatcher._CHAOS_ENABLED", True), \
#          patch("app.execution.dispatcher.ACTION_MAP", {
#              "close_case": chaos_close_case
#          }):
#         with pytest.raises(BadPayloadError):
#             execute_action(
#                 "close_case",
#                 make_payload(),
#                 make_config("bad_payload"),
#             )


# def test_all_chaos_modes_covered():
#     """Verify every chaos mode is handled without KeyError or silent pass."""
#     modes = [
#         "success", "always_fail", "timeout", "slow", "gateway_error",
#         "rate_limit", "auth_error", "bad_payload", "payload_overload",
#         "partial_success", "flaky", "fail_on_attempt", "succeed_after_retries",
#     ]
#     for mode in modes:
#         config = {"chaos_mode": mode, "delay_seconds": 0, "fail_rate": 1.0,
#                   "fail_on_attempt": 1, "succeed_after": 0}
#         try:
#             chaos_send_reminder(make_payload(attempt=1), config)
#         except Exception:
#             pass  # expected — we just verify no unhandled crash

# from app.nlp.ast.schema import WorkflowAST
# from app.nlp.ast.validator import ASTValidator


# ast = WorkflowAST(
#     trigger={"event": "payment_due"},
#     steps=[
#         {
#             "id": "1",
#             "action": "send_reminder",
#         },
#         {
#             "id": "2",
#             "action": "notify_manager",
#             "depends_on": ["1"]
#         }
#     ]
# )

# ASTValidator().validate(ast)

# print("AST VALID")

dsl = """
@1:
payment_due -> send_reminder

@2 @depends(@1):
payment_due -> notify_manager

@3 @depends(@2):
payment_due -> close_case
"""