"""Zero config: a repo with no humane-policy.toml still gets a real run.

The first run has to work before anyone will write a policy file, so the
action carries a default and says plainly in the comment that it used one.

No API key, no network, no spend.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _harness import new_repo, write, commit, load_judge, check

repo = new_repo()
write(repo, "app/notifications.py", "DAILY_CAP = 3\n")
base = commit(repo, "base")
write(repo, "app/notifications.py", "DAILY_CAP = 40\n")
head = commit(repo, "raise the cap")

m = load_judge(repo, BASE_SHA=base, HEAD_SHA=head)
ok = True

ok &= check("no policy in the repo, so the bundled default is used",
            m.POLICY_IS_DEFAULT is True)
ok &= check("the policy in use is the action's bundled file",
            m.POLICY == m.BUNDLED_POLICY and os.path.exists(m.POLICY))
ok &= check("the bundled default is not silently the demo repo's policy",
            "bundled default policy" in open(m.POLICY).read())

system = m.build_system()
ok &= check("default policy reaches the system prompt",
            "max_notifications_per_day" in system)
ok &= check("default floor is declared",
            m.floor_principles() == {"Protect Dignity & Safety",
                                     "Be Transparent and Honest"})
ok &= check("no policy documents are claimed that the repo does not have",
            m.policy_documents() == [])

diff, _ = m.get_diff()
ok &= check("the diff is still read from the customer repo", "DAILY_CAP" in diff)

body = m.render({
    "verdict": "review", "summary": "Test.", "mode": "diff",
    "findings": [], "commendations": [], "unresolved": [],
})
ok &= check("footer says the bundled default was used",
            "bundled default policy" in body)
ok &= check("footer suggests writing your own policy",
            "Copy" in body and "default-humane-policy.toml" in body)
ok &= check("footer does not claim a humane-policy.toml this repo lacks",
            "plus this repo's <code>humane-policy.toml</code>" not in body)

# And with a policy present the notice must disappear.
write(repo, "humane-policy.toml", '[floor]\nprinciples = ["Protect Dignity & Safety"]\n')
commit(repo, "add our own policy")
m2 = load_judge(repo, BASE_SHA=base, HEAD_SHA=head)
body2 = m2.render({
    "verdict": "review", "summary": "Test.", "mode": "diff",
    "findings": [], "commendations": [], "unresolved": [],
})
ok &= check("with a real policy, POLICY_IS_DEFAULT is False",
            m2.POLICY_IS_DEFAULT is False)
ok &= check("with a real policy, the nudge is gone",
            "Copy" not in body2 or "default-humane-policy.toml" not in body2)

print("PASS" if ok else "FAIL")
sys.exit(0 if ok else 1)
