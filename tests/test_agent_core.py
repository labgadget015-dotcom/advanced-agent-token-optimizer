"""Unit tests for agent_core module."""
import pytest
from agent_core import (
    AdvancedAgent,
    Task,
    TaskStatus,
    TokenBudget,
    StrategyEngine,
)


class TestTokenBudget:
    """Tests for TokenBudget class."""

    def test_token_budget_initialization(self):
        budget = TokenBudget(total=10000)
        assert budget.total == 10000
        assert budget.used == 0
        assert budget.remaining == 10000

    def test_token_budget_update(self):
        budget = TokenBudget(total=10000)
        budget.update(1000)
        assert budget.used == 1000
        assert budget.remaining == 9000

    def test_token_budget_warning(self):
        budget = TokenBudget(total=10000)
        budget.update(7500)
        assert budget.is_warning is True
        assert budget.is_critical is False

    def test_token_budget_critical(self):
        budget = TokenBudget(total=10000)
        budget.update(9500)
        assert budget.is_warning is True
        assert budget.is_critical is True


class TestTask:
    """Tests for Task class."""

    def test_task_initialization(self):
        task = Task(content="Test task", active_form="Testing")
        assert task.content == "Test task"
        assert task.status == TaskStatus.PENDING
        assert task.attempts == 0

    def test_task_mark_in_progress(self):
        task = Task(content="Test task")
        task.mark_in_progress()
        assert task.status == TaskStatus.IN_PROGRESS
        assert task.attempts == 1

    def test_task_mark_completed(self):
        task = Task(content="Test task")
        task.mark_completed()
        assert task.status == TaskStatus.COMPLETED

    def test_task_mark_failed(self):
        task = Task(content="Test task")
        task.mark_failed()
        assert task.status == TaskStatus.FAILED


class TestAdvancedAgent:
    """Tests for AdvancedAgent class."""

    def test_agent_initialization(self):
        agent = AdvancedAgent(token_budget=50000)
        assert agent.token_budget.total == 50000
        assert len(agent.tasks) == 0

    def test_add_task(self):
        agent = AdvancedAgent()
        task = agent.add_task("Test task", "Testing")
        assert len(agent.tasks) == 1
        assert task.content == "Test task"

    def test_get_pending_tasks(self):
        agent = AdvancedAgent()
        agent.add_task("Task 1")
        agent.add_task("Task 2")
        agent.tasks[0].mark_completed()
        pending = agent.get_pending_tasks()
        assert len(pending) == 1

    def test_handle_validation_error(self):
        agent = AdvancedAgent()
        agent.max_validation_errors = 3
        assert agent.handle_validation_error() is True
        assert agent.handle_validation_error() is True
        assert agent.handle_validation_error() is False

    def test_should_optimize_output(self):
        agent = AdvancedAgent(token_budget=10000)
        assert agent.should_optimize_output() is False
        agent.token_budget.update(7500)
        assert agent.should_optimize_output() is True

    def test_record_execution(self):
        agent = AdvancedAgent()
        agent.record_execution("test_action", {"key": "value"})
        assert len(agent.execution_history) == 1
        assert agent.execution_history[0]["action"] == "test_action"


class TestStrategyEngine:
    """Tests for StrategyEngine class."""

    def test_get_search_strategies(self):
        strategies = StrategyEngine.get_search_strategies()
        assert len(strategies) > 0
        assert "direct_search" in strategies

    def test_get_navigation_strategies(self):
        strategies = StrategyEngine.get_navigation_strategies()
        assert len(strategies) > 0
        assert "direct_link" in strategies

    def test_should_backtrack(self):
        assert StrategyEngine.should_backtrack(1) is False
        assert StrategyEngine.should_backtrack(2) is False
        assert StrategyEngine.should_backtrack(3) is True
