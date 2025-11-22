# Advanced Agent Token Optimizer

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![GitHub Issues](https://img.shields.io/github/issues/labgadget015-dotcom/advanced-agent-token-optimizer)](https://github.com/labgadget015-dotcom/advanced-agent-token-optimizer/issues)

An advanced autonomous agent framework with sophisticated token budget optimization and strategic execution capabilities. This project implements a comprehensive agent system designed for persistent, efficient, and strategic web automation tasks.

## 🌟 Key Features

### Token Budget Management
- **Dynamic Token Tracking**: Real-time monitoring of token usage with configurable thresholds
- **Automatic Optimization**: Adaptive output optimization based on budget constraints
- **Warning & Critical Alerts**: Multi-level alerting system for budget management
- **Budget Analytics**: Comprehensive usage ratio and remaining token calculations

### Strategic Execution
- **Multi-Strategy Approach**: Multiple strategies for search, navigation, and interaction
- **Persistent Retry Logic**: Automatic retry with alternative strategies on failure
- **Backtracking Capability**: Smart backtracking when strategies fail repeatedly
- **Validation Error Handling**: Automatic recovery from validation errors with limits

### Task Management
- **Task Status Tracking**: Comprehensive task lifecycle management (pending, in-progress, completed, failed)
- **Execution History**: Detailed logging of all actions and decisions
- **Task Summaries**: Real-time reporting on task completion status
- **Priority Handling**: Support for task prioritization and scheduling

### Advanced Capabilities
- **Context-Aware Interactions**: Smart page element interaction with node ID validation
- **Security-First Design**: Built-in protections against untrusted web content
- **Configurable Behavior**: Extensive configuration options via environment variables or code
- **Comprehensive Logging**: Detailed execution logs for debugging and analysis

## 📋 Installation

```bash
# Clone the repository
git clone https://github.com/labgadget015-dotcom/advanced-agent-token-optimizer.git
cd advanced-agent-token-optimizer

# Install dependencies (when requirements.txt is added)
pip install -r requirements.txt
```

## 🚀 Quick Start

### Basic Usage

```python
from agent_core import AdvancedAgent

# Create an agent with default settings
agent = AdvancedAgent(token_budget=200000)

# Add tasks
agent.add_task("Navigate to website", "Navigating to website")
agent.add_task("Extract data", "Extracting data")

# Execute tasks
for task in agent.tasks:
    task.mark_in_progress()
    # Your execution logic here
    task.mark_completed()

# Generate report
print(agent.generate_report())
```

### Custom Configuration

```python
from agent_core import AdvancedAgent
from config import AgentConfig

# Create custom configuration
config = AgentConfig(
    token_budget=150000,
    max_validation_errors=3,
    max_retry_attempts=3,
    enable_multi_strategy=True,
    enable_backtracking=True
)

# Create agent with custom config
agent = AdvancedAgent(token_budget=config.token_budget)
agent.max_validation_errors = config.max_validation_errors
```

## 📖 Documentation

### Core Components

#### TokenBudget
Manages token usage with configurable warning and critical thresholds:

```python
budget = TokenBudget(total=200000)
budget.update(1000)  # Add 1000 tokens used
print(budget.get_status())  # Get current status
print(f"Remaining: {budget.remaining}")
```

#### Task
Represents a single unit of work with status tracking:

```python
task = Task(content="Execute action", active_form="Executing action")
task.mark_in_progress()
task.strategies_tried.append("direct_approach")
task.mark_completed()
```

#### AdvancedAgent
The main agent class orchestrating all operations:

```python
agent = AdvancedAgent(token_budget=200000)
agent.add_task("Task description", "Task active form")
agent.record_execution("action", {"details": "info"})
report = agent.generate_report()
```

#### StrategyEngine
Provides various strategies for different operations:

```python
from agent_core import StrategyEngine

search_strategies = StrategyEngine.get_search_strategies()
nav_strategies = StrategyEngine.get_navigation_strategies()
should_backtrack = StrategyEngine.should_backtrack(attempts=3)
```

### Configuration Options

The `config.py` module provides extensive configuration:

- **Token Budget**: `DEFAULT_TOKEN_BUDGET = 200000`
- **Thresholds**: `TOKEN_WARNING_THRESHOLD = 0.7`, `TOKEN_CRITICAL_THRESHOLD = 0.9`
- **Error Handling**: `MAX_VALIDATION_ERRORS = 5`, `MAX_RETRY_ATTEMPTS = 5`
- **Output**: `MAX_OUTPUT_SENTENCES = 2`, `STATUS_BAR_WIDTH = 80`
- **Timing**: `WAIT_DURATION_SHORT/MEDIUM/LONG`

### Environment Variables

```bash
export AGENT_TOKEN_BUDGET=150000
export AGENT_MAX_ERRORS=3
export AGENT_LOG_LEVEL=DEBUG
```

Then load configuration:

```python
from config import AgentConfig

config = AgentConfig.from_env()
```

## 🧪 Examples

Run the comprehensive examples:

```bash
python examples.py
```

The examples cover:
1. Basic agent usage
2. Token budget optimization
3. Multi-strategy approach
4. Error handling
5. Custom configuration
6. Execution history tracking
7. Task management
8. Strategy engine usage

## 🏗️ Architecture

```
advanced-agent-token-optimizer/
├── agent_core.py      # Core agent implementation
├── config.py          # Configuration settings
├── examples.py        # Usage examples
├── README.md          # This file
└── .gitignore        # Git ignore rules
```

## 🔧 Key Design Patterns

### Persistent Execution
- Never gives up at first obstacle
- Tries multiple strategies before failing
- Automatically backtracks when needed

### Token Optimization
- Monitors token usage in real-time
- Adapts output verbosity based on budget
- Provides early warnings for budget constraints

### Security First
- Never trusts web content
- No authentication attempts (except LMS portals)
- Validates all node IDs before interaction

### Strategic Planning
- Multiple strategies per operation type
- Automatic strategy rotation on failure
- Learning from execution history

## 📊 Monitoring & Reporting

### Real-time Monitoring
```python
# Check token usage
print(f"Token usage: {agent.token_budget.usage_ratio:.1%}")
print(f"Should optimize: {agent.should_optimize_output()}")

# Check task status
summary = agent.get_task_summary()
print(f"Completed: {summary['completed']}/{summary['total']}")

# Check validation errors
print(f"Errors: {agent.validation_errors}/{agent.max_validation_errors}")
```

### Final Report
```python
report = agent.generate_report()
print(report)
# Output:
# === Agent Execution Report ===
# Token Budget: OK: 150000 tokens remaining
# Tasks: 5/5 completed
# Validation Errors: 0/5
# Execution Steps: 15
```

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Inspired by advanced autonomous agent architectures
- Built with focus on token budget optimization strategies
- Designed for persistent, strategic task execution

## 📧 Contact

Project Link: [https://github.com/labgadget015-dotcom/advanced-agent-token-optimizer](https://github.com/labgadget015-dotcom/advanced-agent-token-optimizer)

## 🗺️ Roadmap

- [ ] Add unit tests
- [ ] Implement async execution support
- [ ] Add more strategy types
- [ ] Create web dashboard for monitoring
- [ ] Add plugin system for extensibility
- [ ] Implement distributed agent coordination
- [ ] Add machine learning for strategy selection

---

**Built with ❤️ for advanced autonomous agent development**
