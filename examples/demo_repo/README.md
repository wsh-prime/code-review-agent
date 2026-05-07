# Demo Shop

Small Python project used to demonstrate `code-review-agent`.

It intentionally contains:

- normal application code under `src/shop/`
- related tests under `tests/`
- design notes under `docs/`
- a few process artifacts at the repository root for `hygiene` to classify
- review patches under `patches/`

Useful demo commands:

```powershell
code-review-agent hygiene --repo examples/demo_repo --out outputs/demo-hygiene
code-review-agent map --repo examples/demo_repo --out outputs/demo-map
code-review-agent review --repo examples/demo_repo --diff examples/demo_repo/patches/case_001_test_gap.patch --out outputs/demo-review
```
