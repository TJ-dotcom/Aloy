DOCKERFILE_PROMPT = """
You are a Senior DevOps Engineer. Your task is to create a production-quality, multi-stage Dockerfile for a Python application.

**Analysis Context:**
{full_context}

**Instructions:**
1.  **Analyze the Context:** Review both the `<requirements>` and `<project_files>` to understand the application type (Flask, FastAPI, or a general script) and identify the main application file.
2.  **Builder Stage:**
    * Start from the `python:3.11-slim-bullseye` base image.
    * Set the working directory to `/app`.
    * Copy only `requirements.txt` and install dependencies with `--no-cache-dir`.
3.  **Final Stage:**
    * Start from the same slim image.
    * Create a non-root user and group named `compiler_user`.
    * Set the working directory, copy dependencies from the builder, copy application source code, and set ownership for the `compiler_user`.
    * Switch to the `compiler_user`.
4.  **EXPOSE Port:** If the application is a web server (Flask/FastAPI), add an `EXPOSE 8000` instruction.
5.  **CMD Instruction:**
    * **Crucially, infer the main application file from the `<project_files>` list.**
    * If `flask` is in requirements, generate a `CMD` using `gunicorn`. Example: `["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]`, but replace `app:app` with the correct filename and object you inferred.
    * If `fastapi` is in requirements, generate a `CMD` using `uvicorn`. Example: `["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]`, replacing `main:app` as needed.
    * Otherwise, use `CMD ["python", "-u", "main.py"]`, replacing `main.py` with the most likely script from the file list.
6.  **Final Output:** Respond ONLY with the raw Dockerfile content. Do NOT include markdown code blocks (```dockerfile), explanations, greetings, or any other formatting. Start directly with the first Dockerfile instruction.
"""

DOCKERIGNORE_PROMPT = """
You are a build optimization expert. Generate a comprehensive `.dockerignore` file suitable for a standard Python project.

**Instructions:**
* Exclude virtual environments (`venv`, `.venv`, `env`).
* Exclude Git and CI/CD related files (`.git`, `.github`, `.gitlab-ci.yml`).
* Exclude IDE and system-specific files (`.idea`, `.vscode`, `.DS_Store`).
* Exclude Python cache files (`__pycache__`, `*.pyc`).
* Exclude local configuration (`.env`).
* Exclude the `Dockerfile` itself.
* Exclude build and distribution artifacts.

**Final Output:** Respond ONLY with the raw .dockerignore content. Do NOT include markdown code blocks (```ignore), explanations, or any other formatting. Start directly with the first ignore pattern.
"""

GITLAB_CI_PROMPT = """
You are a CI/CD specialist. Create a basic but robust `.gitlab-ci.yml` file for a containerized Python application.

**Instructions:**
1.  **Define Stages:** Use two stages: `build` and `push`.
2.  **Use Specific Versions:** Use a specific, stable version for the Docker image, like `image: docker:20.10.17`, and a `docker:20.10.17-dind` service. Do not use `:latest`.
3.  **Build Job:**
    * The `build_docker_image` job should run in the `build` stage.
    * Its script should run `docker build -t $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA .`
4.  **Push Job:**
    * The `push_docker_image` job should run in the `push` stage.
    * **Add a `before_script` section** to log into the GitLab container registry using `docker login -u $CI_REGISTRY_USER -p $CI_REGISTRY_PASSWORD $CI_REGISTRY`.
    * Its main `script` should run `docker push $CI_REGISTRY_IMAGE:$CI_COMMIT_SHA`.
    * **Add a `rules` clause** so this job ONLY runs on the `main` branch (e.g., `if: '$CI_COMMIT_BRANCH == "main"'`).
5.  **Final Output:** Respond ONLY with the raw YAML content. Do NOT include markdown code blocks (```yaml), explanations, or any other formatting. Start directly with the first YAML instruction.
"""
