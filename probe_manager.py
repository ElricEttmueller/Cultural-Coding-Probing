import yaml
import os
import datetime
import random
from pathlib import Path
from typing import Dict, List, Optional

class ProbeManager:
    def __init__(self, config_path: str = "probe_config.yaml"):
        """Initialize the probe manager with configuration."""
        self.config_path = config_path
        self.config = self._load_config()
        self.response_dir = Path(self.config["probe_settings"]["storage"]["location"])
        self._ensure_response_directory()

    def _load_config(self) -> Dict:
        """Load probe configuration from YAML file."""
        with open(self.config_path, 'r') as f:
            return yaml.safe_load(f)

    def _ensure_response_directory(self) -> None:
        """Create response directory if it doesn't exist."""
        self.response_dir.mkdir(parents=True, exist_ok=True)

    def get_random_probe(self, probe_type: str) -> Optional[str]:
        """Get a random probe template of the specified type."""
        probe_types = self.config["probe_types"]
        if probe_type not in probe_types:
            return None
        
        templates = probe_types[probe_type]["templates"]
        return random.choice(templates)

    def store_response(self, probe_type: str, prompt: str, response: str) -> None:
        """Store a probe response in the designated format."""
        timestamp = datetime.datetime.now().isoformat()
        filename = f"{probe_type}_{timestamp}.md"
        
        content = f"""# Probe Response

## Type
{probe_type}

## Prompt
{prompt}

## Response
{response}

## Timestamp
{timestamp}
"""
        
        with open(self.response_dir / filename, 'w') as f:
            f.write(content)

    def inject_probe_comment(self, file_path: str, probe_type: str) -> str:
        """Generate a probe comment to be injected into code."""
        prompt = self.get_random_probe(probe_type)
        if not prompt:
            return ""
        
        return f"# @probe:{probe_type} {prompt}"

    def get_commit_probe(self) -> Optional[str]:
        """Get a probe template for commit messages."""
        workflow_probes = self.config["probe_types"]["workflow"]["templates"]
        return random.choice(workflow_probes)

if __name__ == "__main__":
    # Example usage
    probe_manager = ProbeManager()
    
    # Get a random environment probe
    env_probe = probe_manager.get_random_probe("environment")
    print(f"Environment Probe: {env_probe}")
    
    # Generate a code comment probe
    code_probe = probe_manager.inject_probe_comment("example.py", "tools")
    print(f"\nCode Probe: {code_probe}")
    
    # Store a sample response
    probe_manager.store_response(
        "environment",
        "How does your current development environment affect your productivity?",
        "I find that having multiple monitors helps me maintain context while coding."
    )
