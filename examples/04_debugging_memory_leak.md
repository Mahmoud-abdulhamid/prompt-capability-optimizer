# Example 04: Debugging Memory Leaks

## 1. Raw User Input
```text
Find and fix the memory leak in this application.
```

## 2. Optimizer Processing & Capability Analysis
- **Task Depth**: Level 2 (Debugging / Runtime Performance)
- **Primary Intent**: Diagnose root cause of unbounded heap growth, analyze event listeners, caches, or uncollected closures, reproduce the issue deterministically, apply surgical fix, and verify heap stabilization.
- **Discovered Capabilities**:
  - Memory profiling (Heap snapshots, V8 inspector, memory dumps).
  - Concurrency & Async leak patterns (unbounded maps, lingering subscriptions, unclosed streams).
  - Benchmark & stress testing (Node.js `--inspect`, clinic.js, k6).
- **Output Mode**: Mode B (Optimize + Prepare).

---

## 3. Optimized Prompt Output

```text
ROLE:
Senior Performance Engineer & Runtime Diagnostics Specialist

OBJECTIVE:
Systematically locate, diagnose, and remediate the memory leak in the application, verify heap reclamation through automated garbage collection metrics, and ensure zero performance regressions.

INVESTIGATION PROTOCOL:
- Never guess the root cause. Follow evidence-based runtime analysis.
- Inspect common memory leak vectors:
  1. Global caches without eviction policy (e.g., unbounded JavaScript Maps/Objects).
  2. Uncleaned event listeners (`EventEmitter.on` without `.removeListener` / DOM listeners).
  3. Closures retaining references to large scopes or detached DOM nodes.
  4. Lingering WebSocket / database connections or unclosed streams.
  5. Asynchronous timers (`setInterval`) that never get cleared.

CONSTRAINTS:
- The fix must be surgical and minimal; do not refactor unrelated codebase logic.
- Must not introduce performance bottlenecks or latency regressions to fix the leak.

REQUIRED CAPABILITIES & TOOLS:
- Diagnostics: Node.js `--inspect`, heapdump, or Chrome DevTools memory snapshot.
- Execution: `run_command` to execute memory stress scripts under load.

IMPLEMENTATION STEPS:
1. Reproduction:
   - Create a minimal reproduction script or load test triggering memory accumulation under repeated iterations.
2. Root Cause Isolation:
   - Inspect retained heap size and dominator trees to pinpoint the leaking allocation site.
3. Code Remediation:
   - Introduce bounded caches (e.g., LRU cache with TTL and max items), dispose of listener handles, or replace strong references with `WeakMap`/`WeakSet`.
4. Verification & Garbage Collection Assertion:
   - Run reproduction test under heap monitoring (`v8.getHeapStatistics()` or `process.memoryUsage()`).
   - Trigger explicit garbage collection (`node --expose-gc`) before and after iterations to prove memory stabilizes at baseline.

VERIFICATION DIRECTIVES:
- Run memory benchmark: `node --expose-gc test/memory-leak.test.js`.
- Assert resident set size (RSS) and HeapUsed remain bounded within expected thresholds under 10,000 synthetic requests.

COMPLETION CRITERIA:
Heap growth graph plateaus under sustained load; reproduction script confirms clean object deallocation.
```
