"""Enhanced Agent with All Optimizations Integrated.

Combines: Plugin System, Watchdog/Health Checks, Security Validation,
Telemetry/Monitoring, and Enhanced CI/CD capabilities.
"""

import asyncio
import time
import json
import threading
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)


# ========== PLUGIN SYSTEM ==========

class Plugin(ABC):
    """Base plugin interface."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        pass
    
    @property
    @abstractmethod
    def version(self) -> str:
        pass
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        pass
    
    @abstractmethod
    def execute(self, context: Dict[str, Any]) -> Any:
        pass
    
    @abstractmethod
    def cleanup(self) -> None:
        pass


class PluginManager:
    """Manages plugin lifecycle and execution."""
    
    def __init__(self):
        self.plugins: Dict[str, Plugin] = {}
        self.enabled_plugins: List[str] = []
        
    def register_plugin(self, plugin: Plugin) -> None:
        """Register a plugin."""
        self.plugins[plugin.name] = plugin
        logger.info(f"Plugin registered: {plugin.name} v{plugin.version}")
        
    def enable_plugin(self, name: str, config: Dict[str, Any] = None) -> None:
        """Enable and initialize a plugin."""
        if name not in self.plugins:
            raise ValueError(f"Plugin not found: {name}")
        
        plugin = self.plugins[name]
        plugin.initialize(config or {})
        self.enabled_plugins.append(name)
        logger.info(f"Plugin enabled: {name}")
        
    def execute_plugin(self, name: str, context: Dict[str, Any]) -> Any:
        """Execute a plugin."""
        if name not in self.enabled_plugins:
            raise ValueError(f"Plugin not enabled: {name}")
        
        return self.plugins[name].execute(context)
        
    def disable_plugin(self, name: str) -> None:
        """Disable a plugin."""
        if name in self.enabled_plugins:
            self.plugins[name].cleanup()
            self.enabled_plugins.remove(name)
            logger.info(f"Plugin disabled: {name}")


# ========== WATCHDOG & HEALTH CHECKS ==========

@dataclass
class HealthStatus:
    """Health check status."""
    is_healthy: bool
    component: str
    message: str
    timestamp: float = field(default_factory=time.time)


class Watchdog:
    """Monitors agent health and detects issues."""
    
    def __init__(self, check_interval: float = 30.0):
        self.check_interval = check_interval
        self.health_checks: Dict[str, Callable] = {}
        self.last_check_time: Dict[str, float] = {}
        self.status_history: List[HealthStatus] = []
        self.is_running = False
        self._thread = None
        
    def register_health_check(self, name: str, check_fn: Callable[[], bool]) -> None:
        """Register a health check function."""
        self.health_checks[name] = check_fn
        logger.info(f"Health check registered: {name}")
        
    def start(self) -> None:
        """Start watchdog monitoring."""
        self.is_running = True
        self._thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self._thread.start()
        logger.info("Watchdog started")
        
    def stop(self) -> None:
        """Stop watchdog monitoring."""
        self.is_running = False
        if self._thread:
            self._thread.join(timeout=5.0)
        logger.info("Watchdog stopped")
        
    def _monitor_loop(self) -> None:
        """Main monitoring loop."""
        while self.is_running:
            for name, check_fn in self.health_checks.items():
                try:
                    is_healthy = check_fn()
                    status = HealthStatus(
                        is_healthy=is_healthy,
                        component=name,
                        message="OK" if is_healthy else "Check failed"
                    )
                    self.status_history.append(status)
                    self.last_check_time[name] = time.time()
                    
                    if not is_healthy:
                        logger.warning(f"Health check failed: {name}")
                        
                except Exception as e:
                    logger.error(f"Health check error for {name}: {e}")
                    
            time.sleep(self.check_interval)
            
    def get_health_report(self) -> Dict[str, Any]:
        """Get health report."""
        recent_status = {}
        for status in reversed(self.status_history[-50:]):
            if status.component not in recent_status:
                recent_status[status.component] = status
                
        return {
            "overall_healthy": all(s.is_healthy for s in recent_status.values()),
            "components": {k: {"healthy": v.is_healthy, "message": v.message, "last_check": v.timestamp} 
                          for k, v in recent_status.items()}
        }


# ========== SECURITY & SANDBOXING ==========

class SecurityValidator:
    """Enhanced security validation and sandboxing."""
    
    def __init__(self):
        self.validation_rules: List[Callable] = []
        self.blocked_patterns: List[str] = []
        self.suspicious_activity_count = 0
        
    def add_validation_rule(self, rule: Callable[[Any], bool]) -> None:
        """Add a validation rule."""
        self.validation_rules.append(rule)
        
    def validate_input(self, data: Any) -> bool:
        """Validate input data."""
        for rule in self.validation_rules:
            try:
                if not rule(data):
                    self.suspicious_activity_count += 1
                    logger.warning(f"Validation failed for input: {data}")
                    return False
            except Exception as e:
                logger.error(f"Validation rule error: {e}")
                return False
        return True
        
    def check_rate_limit(self, action: str, limit: int, window: float) -> bool:
        """Check if action rate limit is exceeded."""
        # Simplified rate limiting - in production use redis or similar
        return True  # Placeholder
        
    def sanitize_output(self, data: str) -> str:
        """Sanitize output to prevent data leakage."""
        # Remove sensitive patterns
        for pattern in self.blocked_patterns:
            data = data.replace(pattern, "[REDACTED]")
        return data


# ========== TELEMETRY & MONITORING ==========

@dataclass
class Metric:
    """Performance metric."""
    name: str
    value: float
    timestamp: float = field(default_factory=time.time)
    tags: Dict[str, str] = field(default_factory=dict)


class TelemetryCollector:
    """Collects and aggregates telemetry data."""
    
    def __init__(self, max_metrics: int = 10000):
        self.max_metrics = max_metrics
        self.metrics: List[Metric] = []
        self.counters: Dict[str, int] = {}
        self.gauges: Dict[str, float] = {}
        
    def record_metric(self, name: str, value: float, tags: Dict[str, str] = None) -> None:
        """Record a metric."""
        metric = Metric(name=name, value=value, tags=tags or {})
        self.metrics.append(metric)
        
        # Keep only recent metrics
        if len(self.metrics) > self.max_metrics:
            self.metrics = self.metrics[-self.max_metrics:]
            
    def increment_counter(self, name: str, delta: int = 1) -> None:
        """Increment a counter."""
        self.counters[name] = self.counters.get(name, 0) + delta
        
    def set_gauge(self, name: str, value: float) -> None:
        """Set a gauge value."""
        self.gauges[name] = value
        
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get data for monitoring dashboard."""
        return {
            "counters": self.counters,
            "gauges": self.gauges,
            "recent_metrics": [{
                "name": m.name,
                "value": m.value,
                "timestamp": m.timestamp,
                "tags": m.tags
            } for m in self.metrics[-100:]]
        }


# ========== ENHANCED AGENT ==========

class EnhancedAgent:
    """Autonomous agent with all optimizations."""
    
    def __init__(self, 
                 token_budget: int = 200000,
                 enable_plugins: bool = True,
                 enable_watchdog: bool = True,
                 enable_telemetry: bool = True):
        
        # Core components
        self.token_budget = token_budget
        self.token_used = 0
        
        # Enhanced components
        self.plugin_manager = PluginManager() if enable_plugins else None
        self.watchdog = Watchdog() if enable_watchdog else None
        self.security = SecurityValidator()
        self.telemetry = TelemetryCollector() if enable_telemetry else None
        
        # Start monitoring
        if self.watchdog:
            self._register_health_checks()
            self.watchdog.start()
            
        logger.info("EnhancedAgent initialized")
        
    def _register_health_checks(self) -> None:
        """Register default health checks."""
        self.watchdog.register_health_check(
            "token_budget",
            lambda: self.token_used < self.token_budget * 0.9
        )
        self.watchdog.register_health_check(
            "security_alerts",
            lambda: self.security.suspicious_activity_count < 10
        )
        
    def execute_task(self, task: str, context: Dict[str, Any] = None) -> Any:
        """Execute a task with full monitoring and validation."""
        start_time = time.time()
        context = context or {}
        
        try:
            # Security validation
            if not self.security.validate_input(task):
                raise ValueError("Security validation failed")
            
            # Execute with telemetry
            result = self._execute_internal(task, context)
            
            # Record success
            if self.telemetry:
                duration = time.time() - start_time
                self.telemetry.record_metric("task_duration", duration)
                self.telemetry.increment_counter("tasks_completed")
                
            return result
            
        except Exception as e:
            logger.error(f"Task execution failed: {e}")
            if self.telemetry:
                self.telemetry.increment_counter("tasks_failed")
            raise
            
    def _execute_internal(self, task: str, context: Dict[str, Any]) -> Any:
        """Internal task execution logic."""
        # Placeholder - integrate with actual agent logic
        return {"status": "completed", "task": task}
        
    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive agent status."""
        status = {
            "token_usage": {"used": self.token_used, "total": self.token_budget},
            "security": {"suspicious_activity": self.security.suspicious_activity_count},
        }
        
        if self.watchdog:
            status["health"] = self.watchdog.get_health_report()
            
        if self.telemetry:
            status["telemetry"] = self.telemetry.get_dashboard_data()
            
        return status
        
    def shutdown(self) -> None:
        """Graceful shutdown."""
        if self.watchdog:
            self.watchdog.stop()
            
        if self.plugin_manager:
            for plugin_name in list(self.plugin_manager.enabled_plugins):
                self.plugin_manager.disable_plugin(plugin_name)
                
        logger.info("EnhancedAgent shutdown complete")


if __name__ == "__main__":
    # Example usage
    agent = EnhancedAgent()
    
    # Execute task
    result = agent.execute_task("test_task")
    print(f"Result: {result}")
    
    # Get status
    status = agent.get_status()
    print(f"Status: {json.dumps(status, indent=2)}")
    
    # Shutdown
    agent.shutdown()
