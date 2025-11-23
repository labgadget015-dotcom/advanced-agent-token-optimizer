"""Async and Distributed Execution Module.

Provides async task execution, distributed coordination, and parallel processing
for the autonomous agent framework.
"""

import asyncio
import time
from typing import Dict, List, Optional, Any, Callable, Coroutine
from dataclasses import dataclass, field
from enum import Enum
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import logging

logger = logging.getLogger(__name__)


class ExecutionMode(Enum):
    """Execution mode for tasks."""
    ASYNC = "async"
    THREADED = "threaded"
    PROCESS = "process"
    DISTRIBUTED = "distributed"


@dataclass
class AsyncTask:
    """Async task representation."""
    id: str
    coroutine: Coroutine
    priority: int = 0
    timeout: Optional[float] = None
    retries: int = 3
    retry_delay: float = 1.0
    dependencies: List[str] = field(default_factory=list)
    
    def __lt__(self, other):
        return self.priority > other.priority  # Higher priority first


class AsyncExecutor:
    """Async task executor with parallel processing."""
    
    def __init__(self, 
                 max_concurrent_tasks: int = 10,
                 thread_pool_size: int = 4,
                 process_pool_size: int = 2):
        self.max_concurrent_tasks = max_concurrent_tasks
        self.thread_pool = ThreadPoolExecutor(max_workers=thread_pool_size)
        self.process_pool = ProcessPoolExecutor(max_workers=process_pool_size)
        self.running_tasks: Dict[str, asyncio.Task] = {}
        self.completed_tasks: Dict[str, Any] = {}
        self.failed_tasks: Dict[str, Exception] = {}
        self.task_queue: asyncio.PriorityQueue = asyncio.PriorityQueue()
        
    async def submit_task(self, task: AsyncTask) -> None:
        """Submit a task for execution."""
        await self.task_queue.put((task.priority, task))
        
    async def execute_task(self, task: AsyncTask) -> Any:
        """Execute a single task with retries."""
        for attempt in range(task.retries):
            try:
                if task.timeout:
                    result = await asyncio.wait_for(
                        task.coroutine, 
                        timeout=task.timeout
                    )
                else:
                    result = await task.coroutine
                    
                self.completed_tasks[task.id] = result
                logger.info(f"Task {task.id} completed successfully")
                return result
                
            except asyncio.TimeoutError:
                logger.warning(f"Task {task.id} timed out (attempt {attempt + 1})")
                if attempt < task.retries - 1:
                    await asyncio.sleep(task.retry_delay)
                else:
                    self.failed_tasks[task.id] = TimeoutError("Task timed out")
                    raise
                    
            except Exception as e:
                logger.error(f"Task {task.id} failed: {e} (attempt {attempt + 1})")
                if attempt < task.retries - 1:
                    await asyncio.sleep(task.retry_delay)
                else:
                    self.failed_tasks[task.id] = e
                    raise
                    
    async def run(self) -> None:
        """Run the async executor."""
        while not self.task_queue.empty() or self.running_tasks:
            # Wait for available slot
            while len(self.running_tasks) >= self.max_concurrent_tasks:
                await asyncio.sleep(0.1)
                
            # Get next task
            if not self.task_queue.empty():
                priority, task = await self.task_queue.get()
                
                # Check dependencies
                if all(dep in self.completed_tasks for dep in task.dependencies):
                    # Start task
                    async_task = asyncio.create_task(self.execute_task(task))
                    self.running_tasks[task.id] = async_task
                    
                    # Clean up when done
                    async_task.add_done_callback(
                        lambda t, tid=task.id: self.running_tasks.pop(tid, None)
                    )
                else:
                    # Re-queue if dependencies not met
                    await self.task_queue.put((priority, task))
                    await asyncio.sleep(0.1)
                    
            await asyncio.sleep(0.01)
            
    async def execute_parallel(self, 
                              tasks: List[AsyncTask]) -> Dict[str, Any]:
        """Execute multiple tasks in parallel."""
        for task in tasks:
            await self.submit_task(task)
            
        await self.run()
        return self.completed_tasks
        
    def shutdown(self):
        """Shutdown executor and cleanup resources."""
        self.thread_pool.shutdown(wait=True)
        self.process_pool.shutdown(wait=True)


class DistributedCoordinator:
    """Coordinator for distributed task execution."""
    
    def __init__(self, node_id: str = "main"):
        self.node_id = node_id
        self.registered_nodes: Dict[str, Dict] = {}
        self.task_assignments: Dict[str, str] = {}
        
    def register_node(self, node_id: str, capabilities: Dict[str, Any]):
        """Register a worker node."""
        self.registered_nodes[node_id] = {
            "capabilities": capabilities,
            "last_heartbeat": time.time(),
            "tasks_assigned": 0,
            "tasks_completed": 0,
        }
        logger.info(f"Node {node_id} registered with capabilities: {capabilities}")
        
    def assign_task(self, task_id: str, requirements: Dict[str, Any]) -> Optional[str]:
        """Assign task to best available node."""
        best_node = None
        best_score = -1
        
        for node_id, node_info in self.registered_nodes.items():
            # Check if node meets requirements
            if self._node_meets_requirements(node_info, requirements):
                # Calculate score based on load and capabilities
                score = self._calculate_node_score(node_info)
                if score > best_score:
                    best_score = score
                    best_node = node_id
                    
        if best_node:
            self.task_assignments[task_id] = best_node
            self.registered_nodes[best_node]["tasks_assigned"] += 1
            logger.info(f"Task {task_id} assigned to node {best_node}")
            return best_node
            
        return None
        
    def _node_meets_requirements(self, node_info: Dict, requirements: Dict) -> bool:
        """Check if node meets task requirements."""
        # Simple capability matching
        node_caps = node_info["capabilities"]
        for req_key, req_value in requirements.items():
            if req_key not in node_caps or node_caps[req_key] < req_value:
                return False
        return True
        
    def _calculate_node_score(self, node_info: Dict) -> float:
        """Calculate node fitness score for task assignment."""
        # Lower load = higher score
        load = node_info["tasks_assigned"] - node_info["tasks_completed"]
        return 1.0 / (load + 1)


if __name__ == "__main__":
    # Example usage
    async def example_task(task_id: str, duration: float):
        print(f"Starting task {task_id}")
        await asyncio.sleep(duration)
        print(f"Completed task {task_id}")
        return f"Result from {task_id}"
    
    async def main():
        executor = AsyncExecutor(max_concurrent_tasks=3)
        
        # Create tasks
        tasks = [
            AsyncTask(
                id=f"task_{i}",
                coroutine=example_task(f"task_{i}", 1.0),
                priority=i,
                timeout=5.0
            )
            for i in range(5)
        ]
        
        # Execute
        results = await executor.execute_parallel(tasks)
        print(f"Results: {results}")
        
        executor.shutdown()
    
    asyncio.run(main())
