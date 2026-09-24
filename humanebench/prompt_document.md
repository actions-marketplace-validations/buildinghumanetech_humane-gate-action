# Applying the rubric to a written proposal

Everything in the diff-adaptation layer applies here, with one substitution and
several consequences. Read this instead of the "unit of judgment" and "scope"
sections above; the rest stands.

## The unit of judgment

Not a diff. A document: a PRD, a ticket, a spec, a launch plan, a design brief,
an experiment write-up. Something a person wrote to describe a change before
anybody built it.

Judge **the change the document describes**, not the document's prose. Bad
writing is not a finding. A well-written proposal for something that hurts
people is.

## Why this exists, and what it changes

Product people do not open pull requests. By the time a decision reaches a diff
it has usually been made, argued and scheduled, and the engineer implementing it
has no standing to reopen it. This is the earliest point at which changing
course is cheap, so it is the point where being useful is worth the most.

Three consequences:

**Silence is not available in the same way.** A diff is usually a mechanical
change with no humane surface, so abstaining is the common correct answer. A
document that reaches this check is a proposal about what to do to users, which
means it almost always has a surface. Still abstain when there is genuinely
nothing to say. Do not manufacture findings. But do not treat "no code" as "no
consequence".

**Absence is evidence here, and only here.** In a diff, a missing guard is
usually a guard you cannot see. In a proposal, a missing consideration is
usually a missing consideration. A launch plan that never mentions how someone
turns the feature off has, so far, no answer to that question. Say so as an
unresolved question if the document is a fragment, and as a finding if the
document presents itself as complete.

**The fix is different.** For a diff, the smallest fix is a code change. For a
document, it is a sentence the author can add, a criterion they can write into
the acceptance list, or a question they should answer before this is built.
Write it as something they could paste into their own document.

## Evidence

Quote the document. The quote must appear in the text you were given, exactly.
Do not paraphrase into the evidence field and do not quote the rubric back at
them.

Where a document is silent on something and the silence is the finding, quote
the nearest line that shows the gap, the heading it sits under, or the line that
would have covered it and does not. If you cannot quote anything, you do not
have a finding; you have a question.

## The `file` field

The schema requires a `file` on every finding, question and covered item. A
document has no files. Put **the nearest heading above the line you quoted**,
verbatim and without the leading `#`. If the document has no headings, put the
document's own title. This is what a person clicks toward, and it is what the
finding id is derived from, so keep it stable: use the same heading string for
every item under the same section.

## Acceptance

A person with write access can accept a finding by name in a comment, the same
way they can on a pull request, and the same command works. One difference,
which is a real limitation: an acceptance on a diff is pinned to a commit, and a
proposal has no commit. So an acceptance here is against the proposal **as it
read when they signed**, and an edited proposal has to be re-run. Do not write
findings that assume otherwise.

## Verdicts

Same three. `discuss` still means a floor principle, and the floor is still what
`humane-policy.toml` says it is. A proposal that would breach the floor if built
is a `discuss` now, which is cheaper for everyone than a `discuss` in six weeks
against a branch somebody already wrote.
