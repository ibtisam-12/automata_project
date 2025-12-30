"""
Clean File Organizer
A safe file organization utility.
This file contains no malware signatures.
"""

import os
from pathlib import Path
from typing import List, Dict
from datetime import datetime


class FileOrganizer:
    """Organize files by extension, size, or date."""
    
    def __init__(self, base_path: str):
        self.base_path = Path(base_path)
        self.file_categories = {
            'images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg'],
            'documents': ['.pdf', '.doc', '.docx', '.txt', '.odt'],
            'spreadsheets': ['.xls', '.xlsx', '.csv'],
            'videos': ['.mp4', '.avi', '.mkv', '.mov'],
            'audio': ['.mp3', '.wav', '.flac', '.aac'],
            'archives': ['.zip', '.rar', '.tar', '.gz'],
            'code': ['.py', '.js', '.java', '.cpp', '.c', '.html', '.css']
        }
    
    def categorize_file(self, filename: str) -> str:
        """Categorize a file based on its extension."""
        ext = Path(filename).suffix.lower()
        
        for category, extensions in self.file_categories.items():
            if ext in extensions:
                return category
        
        return 'others'
    
    def get_file_info(self, filepath: Path) -> Dict[str, any]:
        """Get information about a file."""
        if not filepath.exists():
            return None
        
        stats = filepath.stat()
        return {
            'name': filepath.name,
            'size': stats.st_size,
            'size_mb': stats.st_size / (1024 * 1024),
            'modified': datetime.fromtimestamp(stats.st_mtime),
            'category': self.categorize_file(filepath.name),
            'extension': filepath.suffix
        }
    
    def list_files_by_category(self, directory: Path) -> Dict[str, List[str]]:
        """List all files grouped by category."""
        if not directory.exists():
            print(f"Directory {directory} does not exist")
            return {}
        
        categorized = {}
        
        for item in directory.iterdir():
            if item.is_file():
                category = self.categorize_file(item.name)
                if category not in categorized:
                    categorized[category] = []
                categorized[category].append(item.name)
        
        return categorized
    
    def get_large_files(self, directory: Path, min_size_mb: float = 10) -> List[Dict]:
        """Find files larger than specified size."""
        large_files = []
        
        if not directory.exists():
            return large_files
        
        for item in directory.iterdir():
            if item.is_file():
                info = self.get_file_info(item)
                if info and info['size_mb'] > min_size_mb:
                    large_files.append(info)
        
        # Sort by size (largest first)
        large_files.sort(key=lambda x: x['size'], reverse=True)
        return large_files
    
    def get_statistics(self, directory: Path) -> Dict[str, any]:
        """Get statistics about files in directory."""
        if not directory.exists():
            return {}
        
        total_files = 0
        total_size = 0
        category_counts = {}
        
        for item in directory.iterdir():
            if item.is_file():
                total_files += 1
                info = self.get_file_info(item)
                if info:
                    total_size += info['size']
                    category = info['category']
                    category_counts[category] = category_counts.get(category, 0) + 1
        
        return {
            'total_files': total_files,
            'total_size_mb': total_size / (1024 * 1024),
            'category_counts': category_counts
        }


def demo():
    """Demonstrate file organizer functionality."""
    print("File Organizer Demo")
    print("=" * 60)
    
    # Create organizer for current directory
    organizer = FileOrganizer(".")
    current_dir = Path(".")
    
    # Get statistics
    stats = organizer.get_statistics(current_dir)
    print(f"\nDirectory Statistics:")
    print(f"  Total Files: {stats.get('total_files', 0)}")
    print(f"  Total Size: {stats.get('total_size_mb', 0):.2f} MB")
    
    # Show category distribution
    print("\nFiles by Category:")
    for category, count in stats.get('category_counts', {}).items():
        print(f"  {category}: {count}")
    
    # List files by category
    categorized = organizer.list_files_by_category(current_dir)
    print("\nFile Listing by Category:")
    for category, files in categorized.items():
        print(f"\n{category.upper()}:")
        for filename in files[:5]:  # Show first 5 files
            print(f"  - {filename}")
        if len(files) > 5:
            print(f"  ... and {len(files) - 5} more")


if __name__ == "__main__":
    demo()
