#!/usr/bin/env python3
"""
Performance Benchmark Script for AutoGen Studio Synchronization
Measures and compares performance of different sync approaches
"""

import asyncio
import time
import json
import logging
import statistics
from pathlib import Path
from typing import Dict, List, Any
import psutil
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class BenchmarkResult:
    """Benchmark result storage"""
    
    def __init__(self, name: str):
        self.name = name
        self.times = []
        self.success_count = 0
        self.failure_count = 0
        self.cpu_usage = []
        self.memory_usage = []
        self.start_time = None
        self.end_time = None
    
    def start_benchmark(self):
        """Start benchmark timing"""
        self.start_time = time.time()
        
    def end_benchmark(self):
        """End benchmark timing"""
        self.end_time = time.time()
    
    def add_operation(self, duration: float, success: bool, cpu: float, memory: float):
        """Add operation result"""
        self.times.append(duration)
        if success:
            self.success_count += 1
        else:
            self.failure_count += 1
        self.cpu_usage.append(cpu)
        self.memory_usage.append(memory)
    
    def get_stats(self) -> Dict[str, Any]:
        """Get benchmark statistics"""
        if not self.times:
            return {"error": "No operations recorded"}
        
        total_time = self.end_time - self.start_time if self.end_time and self.start_time else 0
        
        return {
            "name": self.name,
            "total_operations": len(self.times),
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "success_rate": (self.success_count / len(self.times)) * 100,
            "total_time_seconds": total_time,
            "operations_per_second": len(self.times) / total_time if total_time > 0 else 0,
            "avg_operation_time_ms": statistics.mean(self.times) * 1000,
            "median_operation_time_ms": statistics.median(self.times) * 1000,
            "min_operation_time_ms": min(self.times) * 1000,
            "max_operation_time_ms": max(self.times) * 1000,
            "std_dev_ms": statistics.stdev(self.times) * 1000 if len(self.times) > 1 else 0,
            "avg_cpu_percent": statistics.mean(self.cpu_usage) if self.cpu_usage else 0,
            "avg_memory_mb": statistics.mean(self.memory_usage) if self.memory_usage else 0,
            "peak_memory_mb": max(self.memory_usage) if self.memory_usage else 0
        }

class PerformanceBenchmarker:
    """Performance benchmarking for AutoGen Studio sync"""
    
    def __init__(self):
        self.studio_base = "http://localhost:8080/api"
        self.results = {}
        
    def get_system_info(self) -> Dict:
        """Get system information for benchmark context"""
        try:
            process = psutil.Process()
            return {
                "cpu_count": psutil.cpu_count(),
                "memory_total_gb": psutil.virtual_memory().total / (1024**3),
                "python_version": f"{__import__('sys').version_info.major}.{__import__('sys').version_info.minor}",
                "process_id": process.pid,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            logger.warning(f"Failed to get system info: {e}")
            return {}
    
    def measure_resource_usage(self) -> tuple:
        """Measure current CPU and memory usage"""
        try:
            process = psutil.Process()
            cpu_percent = process.cpu_percent()
            memory_mb = process.memory_info().rss / (1024 * 1024)
            return cpu_percent, memory_mb
        except Exception:
            return 0.0, 0.0
    
    async def benchmark_studio_connectivity(self, iterations: int = 10) -> BenchmarkResult:
        """Benchmark AutoGen Studio API connectivity"""
        logger.info(f"Benchmarking Studio connectivity ({iterations} iterations)...")
        
        result = BenchmarkResult("studio_connectivity")
        result.start_benchmark()
        
        for i in range(iterations):
            start_time = time.time()
            cpu_before, mem_before = self.measure_resource_usage()
            
            try:
                response = requests.get(f"{self.studio_base}/health", timeout=5)
                success = response.status_code == 200
            except Exception:
                success = False
            
            end_time = time.time()
            cpu_after, mem_after = self.measure_resource_usage()
            
            duration = end_time - start_time
            avg_cpu = (cpu_before + cpu_after) / 2
            avg_mem = (mem_before + mem_after) / 2
            
            result.add_operation(duration, success, avg_cpu, avg_mem)
            
            # Small delay between requests
            if i < iterations - 1:
                await asyncio.sleep(0.1)
        
        result.end_benchmark()
        return result
    
    async def benchmark_component_fetching(self, iterations: int = 5) -> BenchmarkResult:
        """Benchmark fetching existing components"""
        logger.info(f"Benchmarking component fetching ({iterations} iterations)...")
        
        result = BenchmarkResult("component_fetching")
        result.start_benchmark()
        
        endpoints = ["/models", "/agents", "/teams"]
        
        for i in range(iterations):
            start_time = time.time()
            cpu_before, mem_before = self.measure_resource_usage()
            
            success = True
            try:
                for endpoint in endpoints:
                    response = requests.get(f"{self.studio_base}{endpoint}", timeout=10)
                    if response.status_code != 200:
                        success = False
                        break
            except Exception:
                success = False
            
            end_time = time.time()
            cpu_after, mem_after = self.measure_resource_usage()
            
            duration = end_time - start_time
            avg_cpu = (cpu_before + cpu_after) / 2
            avg_mem = (mem_before + mem_after) / 2
            
            result.add_operation(duration, success, avg_cpu, avg_mem)
            
            await asyncio.sleep(0.5)  # Pause between iterations
        
        result.end_benchmark()
        return result
    
    async def benchmark_file_scanning(self, iterations: int = 10) -> BenchmarkResult:
        """Benchmark file scanning for agent configurations"""
        logger.info(f"Benchmarking file scanning ({iterations} iterations)...")
        
        result = BenchmarkResult("file_scanning")
        result.start_benchmark()
        
        base_path = Path(__file__).parent
        
        for i in range(iterations):
            start_time = time.time()
            cpu_before, mem_before = self.measure_resource_usage()
            
            agent_configs = []
            success = True
            
            try:
                # Simulate file scanning
                search_patterns = [
                    "configs/*.json",
                    "*.json",
                    "../**/*agent*.py",
                    "../examples/*agent*.py"
                ]
                
                for pattern in search_patterns:
                    for file_path in base_path.glob(pattern):
                        if file_path.is_file():
                            try:
                                if file_path.suffix == '.json':
                                    with open(file_path, 'r') as f:
                                        config = json.load(f)
                                        if isinstance(config, dict) and 'name' in config:
                                            agent_configs.append(config)
                            except Exception:
                                continue
                
            except Exception:
                success = False
            
            end_time = time.time()
            cpu_after, mem_after = self.measure_resource_usage()
            
            duration = end_time - start_time
            avg_cpu = (cpu_before + cpu_after) / 2
            avg_mem = (mem_before + mem_after) / 2
            
            result.add_operation(duration, success, avg_cpu, avg_mem)
            
            logger.debug(f"Iteration {i+1}: Found {len(agent_configs)} configs in {duration:.3f}s")
        
        result.end_benchmark()
        return result
    
    async def benchmark_agent_registration(self, test_agents: List[Dict], iterations: int = 3) -> BenchmarkResult:
        """Benchmark agent registration process"""
        logger.info(f"Benchmarking agent registration ({iterations} iterations)...")
        
        result = BenchmarkResult("agent_registration")
        result.start_benchmark()
        
        # First ensure we have a model to use
        model_id = await self._ensure_test_model()
        if not model_id:
            logger.error("Cannot proceed with agent registration benchmark - no model available")
            result.end_benchmark()
            return result
        
        for i in range(iterations):
            # Create unique agent names for each iteration
            test_agents_iter = []
            for j, agent in enumerate(test_agents):
                agent_copy = agent.copy()
                agent_copy['name'] = f"{agent['name']}_bench_{i}_{j}"
                test_agents_iter.append(agent_copy)
            
            start_time = time.time()
            cpu_before, mem_before = self.measure_resource_usage()
            
            success_count = 0
            
            for agent_config in test_agents_iter:
                try:
                    agent_data = {
                        "name": agent_config["name"],
                        "description": agent_config.get("description", "Benchmark test agent"),
                        "system_message": agent_config.get("system_message", "You are a helpful assistant"),
                        "model_id": model_id,
                        "type": "assistant",
                        "config": {
                            "temperature": 0.5,
                            "max_tokens": 1000
                        }
                    }
                    
                    response = requests.post(f"{self.studio_base}/agents", json=agent_data, timeout=10)
                    if response.status_code == 200:
                        success_count += 1
                        # Clean up test agent
                        agent_id = response.json().get("id")
                        if agent_id:
                            try:
                                requests.delete(f"{self.studio_base}/agents/{agent_id}")
                            except:
                                pass
                
                except Exception as e:
                    logger.debug(f"Agent registration failed: {e}")
            
            end_time = time.time()
            cpu_after, mem_after = self.measure_resource_usage()
            
            duration = end_time - start_time
            avg_cpu = (cpu_before + cpu_after) / 2
            avg_mem = (mem_before + mem_after) / 2
            success = success_count == len(test_agents_iter)
            
            result.add_operation(duration, success, avg_cpu, avg_mem)
            
            logger.debug(f"Iteration {i+1}: Registered {success_count}/{len(test_agents_iter)} agents in {duration:.3f}s")
            
            await asyncio.sleep(1)  # Pause between iterations
        
        result.end_benchmark()
        return result
    
    async def _ensure_test_model(self) -> str:
        """Ensure test model exists for benchmarking"""
        try:
            # Check existing models
            response = requests.get(f"{self.studio_base}/models")
            if response.status_code == 200:
                models = response.json()
                for model in models:
                    if "test" in model.get("name", "").lower() or "claude" in model.get("model", "").lower():
                        return model["id"]
            
            # Create test model
            model_data = {
                "name": "Benchmark Test Model",
                "model": "claude-opus-4-20250514",
                "api_type": "openai",
                "base_url": "http://localhost:8000/v1",
                "description": "Test model for benchmarking"
            }
            
            response = requests.post(f"{self.studio_base}/models", json=model_data)
            if response.status_code == 200:
                return response.json()["id"]
            
        except Exception as e:
            logger.error(f"Failed to ensure test model: {e}")
        
        return None
    
    async def run_full_benchmark(self) -> Dict[str, Any]:
        """Run comprehensive benchmark suite"""
        logger.info("🚀 Starting comprehensive performance benchmark...")
        
        # System information
        system_info = self.get_system_info()
        logger.info(f"System: {system_info.get('cpu_count', 'unknown')} CPU cores, "
                   f"{system_info.get('memory_total_gb', 0):.1f}GB RAM")
        
        benchmark_results = {}
        
        # 1. Studio connectivity benchmark
        try:
            result = await self.benchmark_studio_connectivity()
            benchmark_results['connectivity'] = result.get_stats()
        except Exception as e:
            logger.error(f"Connectivity benchmark failed: {e}")
            benchmark_results['connectivity'] = {"error": str(e)}
        
        # 2. Component fetching benchmark
        try:
            result = await self.benchmark_component_fetching()
            benchmark_results['component_fetching'] = result.get_stats()
        except Exception as e:
            logger.error(f"Component fetching benchmark failed: {e}")
            benchmark_results['component_fetching'] = {"error": str(e)}
        
        # 3. File scanning benchmark
        try:
            result = await self.benchmark_file_scanning()
            benchmark_results['file_scanning'] = result.get_stats()
        except Exception as e:
            logger.error(f"File scanning benchmark failed: {e}")
            benchmark_results['file_scanning'] = {"error": str(e)}
        
        # 4. Agent registration benchmark (with test data)
        test_agents = [
            {
                "name": "TestAgent1",
                "description": "Test agent for benchmarking",
                "system_message": "You are a test assistant"
            },
            {
                "name": "TestAgent2", 
                "description": "Another test agent",
                "system_message": "You are another test assistant"
            }
        ]
        
        try:
            result = await self.benchmark_agent_registration(test_agents)
            benchmark_results['agent_registration'] = result.get_stats()
        except Exception as e:
            logger.error(f"Agent registration benchmark failed: {e}")
            benchmark_results['agent_registration'] = {"error": str(e)}
        
        # Compile final results
        final_results = {
            "system_info": system_info,
            "benchmark_timestamp": datetime.now().isoformat(),
            "benchmarks": benchmark_results
        }
        
        return final_results
    
    def save_results(self, results: Dict[str, Any], filename: str = "benchmark_results.json"):
        """Save benchmark results to file"""
        output_path = Path(__file__).parent / filename
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2)
        logger.info(f"Benchmark results saved to: {output_path}")
    
    def generate_performance_report(self, results: Dict[str, Any]):
        """Generate human-readable performance report"""
        print("\n" + "="*80)
        print("🎯 AUTOGEN STUDIO PERFORMANCE BENCHMARK REPORT")
        print("="*80)
        
        # System info
        system_info = results.get('system_info', {})
        print(f"\n🖥️  System Information:")
        print(f"   CPU Cores: {system_info.get('cpu_count', 'Unknown')}")
        print(f"   Total Memory: {system_info.get('memory_total_gb', 0):.1f} GB")
        print(f"   Python Version: {system_info.get('python_version', 'Unknown')}")
        print(f"   Benchmark Time: {results.get('benchmark_timestamp', 'Unknown')}")
        
        # Benchmark results
        benchmarks = results.get('benchmarks', {})
        
        print(f"\n📊 Benchmark Results:")
        print("-" * 60)
        
        for bench_name, bench_data in benchmarks.items():
            if 'error' in bench_data:
                print(f"\n❌ {bench_name.replace('_', ' ').title()}: ERROR")
                print(f"   Error: {bench_data['error']}")
                continue
            
            print(f"\n✅ {bench_name.replace('_', ' ').title()}:")
            print(f"   Operations: {bench_data.get('total_operations', 0)}")
            print(f"   Success Rate: {bench_data.get('success_rate', 0):.1f}%")
            print(f"   Avg Time: {bench_data.get('avg_operation_time_ms', 0):.2f}ms")
            print(f"   Median Time: {bench_data.get('median_operation_time_ms', 0):.2f}ms")
            print(f"   Operations/sec: {bench_data.get('operations_per_second', 0):.2f}")
            print(f"   CPU Usage: {bench_data.get('avg_cpu_percent', 0):.1f}%")
            print(f"   Memory Usage: {bench_data.get('avg_memory_mb', 0):.1f}MB")
        
        # Performance recommendations
        self.generate_recommendations(benchmarks)
    
    def generate_recommendations(self, benchmarks: Dict):
        """Generate performance optimization recommendations"""
        print(f"\n💡 Performance Optimization Recommendations:")
        print("-" * 60)
        
        recommendations = []
        
        # Analyze connectivity performance
        connectivity = benchmarks.get('connectivity', {})
        if connectivity.get('avg_operation_time_ms', 0) > 100:
            recommendations.append("🔗 AutoGen Studio connectivity is slow (>100ms). Check network/server performance.")
        
        # Analyze component fetching
        component_fetching = benchmarks.get('component_fetching', {})
        if component_fetching.get('avg_operation_time_ms', 0) > 1000:
            recommendations.append("📦 Component fetching is slow (>1s). Consider implementing caching.")
        
        # Analyze file scanning
        file_scanning = benchmarks.get('file_scanning', {})
        if file_scanning.get('avg_operation_time_ms', 0) > 500:
            recommendations.append("📁 File scanning is slow (>500ms). Implement file change detection caching.")
        
        # Analyze agent registration
        agent_registration = benchmarks.get('agent_registration', {})
        if agent_registration.get('success_rate', 100) < 100:
            recommendations.append("⚠️  Agent registration has failures. Check API error handling.")
        
        if agent_registration.get('operations_per_second', 0) < 2:
            recommendations.append("🚀 Agent registration is slow (<2 ops/sec). Implement parallel processing.")
        
        # Memory usage analysis
        max_memory = max([
            bench.get('peak_memory_mb', 0) 
            for bench in benchmarks.values() 
            if isinstance(bench, dict) and 'peak_memory_mb' in bench
        ], default=0)
        
        if max_memory > 500:
            recommendations.append(f"🧠 High memory usage detected ({max_memory:.1f}MB). Optimize memory management.")
        
        if not recommendations:
            recommendations.append("✨ Performance looks good! No specific optimizations needed.")
        
        for i, rec in enumerate(recommendations, 1):
            print(f"   {i}. {rec}")

async def main():
    """Main benchmark execution"""
    benchmarker = PerformanceBenchmarker()
    
    # Check if AutoGen Studio is accessible
    try:
        response = requests.get(f"{benchmarker.studio_base}/health", timeout=5)
        if response.status_code != 200:
            print("❌ AutoGen Studio is not accessible. Make sure it's running:")
            print("   autogenstudio ui")
            return
    except Exception:
        print("❌ Cannot connect to AutoGen Studio. Make sure it's running:")
        print("   autogenstudio ui")
        return
    
    print("✅ AutoGen Studio detected. Starting benchmark...")
    
    # Run benchmark suite
    results = await benchmarker.run_full_benchmark()
    
    # Save results
    benchmarker.save_results(results)
    
    # Generate report
    benchmarker.generate_performance_report(results)
    
    print(f"\n🎉 Benchmark complete! Results saved to benchmark_results.json")

if __name__ == "__main__":
    asyncio.run(main())