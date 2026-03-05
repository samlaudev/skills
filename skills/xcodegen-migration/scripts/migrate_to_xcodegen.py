#!/usr/bin/env python3
"""
XcodeGen Migration Assistant

Guided workflow for migrating iOS projects to XcodeGen.
Run with --assess-only to analyze a project without migration.
"""

import argparse
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def print_step(step: int, text: str):
    """Print a formatted step."""
    print(f"\n[{step}] {text}")
    print("-" * 60)


def prompt_yes_no(question: str) -> bool:
    """Prompt user for yes/no response."""
    while True:
        response = input(f"\n{question} [y/n]: ").strip().lower()
        if response in ['y', 'yes']:
            return True
        elif response in ['n', 'no']:
            return False
        print("Please enter 'y' or 'n'")


def find_xcodeproj() -> Optional[Path]:
    """Find the .xcodeproj file in current directory."""
    cwd = Path.cwd()
    xcodeprojs = list(cwd.glob("*.xcodeproj"))
    if not xcodeprojs:
        return None
    if len(xcodeprojs) == 1:
        return xcodeprojs[0]
    # Multiple projects - ask user
    print("Found multiple Xcode projects:")
    for i, proj in enumerate(xcodeprojs, 1):
        print(f"  {i}. {proj.name}")
    while True:
        try:
            choice = int(input("\nSelect project number: ")) - 1
            if 0 <= choice < len(xcodeprojs):
                return xcodeprojs[choice]
        except (ValueError, IndexError):
            pass
        print("Invalid choice. Try again.")


def check_xcodegen_installed() -> bool:
    """Check if XcodeGen is installed."""
    try:
        result = subprocess.run(
            ["xcodegen", "version"],
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def assess_project(project_path: Path) -> Dict:
    """Analyze the Xcode project and return assessment."""
    print_header("PROJECT ASSESSMENT")

    assessment = {
        "project_name": project_path.stem,
        "project_path": str(project_path),
        "targets": [],
        "dependencies": {"cocoapods": False, "carthage": False, "spm": False},
        "build_configs": [],
        "has_schemes": False,
        "complexity": "unknown"
    }

    print_step(1, "Checking for dependency managers...")

    # Check for CocoaPods
    if (Path.cwd() / "Podfile").exists():
        assessment["dependencies"]["cocoapods"] = True
        print("  ✓ CocoaPods detected (Podfile found)")

    # Check for Carthage
    cartfile_path = Path.cwd() / "Cartfile"
    cartfile_resolved = Path.cwd() / "Cartfile.resolved"
    carthage_build = Path.cwd() / "Carthage" / "Build"
    if cartfile_path.exists() or cartfile_resolved.exists() or carthage_build.exists():
        assessment["dependencies"]["carthage"] = True
        print("  ✓ Carthage detected")

    # Check for Swift Packages
    spm_packages = list((Path.cwd() / "Packages").glob("*")) if (Path.cwd() / "Packages").exists() else []
    if spm_packages:
        assessment["dependencies"]["spm"] = True
        print(f"  ✓ Swift Packages detected ({len(spm_packages)} local packages)")

    print_step(2, "Analyzing project structure...")

    # Convert to JSON for analysis
    try:
        result = subprocess.run(
            ["plutil", "-convert", "json", "-o", "-", str(project_path / "project.pbxproj")],
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode == 0:
            project_data = json.loads(result.stdout)

            # Extract targets
            pbx_native_targets = project_data.get("objects", {}).get("PBXNativeTarget", {})
            for target_id, target_data in pbx_native_targets.items():
                assessment["targets"].append({
                    "name": target_data.get("name", "Unknown"),
                    "type": target_data.get("productType", "unknown")
                })

            # Check for schemes (look in shared schemes dir)
            schemes_dir = project_path / "xcshareddata" / "xcschemes"
            assessment["has_schemes"] = schemes_dir.exists()

            # Determine complexity
            target_count = len(assessment["targets"])
            if target_count <= 3:
                assessment["complexity"] = "simple"
            elif target_count <= 8:
                assessment["complexity"] = "moderate"
            else:
                assessment["complexity"] = "complex"

    except (subprocess.TimeoutExpired, json.JSONDecodeError, KeyError) as e:
        print(f"  ⚠ Warning: Could not fully analyze project: {e}")

    return assessment


def print_assessment(assessment: Dict):
    """Print formatted assessment results."""
    print_header("ASSESSMENT RESULTS")

    print(f"\nProject: {assessment['project_name']}")
    print(f"Complexity: {assessment['complexity'].upper()}")
    print(f"Location: {assessment['project_path']}")

    print(f"\nTargets found: {len(assessment['targets'])}")
    for target in assessment['targets']:
        print(f"  - {target['name']} ({target['type']})")

    print(f"\nDependency Managers:")
    if assessment["dependencies"]["cocoapods"]:
        print("  ✓ CocoaPods")
    if assessment["dependencies"]["carthage"]:
        print("  ✓ Carthage")
    if assessment["dependencies"]["spm"]:
        print("  ✓ Swift Package Manager")
    if not any(assessment["dependencies"].values()):
        print("  None detected")

    print(f"\nSchemes: {'Yes' if assessment['has_schemes'] else 'No shared schemes found'}")

    # Provide migration guidance
    print_header("MIGRATION GUIDANCE")

    complexity = assessment["complexity"]
    if complexity == "simple":
        print("✓ This is a simple project. Migration should be straightforward.")
        print("  Estimated time: 30-60 minutes")
    elif complexity == "moderate":
        print("⚠ This is a moderate complexity project.")
        print("  Pay attention to custom build settings and scripts.")
        print("  Estimated time: 1-2 hours")
    else:
        print("⚠ This is a complex project with many targets.")
        print("  Consider migrating incrementally, target by target.")
        print("  Estimated time: 2-4 hours")

    print("\nRecommended next steps:")
    print("  1. Ensure XcodeGen is installed (see Step 2 in workflow)")
    print("  2. Create a backup branch before proceeding")
    print("  3. Run the full migration: python3 scripts/migrate_to_xcodegen.py")


def run_migration(assessment: Dict):
    """Guide user through the migration process."""
    print_header("XCODEGEN MIGRATION")

    print_step(1, "Verify XcodeGen installation")
    if not check_xcodegen_installed():
        print("⚠ XcodeGen is not installed!")
        print("\nInstall options:")
        print("  Mint:     mint install yonaskolb/xcodegen")
        print("  Homebrew: brew install xcodegen")
        print("  Manual:   git clone https://github.com/yonaskolb/XcodeGen.git")
        print("            cd XcodeGen && make install")
        if not prompt_yes_no("Continue anyway?"):
            sys.exit(1)
    else:
        result = subprocess.run(["xcodegen", "version"], capture_output=True, text=True)
        print(f"✓ XcodeGen installed: {result.stdout.strip()}")

    print_step(2, "Backup recommendation")
    print("Before proceeding, ensure you have:")
    print("  ✓ A clean git working directory")
    print("  ✓ A backup branch created")
    print("  ✓ Pushed all changes to remote")
    if not prompt_yes_no("Ready to continue?"):
        print("Migration cancelled. Complete prerequisites and run again.")
        sys.exit(0)

    print_step(3, "Generate initial project.yml")
    project_name = assessment["project_name"]
    project_path = Path(assessment["project_path"])

    print("\nChoose generation method:")
    print("  1. Use xcodegen migrate (requires spec-generation branch)")
    print("  2. Create project.yml manually from scratch")

    while True:
        choice = input("\nSelect method [1/2]: ").strip()
        if choice == "1":
            print("\nTo use the migrate command:")
            print("  1. Clone: git clone https://github.com/yonaskolb/XcodeGen.git -b spec-generation")
            print("  2. Install: cd XcodeGen && make install")
            print("  3. Run: xcodegen migrate --spec project.yml " + project_name + ".xcodeproj")
            print("\n⚠ The spec-generation branch may not always be up to date.")
            print("  Consider creating project.yml manually if it fails.")
            break
        elif choice == "2":
            print("\nManual creation steps:")
            print("  1. Use assets/ios_app_template.yml as a starting point")
            print("  2. Define your targets, sources, and dependencies")
            print("  3. Run: xcodegen generate")
            print("  4. Iterate and fix build issues")
            break

    print_step(4, "Post-generation checklist")
    print("\nAfter generating project.yml and running xcodegen generate:")
    print("  ✓ Build the project in Xcode")
    print("  ✓ Run unit tests")
    print("  ✓ Verify all schemes work")
    print("  ✓ Run: python3 scripts/verify_migration.py")
    print("  ✓ Set up git hooks: ./scripts/setup_git_hooks.sh")

    print_step(5, "Finalize migration")
    print("\nWhen everything works:")
    print("  1. Add *.xcodeproj to .gitignore")
    print("  2. Commit project.yml")
    print("  3. Remove .xcodeproj from git: git rm -r --cached *.xcodeproj")
    print("  4. Commit the changes")

    print_header("MIGRATION COMPLETE")
    print("\nFor troubleshooting, see SKILL.md Troubleshooting section.")


def main():
    parser = argparse.ArgumentParser(
        description="XcodeGen Migration Assistant",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 migrate_to_xcodegen.py --assess-only
  python3 migrate_to_xcodegen.py
        """
    )
    parser.add_argument(
        "--assess-only",
        action="store_true",
        help="Analyze project without performing migration"
    )
    parser.add_argument(
        "--project",
        type=str,
        help="Path to .xcodeproj file (auto-detected if not specified)"
    )

    args = parser.parse_args()

    # Find the project
    project_path = Path(args.project) if args.project else find_xcodeproj()
    if not project_path:
        print("Error: No .xcodeproj found in current directory.")
        print("Run this script from your iOS project root.")
        sys.exit(1)

    # Run assessment
    assessment = assess_project(project_path)

    if args.assess_only:
        print_assessment(assessment)
        return

    # Print assessment and proceed
    print_assessment(assessment)

    if prompt_yes_no("\nProceed with migration?"):
        run_migration(assessment)
    else:
        print("\nMigration cancelled. Run again when ready.")


if __name__ == "__main__":
    main()
