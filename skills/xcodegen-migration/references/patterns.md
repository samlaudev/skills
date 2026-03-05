# XcodeGen Migration Patterns

Common patterns and solutions for typical migration challenges.

## Pattern: Incremental Migration

**Problem**: Large projects are overwhelming to migrate all at once.

**Solution**: Migrate incrementally, target by target.

1. Start with `xcodegen migrate` to get ~80% done
2. Focus on getting one target (usually the main app) working
3. Test build for that target
4. Move to the next target
5. Repeat until all targets build

```yaml
# Start with minimal configuration
targets:
  MyApp:
    type: application
    platform: iOS
    sources: MyApp
    # Add settings, dependencies incrementally
```

## Pattern: Legacy Project with Custom Build Settings

**Problem**: Old projects have accumulated many custom build settings.

**Solution**: Extract and categorize settings systematically.

1. Convert project to JSON: `plutil -convert json -o -- project.pbxproj > project.json`
2. Identify custom settings (not starting with SDK defaults)
3. Categorize by: code signing, paths, compiler flags, other
4. Add to `project.yml` under appropriate config

```yaml
targets:
  MyApp:
    settings:
      configs:
        Debug:
          # Code signing
          CODE_SIGN_IDENTITY: iPhone Developer
          DEVELOPMENT_TEAM: ABC123
          # Paths
          HEADER_SEARCH_PATHS: "$(SRCROOT)/Headers"
          # Compiler
          OTHER_SWIFT_FLAGS: "-DDEBUG"
```

## Pattern: Workspace with Multiple Projects

**Problem**: Project references multiple other `.xcodeproj` files.

**Solution**: Use project references.

```yaml
projectReferences:
  FrameworkA:
    path: Frameworks/FrameworkA.xcodeproj
  FrameworkB:
    path: Frameworks/FrameworkB.xcodeproj

targets:
  MyApp:
    dependencies:
      - target: FrameworkA/FrameworkA
      - target: FrameworkB/FrameworkB
```

## Pattern: Mixed Dependency Managers

**Problem**: Projects using CocoaPods, Carthage, and SPM together.

**Solution**: Configure each independently and let XcodeGen handle linking.

```yaml
packages:
  SomeSPMPackage:
    url: https://github.com/example/package
    from: 1.0.0

targets:
  MyApp:
    dependencies:
      # CocoaPods: handled by Podfile, no spec needed
      - carthage: Alamofire
      - carthage: Result
        findFrameworks: true
      - package: SomeSPMPackage
      - framework: Carthage/Build/iOS/ManualFramework.framework
      - sdk: Contacts.framework
```

## Pattern: Multiple Schemes for Environments

**Problem**: Different build configurations for dev, staging, production.

**Solution**: Use scheme config variants.

```yaml
configs:
  Dev Debug: debug
  Dev Release: release
  Staging Debug: debug
  Staging Release: release
  Prod Debug: debug
  Prod Release: release

targets:
  MyApp:
    scheme:
      configVariants: [Dev, Staging, Prod]
      testTargets: [MyAppTests]
      environmentVariables:
        API_ENDPOINT:
          Dev: https://dev.api.com
          Staging: https://staging.api.com
          Prod: https://api.com
```

## Pattern: Shared Framework Across Apps

**Problem**: Multiple apps sharing a common framework.

**Solution**: Use a workspace with project references.

```
MyWorkspace/
├── Apps/
│   ├── App1/
│   │   └── project.yml
│   └── App2/
│       └── project.yml
└── Frameworks/
    └── SharedFramework/
        └── project.yml
```

Each app's `project.yml` references the framework:

```yaml
projectReferences:
  SharedFramework:
    path: ../Frameworks/SharedFramework/SharedFramework.xcodeproj

targets:
  App1:
    dependencies:
      - target: SharedFramework/SharedFramework
```

## Pattern: Generated Code in Separate Directory

**Problem**: Generated code should be excluded from version control and groups.

**Solution**: Use `excludes` and separate source directories.

```yaml
targets:
  MyApp:
    sources:
      - MyApp
      - path: Generated
        excludes:
          - "*.generated.swift"
        buildPhase: none  # Don't add to build phase

# Or completely exclude
targets:
  MyApp:
    sources:
      - path: MyApp
        excludes:
          - "Generated/**/*"
```

## Pattern: Custom Build Rules

**Problem**: Custom file types need special processing.

**Solution**: Define build rules.

```yaml
targets:
  MyApp:
    buildRules:
      - filePattern: "*.graphql"
        script: graphql-codegen
        outputFiles:
          - $(DERIVED_FILE_DIR)/Generated/API.swift
      - fileType: sourcecode.swift
        script: preprocess_swift.py
```

## Pattern: Conditional Compilation

**Problem**: Different code for different targets/configurations.

**Solution**: Use build settings with conditionals.

```yaml
targets:
  MyApp:
    settings:
      base:
        MY_FEATURE_ENABLED: YES
      configs:
        Debug:
          MY_FEATURE_ENABLED: NO
        Release:
          MY_FEATURE_ENABLED: YES

# In Swift code:
#if MY_FEATURE_ENABLED
// Feature code
#endif
```

## Pattern: Resource Bundles

**Problem**: Multiple resource bundles for different modules.

**Solution**: Use bundle targets.

```yaml
targets:
  MyAppResources:
    type: bundle
    platform: iOS
    sources:
      - Resources/Assets
      - Resources/Strings

  MyApp:
    dependencies:
      - bundle: MyAppResources
```

## Pattern: Complex Pre-Build Setup

**Problem**: Need to run scripts before compilation.

**Solution**: Use preBuildScripts.

```yaml
targets:
  MyApp:
    preBuildScripts:
      - name: Generate Code
        script: |
          ./scripts/generate.sh
          echo "Code generated"
        inputFiles:
          - $(SRCROOT)/templates/*.stencil
        outputFiles:
          - $(SRCROOT)/Generated/*.swift
        basedOnDependencyAnalysis: true  # Skip if inputs unchanged
```

## Pattern: Legacy Objective-C Project

**Problem**: Mixed ObjC/Swift project with bridging header.

**Solution**: Configure header visibility and bridging.

```yaml
targets:
  MyApp:
    sources:
      - path: MyApp
        headerVisibility: public  # For frameworks
        excludes:
          - "*-Private.h"
    settings:
      base:
        SWIFT_OBJC_BRIDGING_HEADER: MyApp/MyApp-Bridging-Header.h
```

## Pattern: Testing with Different Configurations

**Problem**: Tests need different settings than main app.

**Solution**: Override settings in test target.

```yaml
targets:
  MyAppTests:
    type: bundle.unit-test
    platform: iOS
    sources: Tests
    settings:
      base:
        TEST_HOST: $(BUILT_PRODUCTS_DIR)/MyApp.app/MyApp
        BUNDLE_LOADER: $(TEST_HOST)
```

## Troubleshooting Common Issues

### "No such module" error

- Check framework search paths in build settings
- Verify Carthage frameworks are built
- Ensure SPM packages are resolved

### Code signing issues

- Add development team to settings
- Configure provisioning profile specifier
- Check entitlements file path

### Missing Info.plist

- Add `INFOPLIST_FILE` to target settings
- Or let XcodeGen generate it with `info` property

### Schemes not appearing

- Add `scheme` section to target
- Or define top-level `schemes` section
- Check scheme management settings

### Wrong file in wrong build phase

- Override with `buildPhase` property on source
- Options: `sources`, `resources`, `headers`, `copyFiles`, `none`
