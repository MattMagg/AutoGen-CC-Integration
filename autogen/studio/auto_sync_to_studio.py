#!/usr/bin/env python3
"""
AutoGen Studio Performance-Optimized Synchronization Script
This script optimizes the VS Code ↔ AutoGen Studio workflow with automated sync,
performance monitoring, and comprehensive error handling.
"""

import asyncio
import json
import time
import logging
import hashlib
import os
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime
import aiohttp
import aiofiles
import requests
from concurrent.futures import ThreadPoolExecutor
import psutil

# Performance monitoring and logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('autogen_studio_sync.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# AutoGen Studio configuration
STUDIO_API_BASE = "http://localhost:8080/api"
PERFORMANCE_LOG_FILE = "sync_performance.json"
SYNC_CACHE_FILE = "sync_cache.json"

@dataclass
class PerformanceMetrics:
    """Performance metrics tracking"""
    operation: str
    start_time: float
    end_time: float
    success: bool
    error_message: Optional[str] = None
    resource_usage: Optional[Dict] = None
    latency_ms: float = 0.0
    
    def __post_init__(self):
        self.latency_ms = (self.end_time - self.start_time) * 1000

@dataclass
class SyncResult:
    """Synchronization result tracking"""
    agent_name: str
    operation: str
    success: bool
    latency_ms: float
    error_message: Optional[str] = None
    
class PerformanceMonitor:
    """Performance monitoring and metrics collection"""
    
    def __init__(self):
        self.metrics: List[PerformanceMetrics] = []
        self.start_time = time.time()
        
    def start_operation(self, operation: str) -> float:
        """Start timing an operation"""
        return time.time()
    
    def end_operation(self, operation: str, start_time: float, success: bool, 
                     error_message: Optional[str] = None) -> PerformanceMetrics:
        """End timing an operation and record metrics"""
        end_time = time.time()
        
        # Collect resource usage
        process = psutil.Process()
        resource_usage = {
            'cpu_percent': process.cpu_percent(),
            'memory_mb': process.memory_info().rss / 1024 / 1024,
            'memory_percent': process.memory_percent()
        }
        
        metric = PerformanceMetrics(
            operation=operation,
            start_time=start_time,
            end_time=end_time,
            success=success,
            error_message=error_message,
            resource_usage=resource_usage
        )
        
        self.metrics.append(metric)
        logger.info(f"Operation '{operation}' completed in {metric.latency_ms:.2f}ms "
                   f"(Success: {success})")
        
        return metric
    
    def get_summary(self) -> Dict[str, Any]:
        """Get performance summary"""
        total_operations = len(self.metrics)
        successful_operations = sum(1 for m in self.metrics if m.success)
        
        if total_operations == 0:
            return {"error": "No operations recorded"}
        
        avg_latency = sum(m.latency_ms for m in self.metrics) / total_operations
        max_latency = max(m.latency_ms for m in self.metrics)
        min_latency = min(m.latency_ms for m in self.metrics)
        
        success_rate = (successful_operations / total_operations) * 100
        
        # Group by operation type
        operation_stats = {}
        for metric in self.metrics:
            if metric.operation not in operation_stats:
                operation_stats[metric.operation] = {
                    'count': 0,
                    'success_count': 0,
                    'total_latency': 0
                }
            
            operation_stats[metric.operation]['count'] += 1
            if metric.success:
                operation_stats[metric.operation]['success_count'] += 1
            operation_stats[metric.operation]['total_latency'] += metric.latency_ms
        
        # Calculate averages for each operation
        for op_name, stats in operation_stats.items():
            stats['avg_latency'] = stats['total_latency'] / stats['count']
            stats['success_rate'] = (stats['success_count'] / stats['count']) * 100
        
        return {
            'total_operations': total_operations,
            'successful_operations': successful_operations,
            'success_rate_percent': success_rate,
            'avg_latency_ms': avg_latency,
            'max_latency_ms': max_latency,
            'min_latency_ms': min_latency,
            'operation_breakdown': operation_stats,
            'total_runtime_seconds': time.time() - self.start_time
        }
    
    def save_metrics(self):
        """Save metrics to file for analysis"""
        metrics_data = {
            'timestamp': datetime.now().isoformat(),
            'summary': self.get_summary(),
            'detailed_metrics': [asdict(m) for m in self.metrics]
        }
        
        with open(PERFORMANCE_LOG_FILE, 'w') as f:
            json.dump(metrics_data, f, indent=2)

class SyncCache:
    """Caching system to avoid unnecessary synchronizations"""
    
    def __init__(self):
        self.cache = self._load_cache()
    
    def _load_cache(self) -> Dict:
        """Load sync cache from file"""
        if os.path.exists(SYNC_CACHE_FILE):
            try:
                with open(SYNC_CACHE_FILE, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load sync cache: {e}")
        return {}
    
    def _save_cache(self):
        """Save sync cache to file"""
        with open(SYNC_CACHE_FILE, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def get_file_hash(self, file_path: str) -> str:
        """Calculate file hash for change detection"""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""
    
    def has_changed(self, file_path: str) -> bool:
        """Check if file has changed since last sync"""
        current_hash = self.get_file_hash(file_path)
        cached_hash = self.cache.get(file_path)
        return current_hash != cached_hash
    
    def update_file_hash(self, file_path: str):
        """Update file hash in cache"""
        self.cache[file_path] = self.get_file_hash(file_path)
        self._save_cache()

class AutoGenStudioSync:
    """High-performance AutoGen Studio synchronization"""
    
    def __init__(self):
        self.monitor = PerformanceMonitor()
        self.cache = SyncCache()
        self.session = None
        
    async def __aenter__(self):
        """Async context manager entry"""
        self.session = aiohttp.ClientSession()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        if self.session:
            await self.session.close()
    
    async def check_studio_health(self) -> bool:
        """Check if AutoGen Studio is running with async request"""
        start_time = self.monitor.start_operation("health_check")
        
        try:
            async with self.session.get(f"{STUDIO_API_BASE}/health", timeout=5) as response:
                success = response.status == 200
                self.monitor.end_operation("health_check", start_time, success)
                return success
        except Exception as e:
            self.monitor.end_operation("health_check", start_time, False, str(e))
            return False
    
    async def get_existing_components(self) -> Tuple[Dict, Dict, Dict]:
        """Get existing models, agents, and teams from Studio"""
        start_time = self.monitor.start_operation("fetch_existing_components")
        
        try:
            # Fetch all components in parallel
            async with asyncio.gather(
                self.session.get(f"{STUDIO_API_BASE}/models"),
                self.session.get(f"{STUDIO_API_BASE}/agents"),
                self.session.get(f"{STUDIO_API_BASE}/teams"),
                return_exceptions=True
            ) as responses:
                
                models = {}
                agents = {}
                teams = {}
                
                # Process models
                if not isinstance(responses[0], Exception) and responses[0].status == 200:
                    models_data = await responses[0].json()
                    models = {m.get("model", m.get("name")): m for m in models_data}
                
                # Process agents
                if not isinstance(responses[1], Exception) and responses[1].status == 200:
                    agents_data = await responses[1].json()
                    agents = {a.get("name"): a for a in agents_data}
                
                # Process teams
                if not isinstance(responses[2], Exception) and responses[2].status == 200:
                    teams_data = await responses[2].json()
                    teams = {t.get("name"): t for t in teams_data}
                
                self.monitor.end_operation("fetch_existing_components", start_time, True)
                return models, agents, teams
                
        except Exception as e:
            self.monitor.end_operation("fetch_existing_components", start_time, False, str(e))
            return {}, {}, {}
    
    async def register_model_async(self, model_data: Dict) -> Optional[str]:
        """Register model with async request"""
        start_time = self.monitor.start_operation("register_model")
        
        try:
            async with self.session.post(f"{STUDIO_API_BASE}/models", 
                                       json=model_data) as response:
                if response.status == 200:
                    result = await response.json()
                    model_id = result.get("id")
                    self.monitor.end_operation("register_model", start_time, True)
                    logger.info(f"✅ Registered model: {model_data['name']} (ID: {model_id})")
                    return model_id
                else:
                    error_text = await response.text()
                    self.monitor.end_operation("register_model", start_time, False, error_text)
                    logger.error(f"❌ Failed to register model: {error_text}")
                    return None
                    
        except Exception as e:
            self.monitor.end_operation("register_model", start_time, False, str(e))
            logger.error(f"❌ Model registration error: {e}")
            return None
    
    async def register_agent_async(self, agent_data: Dict) -> Optional[str]:
        """Register agent with async request"""
        start_time = self.monitor.start_operation("register_agent")
        
        try:
            async with self.session.post(f"{STUDIO_API_BASE}/agents", 
                                       json=agent_data) as response:
                if response.status == 200:
                    result = await response.json()
                    agent_id = result.get("id")
                    self.monitor.end_operation("register_agent", start_time, True)
                    logger.info(f"✅ Registered agent: {agent_data['name']} (ID: {agent_id})")
                    return agent_id
                else:
                    error_text = await response.text()
                    self.monitor.end_operation("register_agent", start_time, False, error_text)
                    logger.error(f"❌ Failed to register agent: {error_text}")
                    return None
                    
        except Exception as e:
            self.monitor.end_operation("register_agent", start_time, False, str(e))
            logger.error(f"❌ Agent registration error: {e}")
            return None
    
    async def scan_agent_files(self) -> List[Dict]:
        """Scan for agent configuration files"""
        start_time = self.monitor.start_operation("scan_agent_files")
        
        agent_configs = []
        base_path = Path(__file__).parent
        
        # Search patterns for agent files
        search_patterns = [
            "configs/*.json",
            "*.json",
            "../**/*agent*.py",
            "../**/*agent*.json",
            "../examples/*agent*.py"
        ]
        
        try:
            for pattern in search_patterns:
                for file_path in base_path.glob(pattern):
                    if file_path.is_file():
                        # Check if file has changed
                        if not self.cache.has_changed(str(file_path)):
                            logger.debug(f"Skipping unchanged file: {file_path}")
                            continue
                        
                        try:
                            if file_path.suffix == '.json':
                                async with aiofiles.open(file_path, 'r') as f:
                                    content = await f.read()
                                    config = json.loads(content)
                                    
                                    # Validate agent config structure
                                    if self._is_valid_agent_config(config):
                                        config['_file_path'] = str(file_path)
                                        agent_configs.append(config)
                                        self.cache.update_file_hash(str(file_path))
                            
                            elif file_path.suffix == '.py':
                                # Extract agent configs from Python files
                                configs = await self._extract_configs_from_python(file_path)
                                for config in configs:
                                    config['_file_path'] = str(file_path)
                                    agent_configs.append(config)
                                self.cache.update_file_hash(str(file_path))
                                
                        except Exception as e:
                            logger.warning(f"Failed to process {file_path}: {e}")
            
            self.monitor.end_operation("scan_agent_files", start_time, True)
            logger.info(f"Found {len(agent_configs)} agent configurations")
            return agent_configs
            
        except Exception as e:
            self.monitor.end_operation("scan_agent_files", start_time, False, str(e))
            return []
    
    def _is_valid_agent_config(self, config: Dict) -> bool:
        """Validate agent configuration structure"""
        required_fields = ['name', 'description', 'system_message']
        return all(field in config for field in required_fields)
    
    async def _extract_configs_from_python(self, file_path: Path) -> List[Dict]:
        """Extract agent configurations from Python files"""
        configs = []
        
        try:
            async with aiofiles.open(file_path, 'r') as f:
                content = await f.read()
            
            # Look for agent configuration patterns
            import re
            
            # Pattern for dict-style agent configs
            agent_patterns = [
                r'agent_config\s*=\s*({.*?})',
                r'config\s*=\s*({.*?})',
                r'AssistantAgent\s*\(\s*name\s*=\s*["\']([^"\']+)["\'].*?system_message\s*=\s*["\']([^"\']+)["\']'
            ]
            
            for pattern in agent_patterns:
                matches = re.finditer(pattern, content, re.DOTALL)
                for match in matches:
                    try:
                        if match.group(1).startswith('{'):
                            # Try to parse as JSON-like dict
                            config_str = match.group(1)
                            # Basic cleanup for Python dict to JSON conversion
                            config_str = config_str.replace("'", '"').replace('True', 'true').replace('False', 'false')
                            config = json.loads(config_str)
                            
                            if self._is_valid_agent_config(config):
                                configs.append(config)
                        else:
                            # Extract from AssistantAgent constructor
                            name = match.group(1)
                            system_message = match.group(2)
                            config = {
                                'name': name,
                                'description': f"Agent extracted from {file_path.name}",
                                'system_message': system_message
                            }
                            configs.append(config)
                            
                    except Exception as e:
                        logger.debug(f"Failed to parse config from {file_path}: {e}")
            
        except Exception as e:
            logger.warning(f"Failed to extract configs from {file_path}: {e}")
        
        return configs
    
    async def sync_agents_batch(self, agent_configs: List[Dict], 
                               existing_models: Dict, existing_agents: Dict) -> List[SyncResult]:
        """Synchronize agents in batches for optimal performance"""
        start_time = self.monitor.start_operation("batch_sync_agents")
        results = []
        
        try:
            # Ensure we have a model to use
            model_id = await self._ensure_model_exists(existing_models)
            if not model_id:
                self.monitor.end_operation("batch_sync_agents", start_time, False, 
                                         "No model available")
                return results
            
            # Process agents in parallel batches
            batch_size = 5  # Configurable batch size
            semaphore = asyncio.Semaphore(batch_size)
            
            async def sync_single_agent(config):
                async with semaphore:
                    return await self._sync_single_agent(config, model_id, existing_agents)
            
            # Execute all agent syncs in parallel
            sync_tasks = [sync_single_agent(config) for config in agent_configs]
            results = await asyncio.gather(*sync_tasks, return_exceptions=True)
            
            # Process results and handle exceptions
            processed_results = []
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    processed_results.append(SyncResult(
                        agent_name=agent_configs[i].get('name', 'Unknown'),
                        operation='sync_agent',
                        success=False,
                        latency_ms=0,
                        error_message=str(result)
                    ))
                else:
                    processed_results.append(result)
            
            success_count = sum(1 for r in processed_results if r.success)
            self.monitor.end_operation("batch_sync_agents", start_time, 
                                     success_count == len(processed_results))
            
            logger.info(f"Batch sync completed: {success_count}/{len(processed_results)} successful")
            return processed_results
            
        except Exception as e:
            self.monitor.end_operation("batch_sync_agents", start_time, False, str(e))
            logger.error(f"Batch sync failed: {e}")
            return results
    
    async def _ensure_model_exists(self, existing_models: Dict) -> Optional[str]:
        """Ensure a model exists for agent registration"""
        # Check if our preferred model exists
        claude_model = "claude-opus-4-20250514"
        
        for model_key, model in existing_models.items():
            if model.get("model") == claude_model:
                return model["id"]
        
        # Create the model if it doesn't exist
        model_data = {
            "name": "Claude Opus via Wrapper",
            "model": claude_model,
            "api_type": "openai",
            "base_url": "http://localhost:8000/v1",
            "description": "Claude Opus 4 accessed through local OpenAI-compatible wrapper"
        }
        
        return await self.register_model_async(model_data)
    
    async def _sync_single_agent(self, config: Dict, model_id: str, 
                                existing_agents: Dict) -> SyncResult:
        """Synchronize a single agent"""
        agent_name = config.get('name', 'Unknown')
        operation_start = time.time()
        
        try:
            # Check if agent already exists
            if agent_name in existing_agents:
                return SyncResult(
                    agent_name=agent_name,
                    operation='sync_agent',
                    success=True,
                    latency_ms=0,
                    error_message="Agent already exists (skipped)"
                )
            
            # Prepare agent data
            agent_data = {
                "name": agent_name,
                "description": config.get("description", f"Agent from {config.get('_file_path', 'unknown')}"),
                "system_message": config.get("system_message", ""),
                "model_id": model_id,
                "type": "assistant",
                "config": {
                    "temperature": config.get("model_client", {}).get("temperature", 0.5),
                    "max_tokens": config.get("model_client", {}).get("max_tokens", 4096)
                }
            }
            
            # Register agent
            agent_id = await self.register_agent_async(agent_data)
            
            operation_end = time.time()
            latency_ms = (operation_end - operation_start) * 1000
            
            return SyncResult(
                agent_name=agent_name,
                operation='sync_agent',
                success=agent_id is not None,
                latency_ms=latency_ms,
                error_message=None if agent_id else "Registration failed"
            )
            
        except Exception as e:
            operation_end = time.time()
            latency_ms = (operation_end - operation_start) * 1000
            
            return SyncResult(
                agent_name=agent_name,
                operation='sync_agent',
                success=False,
                latency_ms=latency_ms,
                error_message=str(e)
            )

async def run_performance_analysis():
    """Run performance analysis of the sync process"""
    print("🔍 Starting Performance Analysis...")
    print("=" * 60)
    
    async with AutoGenStudioSync() as sync:
        # Test Studio connectivity
        print("📡 Testing AutoGen Studio connectivity...")
        is_healthy = await sync.check_studio_health()
        
        if not is_healthy:
            print("❌ AutoGen Studio is not accessible")
            print("💡 Make sure AutoGen Studio is running: autogenstudio ui")
            return
        
        print("✅ AutoGen Studio is accessible")
        
        # Measure component fetching performance
        print("\n📊 Measuring component fetching performance...")
        models, agents, teams = await sync.get_existing_components()
        
        print(f"   Models found: {len(models)}")
        print(f"   Agents found: {len(agents)}")
        print(f"   Teams found: {len(teams)}")
        
        # Measure file scanning performance
        print("\n📁 Measuring file scanning performance...")
        agent_configs = await sync.scan_agent_files()
        print(f"   Agent configs found: {len(agent_configs)}")
        
        # Display discovered agent configurations
        if agent_configs:
            print("\n📋 Discovered agent configurations:")
            for config in agent_configs:
                file_path = config.get('_file_path', 'Unknown')
                print(f"   • {config['name']} (from {file_path})")
        
        # Measure sync performance
        if agent_configs:
            print("\n⚡ Measuring sync performance...")
            sync_results = await sync.sync_agents_batch(agent_configs, models, agents)
            
            # Display sync results
            successful_syncs = [r for r in sync_results if r.success]
            failed_syncs = [r for r in sync_results if not r.success]
            
            print(f"   Successful syncs: {len(successful_syncs)}")
            print(f"   Failed syncs: {len(failed_syncs)}")
            
            if failed_syncs:
                print("\n❌ Failed synchronizations:")
                for result in failed_syncs:
                    print(f"   • {result.agent_name}: {result.error_message}")
        
        # Generate performance report
        print("\n📈 Generating performance report...")
        performance_summary = sync.monitor.get_summary()
        
        print(f"\n🎯 Performance Summary:")
        print(f"   Total operations: {performance_summary['total_operations']}")
        print(f"   Success rate: {performance_summary['success_rate_percent']:.1f}%")
        print(f"   Average latency: {performance_summary['avg_latency_ms']:.2f}ms")
        print(f"   Max latency: {performance_summary['max_latency_ms']:.2f}ms")
        print(f"   Total runtime: {performance_summary['total_runtime_seconds']:.2f}s")
        
        # Operation breakdown
        print("\n📊 Operation Breakdown:")
        for op_name, stats in performance_summary['operation_breakdown'].items():
            print(f"   {op_name}:")
            print(f"     Count: {stats['count']}")
            print(f"     Success rate: {stats['success_rate']:.1f}%")
            print(f"     Avg latency: {stats['avg_latency']:.2f}ms")
        
        # Save performance metrics
        sync.monitor.save_metrics()
        print(f"\n💾 Performance metrics saved to: {PERFORMANCE_LOG_FILE}")

async def run_automated_sync():
    """Run automated synchronization"""
    print("🚀 Starting Automated Sync...")
    print("=" * 50)
    
    async with AutoGenStudioSync() as sync:
        # Check Studio health
        if not await sync.check_studio_health():
            logger.error("AutoGen Studio is not accessible")
            return False
        
        # Get existing components
        models, agents, teams = await sync.get_existing_components()
        logger.info(f"Existing components: {len(models)} models, {len(agents)} agents, {len(teams)} teams")
        
        # Scan for agent files
        agent_configs = await sync.scan_agent_files()
        logger.info(f"Found {len(agent_configs)} agent configurations")
        
        if not agent_configs:
            logger.info("No new agent configurations found")
            return True
        
        # Sync agents
        sync_results = await sync.sync_agents_batch(agent_configs, models, agents)
        
        # Summary
        successful = [r for r in sync_results if r.success]
        failed = [r for r in sync_results if not r.success]
        
        logger.info(f"Sync completed: {len(successful)} successful, {len(failed)} failed")
        
        # Save performance metrics
        sync.monitor.save_metrics()
        
        return len(failed) == 0

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AutoGen Studio Performance Sync")
    parser.add_argument('--analyze', action='store_true', 
                       help='Run performance analysis')
    parser.add_argument('--sync', action='store_true', 
                       help='Run automated synchronization')
    parser.add_argument('--watch', action='store_true', 
                       help='Watch for changes and auto-sync')
    
    args = parser.parse_args()
    
    if args.analyze:
        asyncio.run(run_performance_analysis())
    elif args.sync:
        asyncio.run(run_automated_sync())
    elif args.watch:
        print("🔄 Watch mode not implemented yet")
    else:
        print("Usage: python auto_sync_to_studio.py [--analyze|--sync|--watch]")
        print("Run with --analyze to measure performance")
        print("Run with --sync to perform automated synchronization")

if __name__ == "__main__":
    main()