"""Advanced Agent with Token Budget Optimization.

This module implements an autonomous agent with:
- Token budget tracking and optimization
- Strategic execution with persistence
- Multi-strategy approach to task completion
- Context-aware page interaction
"""

import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum


class TaskStatus(Enum):
    """Status of a task."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class TokenBudget:
    """Token budget tracker."""
    total: int
    used: int = 0
    threshold_warning: float = 0.7
    threshold_critical: float = 0.9
    
    @property
    def remaining(self) -> int:
        return self.total - self.used
    
    @property
    def usage_ratio(self) -> float:
        return self.used / self.total if self.total > 0 else 0.0
    
    @property
    def is_warning(self) -> bool:
        return self.usage_ratio >= self.threshold_warning
    
    @property
    def is_critical(self) -> bool:
        return self.usage_ratio >= self.threshold_critical
    
    def update(self, tokens: int) -> None:
        """Update token usage."""
        self.used += tokens
    
    def get_status(self) -> str:
        """Get budget status message."""
        if self.is_critical:
            return f"CRITICAL: {self.remaining} tokens remaining"
        elif self.is_warning:
            return f"WARNING: {self.remaining} tokens remaining"
        return f"OK: {self.remaining} tokens remaining"


@dataclass
class Task:
    """Task representation."""
    content: str
    status: TaskStatus = TaskStatus.PENDING
    active_form: str = ""
    attempts: int = 0
    strategies_tried: List[str] = field(default_factory=list)
    
    def mark_in_progress(self) -> None:
        self.status = TaskStatus.IN_PROGRESS
        self.attempts += 1
    
    def mark_completed(self) -> None:
        self.status = TaskStatus.COMPLETED
    
    def mark_failed(self) -> None:
        self.status = TaskStatus.FAILED


class AdvancedAgent:
    """Advanced autonomous agent with token optimization."""
    
    def __init__(self, token_budget: int = 200000):
        self.token_budget = TokenBudget(total=token_budget)
        self.tasks: List[Task] = []
        self.validation_errors = 0
        self.max_validation_errors = 5
        self.page_context: Dict[str, Any] = {}
        self.execution_history: List[Dict] = []
    
    def should_optimize_output(self) -> bool:
        """Determine if output should be optimized based on token budget."""
        return self.token_budget.is_warning
    
    def add_task(self, content: str, active_form: str = "") -> Task:
        """Add a new task to the agent."""
        task = Task(content=content, active_form=active_form)
        self.tasks.append(task)
        return task
    
    def get_pending_tasks(self) -> List[Task]:
        """Get all pending tasks."""
        return [t for t in self.tasks if t.status == TaskStatus.PENDING]
    
    def get_task_summary(self) -> Dict[str, int]:
        """Get summary of task statuses."""
        return {
            "total": len(self.tasks),
            "pending": len([t for t in self.tasks if t.status == TaskStatus.PENDING]),
            "in_progress": len([t for t in self.tasks if t.status == TaskStatus.IN_PROGRESS]),
            "completed": len([t for t in self.tasks if t.status == TaskStatus.COMPLETED]),
            "failed": len([t for t in self.tasks if t.status == TaskStatus.FAILED]),
        }
    
    def record_execution(self, action: str, details: Dict[str, Any]) -> None:
        """Record execution step for analysis."""
        self.execution_history.append({
            "timestamp": time.time(),
            "action": action,
            "details": details,
            "token_usage": self.token_budget.used,
        })
    
    def handle_validation_error(self) -> bool:
        """Handle validation error. Returns True if should continue, False if should terminate."""
        self.validation_errors += 1
        if self.validation_errors >= self.max_validation_errors:
            return False
        return True
    
    def should_try_alternative_strategy(self, task: Task) -> bool:
        """Determine if alternative strategy should be tried."""
        # Try up to 5 different strategies before giving up
        return task.attempts < 5
    
    def generate_report(self) -> str:
        """Generate execution report."""
        task_summary = self.get_task_summary()
        return f"""
=== Agent Execution Report ===
Token Budget: {self.token_budget.get_status()}
Tasks: {task_summary['completed']}/{task_summary['total']} completed
Validation Errors: {self.validation_errors}/{self.max_validation_errors}
Execution Steps: {len(self.execution_history)}
"""


class StrategyEngine:
    """Strategy engine for multi-approach problem solving."""
    
    @staticmethod
    def get_search_strategies() -> List[str]:
        """Get available search strategies."""
        return [
            "direct_search",
            "filtered_search",
            "category_navigation",
            "advanced_filters",
            "alternative_keywords",
        ]
    
    @staticmethod
    def get_navigation_strategies() -> List[str]:
        """Get available navigation strategies."""
        return [
            "direct_link",
            "menu_navigation",
            "breadcrumb_path",
            "search_and_click",
            "url_manipulation",
        ]
    
    @staticmethod
    def should_backtrack(attempts: int) -> bool:
        """Determine if backtracking is needed."""
        return attempts >= 3


if __name__ == "__main__":
    # Example usage
    agent = AdvancedAgent(token_budget=200000)
    
    # Add tasks
    agent.add_task("Navigate to GitHub", "Navigating to GitHub")
    agent.add_task("Create repository", "Creating repository")
    agent.add_task("Add implementation files", "Adding implementation files")
    
    print(agent.generate_report())
