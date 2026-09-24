"""The policy comes from the default branch, never from the pull request.

This is the rule that makes demo PR 9 -- "loosen the policy file for Q4" --
judgeable at all. If a pull request could supply the policy it is scored
against, it could permit itself anything on the way in, and the check would be
theatre. The workflow checks out the default branch, judge.py resolves the
policy against that workspace, and the pull request is only ever read as a
diff.

No API key, no network, no spend.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _harness import new_repo, write, commit, git, load_judge, check

BASE_POLICY = """[floor]
principles = ["Protect Dignity & Safety"]

[attention]
max_notifications_per_day = 3
mute_is_absolute          = true
"""

# What the pull request would like the rules to be.
PR_POLICY = """[floor]
principles = []

[attention]
max_notifications_per_day = 99
mute_is_absolute          = false
"""

repo = new_repo()
write(repo, "humane-policy.toml", BASE_POLICY)
write(repo, "app/notifications.py", "DAILY_CAP = 3\n")
base = commit(repo, "base: policy allows 3 a day, mute is absolute")

git("checkout", "-q", "-b", "loosen", cwd=repo)
write(repo, "humane-policy.toml", PR_POLICY)
write(repo, "app/notifications.py", "DAILY_CAP = 99\n")
head = commit(repo, "pr: raise the cap and drop the floor")

# The workflow checks out the default branch. Do the same here: the working
# tree is main, and the pull request exists only as a pair of shas.
git("checkout", "-q", "main", cwd=repo)

m = load_judge(repo, BASE_SHA=base, HEAD_SHA=head)
ok = True

ok &= check("policy resolved from the workspace, not the action",
            os.path.dirname(m.POLICY) == repo)
ok &= check("repo has its own policy, so the default is not used",
            m.POLICY_IS_DEFAULT is False)

diff, _ = m.get_diff()
ok &= check("the diff does contain the proposed policy edit",
            "max_notifications_per_day = 99" in diff)

system = m.build_system()
ok &= check("system prompt carries the BASE policy (cap 3)",
            "max_notifications_per_day = 3" in system)
ok &= check("system prompt does NOT carry the PR's policy (cap 99)",
            "max_notifications_per_day = 99" not in system.split("<diff>")[0])
ok &= check("base floor survives: Protect Dignity & Safety still declared",
            "Protect Dignity & Safety" in system)
ok &= check("floor_principles() reads the base floor, not the emptied one",
            m.floor_principles() == {"Protect Dignity & Safety"})

# The rubric and prompts must come from the action, never the workspace.
ok &= check("rubric loaded from the action checkout",
            m.RUBRIC.startswith(m.ACTION_ROOT) and os.path.exists(m.RUBRIC))
ok &= check("prompt loaded from the action checkout",
            m.PROMPT.startswith(m.ACTION_ROOT) and os.path.exists(m.PROMPT))

print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
