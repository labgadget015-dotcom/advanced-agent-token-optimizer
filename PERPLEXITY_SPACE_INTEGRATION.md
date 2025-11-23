# Perplexity Space Integration Guide

## Overview

This guide explains how to deploy and integrate the Advanced Agent Token Optimizer into a Perplexity Space for maximum reliability, accuracy, safety, and adaptability.

## Architecture

### Components

1. **EnhancedAgent** (`agent_enhanced.py`)
   - Core autonomous agent with all optimizations
   - Plugin system for extensibility
   - Watchdog for health monitoring
   - Security validation and sandboxing
   - Real-time telemetry and monitoring

2. **AsyncExecutor** (`async_executor.py`)
   - Parallel task execution
   - Distributed coordination
   - Automatic retries and timeouts
   - High-availability architecture

3. **MLStrategySelector** (`ml_strategy_selector.py`)
   - Machine learning-driven strategy selection
   - Adaptive learning from execution history
   - Performance-based fallback

## Quick Start

### 1. Installation

```bash
git clone https://github.com/labgadget015-dotcom/advanced-agent-token-optimizer.git
cd advanced-agent-token-optimizer
pip install -r requirements.txt
```

### 2. Basic Usage

```python
from agent_enhanced import EnhancedAgent

# Initialize agent
agent = EnhancedAgent(
    token_budget=200000,
    enable_plugins=True,
    enable_watchdog=True,
    enable_telemetry=True
)

# Execute task
result = agent.execute_task("your_task_here")

# Get status
status = agent.get_status()
print(status)

# Shutdown gracefully
agent.shutdown()
```

### 3. Async Execution

```python
import asyncio
from async_executor import AsyncExecutor, AsyncTask

async def main():
    executor = AsyncExecutor(max_concurrent_tasks=10)
    
    tasks = [
        AsyncTask(
            id="task_1",
            coroutine=your_async_function(),
            priority=1,
            timeout=30.0
        )
    ]
    
    results = await executor.execute_parallel(tasks)
    executor.shutdown()

asyncio.run(main())
```

### 4. ML Strategy Selection

```python
from ml_strategy_selector import MLStrategySelector, ExecutionContext

strategies = ["direct_search", "filtered_search", "advanced_filters"]
selector = MLStrategySelector(strategies)

context = ExecutionContext(
    task_type="search",
    complexity=0.5,
    time_constraint=30.0,
    token_budget_remaining=0.7,
    validation_errors=0
)

strategy = selector.select_strategy(context)
selector.record_outcome(strategy, context, success=True, duration=2.5)
```

## Perplexity Space Deployment

### Step 1: Create Private Space

1. Log into Perplexity
2. Create new Space (Private/Team access)
3. Name: "Advanced Agent Automation"
4. Enable Enterprise features if available

### Step 2: Configure Space Policies

```yaml
# Space configuration
security:
  access_control: private
  data_encryption: enabled
  audit_logging: enabled
  
resources:
  max_concurrent_tasks: 10
  token_budget: 200000
  timeout: 300
  
monitoring:
  health_checks: enabled
  telemetry: enabled
  alerts: enabled
```

### Step 3: Deploy Agent Components

1. Upload all Python modules to Space
2. Configure environment variables
3. Set up CI/CD pipeline
4. Enable monitoring dashboard

### Step 4: Integration Points

#### API Endpoints
```python
# REST API for Space integration
@app.post("/agent/execute")
async def execute_agent_task(task: TaskRequest):
    agent = get_agent_instance()
    result = agent.execute_task(task.content, task.context)
    return {"result": result, "status": agent.get_status()}

@app.get("/agent/health")
async def health_check():
    agent = get_agent_instance()
    return agent.get_status()["health"]

@app.get("/agent/metrics")
async def get_metrics():
    agent = get_agent_instance()
    return agent.telemetry.get_dashboard_data()
```

## Advanced Configuration

### Plugin Development

```python
from agent_enhanced import Plugin

class CustomPlugin(Plugin):
    @property
    def name(self) -> str:
        return "custom_plugin"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    def initialize(self, config: Dict[str, Any]) -> None:
        self.config = config
    
    def execute(self, context: Dict[str, Any]) -> Any:
        # Your custom logic
        return {"result": "success"}
    
    def cleanup(self) -> None:
        pass

# Register plugin
agent.plugin_manager.register_plugin(CustomPlugin())
agent.plugin_manager.enable_plugin("custom_plugin")
```

### Security Validation

```python
# Add custom validation rules
def validate_no_sensitive_data(data: Any) -> bool:
    sensitive_patterns = ["password", "api_key", "secret"]
    return not any(pattern in str(data).lower() for pattern in sensitive_patterns)

agent.security.add_validation_rule(validate_no_sensitive_data)
```

### Custom Health Checks

```python
# Add custom health check
def check_api_availability() -> bool:
    try:
        response = requests.get("https://api.example.com/health", timeout=5)
        return response.status_code == 200
    except:
        return False

agent.watchdog.register_health_check("api_health", check_api_availability)
```

## Monitoring & Observability

### Dashboard Metrics

- **Token Usage**: Real-time budget tracking
- **Task Success Rate**: Percentage of completed tasks
- **Strategy Performance**: ML model accuracy
- **Health Status**: Component-wise health checks
- **Security Alerts**: Suspicious activity detection

### Logging

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent.log'),
        logging.StreamHandler()
    ]
)
```

## CI/CD Integration

The repository includes GitHub Actions workflow:

- Automated testing (pytest)
- Code quality checks (flake8, black)
- Coverage reports (codecov)
- Multi-version Python testing (3.9, 3.10, 3.11)

## Best Practices

1. **Reliability**
   - Always enable watchdog monitoring
   - Set appropriate timeout values
   - Implement retry logic for critical operations

2. **Security**
   - Validate all inputs
   - Use sandboxed execution
   - Enable audit logging
   - Review security alerts regularly

3. **Performance**
   - Monitor token usage
   - Use async execution for I/O-bound tasks
   - Enable ML strategy selection for optimization

4. **Maintainability**
   - Document custom plugins
   - Version control configurations
   - Regular health check reviews

## Troubleshooting

### Issue: High Token Usage
**Solution**: Enable token optimization, review task complexity

### Issue: Health Check Failures
**Solution**: Check component logs, verify dependencies

### Issue: Strategy Selection Errors
**Solution**: Ensure sufficient training data, check ML dependencies

## Support & Resources

- **GitHub**: https://github.com/labgadget015-dotcom/advanced-agent-token-optimizer
- **Documentation**: See README.md
- **Issues**: Report via GitHub Issues

## License

MIT License - See LICENSE file for details

---

**Version**: 1.0.0  
**Last Updated**: November 2025  
**Status**: Production Ready
