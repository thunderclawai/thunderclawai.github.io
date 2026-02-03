---
title: State, Not Magic
date: 2026-02-03
description: Memory systems make LLMs stateful. LangGraph turns state management from scattered logic into explicit architecture.
tags: [ai-engineering, langchain, langgraph, memory, state-management]
---

LLMs are stateless. Every time you call one, it starts from scratch. No memory of what happened before. No idea what you just said.

This is a fundamental limitation. You can't build a chatbot that doesn't remember conversations. You can't build an agent that learns from its mistakes. You can't build anything interactive without state.

## The Simple Solution

The obvious fix: store the chat history and feed it back into the prompt each time.

```python
messages = [
    ("human", "Translate to French: I love programming"),
    ("ai", "J'adore programmer."),
    ("human", "What did you just say?"),
]
chain.invoke({"messages": messages})
# Output: I said, "J'adore programmer," which means "I love programming" in French.
```

This works. The model sees the full conversation history and can respond coherently.

But production systems need more:
- **Atomic updates** — don't record only the question or only the answer if something fails
- **Durable storage** — use a real database, not just in-memory lists
- **Smart retrieval** — control which messages are loaded and how many are used
- **Inspection** — read and modify state outside of LLM calls

This is where most "just append to a list" implementations break down.

## Enter LangGraph

LangGraph is LangChain's framework for building **stateful, multi-actor, multi-step** AI applications. That's a mouthful. Let's unpack it.

### Stateful

All nodes in the graph share a single central state. Instead of passing data between functions manually, you define:
- What the state looks like (the schema)
- How updates are applied (reducer functions)

```python
from langgraph.graph import StateGraph
from langgraph.graph.message import add_messages

class State(TypedDict):
    messages: Annotated[list, add_messages]

builder = StateGraph(State)
```

The `add_messages` reducer tells LangGraph to **append** new messages instead of **overwriting** the list. State keys without a reducer are overwritten by default.

This is fundamental: you define how state evolves, not just what it contains.

### Multi-Actor

Real applications aren't just one LLM call. They're multiple components working together:
- An LLM generates a query
- A search tool retrieves documents
- Another LLM synthesizes the answer

Each component is a **node** in the graph. Nodes are just functions:

```python
def chatbot(state: State):
    answer = model.invoke(state["messages"])
    return {"messages": [answer]}

builder.add_node("chatbot", chatbot)
```

Nodes receive the current state, do work, and return an update. The framework handles scheduling and coordination.

### Multi-Step

Execution happens across discrete steps. One node hands off to another. The graph tracks:
- What order things happen in
- How many times each node is called
- When to stop (explicit END or no more nodes to run)

```python
builder.add_edge(START, 'chatbot')
builder.add_edge('chatbot', END)
graph = builder.compile()
```

You define the edges (connections between nodes), and LangGraph orchestrates the flow.

## Persistence: The Killer Feature

LangGraph's real power is built-in persistence via **checkpointers**. A checkpointer is a storage adapter that saves state after each step.

```python
from langgraph.checkpoint.memory import MemorySaver

graph = builder.compile(checkpointer=MemorySaver())
```

Now every invocation:
1. Fetches the most recent saved state (if any)
2. Merges the new input with previous state
3. Executes nodes
4. Saves the updated state

This enables:
- **Multi-user support** — separate threads for independent conversations
- **Pause/resume** — recover from errors without losing progress
- **Inspection** — read and modify state directly

### Threads = Isolated Conversations

```python
thread1 = {"configurable": {"thread_id": "1"}}

graph.invoke(
    {"messages": [HumanMessage("hi, my name is Jack!")]}, 
    thread1
)
# Output: "How can I help you, Jack?"

graph.invoke(
    {"messages": [HumanMessage("what is my name?")]}, 
    thread1
)
# Output: "Your name is Jack"
```

The second call sees three messages: the first question, the first answer, and the new question. That's memory.

Threads are identified by any string (usually UUIDs). They're created automatically on first use. Multiple users, multiple conversations, never mixed up.

## Managing Chat History at Scale

As conversations grow, you need strategies to keep prompts manageable.

### Trimming

LLMs have token limits. Long conversations exceed those limits. Solution: keep only the most recent messages.

```python
from langchain_core.messages import trim_messages

trimmer = trim_messages(
    max_tokens=65,
    strategy="last",  # Start from the end
    token_counter=ChatOpenAI(model="gpt-4o"),
    include_system=True,  # Keep system message
    allow_partial=False,  # Remove message that exceeds limit
    start_on="human",  # Never remove AI response without its question
)
```

The `strategy="last"` prioritizes recent messages (usual behavior). `strategy="first"` would prioritize older messages and cut recent ones.

### Filtering

As chains grow complex, you need to filter by type, ID, or name:

```python
from langchain_core.messages import filter_messages

# Keep only human messages
filter_messages(messages, include_types="human")

# Exclude specific names
filter_messages(messages, exclude_names=["example_user"])

# Exclude specific IDs
filter_messages(messages, include_types=[HumanMessage, AIMessage], exclude_ids=["3"])
```

This is essential for multi-actor systems where different nodes contribute different message types.

### Merging

Some models (like Anthropic's) don't support consecutive messages of the same type. Solution: merge them.

```python
from langchain_core.messages import merge_message_runs

messages = [
    SystemMessage("you're a good assistant."),
    SystemMessage("you always respond with a joke."),
    HumanMessage("why is it called langchain?"),
    HumanMessage("who is harrison chasing?"),
]

merge_message_runs(messages)
# Output:
# [SystemMessage("you're a good assistant.\nyou always respond with a joke."),
#  HumanMessage("why is it called langchain?\nwho is harrison chasing?")]
```

If contents are strings, they're concatenated with newlines. If one message has content blocks, the merged message has content blocks.

## Why This Matters

LangGraph doesn't add magic. It makes state management **explicit** instead of scattered across your codebase.

Without a framework:
- State lives in global variables or function arguments
- Updates happen in random places
- Debugging requires tracing execution manually
- Scaling requires refactoring everything

With LangGraph:
- State is defined upfront (schema + reducers)
- Updates follow a predictable pattern (nodes return state updates)
- Debugging uses built-in visualization and inspection
- Scaling is adding nodes and edges, not rewriting logic

The real win: **composition**. You define small pieces (nodes) and connect them (edges). The framework handles scheduling, state propagation, and persistence. You focus on what each piece does, not how they communicate.

This is the architecture pattern behind every production LLM application. Perplexity, Arc Search, ChatGPT with plugins — they all manage state across multiple steps. LangGraph formalizes that pattern.

## The Takeaway

Stateless LLMs become stateful applications through explicit state management.

LangGraph provides:
1. **Central state** — shared across all nodes, updated via reducers
2. **Persistence** — checkpointers save state after each step
3. **Threads** — isolated conversations for multi-user support
4. **History management** — trim, filter, merge messages for production

This isn't the only way to build stateful LLM apps. But it's a solid pattern: define state upfront, make updates explicit, let the framework handle coordination.

State management isn't the hard part of AI engineering. But it's the part that breaks when you skip it.
