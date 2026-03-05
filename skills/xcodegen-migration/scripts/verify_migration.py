#!/usr/bin/env python3
"""
XcodeGen Migration Verification Tool

Compares original and generated Xcode projects to identify
missing build settings, scripts, and file differences.
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple


def print_header(text: str):
    """Print a formatted header."""
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def load_project_json(json_path: Path) -> Dict:
    """Load project JSON file."""
    try:
        with open(json_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Error: File not found: {json_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON in {json_path}: {e}")
        sys.exit(1)


def extract_targets(project_data: Dict) -> Dict[str, Dict]:
    """Extract targets from project data."""
    targets = {}
    objects = project_data.get("objects", {})

    for obj_id, obj_data in objects.get("PBXNativeTarget", {}).items():
        name = obj_data.get("name", "Unknown")
        targets[name] = {
            "id": obj_id,
            "type": obj_data.get("productType", "unknown"),
            "build_configurations": obj_data.get("buildConfigurations", [])
        }

    return targets


def extract_build_settings(project_data: Dict, target_name: str = None) -> Dict[str, Dict]:
    """Extract build settings from project."""
    settings = {}
    objects = project_data.get("objects", {})

    for obj_id, obj_data in objects.get("XCBuildConfiguration", {}).items():
        name = obj_data.get("name", "unknown")
        settings[name] = obj_data.get("buildSettings", {})

    return settings


def extract_build_scripts(project_data: Dict) -> List[Dict]:
    """Extract build scripts from project."""
    scripts = []
    objects = project_data.get("objects", {})

    for obj_id, obj_data in objects.get("PBXShellScriptBuildPhase", {}).items():
        scripts.append({
            "id": obj_id,
            "name": obj_data.get("name", "Unnamed Script"),
            "script": obj_data.get("shellScript", ""),
            "inputFiles": obj_data.get("inputPaths", []),
            "outputFiles": obj_data.get("outputPaths", [])
        })

    return scripts


def extract_file_references(project_data: Dict) -> Dict[str, str]:
    """Extract file references from project."""
    files = {}
    objects = project_data.get("objects", {})

    for obj_id, obj_data in objects.get("PBXFileReference", {}).items():
        path = obj_data.get("path", "")
        if path:
            files[obj_id] = path

    return files


def extract_groups(project_data: Dict) -> Dict[str, Dict]:
    """Extract group structure from project."""
    groups = {}
    objects = project_data.get("objects", {})

    for obj_id, obj_data in objects.get("PBXGroup", {}).items():
        name = obj_data.get("name", obj_data.get("path", "Unknown"))
        groups[name] = {
            "id": obj_id,
            "children": obj_data.get("children", []),
            "sourceTree": obj_data.get("sourceTree", "")
        }

    return groups


def compare_build_settings(original: Dict, generated: Dict) -> Tuple[Set[str], Set[str]]:
    """Compare build settings and return (missing_in_generated, added_in_generated)."""
    missing = set()
    added = set()

    all_configs = set(original.keys()) | set(generated.keys())

    for config in all_configs:
        orig_settings = original.get(config, {})
        gen_settings = generated.get(config, {})

        # Check for missing settings
        for key in orig_settings:
            if key not in gen_settings:
                missing.add(f"{config}.{key}")

        # Check for added settings
        for key in gen_settings:
            if key not in orig_settings:
                added.add(f"{config}.{key}")

    return missing, added


def compare_scripts(original: List[Dict], generated: List[Dict]) -> Tuple[List[Dict], List[Dict]]:
    """Compare build scripts."""
    orig_by_name = {s["name"]: s for s in original}
    gen_by_name = {s["name"]: s for s in generated}

    missing = []
    for name, script in orig_by_name.items():
        if name not in gen_by_name:
            missing.append(script)

    added = []
    for name, script in gen_by_name.items():
        if name not in orig_by_name:
            added.append(script)

    return missing, added


def print_build_settings_comparison(missing: Set[str], added: Set[str]):
    """Print build settings comparison."""
    print_header("BUILD SETTINGS COMPARISON")

    if missing:
        print(f"\n⚠ Missing in generated project ({len(missing)}):")
        for setting in sorted(missing):
            print(f"  - {setting}")
    else:
        print("\n✓ All original build settings present")

    if added:
        print(f"\nℹ Added in generated project ({len(added)}):")
        for setting in sorted(added):
            print(f"  + {setting}")
    else:
        print("\n✓ No unexpected build settings added")


def print_scripts_comparison(missing: List[Dict], added: List[Dict]):
    """Print build scripts comparison."""
    print_header("BUILD SCRIPTS COMPARISON")

    if missing:
        print(f"\n⚠ Missing scripts ({len(missing)}):")
        for script in missing:
            name = script["name"]
            script_preview = script["script"][:50].replace("\n", " ")
            print(f"  - {name}")
            print(f"    {script_preview}...")
    else:
        print("\n✓ All build scripts present")

    if added:
        print(f"\nℹ Added scripts ({len(added)}):")
        for script in added:
            print(f"  + {script['name']}")
    else:
        print("\n✓ No unexpected scripts added")


def print_file_count_comparison(original_files: Dict, generated_files: Dict):
    """Print file count comparison."""
    print_header("FILE REFERENCES")

    orig_count = len(original_files)
    gen_count = len(generated_files)

    print(f"\nOriginal project:  {orig_count} file references")
    print(f"Generated project: {gen_count} file references")
    print(f"Difference:        {gen_count - orig_count:+d}")

    if gen_count < orig_count:
        print("\n⚠ Generated project has fewer files!")
        print("  This may be normal if XcodeGen is using directory references.")
    elif gen_count > orig_count:
        print("\nℹ Generated project has more files.")
        print("  This may include auto-generated files.")


def print_recommendations(missing_settings: Set[str], missing_scripts: List[Dict]):
    """Print migration recommendations."""
    print_header("RECOMMENDATIONS")

    if not missing_settings and not missing_scripts:
        print("\n✓ Migration looks complete!")
        print("  Your generated project should work correctly.")
        return

    print("\nReview the following:")

    if missing_settings:
        print("\n1. Missing build settings:")
        print("   Add these to your project.yml under target settings:")
        for setting in list(missing_settings)[:5]:
            config, key = setting.split(".", 1)
            print(f"     {key}: <value>  # Missing in {config}")
        if len(missing_settings) > 5:
            print(f"     ... and {len(missing_settings) - 5} more")

    if missing_scripts:
        print("\n2. Missing build scripts:")
        print("   Add these to your project.yml target:")
        for script in missing_scripts[:3]:
            name = script["name"]
            print(f"     postBuildScripts:")
            print(f"       - name: {name}")
            print(f"         script: |")
            print(f"           {script['script'][:50].strip()}...")
        if len(missing_scripts) > 3:
            print(f"     ... and {len(missing_scripts) - 3} more")

    print("\n3. Common fixes:")
    print("   - CODE_SIGN_ENTITLEMENTS: Add to target settings")
    print("   - INFOPLIST_FILE: Add to target settings")
    print("   - PRODUCT_BUNDLE_IDENTIFIER: Add to config settings")


def main():
    parser = argparse.ArgumentParser(
        description="Verify XcodeGen migration by comparing projects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Generate JSON files for comparison:
  plutil -convert json -o -- Original.xcodeproj/project.pbxproj | python3 -m json.tool > original.json
  plutil -convert json -o -- Generated.xcodeproj/project.pbxproj | python3 -m json.tool > generated.json

Examples:
  python3 verify_migration.py original.json generated.json
        """
    )
    parser.add_argument("original", help="Path to original project JSON")
    parser.add_argument("generated", help="Path to generated project JSON")

    args = parser.parse_args()

    # Load projects
    original_project = load_project_json(Path(args.original))
    generated_project = load_project_json(Path(args.generated))

    # Extract data
    print_header("LOADING PROJECT DATA")

    orig_settings = extract_build_settings(original_project)
    gen_settings = extract_build_settings(generated_project)

    orig_scripts = extract_build_scripts(original_project)
    gen_scripts = extract_build_scripts(generated_project)

    orig_files = extract_file_references(original_project)
    gen_files = extract_file_references(generated_project)

    # Compare
    missing_settings, added_settings = compare_build_settings(orig_settings, gen_settings)
    missing_scripts, added_scripts = compare_scripts(orig_scripts, gen_scripts)

    # Print results
    print_build_settings_comparison(missing_settings, added_settings)
    print_scripts_comparison(missing_scripts, added_scripts)
    print_file_count_comparison(orig_files, gen_files)
    print_recommendations(missing_settings, missing_scripts)

    # Exit with appropriate code
    if missing_settings or missing_scripts:
        print_header("VERIFICATION INCOMPLETE")
        print("\n⚠ Issues found that need attention.")
        print("  Update project.yml and run xcodegen generate again.")
        sys.exit(1)
    else:
        print_header("VERIFICATION PASSED")
        print("\n✓ Projects match closely!")
        print("  Ready to test building the generated project.")
        sys.exit(0)


if __name__ == "__main__":
    main()
