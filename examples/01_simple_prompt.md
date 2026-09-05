# Example 01: Simple Informational Prompt

## 1. Raw User Input
```text
Explain this JavaScript function.
```

## 2. Optimizer Processing & Capability Analysis
- **Task Depth**: Level 0 (Simple / Informational)
- **Primary Intent**: Explain code behavior, semantics, parameters, and time/space complexity without unnecessary external toolchain overhead.
- **Discovered Capabilities**: Base language evaluation, algorithmic analysis.
- **Local Skills / MCP**: None required (avoids context bloat).
- **Output Mode**: Mode A (Optimize Only).

---

## 3. Optimized Prompt Output

```text
ROLE:
Senior JavaScript / TypeScript Engine Specialist

OBJECTIVE:
Provide a precise, comprehensive technical explanation of the provided JavaScript function, covering its execution mechanics, algorithmic complexity, parameter expectations, and edge-case behavior.

CONTEXT & INPUT:
Target code: [Insert the JavaScript function to be explained here]

CONSTRAINTS:
- Do not introduce external libraries or rewrite the code unless an antipattern or bug is explicitly identified.
- Keep the explanation concise and technical; avoid superficial commentary.

IMPLEMENTATION REQUIREMENTS:
1. Functional Overview:
   - State the exact purpose of the function in one concise paragraph.
2. Step-by-Step Execution Walkthrough:
   - Trace control flow from input parameters to return value.
   - Clarify scope bindings, closures, asynchronous behavior (Promises/async-await), or mutations if present.
3. Computational Complexity:
   - Time Complexity: Big-O notation with justification.
   - Space Complexity: Auxiliary memory consumption with justification.
4. Edge Cases & Potential Pitfalls:
   - Behavior with unexpected inputs (null, undefined, NaN, type coercion, empty arrays/objects).
   - Any silent failures or unhandled exceptions.

COMPLETION CRITERIA:
Clear, technically accurate breakdown delivered directly to the user with zero irrelevant boilerplate.
```
