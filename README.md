# Session 29 — Tool Calling and AI Agents
### NextLeap · Gen AI Engineering Programme · Module 7 (RAG, Agents, Deployment & Governance)

60-minute session for UK working professionals with basic Python. Learning outcome: **design agent
workflows that connect LLM reasoning to controlled external actions.**

## What's in this folder

| File | Purpose |
|---|---|
| `Session_29_Tool_Calling_and_AI_Agents.pptx` | 21-slide teaching deck, 16:9, speaker notes on every slide |
| `Session_29_Tool_Calling_and_AI_Agents.ipynb` | Notebook: define tools, build the agent, run the loop, add a step cap + human gate |
| `data/knowledge_base.json` | A tiny internal KB the agent's search tool looks things up in |
| `data/tool_schema_template.json` | The homework template — define tools + safety rules for a workplace agent |
| `figures/` | Self-made diagrams (tool calling, agent loop, plan vs act, tool selection, human-in-the-loop, failure modes) |

## Session outline

**Theory (~70%):** the shift from a fixed pipeline to a model that chooses; tool/function calling
(the model *requests*, your code *runs*); the agent loop (reason → act → observe); planning vs acting;
tool selection by name and description; human-in-the-loop gating of consequential actions; the six
common agent failure modes and how to design against them.

**Practical (~30%, Gemini API + LangChain):** define tools with the `@tool` decorator; build an agent
with `create_tool_calling_agent` + `AgentExecutor`; watch it select among a calculator, a KB search,
and a gated refund tool; add a step cap (`max_iterations`) and a human approval gate; run a small
workplace-assistant mini-project.

**Homework:** write safety rules and tool schemas for a workplace agent, using
`data/tool_schema_template.json`.

## Running the notebook

```
pip install langchain langchain-google-genai
export GEMINI_API_KEY="your-key-here"
jupyter notebook Session_29_Tool_Calling_and_AI_Agents.ipynb
```

Get a free API key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey).

**Swapping the LLM:** the model is a single `ChatGoogleGenerativeAI` object. Replace it with
`ChatOpenAI` or `ChatOllama` (and its import) to change provider — the tools and agent are unchanged.

**Safety note on the calculator:** the demo uses a character-whitelisted `eval` for simplicity. In
production, never run `eval` on model-generated input — use a dedicated maths-expression parser.

**Note on outputs:** the sandbox this pack was built in has no internet access to the Gemini API, so
every notebook cell was verified to be syntactically correct (`ast.parse`) and the notebook ships with
**outputs cleared**. Students see the agent's real reasoning trace the first time they run it locally.

## Continuity

- **Previous:** Session 28 — Building a RAG Chatbot (the fixed retrieve-then-generate pipeline this
  agent generalises by letting the model choose).
- **Next:** Session 30 — Deployment, Monitoring & Governance (the course finale: taking these systems
  into production responsibly).

## References

- LangChain — [Tools & how to create tools](https://docs.langchain.com/oss/python/langchain/tools) (`@tool`, args schemas).
- LangChain — [Agents](https://docs.langchain.com) (`create_tool_calling_agent`, `AgentExecutor`).
- Google — [Gemini API function calling](https://ai.google.dev/gemini-api/docs/function-calling).
- Yao et al. (2023) — *ReAct: Synergizing Reasoning and Acting in Language Models* (the reason-act-observe loop).
- Schick et al. (2023) — *Toolformer: Language Models Can Teach Themselves to Use Tools*.
- NextLeap Sessions 25 & 28 — Structured Outputs and Prompt Evaluation; Building a RAG Chatbot.
