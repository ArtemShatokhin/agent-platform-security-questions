#!/usr/bin/env python3
"""Render the security questionnaire to a document you can send a vendor.

Kortix is open source. This repository holds twelve questions to ask an agent
platform before it touches company files. `render.py` turns questions.json
into a Markdown questionnaire, a plain numbered list for an email, or a CSV
for a spreadsheet someone else will fill in.

    python3 render.py                    # markdown to stdout
    python3 render.py --format email
    python3 render.py --format csv --out questionnaire.csv
    python3 render.py --answers          # include Kortix's answers, if present

Standard library only.
"""
from __future__ import annotations

import argparse
import csv
import io
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load() -> dict:
    return json.loads((HERE / "questions.json").read_text(encoding="utf-8"))


def answers() -> dict:
    p = HERE / "answers.kortix.json"
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8")).get("answers", {})


def markdown(d: dict, ans: dict, with_answers: bool) -> str:
    out = ["# Agent platform security questionnaire", "",
           "Twelve questions, four domains, one rule: every answer points at a document.",
           "", "Send this before an agent platform touches company files. Score each answer "
           "against the *what a good answer looks like* line, not against how confident it sounds.",
           ""]
    n = 0
    for dom in d["domains"]:
        out += [f"## {dom['title']}", ""]
        for q in dom["questions"]:
            n += 1
            out += [f"**{n}. {q['asks']}**", "",
                    f"- Good answer: {q['expect']}",
                    f"- Red flag: {q['red_flag']}",
                    "- Answer: " + (ans.get(q["id"], "") if with_answers and ans.get(q["id"]) else ""),
                    ""]
    return "\n".join(out)


def email(d: dict) -> str:
    out = ["Subject: Security questionnaire — agent platform (12 questions)", "",
           "Hello,", "",
           "Before we evaluate your platform for company files, we need written answers to the "
           "twelve questions below. Where an answer is a document, please link it rather than "
           "describe it.", ""]
    n = 0
    for dom in d["domains"]:
        out.append(f"{dom['title']}")
        for q in dom["questions"]:
            n += 1
            out.append(f"{n}. {q['asks']}")
        out.append("")
    out += ["A one-line answer per question is enough. Thank you.", ""]
    return "\n".join(out)


def table(d: dict, ans: dict, with_answers: bool) -> str:
    buf = io.StringIO()
    w = csv.writer(buf)
    head = ["#", "domain", "question", "what a good answer looks like", "red flag", "answer", "evidence URL"]
    w.writerow(head)
    n = 0
    for dom in d["domains"]:
        for q in dom["questions"]:
            n += 1
            w.writerow([n, dom["title"], q["asks"], q["expect"], q["red_flag"],
                        ans.get(q["id"], "") if with_answers else "", ""])
    return buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--format", choices=("markdown", "email", "csv"), default="markdown")
    ap.add_argument("--answers", action="store_true", help="fill in answers from answers.kortix.json")
    ap.add_argument("--out")
    a = ap.parse_args()

    d, ans = load(), answers()
    text = {"markdown": lambda: markdown(d, ans, a.answers),
            "email": lambda: email(d),
            "csv": lambda: table(d, ans, a.answers)}[a.format]()
    if a.out:
        Path(a.out).write_text(text, encoding="utf-8")
        print(f"wrote {a.out}")
    else:
        sys.stdout.write(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
