"""Shared harness: import judge.py against a throwaway workspace.

No API key, no network, no spend. `anthropic` and `requests` are stubbed
before the import so judge.py can be loaded and its path handling exercised
directly.
"""
import importlib.util, os, subprocess, sys, tempfile, types

ACTION_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def git(*args, cwd):
    subprocess.run(["git", *args], cwd=cwd, check=True,
                   capture_output=True, text=True)


def new_repo():
    """A throwaway git repo standing in for the customer's checkout."""
    d = tempfile.mkdtemp(prefix="humane-gate-test-")
    git("init", "-q", cwd=d)
    # -b on `git init` needs git >= 2.28; set the branch name the portable way.
    git("symbolic-ref", "HEAD", "refs/heads/main", cwd=d)
    git("config", "user.email", "test@example.com", cwd=d)
    git("config", "user.name", "Test", cwd=d)
    return d


def write(repo, rel, body):
    path = os.path.join(repo, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(body)


def commit(repo, message):
    git("add", "-A", cwd=repo)
    git("commit", "-q", "-m", message, cwd=repo)
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo,
                          capture_output=True, text=True).stdout.strip()


def load_judge(workspace, **env):
    """Import a fresh judge.py with the given workspace and environment.

    judge.py resolves its paths at import time, which is exactly the behaviour
    under test, so every case gets its own module instance.
    """
    sys.modules.setdefault("requests", types.ModuleType("requests"))
    fake = types.ModuleType("anthropic")
    fake.Anthropic = lambda **kw: None
    sys.modules["anthropic"] = fake

    os.environ["GITHUB_ACTION_PATH"] = ACTION_ROOT
    os.environ["GITHUB_WORKSPACE"] = workspace
    os.environ["DRY_RUN"] = "1"
    os.environ.pop("HUMANE_POLICY_PATH", None)
    os.environ.pop("GITHUB_TOKEN", None)
    for k, v in env.items():
        os.environ[k] = v

    spec = importlib.util.spec_from_file_location(
        f"judge_{len(sys.modules)}",
        os.path.join(ACTION_ROOT, "humanebench", "judge.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def check(label, ok):
    print(f"[{'ok' if ok else 'FAIL'}] {label}")
    return bool(ok)
