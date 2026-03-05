---
name: xcodegen-migration
description: Migrate existing iOS projects to XcodeGen to eliminate .xcodeproj merge conflicts, improve project maintainability, and streamline release processes. Use when migrating an existing iOS project to XcodeGen, setting up XcodeGen for a new iOS project, troubleshooting XcodeGen migration issues, or converting legacy Xcode project files to project.yml
---

# XcodeGen Migration

Migrate iOS projects from traditional `.xcodeproj` files to XcodeGen's YAML-based configuration. Eliminate merge conflicts, improve code reviewability, and simplify release management.

## Overview

XcodeGen generates `.xcodeproj` files from a human-readable `project.yml` configuration. This skill guides you through migrating existing iOS projects, following the proven methodology used to migrate a decade-old iOS app with 1,800+ commits.

**Benefits:**
- No more `.xcodeproj` merge conflicts
- Human-readable, git-friendly configuration
- Automatic group/file synchronization with disk
- Easier code review of project changes
- Streamlined release branch management

## Prerequisites

Before starting, verify:
- Xcode command line tools installed
- Python 3.6+ (for verification scripts)
- Git repository with iOS project

**★ Insight ─────────────────────────────────────**
XcodeGen's spec-generation branch provides a reverse-generation tool that handles ~80% of migration automatically. The remaining 20% involves manual verification of build settings, scripts, and folder structures.
─────────────────────────────────────────────────

## Migration Workflow

### Step 1: Pre-Migration Assessment

Analyze the existing project to understand complexity and dependencies.

**Run the assessment:**
```bash
python3 scripts/migrate_to_xcodegen.py --assess-only
```

**Document:**
1. All targets (app, frameworks, tests, extensions)
2. Build configurations (Debug, Release, custom)
3. Dependency managers: CocoaPods, Carthage, Swift Package Manager
4. Custom build scripts (Build Phases)
5. Special build settings (code signing, entitlements, etc.)

### Step 2: Install XcodeGen

Choose an installation method:

**Mint (recommended):**
```bash
mint install yonaskolb/xcodegen
```

**Homebrew:**
```bash
brew install xcodegen
```

**Manual:**
```bash
git clone https://github.com/yonaskolb/XcodeGen.git
cd XcodeGen
make install
```

### Step 3: Reverse-Generate Initial project.yml

Use XcodeGen's migrate command to generate the initial `project.yml`:

**From spec-generation branch:**
```bash
# Clone spec-generation branch
git clone https://github.com/yonaskolb/XcodeGen.git -b spec-generation
cd XcodeGen
make install

# Run migrate from project root
xcodegen migrate --spec project.yml YourProject.xcodeproj
```

This handles ~80% of the work automatically. Common issues to fix:
- Folder structure references
- Missing source files
- Incorrect target dependencies

### Step 4: Verify Build Settings

Convert projects to JSON for comparison:

```bash
# Original project
plutil -convert json -o -- YourProject.xcodeproj/project.pbxproj | python3 -m json.tool > original_project.json

# Generated project (after running xcodegen generate)
plutil -convert json -o -- YourProject.xcodeproj/project.pbxproj | python3 -m json.tool > generated_project.json
```

**Run verification script:**
```bash
python3 scripts/verify_migration.py original_project.json generated_project.json
```

This identifies:
- Missing build settings
- Differences in build scripts
- File/folder structure mismatches

### Step 5: Generate and Validate

**Generate the project:**
```bash
xcodegen generate
```

**Validate by building:**
```bash
# Build all schemes
xcodebuild -workspace YourProject.xcworkspace -scheme YourScheme clean build

# Or open in Xcode and test
open YourProject.xcodeproj
```

**Test:**
1. Clean build for each configuration
2. Run unit tests
3. Verify app launches
4. Check all schemes work

### Step 6: Optimize project.yml

Consolidate common settings using base configurations:

```yaml
settings:
  base:
    PRODUCT_NAME: MyProduct
    SWIFT_VERSION: 5.0
  configs:
    debug:
      CODE_SIGN_IDENTITY: iPhone Developer
      PRODUCT_BUNDLE_IDENTIFIER: com.myapp.debug
    release:
      CODE_SIGN_IDENTITY: iPhone Distribution
      PRODUCT_BUNDLE_IDENTIFIER: com.myapp.app
```

### Step 7: Set Up Git Hooks

Prevent merge conflicts by regenerating on branch operations:

```bash
# Install hooks
./scripts/setup_git_hooks.sh
```

This adds:
- Post-checkout hook to regenerate when switching branches
- Post-merge hook to regenerate after merging
- Pre-commit hook to ensure project is up-to-date

### Step 8: Commit and Ignore

**Add to .gitignore:**
```
*.xcodeproj
!project.yml
```

**Commit the migration:**
```bash
git add project.yml .gitignore .git/hooks/
git commit -m "Migrate to XcodeGen"
```

**Delete .xcodeproj from git:**
```bash
git rm -r --cached YourProject.xcodeproj
git commit -m "Remove .xcodeproj from version control"
```

## Dependency Management

### CocoaPods

Continue using your Podfile normally. After generating the project:

```bash
pod install
```

XcodeGen integrates with CocoaPods automatically. The generated project works with the workspace created by CocoaPods.

### Carthage

Reference Carthage dependencies in `project.yml`:

```yaml
targets:
  MyApp:
    dependencies:
      - carthage: Alamofire
      - carthage: Result
        findFrameworks: true  # Auto-discover multiple frameworks
```

XcodeGen automatically:
- Links frameworks
- Creates copy-frameworks build phase
- Adds FRAMEWORK_SEARCH_PATHS

### Swift Package Manager

Define packages at project level:

```yaml
packages:
  Yams:
    url: https://github.com/jpsim/Yams
    from: 2.0.0

targets:
  MyApp:
    dependencies:
      - package: Yams
      - package: Yams
        product: YamsFramework  # If different from package name
```

## Troubleshooting

### Project Won't Build

1. **Missing build settings**: Compare JSON outputs from Step 4
2. **Wrong file paths**: Check source paths in `project.yml`
3. **Missing frameworks**: Verify dependencies are correctly specified

### Merge Conflicts During Migration

If conflicts occur before completion:
1. Complete migration on main branch
2. Have team members rebase onto main
3. Delete old `.xcodeproj` from git history

### Schemes Missing

Add scheme definitions to `project.yml`:

```yaml
targets:
  MyApp:
    scheme:
      configVariants: [Debug, Release]
      testTargets: [MyAppTests]
```

## Verification

After migration, verify:

- [ ] All targets build successfully
- [ ] All schemes appear in Xcode
- [ ] Unit tests pass
- [ ] App launches and runs
- [ ] Git hooks are installed
- [ ] `.xcodeproj` is in `.gitignore`
- [ ] `project.yml` is committed
- [ ] Team can regenerate project with `xcodegen generate`

## Resources

### scripts/migrate_to_xcodegen.py

Guided migration script with:
- Pre-migration assessment
- XcodeGen installation check
- Interactive migration steps

### scripts/verify_migration.py

Build settings verification:
- Compare original vs generated projects
- Identify missing settings
- List discrepancies

### scripts/setup_git_hooks.sh

Git hooks installation:
- Post-checkout: Regenerate on branch switch
- Post-merge: Regenerate after merges
- Pre-commit: Verify project is current

### references/spec.md

Condensed ProjectSpec reference for common fields and patterns.

### references/patterns.md

Common migration patterns and solutions for typical issues.

### assets/ios_app_template.yml

Example `project.yml` for iOS app with:
- Multiple targets (app, tests, frameworks)
- All dependency managers (CocoaPods, Carthage, SPM)
- Common build settings
- Scheme configurations
