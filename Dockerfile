# Solver sandbox — bind-mounts the submission dir at runtime, does not COPY.
# The base image is pinned by digest so the same code rebuilds to the same
# bytes regardless of when ``setup.sh`` runs. Refresh via:
#   docker pull python:3.11-slim
#   docker inspect --format='{{index .RepoDigests 0}}' python:3.11-slim
# and update the FROM line below.
FROM python:3.11-slim@sha256:233de06753d30d120b1a3ce359d8d3be8bda78524cd8f520c99883bfe33964cf

RUN useradd --system --no-create-home --uid 1000 solver

WORKDIR /solver

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

USER solver

ENTRYPOINT ["python3", "/solver/solver.py"]
