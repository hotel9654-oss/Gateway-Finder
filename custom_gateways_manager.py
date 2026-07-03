#!/usr/bin/env python3
"""
Custom Gateway Manager for Beast Mode
Easily add, manage, and extend payment gateway coverage
"""

import json
import os
from typing import Dict, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class CustomGatewayManager:
    """Manage custom payment gateways"""
    
    def __init__(self, config_file='custom_gateways.json'):
        self.config_file = config_file
        self.gateways = self._load_gateways()
    
    def _load_gateways(self) -> Dict:
        """Load custom gateways from JSON file"""
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_gateways(self):
        """Save gateways to JSON file"""
        with open(self.config_file, 'w') as f:
            json.dump(self.gateways, f, indent=2)
    
    def add_gateway(self, name: str, keywords: List[str], dorks: List[str], 
                   category: str = 'custom', description: str = ''):
        """Add a new custom gateway"""
        gateway = {
            'keywords': keywords,
            'dorks': dorks,
            'category': category,
            'description': description
        }
        
        self.gateways[name.lower()] = gateway
        self._save_gateways()
        
        console.print(
            f"[green]✓[/green] Gateway '{name}' added successfully!",
            style="bold green"
        )
    
    def list_gateways(self):
        """Display all custom gateways in a table"""
        if not self.gateways:
            console.print("[yellow]No custom gateways configured.[/yellow]")
            return
        
        table = Table(title="[bold cyan]Custom Gateways[/bold cyan]", show_header=True)
        table.add_column("Gateway Name", style="cyan")
        table.add_column("Category", style="magenta")
        table.add_column("Dorks", style="yellow")
        
        for name, config in self.gateways.items():
            dorks = f"{len(config['dorks'])} dorks"
            table.add_row(
                name.upper(),
                config.get('category', 'custom'),
                dorks
            )
        
        console.print(table)
    
    def get_all_gateways(self) -> Dict:
        """Get all custom gateways"""
        return self.gateways

if __name__ == '__main__':
    manager = CustomGatewayManager()
    manager.list_gateways()
