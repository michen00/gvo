# gvo

guidance vs. outlines

## Overview

we're here to compare two structured generation libraries.

### agentic use cases

we will reimplement each tutorial using the other library, and compare the results.

<https://github.com/guidance-ai/guidance/blob/main/notebooks/tutorials/tool_calling.ipynb>

<https://dottxt-ai.github.io/outlines/latest/examples/react_agent/>

(we should probably download our own copies and commit)

### dynamic task-based evaluation

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

### objective tasks

#### repeat after me

- lorem ipsum\*
- 50-100 digits of pi
- tongue twister\*
- regex patterns\*
- consecutive white spaces\*
- arbitrary text generation\*
- \*(some of these can be generated with a small model)
