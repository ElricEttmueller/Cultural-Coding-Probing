"""
Weather Dashboard Application 🌤️

An intermediate-level example demonstrating:
- API integration
- Data visualization
- Error handling
- Configuration management
- Basic caching

@probe:architecture 🏛️ How would you structure this application?
- What components would you split out?
- How would you handle dependencies?
- What patterns would you apply?

@probe:error_handling 🚨 How would you improve error handling?
- What edge cases should we consider?
- How would you handle API failures?
- What user errors might occur?

@probe:performance 🚀 How would you optimize the application?
- Where are the bottlenecks?
- How would you improve caching?
- What could be parallelized?
"""

import json
import time
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import requests
from rich.console import Console
from rich.table import Table

@dataclass
class WeatherConfig:
    """Weather API configuration."""
    api_key: str
    base_url: str
    cache_duration: int  # seconds
    units: str = "metric"
    
    @classmethod
    def from_file(cls, filename: str = "weather_config.json") -> "WeatherConfig":
        """Load configuration from file."""
        try:
            with open(filename) as f:
                config = json.load(f)
            return cls(**config)
        except Exception as e:
            print(f"Error loading config: {e}")
            return cls(
                api_key="demo_key",
                base_url="https://api.weather.example.com",
                cache_duration=300
            )

class WeatherCache:
    """Simple cache for weather data."""
    
    def __init__(self, cache_file: str = "weather_cache.json"):
        self.cache_file = cache_file
        self.cache: Dict[str, Tuple[float, dict]] = {}
        self.load_cache()
    
    def get(self, key: str) -> Optional[dict]:
        """Get cached data if not expired."""
        if key in self.cache:
            timestamp, data = self.cache[key]
            if time.time() - timestamp < WeatherConfig.from_file().cache_duration:
                return data
        return None
    
    def set(self, key: str, data: dict) -> None:
        """Cache data with timestamp."""
        self.cache[key] = (time.time(), data)
        self.save_cache()
    
    def load_cache(self) -> None:
        """Load cache from file."""
        try:
            if Path(self.cache_file).exists():
                with open(self.cache_file) as f:
                    self.cache = json.load(f)
        except Exception as e:
            print(f"Error loading cache: {e}")
            self.cache = {}
    
    def save_cache(self) -> None:
        """Save cache to file."""
        try:
            with open(self.cache_file, "w") as f:
                json.dump(self.cache, f)
        except Exception as e:
            print(f"Error saving cache: {e}")

class WeatherDashboard:
    """Weather dashboard with visualization."""
    
    def __init__(self):
        self.config = WeatherConfig.from_file()
        self.cache = WeatherCache()
        self.console = Console()
    
    def get_weather(self, city: str) -> Optional[dict]:
        """Get weather data for city."""
        # @probe:caching 💾 How would you improve the caching?
        # - What caching strategy would you use?
        # - How would you handle cache invalidation?
        # - What data should be cached?
        
        # Check cache first
        cached = self.cache.get(city)
        if cached:
            return cached
        
        # Make API request
        try:
            url = f"{self.config.base_url}/weather"
            params = {
                "q": city,
                "appid": self.config.api_key,
                "units": self.config.units
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            self.cache.set(city, data)
            return data
            
        except requests.RequestException as e:
            self.console.print(f"[red]Error fetching weather: {e}[/red]")
            return None
    
    def plot_temperature_trend(self, city: str, days: int = 5) -> None:
        """Plot temperature trend for city."""
        try:
            url = f"{self.config.base_url}/forecast"
            params = {
                "q": city,
                "appid": self.config.api_key,
                "units": self.config.units
            }
            
            response = requests.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            timestamps = []
            temperatures = []
            
            for item in data["list"][:days * 8]:  # 8 readings per day
                dt = datetime.fromtimestamp(item["dt"])
                timestamps.append(dt)
                temperatures.append(item["main"]["temp"])
            
            plt.figure(figsize=(10, 6))
            plt.plot(timestamps, temperatures, marker="o")
            plt.title(f"Temperature Trend - {city}")
            plt.xlabel("Date")
            plt.ylabel("Temperature (°C)")
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()
            
            # Save plot
            plt.savefig(f"{city}_temperature.png")
            plt.close()
            
        except Exception as e:
            self.console.print(f"[red]Error plotting temperature: {e}[/red]")
    
    def display_weather(self, city: str) -> None:
        """Display current weather in a table."""
        data = self.get_weather(city)
        if not data:
            return
        
        table = Table(title=f"Weather in {city}")
        
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="magenta")
        
        table.add_row("Temperature", f"{data['main']['temp']}°C")
        table.add_row("Feels Like", f"{data['main']['feels_like']}°C")
        table.add_row("Humidity", f"{data['main']['humidity']}%")
        table.add_row("Wind Speed", f"{data['wind']['speed']} m/s")
        table.add_row("Description", data['weather'][0]['description'].title())
        
        self.console.print(table)

def main():
    """Main program loop."""
    dashboard = WeatherDashboard()
    console = Console()
    
    while True:
        console.print("\n[bold cyan]Weather Dashboard Menu:[/bold cyan]")
        console.print("1. View Current Weather")
        console.print("2. Plot Temperature Trend")
        console.print("3. Exit")
        
        choice = input("\nWhat would you like to do? (1-3): ")
        
        if choice == "1":
            city = input("Enter city name: ")
            dashboard.display_weather(city)
            
        elif choice == "2":
            city = input("Enter city name: ")
            days = input("Enter number of days (1-5): ")
            try:
                dashboard.plot_temperature_trend(city, int(days))
                console.print(f"[green]Plot saved as {city}_temperature.png[/green]")
            except ValueError:
                console.print("[red]Please enter a valid number of days![/red]")
            
        elif choice == "3":
            console.print("[yellow]Goodbye! 👋[/yellow]")
            break
            
        else:
            console.print("[red]Invalid choice! Please try again.[/red]")

if __name__ == "__main__":
    main()
