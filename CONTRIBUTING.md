# Contributing to Job Scraper Pipeline

Thank you for considering contributing! This document outlines our development workflow and contribution guidelines.

## 📋 Table of Contents
- [Getting Started](#getting-started)
- [Branching Strategy](#branching-strategy)
- [Commit Message Guidelines](#commit-message-guidelines)
- [Pull Request Process](#pull-request-process)
- [Code Review Guidelines](#code-review-guidelines)
- [Testing Requirements](#testing-requirements)
- [Code Style](#code-style)

---

## 🚀 Getting Started

### 1. Fork and Clone
```bash
# Fork the repository on GitHub, then:
git clone https://github.com/husseini2000/job-scraper.git
cd job-scraper
```

### 2. Set Up Development Environment
```bash
# Install dependencies
make install

# Activate virtual environment
source venv/bin/activate

# Run tests to ensure everything works
make test
```

### 3. Configure Git
```bash
# Set up upstream remote
git remote add upstream https://github.com/husseini2000/job-scraper.git

# Verify remotes
git remote -v
```

---

## 🌿 Branching Strategy

We follow **Git Flow** with these main branches:

### Main Branches

#### `main`
- **Purpose**: Production-ready code
- **Protection**: 
  - Requires pull request reviews
  - Must pass all CI checks
  - No direct commits allowed
- **Merge from**: `dev` branch only
- **Deploy**: Automatically deployed to production

#### `dev`
- **Purpose**: Integration branch for features
- **Protection**: 
  - Requires pull request reviews
  - Must pass all tests
- **Merge from**: Feature and bugfix branches
- **Merge to**: `main` for releases

### Supporting Branches

#### Feature Branches: `feature/<feature-name>`
```bash
# Create feature branch from dev
git checkout dev
git pull upstream dev
git checkout -b feature/wuzzuf-scraper

# Work on your feature...
# When done, push and create PR to dev
git push origin feature/wuzzuf-scraper
```

**Naming examples:**
- `feature/bayt-scraper` - Add Bayt.com scraper
- `feature/salary-parser` - Implement salary parsing
- `feature/api-endpoint` - Add REST API endpoint

#### Bugfix Branches: `bugfix/<bug-name>`
```bash
# Create bugfix branch from dev
git checkout dev
git checkout -b bugfix/fix-encoding-issue

# Fix the bug, push, and create PR
```

**Naming examples:**
- `bugfix/fix-arabic-encoding` - Fix Arabic text encoding
- `bugfix/rate-limit-error` - Fix rate limiter issue

#### Hotfix Branches: `hotfix/<issue>`
```bash
# For urgent production fixes
git checkout main
git checkout -b hotfix/critical-scraper-crash

# Fix, test thoroughly, and merge to both main and dev
```

#### Enhancement Branches: `enhancement/<name>`
```bash
# For improvements to existing features
git checkout dev
git checkout -b enhancement/improve-deduplication
```

### Branch Naming Rules
- Use lowercase and hyphens
- Be descriptive but concise
- Include ticket number if applicable: `feature/123-add-gulftalent`

---

## 📝 Commit Message Guidelines

We follow **Conventional Commits** specification.

### Format
```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, no logic change)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks (dependencies, config)
- `perf`: Performance improvements

### Examples

#### Good Commit Messages ✅
```bash
feat(extract): add Wuzzuf scraper with rate limiting

- Implement BaseScraper inheritance
- Add rate limiter with token bucket algorithm
- Handle pagination up to 50 pages
- Extract job title, company, location, and salary

Closes #42
```

```bash
fix(transform): handle None values in salary parsing

Previously crashed when salary field was None. Now returns
SalaryInfo with all fields as None.

Fixes #58
```

```bash
test(models): add tests for SalaryInfo validation

- Test salary range auto-correction
- Test negative amount rejection
- Test currency validation
- Increase coverage to 95%
```

#### Bad Commit Messages ❌
```bash
update code          # Too vague
fixed stuff          # Not descriptive
WIP                  # Should squash before PR
minor changes        # What changes?
```

### Commit Best Practices
1. **One logical change per commit**
2. **Present tense**: "Add feature" not "Added feature"
3. **Imperative mood**: "Fix bug" not "Fixes bug"
4. **Limit subject to 72 characters**
5. **Reference issues**: Use "Closes #123" or "Fixes #456"

---

## 🔄 Pull Request Process

### 1. Before Creating PR

```bash
# Ensure your branch is up to date
git checkout dev
git pull upstream dev
git checkout feature/your-feature
git rebase dev

# Run quality checks
make format        # Format code
make lint          # Check code quality
make test          # Run all tests

# Ensure tests pass and coverage is good
pytest tests/ --cov=. --cov-report=term
```

### 2. Creating the PR

1. **Push your branch**
   ```bash
   git push origin feature/your-feature
   ```

2. **Open PR on GitHub**
   - Base branch: `dev` (not `main`!)
   - Compare branch: `feature/your-feature`
   - Fill out the PR template completely
   - Add relevant labels: `enhancement`, `bug`, `documentation`
   - Link related issues
   - Request reviewers

3. **PR Title Format**
   ```
   feat(extract): Add Wuzzuf scraper implementation
   ```

### 3. PR Requirements

Your PR must meet these criteria:

✅ **Tests**
- All existing tests pass
- New tests added for new functionality
- Coverage remains ≥ 80%

✅ **Code Quality**
- Black formatting applied (`make format`)
- Flake8 linting passes (`make lint`)
- Type hints added for new functions
- No deprecated methods used

✅ **Documentation**
- Docstrings for new functions/classes
- README updated if needed
- Comments for complex logic

✅ **CI/CD**
- All GitHub Actions checks pass
- No merge conflicts
- Branch is up to date with base

### 4. Responding to Reviews

```bash
# Make requested changes
git add .
git commit -m "refactor: address review comments

- Extract duplicate code into helper function
- Add error handling for edge cases
- Improve docstrings clarity
"

git push origin feature/your-feature
```

### 5. Squashing Commits (Optional)

If you have many small commits, squash before merging:

```bash
# Interactive rebase to squash last 3 commits
git rebase -i HEAD~3

# In the editor, mark commits to squash:
# pick abc1234 First commit
# squash def5678 Fix typo
# squash ghi9012 Address review

# Force push (since history changed)
git push origin feature/your-feature --force-with-lease
```

---

## 👀 Code Review Guidelines

### For Reviewers

#### What to Look For

**Functionality**
- Does it work as intended?
- Are edge cases handled?
- Could this break existing functionality?

**Code Quality**
- Is the code readable and maintainable?
- Are variable names descriptive?
- Is there duplicated code that should be extracted?
- Are functions too long or complex?

**Testing**
- Are there sufficient tests?
- Do tests cover edge cases?
- Is the happy path and error path tested?

**Performance**
- Are there obvious performance issues?
- Could this cause memory leaks?
- Is caching used appropriately?

**Security**
- Are there SQL injection risks?
- Is user input validated?
- Are secrets handled properly?

#### Review Comments

**Good Comments** ✅
```
💡 Suggestion: Consider extracting this logic into a separate 
function for better testability.

❓ Question: What happens if the API returns a 429 status? 
Should we add retry logic?

⚠️ Issue: This could raise KeyError if 'salary' key is missing. 
Suggest using .get() with a default value.

✨ Nice: Good use of type hints here! Makes the code much clearer.
```

**Bad Comments** ❌
```
This is wrong.
I don't like this.
Why did you do it this way?
```

### For Contributors

**Responding to Reviews**
- Be receptive to feedback
- Ask questions if unclear
- Explain your reasoning respectfully
- Thank reviewers for their time

**When to Push Back**
- If suggestion contradicts project standards
- If change is outside PR scope (create new issue)
- If reviewer misunderstands the code (explain clearly)

---

## 🧪 Testing Requirements

### Test Coverage
- Maintain **≥ 80% coverage**
- All new functions must have tests
- Test both success and failure paths

### Test Structure
```python
def test_descriptive_name():
    """Test that X does Y when Z happens."""
    # Arrange: Set up test data
    job = JobListing(...)
    
    # Act: Execute the code
    result = transform(job)
    
    # Assert: Verify results
    assert result.title == "Expected Title"
```

### Running Tests
```bash
# Run all tests
make test

# Run specific test file
pytest tests/test_models.py -v

# Run with coverage report
pytest --cov=. --cov-report=html

# Run tests matching pattern
pytest -k "test_salary" -v
```

---

## 🎨 Code Style

### Python Style Guide
We follow **PEP 8** with these tools:

#### Black (Code Formatter)
```bash
# Format all code
make format

# Check formatting without changing files
black --check extract/ transform/
```

#### Flake8 (Linter)
```bash
# Run linter
make lint

# Run on specific files
flake8 core/models.py
```

### Style Guidelines

**Imports**
```python
# Standard library
import os
from pathlib import Path

# Third-party
import pandas as pd
from pydantic import BaseModel

# Local
from core.models import JobListing
from core.exceptions import ScraperError
```

**Type Hints**
```python
def parse_salary(text: str) -> Optional[SalaryInfo]:
    """Parse salary from text."""
    pass

def scrape_jobs(site: str, max_pages: int = 50) -> list[JobListing]:
    """Scrape jobs from site."""
    pass
```

**Docstrings** (Google Style)
```python
def transform_job(raw_job: dict[str, Any]) -> JobListing:
    """
    Transform raw job data to JobListing model.
    
    Args:
        raw_job: Raw job dictionary from scraper
    
    Returns:
        Validated JobListing instance
    
    Raises:
        ValidationError: If required fields are missing
    
    Example:
        >>> raw = {"title": "Developer", ...}
        >>> job = transform_job(raw)
        >>> print(job.title)
        'Developer'
    """
    pass
```

---

## 🏷️ Issue Labels

When creating issues or PRs, use these labels:

| Label | Description |
|-------|-------------|
| `bug` | Something isn't working |
| `enhancement` | New feature or improvement |
| `documentation` | Documentation updates |
| `good first issue` | Good for newcomers |
| `help wanted` | Extra attention needed |
| `priority: high` | Urgent issue |
| `priority: low` | Can wait |
| `wontfix` | This will not be worked on |
| `duplicate` | Already exists |
| `question` | Further information requested |

---

## 🚢 Release Process

### Versioning
We follow **Semantic Versioning** (SemVer):
- `v1.0.0` - Major release (breaking changes)
- `v1.1.0` - Minor release (new features)
- `v1.1.1` - Patch release (bug fixes)

### Creating a Release

1. **Merge dev to main**
   ```bash
   git checkout main
   git merge dev --no-ff
   ```

2. **Tag the release**
   ```bash
   git tag -a v1.0.0 -m "Release version 1.0.0
   
   Features:
   - Wuzzuf scraper
   - Bayt scraper
   - Salary parsing
   - Data deduplication
   "
   ```

3. **Push tags**
   ```bash
   git push origin main
   git push origin v1.0.0
   ```

4. **Create GitHub Release**
   - Go to GitHub Releases
   - Create new release from tag
   - Add release notes
   - Upload any artifacts

---

## 📞 Getting Help

- **Questions**: Open a GitHub Discussion
- **Bugs**: Create a bug report issue
- **Features**: Create a feature request issue
- **Chat**: Join our [Discord/Slack] (if applicable)

---

## 📜 License

By contributing, you agree that your contributions will be licensed under the project's MIT License.

---

Thank you for contributing to Job Scraper Pipeline! 🎉