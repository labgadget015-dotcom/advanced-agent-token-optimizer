"""Example usage of the Advanced Agent with Token Budget Optimization.

This module demonstrates how to use the advanced autonomous agent
with various scenarios and configurations.
"""

import sys
from agent_core import AdvancedAgent, Task, TaskStatus, StrategyEngine, TokenBudget
from config import AgentConfig, STRATEGIES


def example_basic_usage():
    """Example: Basic agent usage."""
    print("=" * 60)
    print("Example 1: Basic Agent Usage")
    print("=" * 60)
    
    # Create agent with default configuration
    agent = AdvancedAgent(token_budget=200000)
    
    # Add tasks
    agent.add_task("Navigate to website", "Navigating to website")
    agent.add_task("Extract information", "Extracting information")
    agent.add_task("Process results", "Processing results")
    
    # Simulate task execution
    for task in agent.tasks:
        task.mark_in_progress()
        print(f"Executing: {task.content}")
        # Simulate token usage
        agent.token_budget.update(1000)
        task.mark_completed()
    
    # Generate report
    print(agent.generate_report())


def example_token_optimization():
    """Example: Token budget optimization."""
    print("\n" + "=" * 60)
    print("Example 2: Token Budget Optimization")
    print("=" * 60)
    
    # Create agent with smaller token budget
    agent = AdvancedAgent(token_budget=10000)
    
    # Simulate high token usage
    agent.token_budget.update(7500)  # 75% usage
    
    print(f"Token usage ratio: {agent.token_budget.usage_ratio:.1%}")
    print(f"Should optimize output: {agent.should_optimize_output()}")
    print(f"Budget status: {agent.token_budget.get_status()}")
    
    # Warning threshold
    if agent.token_budget.is_warning:
        print("⚠️  Warning: Token budget is running low!")
    
    # Critical threshold
    agent.token_budget.update(1600)  # Push to 91% usage
    if agent.token_budget.is_critical:
        print("🚨 Critical: Token budget is critically low!")


def example_multi_strategy():
    """Example: Multi-strategy approach."""
    print("\n" + "=" * 60)
    print("Example 3: Multi-Strategy Approach")
    print("=" * 60)
    
    agent = AdvancedAgent()
    task = agent.add_task("Find product", "Finding product")
    
    # Try different strategies
    strategies = StrategyEngine.get_search_strategies()
    
    for strategy in strategies:
        if not agent.should_try_alternative_strategy(task):
            print(f"Max attempts reached for task: {task.content}")
            break
        
        task.mark_in_progress()
        task.strategies_tried.append(strategy)
        print(f"Attempt {task.attempts}: Trying strategy '{strategy}'")
        
        # Simulate strategy execution
        agent.record_execution(strategy, {"task": task.content})
    
    print(f"\nStrategies tried: {', '.join(task.strategies_tried)}")
    print(f"Total attempts: {task.attempts}")


def example_error_handling():
    """Example: Error handling and validation."""
    print("\n" + "=" * 60)
    print("Example 4: Error Handling and Validation")
    print("=" * 60)
    
    agent = AdvancedAgent()
    
    # Simulate validation errors
    for i in range(7):
        should_continue = agent.handle_validation_error()
        print(f"Validation error {i+1}: Should continue = {should_continue}")
        
        if not should_continue:
            print(f"\n❌ Max validation errors ({agent.max_validation_errors}) reached!")
            print("Agent should terminate to avoid bad state.")
            break


def example_custom_configuration():
    """Example: Custom configuration."""
    print("\n" + "=" * 60)
    print("Example 5: Custom Configuration")
    print("=" * 60)
    
    # Create custom configuration
    config = AgentConfig(
        token_budget=150000,
        max_validation_errors=3,
        max_retry_attempts=3,
        enable_multi_strategy=True,
        enable_backtracking=True,
        log_level="DEBUG"
    )
    
    print("Custom Configuration:")
    for key, value in config.to_dict().items():
        print(f"  {key}: {value}")
    
    # Create agent with custom config
    agent = AdvancedAgent(token_budget=config.token_budget)
    agent.max_validation_errors = config.max_validation_errors
    
    print(f"\nAgent created with custom token budget: {agent.token_budget.total}")


def example_execution_history():
    """Example: Execution history tracking."""
    print("\n" + "=" * 60)
    print("Example 6: Execution History Tracking")
    print("=" * 60)
    
    agent = AdvancedAgent()
    
    # Record various actions
    actions = [
        ("navigate", {"url": "https://example.com"}),
        ("click", {"element": "button", "node_id": "123"}),
        ("form_fill", {"field": "search", "value": "query"}),
        ("scroll", {"direction": "down"}),
    ]
    
    for action, details in actions:
        agent.record_execution(action, details)
        agent.token_budget.update(500)
        print(f"Recorded: {action} - {details}")
    
    print(f"\nTotal execution steps: {len(agent.execution_history)}")
    print(f"Total token usage: {agent.token_budget.used}")


def example_task_management():
    """Example: Advanced task management."""
    print("\n" + "=" * 60)
    print("Example 7: Advanced Task Management")
    print("=" * 60)
    
    agent = AdvancedAgent()
    
    # Add various tasks
    tasks = [
        ("Initialize system", "Initializing system"),
        ("Load configuration", "Loading configuration"),
        ("Connect to service", "Connecting to service"),
        ("Execute workflow", "Executing workflow"),
        ("Generate report", "Generating report"),
    ]
    
    for content, active_form in tasks:
        agent.add_task(content, active_form)
    
    # Execute tasks
    for i, task in enumerate(agent.tasks):
        task.mark_in_progress()
        print(f"{i+1}. {task.active_form}...")
        
        # Simulate some failures
        if i == 2:  # Fail the third task
            task.mark_failed()
            print(f"   ❌ Failed: {task.content}")
        else:
            task.mark_completed()
            print(f"   ✓ Completed: {task.content}")
    
    # Get task summary
    summary = agent.get_task_summary()
    print(f"\nTask Summary:")
    for status, count in summary.items():
        print(f"  {status}: {count}")


def example_strategy_engine():
    """Example: Strategy engine usage."""
    print("\n" + "=" * 60)
    print("Example 8: Strategy Engine")
    print("=" * 60)
    
    print("Available Search Strategies:")
    for strategy in StrategyEngine.get_search_strategies():
        print(f"  - {strategy}")
    
    print("\nAvailable Navigation Strategies:")
    for strategy in StrategyEngine.get_navigation_strategies():
        print(f"  - {strategy}")
    
    print("\nBacktracking decisions:")
    for attempts in range(1, 6):
        should_backtrack = StrategyEngine.should_backtrack(attempts)
        print(f"  Attempts: {attempts} -> Backtrack: {should_backtrack}")


def main():
    """Run all examples."""
    print("\n" + "#" * 60)
    print("# Advanced Agent Token Optimizer - Examples")
    print("#" * 60)
    
    examples = [
        example_basic_usage,
        example_token_optimization,
        example_multi_strategy,
        example_error_handling,
        example_custom_configuration,
        example_execution_history,
        example_task_management,
        example_strategy_engine,
    ]
    
    for example in examples:
        try:
            example()
        except Exception as e:
            print(f"\n❌ Error running {example.__name__}: {e}")
    
    print("\n" + "#" * 60)
    print("# All examples completed!")
    print("#" * 60)


if __name__ == "__main__":
    main()
