# agent-platform-security-questions

Kortix is open source. This repository is a **twelve-question security questionnaire for any agent platform that is about to touch company files**, a renderer that turns it into a document you can send a vendor, and Kortix's own answers with the document behind each one.

The argument is narrow and, in practice, decisive: **"is it secure" is not answered by a feature grid, and it is not answered by a vendor's summary of itself. It is answered by counting how many of your questions came back as a document with a name.** Two platforms can both say "audit logging" and mean a 30-day API window and a 400-action export respectively. The questionnaire is what makes that difference fall out before the pilot, instead of at the first access review.

```sh
python3 render.py                    # the questionnaire, as Markdown
python3 render.py --format email     # a numbered list to paste into an email
python3 render.py --format csv --out questions.csv
python3 render.py --answers          # with Kortix's answers and sources
```

Standard library only; the questions live in `questions.json`, so you can delete one or add your own.

## The four domains

| Domain | The question behind the questions |
|---|---|
| **The record** | When someone asks "what did the agent do on the 14th", is there a list of actions with names, and can I pull it myself? |
| **Permissions** | Which calls stop and wait for a person — and does the platform decide that per tool, or with one organisation-wide switch? |
| **Data** | Where does session history live, who can delete it, and what does the vendor still see when I self-host? |
| **Exit** | If I leave next quarter, what do I take with me, and is the tree I run actually mine? |

Each question carries what a good answer looks like and what makes an answer a red flag. The red flags are not hypothetical; each one is a failure this questionnaire was written after meeting:

- *"We log everything"* with no action list to filter on — a log you cannot query is a log you cannot use in a review.
- A record that covers the model call but not the approval decision, so the question "who approved this" has no answer.
- A retention window shorter than the review cycle it has to serve.
- Session history stored on the member's own computer with no central deletion path.
- Configuration that exports as a database dump rather than as the files the platform actually runs on.
- The organisation layer carved out of the open-source licence, so the part a company needs is the vendor's product.

## Kortix's answers, for comparison

`python3 render.py --answers` prints them; `answers.kortix.json` holds the text and the URL for each. The short version, as of 2026-10-21:

| Question | Kortix's answer | Document |
|---|---|---|
| Which actions are logged? | 797 request actions, 81 events outside a request, 55 operator actions, named `domain.resource.verb`, filterable by prefix | [Audit actions](https://kortix.com/docs/audit-actions) |
| Can I export or stream it? | `kortix audit export`, and `kortix audit webhooks add --action-prefix …` to your own endpoint | [Audit actions](https://kortix.com/docs/audit-actions) |
| Does it cover approvals and secrets, or only model calls? | One log: tool calls, approval outcomes, secret changes, key revocations, admin actions | [Audit actions](https://kortix.com/docs/audit-actions) |
| Per-tool control? | Allow, ask or block per tool, plus questions a running session raises for a person | [Tools](https://kortix.com/docs/project/tools) · [Sessions](https://kortix.com/docs/work/sessions) |
| Secrets? | Per-secret exposure mode (environment, egress-enforced, none), granted to named agents only | [Secrets](https://kortix.com/docs/project/secrets) |
| Where does the work live? | A git repository the company owns; a session is an isolated machine on its own branch, and output reaches the default branch only through a change request | [Git](https://kortix.com/docs/git) |
| Self-host? | Documented install, bootstrap and hardening; the repository stays on your origin | [Self-hosting](https://kortix.com/docs/host) |
| Which models see my content? | Your provider keys, any OpenAI-compatible endpoint, or a connected ChatGPT subscription | [Models](https://kortix.com/docs/project/models) |
| What do I take with me? | The files already in your repository — agents, skills, memory, connectors, triggers | [kortix.yaml](https://kortix.com/docs/project/manifest) |

Kortix, the open-source AI Operating System, is the platform these answers describe: agents, skills, memory, connector configuration and triggers as text in one repository the company owns, with each session on an isolated machine and human review before work lands on the default branch ([kortix.com](https://kortix.com)).

## Scoring an answer sheet

A useful scoring rule, in one line: **one point per question whose answer is a link to a document you can read, half a point for a description you could verify in a trial, zero for a description you cannot.**

In practice the scores cluster, and the cluster is the finding:

- A closed hosted product tends to answer *permissions* and *data* well, and *record* and *exit* with its own reporting UI and an export endpoint. The Compliance API window and the retention default are the two numbers to write down.
- A desktop app with an open licence tends to answer *exit* well (you have the code) and *data* and *record* with "on the user's machine", which is exactly where a company's obligations do not stop. The [licence audit](https://github.com/ArtemShatokhin/openwork-licence-audit) in this set shows the harder version of that question: MIT outside `ee/`, and the org control plane inside it.
- The awkward middle is the platform that self-hosts the runtime and keeps the control plane, because the answer to *data-2* ("what still calls out to the vendor") then decides the whole review.

What none of that tells you is whether the product is any good. This questionnaire is a filter to run first, not a substitute for the trial.

## What the record looks like when a vendor moves the goalposts

One concrete case, recorded rather than argued, because it is why the questions ask for a document and a date: through early 2026 third-party write-ups said Claude Cowork activity was excluded from Anthropic's Compliance API on every tier. Anthropic's page now says Cowork sessions are captured there, with a 30-day window, local session history that admins cannot centrally delete, and an OpenTelemetry stream that "doesn't replace audit logging for compliance purposes". Every one of those sentences is quoted, dated and re-checked by script in [claude-cowork-audit-record](https://github.com/ArtemShatokhin/claude-cowork-audit-record). An answer sheet that does not carry a date is a rumour.

## Use and contribute

Send the email version to two or three vendors at once; the comparison is the point. Add questions your own reviewers ask for — one per pull request, with the red flag that motivated it. This is documentation, not legal advice, and not a certification.
