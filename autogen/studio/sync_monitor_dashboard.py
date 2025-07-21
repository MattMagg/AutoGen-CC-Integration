#!/usr/bin/env python3
"""
Real-time Monitoring Dashboard for AutoGen Studio Synchronization
Provides live performance metrics and alerts
"""

import asyncio
import json
import time
import logging
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Optional
import psutil
import requests
from dataclasses import dataclass
import threading
import signal
import sys

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class SystemMetrics:
    """System performance metrics"""
    timestamp: float
    cpu_percent: float
    memory_percent: float
    memory_mb: float
    disk_usage_percent: float
    network_io: Dict[str, int]

@dataclass
class StudioMetrics:
    """AutoGen Studio specific metrics"""
    timestamp: float
    api_response_time_ms: float
    api_available: bool
    models_count: int
    agents_count: int
    teams_count: int
    last_sync_time: Optional[float] = None
    sync_success_rate: float = 100.0

class MetricsCollector:
    """Collects system and Studio metrics"""
    
    def __init__(self):
        self.studio_base = "http://localhost:8080/api"
        self.system_metrics: List[SystemMetrics] = []
        self.studio_metrics: List[StudioMetrics] = []
        self.max_history = 100  # Keep last 100 measurements
        
    def collect_system_metrics(self) -> SystemMetrics:
        """Collect current system metrics"""
        try:
            # CPU and memory
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            
            # Disk usage
            disk = psutil.disk_usage('/')
            disk_percent = (disk.used / disk.total) * 100
            
            # Network I/O
            network = psutil.net_io_counters()
            network_io = {
                'bytes_sent': network.bytes_sent,
                'bytes_recv': network.bytes_recv,
                'packets_sent': network.packets_sent,
                'packets_recv': network.packets_recv
            }
            
            return SystemMetrics(
                timestamp=time.time(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                memory_mb=memory.used / (1024 * 1024),
                disk_usage_percent=disk_percent,
                network_io=network_io
            )
            
        except Exception as e:
            logger.error(f"Failed to collect system metrics: {e}")
            return SystemMetrics(
                timestamp=time.time(),
                cpu_percent=0,
                memory_percent=0,
                memory_mb=0,
                disk_usage_percent=0,
                network_io={}
            )
    
    def collect_studio_metrics(self) -> StudioMetrics:
        """Collect AutoGen Studio metrics"""
        start_time = time.time()
        
        try:
            # Test API availability and response time
            response = requests.get(f"{self.studio_base}/health", timeout=5)
            api_response_time = (time.time() - start_time) * 1000
            api_available = response.status_code == 200
            
            # Get component counts
            models_count = 0
            agents_count = 0
            teams_count = 0
            
            if api_available:
                try:
                    # Get models count
                    models_response = requests.get(f"{self.studio_base}/models", timeout=5)
                    if models_response.status_code == 200:
                        models_count = len(models_response.json())
                    
                    # Get agents count
                    agents_response = requests.get(f"{self.studio_base}/agents", timeout=5)
                    if agents_response.status_code == 200:
                        agents_count = len(agents_response.json())
                    
                    # Get teams count
                    teams_response = requests.get(f"{self.studio_base}/teams", timeout=5)
                    if teams_response.status_code == 200:
                        teams_count = len(teams_response.json())
                        
                except Exception as e:
                    logger.debug(f"Failed to get component counts: {e}")
            
            return StudioMetrics(
                timestamp=time.time(),
                api_response_time_ms=api_response_time,
                api_available=api_available,
                models_count=models_count,
                agents_count=agents_count,
                teams_count=teams_count
            )
            
        except Exception as e:
            logger.error(f"Failed to collect Studio metrics: {e}")
            return StudioMetrics(
                timestamp=time.time(),
                api_response_time_ms=5000,  # Timeout indicator
                api_available=False,
                models_count=0,
                agents_count=0,
                teams_count=0
            )
    
    def add_system_metrics(self, metrics: SystemMetrics):
        """Add system metrics to history"""
        self.system_metrics.append(metrics)
        if len(self.system_metrics) > self.max_history:
            self.system_metrics.pop(0)
    
    def add_studio_metrics(self, metrics: StudioMetrics):
        """Add Studio metrics to history"""
        self.studio_metrics.append(metrics)
        if len(self.studio_metrics) > self.max_history:
            self.studio_metrics.pop(0)

class AlertManager:
    """Manages performance alerts and notifications"""
    
    def __init__(self):
        self.alerts = []
        self.thresholds = {
            'cpu_high': 80.0,
            'memory_high': 85.0,
            'disk_high': 90.0,
            'api_slow': 1000.0,  # ms
            'api_timeout': 5000.0  # ms
        }
    
    def check_alerts(self, system_metrics: SystemMetrics, studio_metrics: StudioMetrics):
        """Check for alert conditions"""
        alerts = []
        
        # System alerts
        if system_metrics.cpu_percent > self.thresholds['cpu_high']:
            alerts.append({
                'type': 'CPU_HIGH',
                'level': 'WARNING',
                'message': f"High CPU usage: {system_metrics.cpu_percent:.1f}%",
                'timestamp': system_metrics.timestamp
            })
        
        if system_metrics.memory_percent > self.thresholds['memory_high']:
            alerts.append({
                'type': 'MEMORY_HIGH',
                'level': 'WARNING',
                'message': f"High memory usage: {system_metrics.memory_percent:.1f}%",
                'timestamp': system_metrics.timestamp
            })
        
        if system_metrics.disk_usage_percent > self.thresholds['disk_high']:
            alerts.append({
                'type': 'DISK_HIGH',
                'level': 'CRITICAL',
                'message': f"High disk usage: {system_metrics.disk_usage_percent:.1f}%",
                'timestamp': system_metrics.timestamp
            })
        
        # Studio alerts
        if not studio_metrics.api_available:
            alerts.append({
                'type': 'API_DOWN',
                'level': 'CRITICAL',
                'message': "AutoGen Studio API is not available",
                'timestamp': studio_metrics.timestamp
            })
        elif studio_metrics.api_response_time_ms > self.thresholds['api_timeout']:
            alerts.append({
                'type': 'API_TIMEOUT',
                'level': 'CRITICAL',
                'message': f"API timeout: {studio_metrics.api_response_time_ms:.0f}ms",
                'timestamp': studio_metrics.timestamp
            })
        elif studio_metrics.api_response_time_ms > self.thresholds['api_slow']:
            alerts.append({
                'type': 'API_SLOW',
                'level': 'WARNING',
                'message': f"Slow API response: {studio_metrics.api_response_time_ms:.0f}ms",
                'timestamp': studio_metrics.timestamp
            })
        
        # Store new alerts
        for alert in alerts:
            self.alerts.append(alert)
            logger.warning(f"ALERT [{alert['level']}] {alert['type']}: {alert['message']}")
        
        # Cleanup old alerts (keep last 50)
        if len(self.alerts) > 50:
            self.alerts = self.alerts[-50:]
        
        return alerts

class MonitoringDashboard:
    """Main monitoring dashboard"""
    
    def __init__(self, refresh_interval: float = 5.0):
        self.refresh_interval = refresh_interval
        self.metrics_collector = MetricsCollector()
        self.alert_manager = AlertManager()
        self.running = False
        self.start_time = time.time()
        
        # Setup graceful shutdown
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)
    
    def shutdown(self, signum, frame):
        """Graceful shutdown"""
        print("\n📊 Shutting down monitoring dashboard...")
        self.running = False
        sys.exit(0)
    
    def clear_screen(self):
        """Clear terminal screen"""
        import os
        os.system('cls' if os.name == 'nt' else 'clear')
    
    def format_uptime(self) -> str:
        """Format monitoring uptime"""
        uptime_seconds = time.time() - self.start_time
        hours = int(uptime_seconds // 3600)
        minutes = int((uptime_seconds % 3600) // 60)
        seconds = int(uptime_seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    
    def format_bytes(self, bytes_val: float) -> str:
        """Format bytes to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if bytes_val < 1024:
                return f"{bytes_val:.1f} {unit}"
            bytes_val /= 1024
        return f"{bytes_val:.1f} TB"
    
    def get_status_indicator(self, value: float, warning_threshold: float, 
                           critical_threshold: float) -> str:
        """Get colored status indicator"""
        if value >= critical_threshold:
            return "🔴"
        elif value >= warning_threshold:
            return "🟡"
        else:
            return "🟢"
    
    def render_dashboard(self):
        """Render the monitoring dashboard"""
        self.clear_screen()
        
        # Get latest metrics
        system_metrics = self.metrics_collector.system_metrics[-1] if self.metrics_collector.system_metrics else None
        studio_metrics = self.metrics_collector.studio_metrics[-1] if self.metrics_collector.studio_metrics else None
        
        print("=" * 80)
        print("🔍 AUTOGEN STUDIO SYNC - PERFORMANCE MONITOR")
        print("=" * 80)
        print(f"Uptime: {self.format_uptime()} | Refresh: {self.refresh_interval}s | Time: {datetime.now().strftime('%H:%M:%S')}")
        print()
        
        if system_metrics:
            # System Metrics
            print("🖥️  SYSTEM METRICS")
            print("-" * 40)
            cpu_status = self.get_status_indicator(system_metrics.cpu_percent, 70, 85)
            mem_status = self.get_status_indicator(system_metrics.memory_percent, 80, 90)
            disk_status = self.get_status_indicator(system_metrics.disk_usage_percent, 85, 95)
            
            print(f"CPU Usage:    {cpu_status} {system_metrics.cpu_percent:5.1f}%")
            print(f"Memory Usage: {mem_status} {system_metrics.memory_percent:5.1f}% ({self.format_bytes(system_metrics.memory_mb * 1024 * 1024)})")
            print(f"Disk Usage:   {disk_status} {system_metrics.disk_usage_percent:5.1f}%")
            print()
        
        if studio_metrics:
            # Studio Metrics
            print("🤖 AUTOGEN STUDIO METRICS")
            print("-" * 40)
            api_status = "🟢" if studio_metrics.api_available else "🔴"
            response_status = self.get_status_indicator(studio_metrics.api_response_time_ms, 500, 1000)
            
            print(f"API Status:   {api_status} {'Online' if studio_metrics.api_available else 'Offline'}")
            print(f"Response Time:{response_status} {studio_metrics.api_response_time_ms:6.0f}ms")
            print(f"Models:       📊 {studio_metrics.models_count:3d}")
            print(f"Agents:       👥 {studio_metrics.agents_count:3d}")
            print(f"Teams:        🏆 {studio_metrics.teams_count:3d}")
            print()
        
        # Performance Trends (last 10 measurements)
        if len(self.metrics_collector.system_metrics) >= 2:
            print("📈 PERFORMANCE TRENDS (Last 10 measurements)")
            print("-" * 40)
            
            recent_system = self.metrics_collector.system_metrics[-10:]
            recent_studio = self.metrics_collector.studio_metrics[-10:]
            
            # Calculate averages
            avg_cpu = sum(m.cpu_percent for m in recent_system) / len(recent_system)
            avg_memory = sum(m.memory_percent for m in recent_system) / len(recent_system)
            
            if recent_studio:
                avg_response = sum(m.api_response_time_ms for m in recent_studio) / len(recent_studio)
                uptime_pct = (sum(1 for m in recent_studio if m.api_available) / len(recent_studio)) * 100
                
                print(f"Avg CPU:      {avg_cpu:5.1f}%")
                print(f"Avg Memory:   {avg_memory:5.1f}%")
                print(f"Avg Response: {avg_response:6.0f}ms")
                print(f"API Uptime:   {uptime_pct:5.1f}%")
            print()
        
        # Recent Alerts
        recent_alerts = self.alert_manager.alerts[-5:]  # Last 5 alerts
        if recent_alerts:
            print("🚨 RECENT ALERTS")
            print("-" * 40)
            for alert in recent_alerts:
                timestamp = datetime.fromtimestamp(alert['timestamp']).strftime('%H:%M:%S')
                level_icon = "🔴" if alert['level'] == 'CRITICAL' else "🟡"
                print(f"{timestamp} {level_icon} {alert['type']}: {alert['message']}")
            print()
        
        # Sync Performance Summary
        if Path("sync_performance.json").exists():
            try:
                with open("sync_performance.json", 'r') as f:
                    perf_data = json.load(f)
                
                print("⚡ LAST SYNC PERFORMANCE")
                print("-" * 40)
                summary = perf_data.get('summary', {})
                print(f"Total Ops:    {summary.get('total_operations', 0):3d}")
                print(f"Success Rate: {summary.get('success_rate_percent', 0):5.1f}%")
                print(f"Avg Latency:  {summary.get('avg_latency_ms', 0):6.1f}ms")
                print(f"Runtime:      {summary.get('total_runtime_seconds', 0):6.1f}s")
                print()
            except Exception:
                pass
        
        print("Press Ctrl+C to stop monitoring")
        print("=" * 80)
    
    async def collect_metrics_loop(self):
        """Main metrics collection loop"""
        while self.running:
            try:
                # Collect metrics
                system_metrics = self.metrics_collector.collect_system_metrics()
                studio_metrics = self.metrics_collector.collect_studio_metrics()
                
                # Store metrics
                self.metrics_collector.add_system_metrics(system_metrics)
                self.metrics_collector.add_studio_metrics(studio_metrics)
                
                # Check for alerts
                self.alert_manager.check_alerts(system_metrics, studio_metrics)
                
                # Render dashboard
                self.render_dashboard()
                
                # Wait for next refresh
                await asyncio.sleep(self.refresh_interval)
                
            except Exception as e:
                logger.error(f"Error in metrics collection loop: {e}")
                await asyncio.sleep(1)
    
    async def run(self):
        """Run the monitoring dashboard"""
        print("🚀 Starting AutoGen Studio Performance Monitor...")
        print("   Checking AutoGen Studio availability...")
        
        # Initial connectivity check
        try:
            response = requests.get(f"{self.metrics_collector.studio_base}/health", timeout=5)
            if response.status_code != 200:
                print("⚠️  AutoGen Studio API not responding properly")
                print("   Monitor will continue but some metrics may be unavailable")
            else:
                print("✅ AutoGen Studio detected")
        except Exception:
            print("⚠️  Cannot connect to AutoGen Studio")
            print("   Make sure it's running: autogenstudio ui")
            print("   Monitor will continue with system metrics only")
        
        print(f"   Refresh interval: {self.refresh_interval}s")
        print("   Starting in 3 seconds...")
        await asyncio.sleep(3)
        
        self.running = True
        await self.collect_metrics_loop()
    
    def save_session_data(self):
        """Save monitoring session data"""
        session_data = {
            'session_start': self.start_time,
            'session_end': time.time(),
            'refresh_interval': self.refresh_interval,
            'system_metrics': [
                {
                    'timestamp': m.timestamp,
                    'cpu_percent': m.cpu_percent,
                    'memory_percent': m.memory_percent,
                    'memory_mb': m.memory_mb,
                    'disk_usage_percent': m.disk_usage_percent
                }
                for m in self.metrics_collector.system_metrics
            ],
            'studio_metrics': [
                {
                    'timestamp': m.timestamp,
                    'api_response_time_ms': m.api_response_time_ms,
                    'api_available': m.api_available,
                    'models_count': m.models_count,
                    'agents_count': m.agents_count,
                    'teams_count': m.teams_count
                }
                for m in self.metrics_collector.studio_metrics
            ],
            'alerts': self.alert_manager.alerts
        }
        
        filename = f"monitoring_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(session_data, f, indent=2)
        
        print(f"📊 Session data saved to: {filename}")

async def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="AutoGen Studio Performance Monitor")
    parser.add_argument('--refresh', type=float, default=5.0, 
                       help='Refresh interval in seconds (default: 5.0)')
    parser.add_argument('--save-session', action='store_true',
                       help='Save session data on exit')
    
    args = parser.parse_args()
    
    dashboard = MonitoringDashboard(refresh_interval=args.refresh)
    
    try:
        await dashboard.run()
    except KeyboardInterrupt:
        pass
    finally:
        if args.save_session:
            dashboard.save_session_data()
        print("\n👋 Monitoring stopped.")

if __name__ == "__main__":
    asyncio.run(main())