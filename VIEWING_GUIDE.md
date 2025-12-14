# Report Viewing Guide

## Quick Start

After running tests, view reports easily with the provided viewer script:

```bash
python view_reports.py
```

This shows all available reports and documentation.

## Viewing Test Reports

### JSON Report (Machine-Readable)
```bash
# Summary view (recommended)
python view_reports.py json

# Output:
# ============================================================
# COVERAGE SUMMARY (from report.json)
# ============================================================
#
# Requirements:
#   Total: 4
#   Verified: 4
#   Verification: 100.0%
#
# Features:
#   Total: 11
#   Verified: 10
#   Verification: 90.9%
# ...

# Full JSON view
python view_reports.py json --full
```

### HTML Report (Visual Dashboard)
```bash
python view_reports.py html

# Opens report.html in your default browser
# Shows beautiful color-coded dashboard with:
# - Coverage statistics
# - Requirement details
# - Feature tracking
# - Test case links
```

### Markdown Report (Documentation)
```bash
python view_reports.py md

# Views with bat (syntax highlighting) if available
# Falls back to cat if not
# Shows formatted markdown with all details
```

### Table Report (Terminal View)
```bash
python view_reports.py table

# Shows formatted table in terminal
# Uses bat for syntax highlighting (line numbers + colors)
# Perfect for quick checks in terminal
```

## Viewing Documentation

### Quick Reference
```bash
python view_reports.py quick
# Shows QUICK_REFERENCE.md with decorators, strategies, examples
```

### Complete Guide
```bash
python view_reports.py readme
# Shows README.md - the complete documentation
```

### Quick Start Guide
```bash
python view_reports.py start
# Shows START_HERE.txt - 5-minute introduction
```

### Complete Walkthrough
```bash
python view_reports.py complete
# Shows COMPLETE_README.md - detailed walkthrough
```

### Troubleshooting
```bash
python view_reports.py troubleshooting
# Shows TROUBLESHOOTING.md - common issues and solutions
```

## Tools Used by the Viewer

The viewer automatically adapts to your system:

### bat (Recommended)
If `bat` is installed, the viewer uses it for:
- Syntax highlighting
- Line numbers
- Paging (for long files)
- Better readability

You have `bat` installed! ✓

### Browser Integration
The viewer automatically detects and uses:
- `xdg-open` (Linux)
- `open` (macOS)

For opening HTML reports in your default browser.

### Fallback
If `bat` is not available, the viewer falls back to `cat` for text viewing.

## Manual Viewing (Without Viewer Script)

You can also view reports manually:

### Using bat directly
```bash
bat report_table.txt          # Table with highlighting
bat report.md                 # Markdown with highlighting
bat report.json               # JSON with highlighting
bat README.md                 # Documentation
```

### Using cat
```bash
cat report_table.txt          # Plain table
cat report.json               # Plain JSON
cat report.md                 # Plain markdown
```

### Opening HTML
```bash
xdg-open report.html          # Linux
open report.html              # macOS
firefox report.html           # Specific browser
```

## Neovim/Vim Users

If you're using Neovim or Vim:

### View Markdown in Neovim
```bash
nvim report.md
# Or
nvim README.md
```

Recommended plugins for better markdown viewing:
- `mason.nvim` - LSP installer (for markdown LSP)
- `nvim-treesitter` - Better syntax highlighting
- `markdown-preview.nvim` - Live HTML preview
- `glow.nvim` - Render markdown in terminal

### View with Glow (if installed)
```bash
glow report.md                # Beautiful terminal markdown
glow README.md
```

Install glow: `yay -S glow` (Arch) or `brew install glow` (macOS)

## Best Practices

### Daily Workflow
```bash
# 1. Run tests
python -m pytest simple_test.py -v

# 2. Quick check - view table
python view_reports.py table

# 3. Detailed review - open HTML
python view_reports.py html

# 4. Check JSON for CI/CD
python view_reports.py json
```

### CI/CD Workflow
```bash
# In CI/CD pipeline
python -m pytest simple_test.py -v
python check_coverage.py --min-verification 95

# Archive artifacts
# - report.json (for parsing)
# - report.html (for viewing in CI/CD UI)
# - report.md (for documentation)
```

### Documentation Workflow
```bash
# Quick reference while coding
python view_reports.py quick

# When stuck
python view_reports.py troubleshooting

# Learning the system
python view_reports.py start
python view_reports.py readme
```

## Summary

The viewer script provides:
- ✅ One command to list everything
- ✅ Easy access to all reports
- ✅ Automatic tool selection (bat/cat)
- ✅ Browser integration for HTML
- ✅ Pretty JSON summaries
- ✅ Documentation access

Just remember:
```bash
python view_reports.py [report-name]
```

That's it!
