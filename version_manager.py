#!/usr/bin/env python3
"""
Automated Version Management for Streamlit-Theta

This script provides automated version management including:
- Auto-increment version numbers
- Changelog generation
- Git tagging
- PyPI publishing preparation
"""

import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

class VersionManager:
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.pyproject_path = self.repo_path / "pyproject.toml"
        self.init_path = self.repo_path / "streamlit_theta" / "__init__.py"
        self.changelog_path = self.repo_path / "CHANGELOG.md"
        
    def get_current_version(self) -> str:
        """Get current version from pyproject.toml"""
        with open(self.pyproject_path, 'r') as f:
            content = f.read()
        
        version_match = re.search(r'version = "([^"]+)"', content)
        if version_match:
            return version_match.group(1)
        raise ValueError("Version not found in pyproject.toml")
    
    def increment_version(self, version_type: str = "patch") -> str:
        """Increment version number"""
        current_version = self.get_current_version()
        major, minor, patch = map(int, current_version.split('.'))
        
        if version_type == "major":
            major += 1
            minor = 0
            patch = 0
        elif version_type == "minor":
            minor += 1
            patch = 0
        elif version_type == "patch":
            patch += 1
        else:
            raise ValueError("version_type must be 'major', 'minor', or 'patch'")
        
        return f"{major}.{minor}.{patch}"
    
    def update_version_files(self, new_version: str):
        """Update version in pyproject.toml and __init__.py"""
        current_version = self.get_current_version()
        
        # Update pyproject.toml
        with open(self.pyproject_path, 'r') as f:
            content = f.read()
        
        content = content.replace(
            f'version = "{current_version}"',
            f'version = "{new_version}"'
        )
        
        with open(self.pyproject_path, 'w') as f:
            f.write(content)
        
        # Update __init__.py
        with open(self.init_path, 'r') as f:
            content = f.read()
        
        content = content.replace(
            f'__version__ = "{current_version}"',
            f'__version__ = "{new_version}"'
        )
        
        with open(self.init_path, 'w') as f:
            f.write(content)
    
    def get_git_commits_since_last_tag(self) -> List[str]:
        """Get commits since last tag"""
        try:
            # Get last tag
            result = subprocess.run(
                ["git", "describe", "--tags", "--abbrev=0"],
                capture_output=True,
                text=True,
                cwd=self.repo_path
            )
            last_tag = result.stdout.strip()
            
            # Get commits since last tag
            result = subprocess.run(
                ["git", "log", f"{last_tag}..HEAD", "--oneline"],
                capture_output=True,
                text=True,
                cwd=self.repo_path
            )
            
            return result.stdout.strip().split('\n') if result.stdout.strip() else []
        except:
            # If no tags exist, get all commits
            result = subprocess.run(
                ["git", "log", "--oneline"],
                capture_output=True,
                text=True,
                cwd=self.repo_path
            )
            return result.stdout.strip().split('\n') if result.stdout.strip() else []
    
    def categorize_commits(self, commits: List[str]) -> Dict[str, List[str]]:
        """Categorize commits by type"""
        categories = {
            "Features": [],
            "Bug Fixes": [],
            "Documentation": [],
            "Performance": [],
            "Other": []
        }
        
        for commit in commits:
            if not commit.strip():
                continue
                
            commit_lower = commit.lower()
            
            if any(keyword in commit_lower for keyword in ["feat", "feature", "add", "implement"]):
                categories["Features"].append(commit)
            elif any(keyword in commit_lower for keyword in ["fix", "bug", "resolve", "patch"]):
                categories["Bug Fixes"].append(commit)
            elif any(keyword in commit_lower for keyword in ["doc", "readme", "documentation"]):
                categories["Documentation"].append(commit)
            elif any(keyword in commit_lower for keyword in ["perf", "performance", "optimize"]):
                categories["Performance"].append(commit)
            else:
                categories["Other"].append(commit)
        
        return categories
    
    def generate_changelog_entry(self, version: str, commits: List[str]) -> str:
        """Generate changelog entry for new version"""
        today = datetime.now().strftime("%Y-%m-%d")
        categorized = self.categorize_commits(commits)
        
        changelog_entry = f"\n## [{version}] - {today}\n\n"
        
        for category, commit_list in categorized.items():
            if commit_list:
                changelog_entry += f"### {category}\n\n"
                for commit in commit_list:
                    # Remove commit hash and clean up
                    commit_clean = re.sub(r'^[a-f0-9]+\s+', '', commit)
                    changelog_entry += f"- {commit_clean}\n"
                changelog_entry += "\n"
        
        return changelog_entry
    
    def update_changelog(self, version: str, commits: List[str]):
        """Update CHANGELOG.md with new version"""
        if not self.changelog_path.exists():
            # Create new changelog
            changelog_content = "# Changelog\n\nAll notable changes to this project will be documented in this file.\n"
        else:
            with open(self.changelog_path, 'r') as f:
                changelog_content = f.read()
        
        # Generate new entry
        new_entry = self.generate_changelog_entry(version, commits)
        
        # Insert new entry after the header
        lines = changelog_content.split('\n')
        header_end = 0
        for i, line in enumerate(lines):
            if line.startswith('## '):
                header_end = i
                break
        
        if header_end == 0:
            # No existing entries, add after header
            for i, line in enumerate(lines):
                if line.strip() == '' and i > 0:
                    header_end = i
                    break
        
        lines.insert(header_end, new_entry)
        
        with open(self.changelog_path, 'w') as f:
            f.write('\n'.join(lines))
    
    def create_git_tag(self, version: str):
        """Create git tag for version"""
        try:
            subprocess.run(
                ["git", "tag", f"v{version}"],
                cwd=self.repo_path,
                check=True
            )
            print(f"✅ Created git tag v{version}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to create git tag v{version}")
    
    def commit_version_changes(self, version: str):
        """Commit version changes"""
        try:
            subprocess.run(
                ["git", "add", "pyproject.toml", "streamlit_theta/__init__.py", "CHANGELOG.md"],
                cwd=self.repo_path,
                check=True
            )
            subprocess.run(
                ["git", "commit", "-m", f"Bump version to {version}"],
                cwd=self.repo_path,
                check=True
            )
            print(f"✅ Committed version changes for {version}")
        except subprocess.CalledProcessError:
            print(f"❌ Failed to commit version changes")
    
    def release(self, version_type: str = "patch", dry_run: bool = False):
        """Create a new release"""
        current_version = self.get_current_version()
        new_version = self.increment_version(version_type)
        
        print(f"🚀 Creating release: {current_version} → {new_version}")
        
        if dry_run:
            print("🔍 DRY RUN MODE - No changes will be made")
        
        # Get commits since last tag
        commits = self.get_git_commits_since_last_tag()
        
        if not commits or (len(commits) == 1 and not commits[0].strip()):
            print("ℹ️  No new commits since last release")
            return
        
        print(f"📝 Found {len(commits)} commits since last release")
        
        if not dry_run:
            # Update version files
            self.update_version_files(new_version)
            print(f"✅ Updated version files to {new_version}")
            
            # Update changelog
            self.update_changelog(new_version, commits)
            print(f"✅ Updated changelog")
            
            # Commit changes
            self.commit_version_changes(new_version)
            
            # Create tag
            self.create_git_tag(new_version)
            
            print(f"🎉 Release {new_version} created successfully!")
            print(f"💡 Next steps:")
            print(f"   - Review changes: git show v{new_version}")
            print(f"   - Push changes: git push origin main")
            print(f"   - Push tag: git push origin v{new_version}")
        else:
            print(f"📋 Would create release {new_version} with {len(commits)} commits")

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Automated version management for Streamlit-Theta")
    parser.add_argument("--type", choices=["major", "minor", "patch"], default="patch",
                        help="Type of version increment")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done without making changes")
    parser.add_argument("--current", action="store_true", help="Show current version")
    
    args = parser.parse_args()
    
    manager = VersionManager()
    
    if args.current:
        print(f"Current version: {manager.get_current_version()}")
        return
    
    manager.release(args.type, args.dry_run)

if __name__ == "__main__":
    main()