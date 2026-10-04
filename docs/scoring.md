# Deterministic Job Match Score

The API computes the displayed score from seven factors and fixed weights. Each
factor is on a 0–100 scale; the overall score is the rounded weighted sum.

| Factor | Weight |
| --- | ---: |
| Keyword and skill match | 25% |
| Required requirements | 20% |
| Experience evidence | 15% |
| Resume structure | 10% |
| Education match | 10% |
| Job-language overlap | 10% |
| ATS-style readability | 10% |

Skills are detected from a small explicit alias list. A direct alias match
earns full credit, partial evidence earns half credit, and a missing skill
earns zero for the skill factors. Required/preferred classification is inferred
from wording and section headings; unlabelled requirements default to
preferred so the analyzer does not overstate what an employer requires.

The current “job-language overlap” factor compares repeated words only. It is
not an embedding model or a proprietary ATS score. The formatting factor uses
basic extracted-text and heading checks and cannot predict every parser.
