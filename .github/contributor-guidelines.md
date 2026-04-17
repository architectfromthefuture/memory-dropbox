# Contributor guidelines: architecture and conventions

This project is a local-first, memory-first, event-driven system—not a typical CRUD or UI-first application. Memory and state persist and evolve over time.

---

## 1. Core system principles

- Memory comes first.
- The system is stateful and continuously evolving.
- The system exists independently of the UI.
- The UI is an observability and interaction layer, not the execution driver.
- Prefer event-driven design over purely request/response patterns.
- Deterministic services handle ingestion, indexing, and persistence.
- Agents handle synthesis, summarization, prioritization, and interpretation.
- All conclusions should be traceable back to stored memory or source data.

---

## 2. System architecture model

Two primary layers:

### A. Live system (always running)

- ingestion, indexing, memory updates, background processing, event emission, agent activity

### B. Interaction layer (user-facing)

- querying system state, inspecting outputs and memory, validating conclusions, steering priorities

Do not collapse these layers.

---

## 3. Repository roles

Respect repository boundaries unless explicitly coordinated.

- **memory-dropbox** — memory substrate (ingestion, storage, indexing, retrieval)
- **Obversary-OS** — runtime (event system, agent orchestration, system state)
- **ai-systems-atlas** — research and ontology (not runtime logic)

Do not merge responsibilities across repos without a clear plan.

---

## 4. Implementation priorities

Build in this order:

1. Event layer  
2. Memory persistence  
3. Indexing and retrieval  
4. Observability of system state  
5. Controlled agent behavior  

Avoid: UI-first design, multiple agents early, autonomous loops without clear outputs, speculative abstraction.

---

## 5. Contribution workflow

- Prefer small, incremental steps.
- Keep code readable and explicit.
- Identify which layer (memory, event, agent, UI) a change belongs to.
- Preserve existing behavior unless you are explicitly changing it.

---

## 6. Event-driven discipline

Emit events for meaningful system changes (e.g. ingestion completed, indexing completed, contradiction detected). Prefer components that react to events over only direct calls. Keep event definitions simple.

---

## 7. Memory model expectations

Memory is not only a vector database. Consider: source memory, semantic memory, episodic memory, and working memory when adding features.

---

## 8. Agent discipline

Agents operate on existing memory, respond to events, produce structured outputs, and stay limited in scope. Avoid unnecessary multi-agent complexity and self-directed loops without persistence.

---

## 9. Failure modes to avoid

- UI-first design creeping in  
- Request/response patterns replacing system-state thinking  
- Unnecessary abstraction layers  
- Overuse of “agents” without clear responsibility  
- Code that does not map to memory or event flow  

---

## 10. Guiding principle

This is a memory-first system. Implementation should help answer: what changed, what is known, what is uncertain, and what needs attention.
