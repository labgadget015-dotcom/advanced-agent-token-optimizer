"""Configuration for Advanced Agent.

This module contains configuration settings for the advanced autonomous agent
with token budget optimization.
"""

import os
from typing import Dict, Any


# Token Budget Configuration
DEFAULT_TOKEN_BUDGET = 200000
TOKEN_WARNING_THRESHOLD = 0.7  # Warn at 70% usage
TOKEN_CRITICAL_THRESHOLD = 0.9  # Critical at 90% usage

# Validation and Error Handling
MAX_VALIDATION_ERRORS = 5
MAX_RETRY_ATTEMPTS = 5
BACKTRACK_THRESHOLD = 3

# Output Configuration
MAX_OUTPUT_SENTENCES = 2
STATUS_BAR_WIDTH = 80

# Task Management
DEFAULT_TASK_TIMEOUT = 300  # seconds
TASK_PRIORITY_LEVELS = ["low", "medium", "high", "critical"]

# Strategy Configuration
STRATEGIES = {
    "search": [
        "direct_search",
        "filtered_search",
        "category_navigation",
        "advanced_filters",
        "alternative_keywords",
    ],
    "navigation": [
        "direct_link",
        "menu_navigation",
        "breadcrumb_path",
        "search_and_click",
        "url_manipulation",
    ],
    "interaction": [
        "click",
        "form_fill",
        "search",
        "scroll",
        "wait",
        "navigate",
    ],
}

# Page Interaction Settings
WAIT_DURATION_SHORT = 2  # seconds
WAIT_DURATION_MEDIUM = 5  # seconds
WAIT_DURATION_LONG = 10  # seconds

SCROLL_ATTEMPTS = 3
SCROLL_DIRECTION = ["down", "up"]

# Security Settings
TRUST_WEB_CONTENT = False
ALLOW_AUTHENTICATION = False  # Except for LMS portals
LMS_DOMAINS = [
    "canvas",
    "moodle",
    "blackboard",
    "brightspace",
    "d2l",
    "sakai",
    "schoology",
    "edx",
    "powerschool",
    "classroom.google.com",
]

# Logging and Reporting
LOG_LEVEL = "INFO"
DETAILED_EXECUTION_LOG = True
GENERATE_REPORT_ON_COMPLETION = True

# Context Management
MAX_CONTEXT_PAGES = 10
CONTEXT_COMPRESSION_ENABLED = True

# Advanced Features
ENABLE_MULTI_STRATEGY = True
ENABLE_BACKTRACKING = True
ENABLE_ADAPTIVE_OPTIMIZATION = True


class AgentConfig:
    """Agent configuration manager."""
    
    def __init__(self, **kwargs):
        self.token_budget = kwargs.get("token_budget", DEFAULT_TOKEN_BUDGET)
        self.max_validation_errors = kwargs.get("max_validation_errors", MAX_VALIDATION_ERRORS)
        self.max_retry_attempts = kwargs.get("max_retry_attempts", MAX_RETRY_ATTEMPTS)
        self.enable_multi_strategy = kwargs.get("enable_multi_strategy", ENABLE_MULTI_STRATEGY)
        self.enable_backtracking = kwargs.get("enable_backtracking", ENABLE_BACKTRACKING)
        self.log_level = kwargs.get("log_level", LOG_LEVEL)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        return {
            "token_budget": self.token_budget,
            "max_validation_errors": self.max_validation_errors,
            "max_retry_attempts": self.max_retry_attempts,
            "enable_multi_strategy": self.enable_multi_strategy,
            "enable_backtracking": self.enable_backtracking,
            "log_level": self.log_level,
        }
    
    @classmethod
    def from_env(cls) -> "AgentConfig":
        """Create configuration from environment variables."""
        return cls(
            token_budget=int(os.getenv("AGENT_TOKEN_BUDGET", DEFAULT_TOKEN_BUDGET)),
            max_validation_errors=int(os.getenv("AGENT_MAX_ERRORS", MAX_VALIDATION_ERRORS)),
            log_level=os.getenv("AGENT_LOG_LEVEL", LOG_LEVEL),
        )


if __name__ == "__main__":
    # Example usage
    config = AgentConfig()
    print("Agent Configuration:")
    for key, value in config.to_dict().items():
        print(f"  {key}: {value}")
