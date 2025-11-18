#!/bin/bash
# ============================================================================
# GIT COMMANDS - Quick Reference
# Save as: git-commands.sh
# ============================================================================

# Basic git workflow
git_workflow() {
    echo "Git Workflow Commands"
    echo "====================="
    echo ""
    echo "# Check status"
    echo "git status"
    echo ""
    echo "# Add all changes"
    echo "git add ."
    echo ""
    echo "# Commit with message"
    echo "git commit -m 'Your message here'"
    echo ""
    echo "# Push to GitHub"
    echo "git push origin main"
    echo ""
}

# Quick commit and push
quick_commit() {
    if [ -z "$1" ]; then
        echo "Usage: quick_commit 'commit message'"
        return 1
    fi
    
    git add .
    git commit -m "$1"
    git push origin main
    echo "✅ Changes committed and pushed!"
}

# Initialize git repository
init_repo() {
    echo "Initializing Git repository..."
    git init
    git add .
    git commit -m "Initial commit: Invoice Agent project setup"
    echo ""
    echo "✅ Repository initialized"
    echo ""
    echo "Next steps:"
    echo "1. Create repository on GitHub"
    echo "2. Run: git remote add origin https://github.com/YOUR_USERNAME/invoice-agent.git"
    echo "3. Run: git push -u origin main"
}

# View recent commits
view_history() {
    echo "Recent Commits:"
    echo "==============="
    git log --oneline -10
}

# Create feature branch
create_branch() {
    if [ -z "$1" ]; then
        echo "Usage: create_branch 'branch-name'"
        return 1
    fi
    
    git checkout -b "$1"
    echo "✅ Created and switched to branch: $1"
}

# Switch to main branch
to_main() {
    git checkout main
    echo "✅ Switched to main branch"
}

# Pull latest changes
pull_latest() {
    git pull origin main
    echo "✅ Pulled latest changes"
}

# Show uncommitted changes
show_changes() {
    echo "Uncommitted Changes:"
    echo "==================="
    git diff
}

# Undo last commit (keep changes)
undo_commit() {
    git reset --soft HEAD~1
    echo "✅ Last commit undone (changes kept)"
}

# Show all commands
show_help() {
    echo "Available Git Commands:"
    echo "======================="
    echo ""
    echo "git_workflow         - Show basic git workflow"
    echo "quick_commit 'msg'   - Quick commit and push"
    echo "init_repo            - Initialize new repository"
    echo "view_history         - View recent commits"
    echo "create_branch 'name' - Create new feature branch"
    echo "to_main              - Switch to main branch"
    echo "pull_latest          - Pull latest changes"
    echo "show_changes         - Show uncommitted changes"
    echo "undo_commit          - Undo last commit (keep changes)"
    echo ""
}

# Export functions
export -f git_workflow
export -f quick_commit
export -f init_repo
export -f view_history
export -f create_branch
export -f to_main
export -f pull_latest
export -f show_changes
export -f undo_commit
export -f show_help

# Show help on source
show_help
