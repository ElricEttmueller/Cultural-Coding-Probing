"""
Code Analysis Tool 🔍

An advanced example demonstrating:
- Abstract Syntax Tree (AST) parsing
- Design patterns (Visitor, Factory)
- Advanced type hints
- Concurrent processing
- Custom metrics calculation

@probe:design_patterns 🎨 What patterns would you use?
- Which design patterns fit this problem?
- How would you implement them?
- What are the trade-offs?

@probe:metrics 📊 What metrics would you add?
- What code qualities should we measure?
- How would you calculate them?
- What insights are we missing?

@probe:scalability 🚀 How would you scale this?
- How would you handle large codebases?
- What could be parallelized?
- Where are the bottlenecks?
"""

import ast
import concurrent.futures
import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Type, Union

@dataclass
class CodeMetrics:
    """Code metrics container."""
    lines_of_code: int = 0
    comment_lines: int = 0
    function_count: int = 0
    class_count: int = 0
    complexity: int = 0
    dependencies: Set[str] = field(default_factory=set)
    nested_depth: int = 0
    
    def to_dict(self) -> dict:
        """Convert metrics to dictionary."""
        return {
            "lines_of_code": self.lines_of_code,
            "comment_lines": self.comment_lines,
            "function_count": self.function_count,
            "class_count": self.class_count,
            "complexity": self.complexity,
            "dependencies": list(self.dependencies),
            "nested_depth": self.nested_depth
        }

class MetricsVisitor(ast.NodeVisitor):
    """AST visitor for collecting metrics."""
    
    def __init__(self):
        self.metrics = CodeMetrics()
        self.current_depth = 0
    
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit class definition."""
        self.metrics.class_count += 1
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definition."""
        # @probe:complexity 🧮 How would you measure complexity?
        # - What factors indicate complexity?
        # - How would you weight different factors?
        # - What other metrics would help?
        
        self.metrics.function_count += 1
        
        # Calculate complexity (simplified)
        complexity = 1  # Base complexity
        for child in ast.walk(node):
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        self.metrics.complexity += complexity
        self.generic_visit(node)
    
    def visit_Import(self, node: ast.Import) -> None:
        """Visit import statement."""
        for name in node.names:
            self.metrics.dependencies.add(name.name)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit from-import statement."""
        if node.module:
            self.metrics.dependencies.add(node.module)
        self.generic_visit(node)
    
    def generic_visit(self, node: ast.AST) -> None:
        """Visit a node."""
        self.current_depth += 1
        self.metrics.nested_depth = max(self.metrics.nested_depth, self.current_depth)
        super().generic_visit(node)
        self.current_depth -= 1

class BaseAnalyzer(ABC):
    """Base class for code analyzers."""
    
    @abstractmethod
    def analyze(self, content: str) -> CodeMetrics:
        """Analyze code content."""
        pass

class PythonAnalyzer(BaseAnalyzer):
    """Python code analyzer."""
    
    def analyze(self, content: str) -> CodeMetrics:
        """Analyze Python code."""
        tree = ast.parse(content)
        visitor = MetricsVisitor()
        visitor.visit(tree)
        
        # Count lines
        lines = content.splitlines()
        visitor.metrics.lines_of_code = len(lines)
        visitor.metrics.comment_lines = sum(
            1 for line in lines
            if line.strip().startswith("#")
        )
        
        return visitor.metrics

class AnalyzerFactory:
    """Factory for creating appropriate analyzer."""
    
    _analyzers: Dict[str, Type[BaseAnalyzer]] = {
        ".py": PythonAnalyzer
    }
    
    @classmethod
    def get_analyzer(cls, file_path: Union[str, Path]) -> Optional[BaseAnalyzer]:
        """Get appropriate analyzer for file type."""
        suffix = Path(file_path).suffix
        analyzer_class = cls._analyzers.get(suffix)
        return analyzer_class() if analyzer_class else None

class CodeAnalyzer:
    """Main code analyzer class."""
    
    def __init__(self, max_workers: int = None):
        self.max_workers = max_workers
    
    def analyze_file(self, file_path: Union[str, Path]) -> Optional[CodeMetrics]:
        """Analyze a single file."""
        file_path = Path(file_path)
        if not file_path.exists():
            print(f"File not found: {file_path}")
            return None
        
        analyzer = AnalyzerFactory.get_analyzer(file_path)
        if not analyzer:
            print(f"No analyzer available for: {file_path}")
            return None
        
        try:
            content = file_path.read_text()
            return analyzer.analyze(content)
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
            return None
    
    def analyze_directory(self, directory: Union[str, Path], pattern: str = "**/*.py") -> Dict[str, CodeMetrics]:
        """Analyze all matching files in directory."""
        directory = Path(directory)
        if not directory.is_dir():
            raise ValueError(f"Not a directory: {directory}")
        
        files = list(directory.glob(pattern))
        results = {}
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            future_to_file = {
                executor.submit(self.analyze_file, file): file
                for file in files
            }
            
            for future in concurrent.futures.as_completed(future_to_file):
                file = future_to_file[future]
                try:
                    metrics = future.result()
                    if metrics:
                        results[str(file)] = metrics
                except Exception as e:
                    print(f"Error processing {file}: {e}")
        
        return results

def main():
    """Main program."""
    analyzer = CodeAnalyzer()
    
    while True:
        print("\n🔍 Code Analyzer Menu:")
        print("1. Analyze File")
        print("2. Analyze Directory")
        print("3. Exit")
        
        choice = input("\nWhat would you like to do? (1-3): ")
        
        if choice == "1":
            file_path = input("Enter file path: ")
            metrics = analyzer.analyze_file(file_path)
            if metrics:
                print("\nAnalysis Results:")
                print(json.dumps(metrics.to_dict(), indent=2))
        
        elif choice == "2":
            directory = input("Enter directory path: ")
            pattern = input("Enter file pattern (default: **/*.py): ").strip() or "**/*.py"
            
            try:
                results = analyzer.analyze_directory(directory, pattern)
                print("\nAnalysis Results:")
                for file, metrics in results.items():
                    print(f"\n{file}:")
                    print(json.dumps(metrics.to_dict(), indent=2))
            except ValueError as e:
                print(f"Error: {e}")
        
        elif choice == "3":
            print("Goodbye! 👋")
            break
        
        else:
            print("Invalid choice! Please try again.")

if __name__ == "__main__":
    main()
