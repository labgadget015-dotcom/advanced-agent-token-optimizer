"""ML-Driven Strategy Selection Module.

Provides machine learning capabilities for dynamic strategy selection based on
historical performance and context.
"""

import json
import time
import pickle
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field, asdict
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)

try:
    import numpy as np
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.preprocessing import StandardScaler
    HAS_ML = True
except ImportError:
    logger.warning("scikit-learn not available. Using fallback strategy selection.")
    HAS_ML = False


@dataclass
class StrategyPerformance:
    """Track strategy performance metrics."""
    strategy_name: str
    success_count: int = 0
    failure_count: int = 0
    total_duration: float = 0.0
    context_features: Dict[str, Any] = field(default_factory=dict)
    
    @property
    def success_rate(self) -> float:
        total = self.success_count + self.failure_count
        return self.success_count / total if total > 0 else 0.0
    
    @property
    def avg_duration(self) -> float:
        total = self.success_count + self.failure_count
        return self.total_duration / total if total > 0 else 0.0


@dataclass
class ExecutionContext:
    """Execution context for strategy selection."""
    task_type: str
    complexity: float  # 0-1
    time_constraint: Optional[float]  # seconds
    token_budget_remaining: float  # 0-1 ratio
    validation_errors: int
    previous_strategy: Optional[str] = None
    previous_failed: bool = False
    
    def to_features(self) -> List[float]:
        """Convert context to feature vector."""
        return [
            hash(self.task_type) % 100 / 100.0,  # Normalized task type hash
            self.complexity,
            (self.time_constraint or 60) / 60.0,  # Normalized time
            self.token_budget_remaining,
            min(self.validation_errors / 10.0, 1.0),  # Normalized errors
            1.0 if self.previous_failed else 0.0,
        ]


class MLStrategySelector:
    """ML-driven strategy selector."""
    
    def __init__(self, 
                 strategies: List[str],
                 use_ml: bool = HAS_ML,
                 learning_rate: float = 0.1):
        self.strategies = strategies
        self.use_ml = use_ml and HAS_ML
        self.learning_rate = learning_rate
        
        # Performance tracking
        self.performance_history: Dict[str, StrategyPerformance] = {
            s: StrategyPerformance(strategy_name=s) for s in strategies
        }
        
        # ML components
        if self.use_ml:
            self.model = RandomForestClassifier(
                n_estimators=100,
                max_depth=10,
                random_state=42
            )
            self.scaler = StandardScaler()
            self.is_trained = False
            self.training_data: List[Tuple[List[float], int]] = []
        else:
            self.model = None
            self.scaler = None
            
    def select_strategy(self, 
                       context: ExecutionContext,
                       exclude: Optional[List[str]] = None) -> str:
        """Select best strategy for given context."""
        exclude = exclude or []
        available_strategies = [s for s in self.strategies if s not in exclude]
        
        if not available_strategies:
            logger.warning("No available strategies. Using first strategy.")
            return self.strategies[0]
        
        # Use ML model if trained
        if self.use_ml and self.is_trained and len(self.training_data) >= 10:
            return self._ml_select(context, available_strategies)
        
        # Fallback to performance-based selection
        return self._performance_select(context, available_strategies)
    
    def _ml_select(self, 
                   context: ExecutionContext,
                   available_strategies: List[str]) -> str:
        """Select strategy using ML model."""
        features = np.array([context.to_features()])
        features_scaled = self.scaler.transform(features)
        
        # Get probability predictions
        probabilities = self.model.predict_proba(features_scaled)[0]
        
        # Map to available strategies
        strategy_scores = {}
        for idx, strategy in enumerate(self.strategies):
            if strategy in available_strategies:
                strategy_scores[strategy] = probabilities[idx]
        
        # Select highest scoring strategy
        best_strategy = max(strategy_scores, key=strategy_scores.get)
        logger.info(f"ML selected strategy: {best_strategy} (score: {strategy_scores[best_strategy]:.3f})")
        return best_strategy
    
    def _performance_select(self,
                           context: ExecutionContext,
                           available_strategies: List[str]) -> str:
        """Select strategy based on historical performance."""
        # Score each strategy
        scores = {}
        for strategy in available_strategies:
            perf = self.performance_history[strategy]
            
            # Calculate composite score
            score = (
                perf.success_rate * 0.6 +  # Success rate weight
                (1.0 / (perf.avg_duration + 0.1)) * 0.2 +  # Speed weight
                (1.0 if strategy != context.previous_strategy else 0.5) * 0.2  # Diversity weight
            )
            
            # Penalize if previous strategy failed
            if context.previous_failed and strategy == context.previous_strategy:
                score *= 0.3
            
            scores[strategy] = score
        
        best_strategy = max(scores, key=scores.get)
        logger.info(f"Performance-based selected strategy: {best_strategy} (score: {scores[best_strategy]:.3f})")
        return best_strategy
    
    def record_outcome(self,
                      strategy: str,
                      context: ExecutionContext,
                      success: bool,
                      duration: float) -> None:
        """Record strategy execution outcome."""
        perf = self.performance_history[strategy]
        
        if success:
            perf.success_count += 1
        else:
            perf.failure_count += 1
        
        perf.total_duration += duration
        
        # Store training data
        if self.use_ml:
            features = context.to_features()
            label = self.strategies.index(strategy)
            self.training_data.append((features, label))
            
            # Retrain if enough new data
            if len(self.training_data) % 20 == 0:
                self._retrain_model()
    
    def _retrain_model(self) -> None:
        """Retrain ML model with collected data."""
        if not self.use_ml or len(self.training_data) < 10:
            return
        
        logger.info(f"Retraining model with {len(self.training_data)} samples")
        
        # Prepare data
        X = np.array([features for features, _ in self.training_data])
        y = np.array([label for _, label in self.training_data])
        
        # Scale features
        self.scaler.fit(X)
        X_scaled = self.scaler.transform(X)
        
        # Train model
        self.model.fit(X_scaled, y)
        self.is_trained = True
        
        logger.info("Model retrained successfully")
    
    def get_performance_report(self) -> Dict[str, Any]:
        """Generate performance report."""
        report = {}
        for strategy, perf in self.performance_history.items():
            report[strategy] = {
                "success_rate": perf.success_rate,
                "success_count": perf.success_count,
                "failure_count": perf.failure_count,
                "avg_duration": perf.avg_duration,
            }
        return report
    
    def save(self, filepath: str) -> None:
        """Save selector state to file."""
        state = {
            "strategies": self.strategies,
            "performance_history": {k: asdict(v) for k, v in self.performance_history.items()},
            "training_data": self.training_data if self.use_ml else [],
        }
        
        with open(filepath, 'wb') as f:
            pickle.dump(state, f)
        
        logger.info(f"Selector state saved to {filepath}")
    
    def load(self, filepath: str) -> None:
        """Load selector state from file."""
        with open(filepath, 'rb') as f:
            state = pickle.load(f)
        
        self.strategies = state["strategies"]
        self.performance_history = {
            k: StrategyPerformance(**v) for k, v in state["performance_history"].items()
        }
        self.training_data = state.get("training_data", [])
        
        # Retrain model if data available
        if self.use_ml and self.training_data:
            self._retrain_model()
        
        logger.info(f"Selector state loaded from {filepath}")


class AdaptiveStrategyManager:
    """Manages multiple strategy selectors with adaptive learning."""
    
    def __init__(self):
        self.selectors: Dict[str, MLStrategySelector] = {}
        self.global_stats = defaultdict(int)
    
    def register_selector(self, 
                         domain: str,
                         strategies: List[str]) -> None:
        """Register a strategy selector for a domain."""
        self.selectors[domain] = MLStrategySelector(strategies)
        logger.info(f"Registered selector for domain: {domain}")
    
    def select_strategy(self,
                       domain: str,
                       context: ExecutionContext,
                       exclude: Optional[List[str]] = None) -> str:
        """Select strategy for a domain."""
        if domain not in self.selectors:
            raise ValueError(f"No selector registered for domain: {domain}")
        
        return self.selectors[domain].select_strategy(context, exclude)
    
    def record_outcome(self,
                      domain: str,
                      strategy: str,
                      context: ExecutionContext,
                      success: bool,
                      duration: float) -> None:
        """Record outcome for a domain."""
        if domain in self.selectors:
            self.selectors[domain].record_outcome(strategy, context, success, duration)
            self.global_stats["total_executions"] += 1
            if success:
                self.global_stats["total_successes"] += 1


if __name__ == "__main__":
    # Example usage
    strategies = ["direct_search", "filtered_search", "category_navigation"]
    selector = MLStrategySelector(strategies)
    
    # Simulate executions
    for i in range(50):
        context = ExecutionContext(
            task_type="search",
            complexity=0.5,
            time_constraint=30.0,
            token_budget_remaining=0.7,
            validation_errors=0
        )
        
        strategy = selector.select_strategy(context)
        success = True  # Simulate success
        duration = 2.0
        
        selector.record_outcome(strategy, context, success, duration)
    
    print(json.dumps(selector.get_performance_report(), indent=2))
