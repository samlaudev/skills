# XcodeGen ProjectSpec Quick Reference

Essential fields for migrating iOS projects to XcodeGen.

## Core Project Structure

```yaml
name: MyApp                    # Required: Project name
options:
  bundleIdPrefix: com.myapp    # Auto-generate bundle IDs
  deploymentTarget:            # Project-wide deployment targets
    iOS: "13.0"
  createIntermediateGroups: true
  carthageBuildPath: Carthage/Build
  postGenCommand: pod install  # Run after project generation

configs:                       # Build configurations
  Debug: debug
  Release: release

targets:
  MyApp:
    type: application
    platform: iOS
    deploymentTarget: "13.0"
    sources: MyApp
```

## Common Target Types

- `application` - iOS app
- `framework` - Framework
- `library.static` - Static library
- `library.dynamic` - Dynamic library
- `bundle.unit-test` - Unit tests
- `bundle.ui-testing` - UI tests
- `app-extension` - App extension
- `watchkit2-extension` - WatchKit extension

## Platform Values

- `iOS` - iOS platform
- `tvOS` - tvOS platform
- `macOS` - macOS platform
- `watchOS` - watchOS platform
- `visionOS` - visionOS platform

## Sources Configuration

```yaml
targets:
  MyApp:
    sources:
      - MyApp                      # Simple directory reference
      - path: Frameworks/Something  # Explicit path
        name: Something             # Custom display name
        group: Frameworks           # Parent group
        excludes:                  # Exclude patterns
          - "**/*.md"
          - "Tests/*"
        compilerFlags: "-werror -Xswiftc -frontend"
        buildPhase: resources       # Override default build phase
```

## Build Settings

```yaml
targets:
  MyApp:
    settings:
      base:                        # Applied to all configs
        PRODUCT_NAME: MyApp
        SWIFT_VERSION: 5.0
        IPHONEOS_DEPLOYMENT_TARGET: "13.0"
      configs:
        Debug:
          DEBUG_MODE: YES
          SWIFT_OPTIMIZATION_LEVEL: -Onone
        Release:
          SWIFT_OPTIMIZATION_LEVEL: -O
          VALIDATE_PRODUCT: YES
```

## Dependencies

### CocoaPods
```yaml
# No spec changes needed - use Podfile normally
# After xcodegen generate, run: pod install
```

### Carthage
```yaml
targets:
  MyApp:
    dependencies:
      - carthage: Alamofire
      - carthage: Result
        findFrameworks: true    # Auto-discover multiple frameworks
```

### Swift Package Manager
```yaml
packages:
  Yams:
    url: https://github.com/jpsim/Yams
    from: 2.0.0
  LocalPackage:
    path: ../LocalPackage

targets:
  MyApp:
    dependencies:
      - package: Yams
      - package: Yams
        product: YamsFramework   # If different from package name
```

### Frameworks and SDKs
```yaml
targets:
  MyApp:
    dependencies:
      - framework: Vendor/MyFramework.framework
      - sdk: Contacts.framework
      - sdk: libc++.tbd
```

## Schemes

```yaml
targets:
  MyApp:
    scheme:
      configVariants: [Debug, Release]  # Creates MyApp-Debug, MyApp-Release
      testTargets: [MyAppTests]
      gatherCoverageData: true
      commandLineArguments:
        "-EnableTesting": true
      environmentVariables:
        TEST_MODE: "1"
```

## Build Scripts

```yaml
targets:
  MyApp:
    preBuildScripts:
      - name: SwiftGen
        script: swiftgen
        inputFiles:
          - $(SRCROOT)/templates/*
        outputFiles:
          - $(SRCROOT)/Generated/generated.swift
    postCompileScripts:
      - script: swiftlint
        name: SwiftLint
    postBuildScripts:
      - script: |
          echo "Build complete!"
          ls -la
```

## Target Templates

```yaml
targetTemplates:
  iOSFramework:
    type: framework
    platform: iOS
    settings:
      base:
        CURRENT_PROJECT_VERSION: 1

targets:
  MyFramework:
    templates: [iOSFramework]
    sources: MyFramework
```

## Settings Groups

```yaml
settingGroups:
  baseAppSettings:
    base:
      SWIFT_VERSION: 5.0
      TARGETED_DEVICE_FAMILY: 1,2

targets:
  MyApp:
    settings:
      groups: [baseAppSettings]
```

## Config Files (xcconfig)

```yaml
configFiles:
  Debug: Configs/Debug.xcconfig
  Release: Configs/Release.xcconfig

targets:
  MyApp:
    configFiles:
      Debug: Configs/App-Debug.xcconfig
      Release: Configs/App-Release.xcconfig
```

## Info.plist

```yaml
targets:
  MyApp:
    info:
      path: MyApp/Info.plist
      properties:
        CFBundleIdentifier: $(PRODUCT_BUNDLE_IDENTIFIER)
        CFBundleShortVersionString: 1.0.0
        UILaunchStoryboardName: LaunchScreen
        UIRequiredDeviceCapabilities: [armv7]
        UISupportedInterfaceOrientations:
          - UIInterfaceOrientationPortrait
          - UIInterfaceOrientationLandscapeLeft
          - UIInterfaceOrientationLandscapeRight
```

## Entitlements

```yaml
targets:
  MyApp:
    entitlements:
      path: MyApp/App.entitlements
      properties:
        com.apple.security.application-groups:
          - group.com.myapp
        aps-environment: production
```

## Multi-Platform Targets

```yaml
targets:
  MyFramework:
    type: framework
    platform: [iOS, tvOS]
    deploymentTarget:
      iOS: "13.0"
      tvOS: "13.0"
    sources: MyFramework
    settings:
      base:
        PRODUCT_NAME: MyFramework
        MY_PLATFORM: ${platform}  # Expands to iOS or tvOS
```

## Including Other Files

```yaml
fileGroups:
  - Documentation
  - Configs
  - README.md
```
