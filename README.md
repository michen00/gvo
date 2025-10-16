# gvo

Guidance vs. Outlines

## Overview

This project compares two structured generation libraries: [guidance](https://github.com/guidance-ai/guidance) and [Outlines](https://github.com/dottxt-ai/outlines).

### Main differences (guidance vs outlines)

A concise comparison to help decide which library to use for a task:

- **Guidance**

  - Programming model: Python-first DSL that interleaves control flow and generation via context managers (`system`, `user`, `assistant`) and guidance functions (`gen`, `select`, `one_or_more`).
  - Strengths: Fine-grained control, constrained decoding with regex/CFG grammars, token healing and fast-forwarding, notebook widgets, and straightforward tool integration.
  - Best for: workflows that need programmatic orchestration, custom generation loops, or experiments with advanced constraint strategies across multiple backends (Transformers, llama.cpp, OpenAI, etc.).

- **Outlines**
  - Programming model: Schema-first API that takes a prompt plus a Python type (e.g., `Literal`, `BaseModel`, `Regex`) and guarantees the structure during decoding.
  - Strengths: Reliable structured outputs, reusable generators that cache compiled constraints, provider-agnostic adapters (OpenAI, vLLM, Ollama, Transformers, llama.cpp, Gemini, MLX), and a rich library of output types.
  - Best for: production pipelines that require validated JSON-like payloads with minimal glue code and teams that prefer declarative type hints over imperative control flow.

### Agentic Use Cases

We will reimplement two tutorials, each using the other library, and compare the results.

<https://github.com/guidance-ai/guidance/blob/main/notebooks/tutorials/tool_calling.ipynb>

<https://dottxt-ai.github.io/outlines/latest/examples/react_agent/>

Local copies:

- `docs/tutorials/guidance/tool_calling.ipynb`
- `docs/tutorials/outlines/react_agent.md`

### Dynamic Task-Based Evaluation

TODO: define a set of tasks that can be used to evaluate the performance of each library.

#### objective metrics

- correctness
  - edit distance
  - embedding similarity
- latency
  - time to first token
  - time to complete
- cost (estimated)
  - $ per 1K tokens
  - $ per call

#### subjective metrics

...

### Objective Tasks

#### repeat after me

- lorem ipsum\*
- 50-100 digits of pi
- tongue twister\*
- regex patterns\*
- consecutive white spaces\*
- arbitrary text generation\*
- \*(some of these can be generated with a small model)
