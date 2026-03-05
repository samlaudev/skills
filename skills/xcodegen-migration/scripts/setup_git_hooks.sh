#!/bin/bash
#
# XcodeGen Git Hooks Setup
#
# Installs git hooks to automatically regenerate .xcodeproj
# when switching branches or merging changes.
#

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

print_header() {
    echo ""
    echo "=========================================="
    echo "  $1"
    echo "=========================================="
    echo ""
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# Check if we're in a git repository
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    print_error "Not in a git repository"
    exit 1
fi

print_header "XCODEGEN GIT HOOKS SETUP"

# Get the git directory
GIT_DIR=$(git rev-parse --git-dir)
HOOKS_DIR="$GIT_DIR/hooks"

print_success "Git repository found"
echo "Hooks directory: $HOOKS_DIR"

# Create hooks directory if it doesn't exist
mkdir -p "$HOOKS_DIR"

# Function to install a hook
install_hook() {
    local hook_name=$1
    local hook_file="$HOOKS_DIR/$hook_name"

    cat > "$hook_file" << 'EOF'
#!/bin/bash
# XcodeGen auto-regeneration hook

# Check if project.yml exists
if [ ! -f "project.yml" ]; then
    # project.yml not found, skip regeneration
    exit 0
fi

# Check if XcodeGen is installed
if ! command -v xcodegen &> /dev/null; then
    echo "Warning: XcodeGen not found. Skipping project regeneration."
    exit 0
fi

# Get the current directory
PROJECT_DIR=$(git rev-parse --show-toplevel)

# Change to project directory
cd "$PROJECT_DIR"

echo "Running xcodegen generate..."
xcodegen generate --quiet

# Check if generation was successful
if [ $? -eq 0 ]; then
    echo "Xcode project regenerated successfully"
else
    echo "Warning: XcodeGen failed to regenerate project"
    exit 1
fi
EOF

    chmod +x "$hook_file"
    print_success "Installed $hook_name hook"
}

# Check for existing hooks and warn
print_warning "Checking for existing hooks..."
existing_hooks=()

for hook in post-checkout post-merge pre-commit; do
    if [ -f "$HOOKS_DIR/$hook" ] && [ -s "$HOOKS_DIR/$hook" ]; then
        existing_hooks+=("$hook")
    fi
done

if [ ${#existing_hooks[@]} -gt 0 ]; then
    print_warning "Found existing hooks:"
    for hook in "${existing_hooks[@]}"; do
        echo "  - $hook"
    done
    echo ""
    read -p "Backup existing hooks and continue? [y/N] " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        for hook in "${existing_hooks[@]}"; do
            mv "$HOOKS_DIR/$hook" "$HOOKS_DIR/$hook.backup"
            echo "Backed up $hook"
        done
    else
        print_error "Setup cancelled"
        exit 1
    fi
fi

# Install the hooks
print_header "INSTALLING HOOKS"

install_hook "post-checkout"
install_hook "post-merge"
install_hook "pre-commit"

print_success "All hooks installed successfully!"

# Instructions
print_header "NEXT STEPS"

echo "The following hooks are now active:"
echo ""
echo "  post-checkout: Regenerates .xcodeproj when switching branches"
echo "  post-merge:    Regenerates .xcodeproj after merging"
echo "  pre-commit:    Ensures .xcodeproj is current before commit"
echo ""
echo "Your .xcodeproj will stay in sync with project.yml automatically!"
echo ""
print_warning "IMPORTANT:"
echo "1. Add *.xcodeproj to your .gitignore"
echo "2. Commit project.yml as your source of truth"
echo "3. Remove .xcodeproj from git if already tracked:"
echo "   git rm -r --cached *.xcodeproj"
echo ""
print_success "Setup complete!"
