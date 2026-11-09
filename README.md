# 🚀 Task Tracker API

**A RESTful Task Management API built with Python and FastAPI.**

A backend project focused on developing and testing a task management REST API, with an emphasis on code quality, test automation, type safety, and CI/CD practices.

---

## ✨ Features

- **REST API** — CRUD operations for task management.
- **Data validation** — request and response validation with Pydantic v2.
- **Database integration** — SQLite with SQLAlchemy 2.0.
- **Automated testing** — API and database tests using Pytest and HTTPX.
- **Negative testing** — validation errors, invalid requests, and edge cases.
- **Test reporting** — detailed Allure reports.
- **Code quality** — Ruff linting and formatting.
- **Static type checking** — BasedPyright.
- **Code coverage** — pytest-cov with a 100% coverage threshold.
- **Containerization** — Docker and Docker Compose.
- **CI/CD** — automated checks with GitHub Actions.
- **Quality Gate** — local quality checks and Git pre-commit hook.

## 🛠 Tech Stack

| Category             | Technology             |
| -------------------- | ---------------------- |
| Language             | Python 3.14            |
| API Framework        | FastAPI                |
| Data Validation      | Pydantic v2            |
| Database             | SQLite                 |
| ORM                  | SQLAlchemy 2.0         |
| Testing              | Pytest                 |
| HTTP Client          | HTTPX                  |
| Test Reporting       | Allure                 |
| Linting & Formatting | Ruff                   |
| Type Checking        | BasedPyright           |
| Coverage             | pytest-cov             |
| Containerization     | Docker, Docker Compose |
| CI/CD                | GitHub Actions         |

## 📁 Project Structure

```text
task-tracker/
├── .github/
│   └── workflows/
│       └── tests.yml
├── .githooks/
│   └── pre-commit
├── .zed/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── scripts/
│   └── quality_gate.sh
├── tests/
│   ├── conftest.py
│   └── test_*.py
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── ruff.toml
└── README.md
```

## ⚙️ Getting Started

### Prerequisites

- Python 3.14
- Git
- Docker and Docker Compose (for containerized test execution)

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd task-tracker
```

### 2. Create a virtual environment

```bash
python3.14 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Run the API

```bash
uvicorn app.main:app --reload
```

The API will be available at:

- API: `http://127.0.0.1:8000`
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## 🧪 Testing

Run the complete test suite:

```bash
pytest -v
```

Run tests with coverage:

```bash
pytest -v --cov=app --cov-report=term-missing
```

Enforce the 100% coverage threshold:

```bash
pytest --cov=app --cov-fail-under=100
```

## 🐳 Docker

Build and run the test environment:

```bash
docker compose build
docker compose run --rm tests
```

The Docker Compose test service executes the test suite, generates Allure results, and checks code coverage.

## 📊 Allure Reports

Allure is used to provide detailed and structured test reports.

The reports include:

- Test execution results.
- Test descriptions and severity.
- Test steps.
- Attachments and diagnostic information.

Test results are generated in the `allure-results/` directory.

## 🔍 Code Quality

The project uses several tools to maintain code quality and prevent common issues.

### Ruff

```bash
ruff check app tests
ruff format --check app tests
```

### BasedPyright

```bash
basedpyright app tests
```

### Quality Gate

Run all local quality checks with one command:

```bash
./scripts/quality_gate.sh
```

The Quality Gate includes:

1. Ruff linting.
2. Ruff formatting validation.
3. BasedPyright static type checking.
4. Pytest execution with coverage enforcement.

A Git pre-commit hook runs the Quality Gate before creating a commit.

## 🔄 CI/CD

GitHub Actions automates project verification.

The CI pipeline includes:

- Ruff linting and formatting checks.
- BasedPyright static type checking.
- Automated tests in Docker.
- Coverage enforcement.
- Allure report generation and publishing.

This helps ensure that code changes pass the project's quality checks before integration.

## 🎯 Project Goals

This project demonstrates practical experience with:

- Designing and testing REST APIs.
- Building automated API tests.
- Working with fixtures and test isolation.
- Testing positive and negative scenarios.
- Database verification.
- Static type checking.
- Test reporting and coverage analysis.
- Docker-based test execution.
- CI/CD pipeline configuration.
- Automated quality enforcement.

---

**Built with Python 🐍 and a focus on reliable test automation.**
