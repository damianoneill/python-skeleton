#!/bin/bash

# Script to rename all instances of "project_name" to a custom project name
# with proper docstrings added to empty init files to preserve Git history

set -e # Exit immediately if a command exits with a non-zero status

# Get the script name to exclude it from changes
SCRIPT_NAME=$(basename "$0")
SCRIPT_PATH=$(realpath "$0")

# Check if a project name was provided
if [ $# -ne 1 ]; then
    echo "=================================================="
    echo "Usage: $0 new_project_name"
    echo "Example: $0 my_awesome_app"
    echo "=================================================="
    exit 1
fi

NEW_NAME=$1
OLD_NAME="project_name"

# If the project is already renamed, warn and exit
if [ ! -d "src/$OLD_NAME" ] && [ -d "src/$NEW_NAME" ]; then
    echo "Warning: Project appears to already be named '$NEW_NAME'."
    echo "No action taken. If you want to rename again, restore the original repo first."
    exit 0
fi

# Validate that the new name is a valid Python package name
if ! [[ $NEW_NAME =~ ^[a-zA-Z][a-zA-Z0-9_]*$ ]]; then
    echo "Error: The project name must be a valid Python package name."
    echo "It should start with a letter and contain only letters, numbers, and underscores."
    exit 1
fi

# Check if we're in a git repository
if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    echo "Warning: This doesn't appear to be a git repository."
    echo "The script will use standard mv instead of git mv."
    USE_GIT=false
else
    USE_GIT=true
fi

echo "=================================================="
echo "Renaming project from '$OLD_NAME' to '$NEW_NAME'"
echo "=================================================="

if [ -d "src/$OLD_NAME" ]; then
    echo "Preparing to rename src/$OLD_NAME directory to src/$NEW_NAME"

    # First, add proper docstrings to all __init__.py files
    for init_file in $(find "src/$OLD_NAME" -name "__init__.py"); do
        # Get the module path for the docstring
        module_path=${init_file#src/}
        module_path=${module_path%.py}
        module_path=${module_path//\//.}

        # Check if file is empty or very small
        if [ ! -s "$init_file" ] || [ $(wc -c <"$init_file") -lt 10 ]; then
            echo "Adding docstring to: $init_file"
            # Create a proper docstring that will be replaced with the new name later
            echo "\"\"\"$OLD_NAME.$module_path module.\"\"\"" >"$init_file"
        fi
    done

    # Stage these changes before moving files
    if [ "$USE_GIT" = true ]; then
        git add "src/$OLD_NAME"
    fi

    # Create target directory structure first
    mkdir -p "src/$NEW_NAME"

    # Now move each file individually with Git
    for file in $(find "src/$OLD_NAME" -type f | sort); do
        # Get the relative path from the old root
        rel_path=${file#src/$OLD_NAME/}
        target_dir="src/$NEW_NAME/$(dirname "$rel_path")"
        target_file="$target_dir/$(basename "$rel_path")"

        # Create target directory if needed
        mkdir -p "$target_dir"

        echo "Moving $file to $target_file"
        if [ "$USE_GIT" = true ] && git ls-files --error-unmatch "$file" >/dev/null 2>&1; then
            # For tracked files, use git mv
            git mv "$file" "$target_file"
        else
            # For untracked files, use regular mv
            mv "$file" "$target_file"
        fi
    done

    # Remove any empty directories left behind
    find "src/$OLD_NAME" -type d -empty -delete 2>/dev/null || true
fi

# Find and rename other files with the old name in their filename
echo -e "\nRenaming files containing '$OLD_NAME' in their names..."
for file in $(find . -name "*$OLD_NAME*" -type f -not -path "*/\.*cache*/*" -not -path "*/.venv/*" -not -path "*/__pycache__/*" | sort); do
    # Skip the script itself
    if [ "$file" = "./$SCRIPT_NAME" ] || [ "$file" = "$SCRIPT_PATH" ]; then
        echo "Skipping the rename script itself: $file"
        continue
    fi

    dir=$(dirname "$file")
    base=$(basename "$file")
    newbase=$(echo "$base" | sed "s/$OLD_NAME/$NEW_NAME/g")
    if [ "$base" != "$newbase" ]; then
        newfile="$dir/$newbase"
        echo "Renaming file: $file -> $newfile"
        if [ "$USE_GIT" = true ] && git ls-files --error-unmatch "$file" >/dev/null 2>&1; then
            git mv "$file" "$newfile"
        else
            mv "$file" "$newfile"
        fi
    fi
done

# Find all text files containing the old name in their content
echo -e "\nFinding files containing '$OLD_NAME' in their content..."
FILES=$(grep -r --include="*.*" -l "$OLD_NAME" \
    --exclude="$SCRIPT_NAME" \
    --exclude-dir=.git \
    --exclude-dir=.ruff_cache \
    --exclude-dir=__pycache__ \
    --exclude-dir=.pytest_cache \
    --exclude-dir=.venv \
    --exclude-dir=.mypy_cache \
    --exclude="*.pyc" \
    --exclude="*.pyo" \
    --exclude="*.so" \
    . 2>/dev/null || true)

# Update content in all identified text files
echo -e "\nReplacing '$OLD_NAME' with '$NEW_NAME' in file contents..."
for file in $FILES; do
    # Skip if file doesn't exist (might have been renamed)
    if [ ! -f "$file" ]; then
        continue
    fi

    # Skip the script itself
    if [ "$file" = "./$SCRIPT_NAME" ] || [ "$file" = "$SCRIPT_PATH" ]; then
        echo "Skipping the rename script itself: $file"
        continue
    fi

    # Check if file is a text file
    if file "$file" | grep -q text; then
        echo "Updating content in: $file"
        # Replace occurrences of the old name with the new name
        # Use a more compatible version of sed -i for macOS and Linux
        if [[ "$OSTYPE" == "darwin"* ]]; then
            # macOS requires an extension for -i
            sed -i '' "s/$OLD_NAME/$NEW_NAME/g" "$file"
        else
            # Linux works without an extension
            sed -i "s/$OLD_NAME/$NEW_NAME/g" "$file"
        fi
    else
        echo "Skipping binary file: $file"
    fi
done

# Add any new (previously untracked) files and directories
if [ "$USE_GIT" = true ]; then
    echo -e "\nStaging changes in git..."
    git add -A
    echo "Changes have been staged. Review them with 'git status' and commit with 'git commit'."
fi

echo -e "\n=================================================="
echo "Project successfully renamed from '$OLD_NAME' to '$NEW_NAME'!"
echo "=================================================="
echo "Next steps:"
echo "1. Review changes to ensure everything was updated correctly"
if [ "$USE_GIT" = true ]; then
    echo "2. Commit the changes with: git commit -m 'Rename project from $OLD_NAME to $NEW_NAME'"
fi
echo "3. Run tests to verify everything works"
echo "=================================================="
