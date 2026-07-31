2-Hour Workshop
===============

0\. Introduction (10 min)
-------------------------

### Why Voice is the Next UI

Talk about how we've moved through:

*   Desktop → GUI
    
*   Mobile → Touch
    
*   ChatGPT → Text
    
*   AI Agents → Voice
    

Examples:

*   Customer support
    
*   Restaurant ordering
    
*   Medical assistant
    
*   Personal assistant
    
*   Coding assistant
    

Then ask:

> Why is voice harder than chat?

This naturally leads into the architecture.

1\. How Voice AI Works (10 min)
===============================

This section should explain the naive pipeline — the version most tutorials show.

Traditional Architecture

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   User  ↓  Speech To Text  (Whisper)  ↓  LLM  (GPT)  ↓  Tool Calls  (Database/API)  ↓  LLM  ↓  Text To Speech  ↓  Audio   `

Explain:

*   STT converts speech into text
    
*   LLM reasons
    
*   Tool calls fetch data
    
*   TTS converts answer into speech
    

Discuss drawbacks — **if implemented naively, i.e. wait for each stage to fully finish before starting the next one**:

*   Multiple network calls
    
*   Latency
    
*   Voice interruptions
    
*   No streaming
    
*   Robotic feeling
    

Flag explicitly that this "naive" caveat matters — it sets up the next section, where we show this isn't actually how production systems work today.

2\. Production Reality: Modular vs Unified Architectures (15 min)
==================================================================

### The "traditional pipeline is slow" story is incomplete

Most production voice AI companies today **still don't use end-to-end speech
models**. They use separate STT + LLM + TTS — because it gives them better
control, lower cost, and more flexibility. The "it's slow" story from Section 1
is only true if you implement it naively. Modern systems optimize every stage.

### What a production-grade modular pipeline actually looks like

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   User speaks  ↓  Streaming STT (Deepgram, Gladia, Speechmatics, Google, AssemblyAI, OpenAI gpt-4o-transcribe)  ↓  Partial transcripts every 100-300ms  ↓  LLM starts reasoning before user finishes speaking  ↓  Tool calls execute in parallel  ↓  Streaming TTS (ElevenLabs, Cartesia, OpenAI TTS, Azure)  ↓  Audio streamed back immediately   `

### The five key optimizations

**1. Streaming STT (not wait-until-finished)**

Instead of waiting for the user to stop talking, the STT service continuously
emits partial transcripts:

```
200ms → "I want"
400ms → "I want to"
700ms → "I want to book"
1.0s  → "I want to book a"
1.2s  → "I want to book a flight"
```

The LLM can begin processing before the sentence is complete.

**2. Incremental LLM generation**

The LLM doesn't wait for the entire transcript either — it starts generating
tokens as soon as it has enough confidence about the user's intent.

**3. Streaming TTS**

Instead of generating the full response and then synthesizing speech, TTS
starts speaking as soon as the first text tokens are available. Speech
synthesis overlaps with text generation:

```
"The"                         → TTS starts speaking
"The weather"                 → continues speaking
"The weather in Pune is..."   → still speaking, still generating
```

**4. Parallel tool execution**

If the user asks "What's the weather in Pune?", a well-designed system
doesn't wait for the LLM to finish a long response before calling the weather
API. It identifies the tool call quickly, starts the API request, and
prepares the response template while the API call is in flight — minimizing
idle time.

**5. Voice Activity Detection (VAD)**

Modern systems use VAD to determine when the user has likely finished
speaking, rather than waiting for a long silence. This alone can shave
hundreds of milliseconds off every interaction.

### Typical latency breakdown

A well-optimized modular pipeline might look like:

| Stage | Latency |
|---|---|
| Streaming STT | 150–300 ms |
| LLM first token | 150–400 ms |
| Streaming TTS first audio | 100–200 ms |

Users often hear the first spoken response in **400–900 ms** overall — which
feels very natural, and is a far cry from the naive pipeline's 2–6 seconds.

### Then why use GPT Realtime at all?

Its value isn't just lower latency — it's **simplifying the architecture**.

With a modular stack, you manage: mic → STT provider → LLM → TTS provider →
audio player. That means handling different APIs, synchronization, partial
transcripts, audio formats, barge-in, conversation state, and timing between
every component yourself.

With GPT Realtime: mic → GPT Realtime → speaker. A single session handles
speech recognition, language understanding, response generation, speech
synthesis, streaming, interruptions, turn detection, and conversation
management. The trade-off is **simplicity versus flexibility**.

### Why many companies still choose separate STT + LLM + TTS

Because they can optimize each component independently:

*   Use the best STT for noisy call centers
    
*   Use a domain-specific LLM for reasoning
    
*   Choose a TTS voice that matches their brand
    
*   Swap providers without redesigning the whole system
    
*   Reduce costs by selecting cheaper services per stage
    

Common production stacks look like:

```
Deepgram → Claude / GPT / Llama → Cartesia
Gladia   → Gemini               → ElevenLabs
```

This modular architecture is very common in enterprise deployments.

### Present both as valid architectures

**Architecture 1 — Modular Voice Stack** (most common in production)

```
Mic → Streaming STT → LLM → Streaming TTS → Speaker
```

| Pros | Cons |
|---|---|
| Lower operational cost in many cases | More engineering effort |
| Best-in-class components | Multiple APIs and failure points |
| Easier to customize | More orchestration required |
| Provider flexibility | |

**Architecture 2 — Unified Realtime Model**

```
Mic → GPT Realtime → Speaker
```

| Pros | Cons |
|---|---|
| Much simpler architecture | Less control over individual components |
| Built-in interruption handling | Tied to a single provider's capabilities |
| Native multimodal interaction | May not be the most cost-effective at very high scale |
| Faster to prototype and launch | |

Showing both — and explaining why different companies choose different
architectures — gives attendees a much more accurate picture of the current
state of production voice AI, instead of a strawman "realtime is always
better" narrative.

3\. Realtime API Architecture (15 min)
======================================

Draw this.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   Browser  ↓  WebRTC/WebSocket  ↓  GPT Realtime API  ↓  Audio In  ↓  Reasoning  ↓  Audio Out   `

Explain every component.

Cover:

*   Session
    
*   Events
    
*   Audio chunks
    
*   Conversation state
    
*   Streaming responses
    

4\. Demo Architecture (10 min)
==============================

Explain what students are building.

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   Browser  ↓  Mic  ↓  Realtime API  ↓  Function Calling  ↓  Local FastAPI  ↓  Weather  Order Status  Calculator  Inventory  ↓  Realtime  ↓  Speaker   `

5\. Coding Session (40 min)
===========================

This should be the majority.

Step 1

Create session

Step 2

Connect browser

Step 3

Capture microphone

Step 4

Send audio

Step 5

Receive audio

Step 6

Play response

Students should already have the starter project cloned.

6\. Events Deep Dive (10 min)
=============================

Explain the important events.

Examples:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   session.created  input_audio_buffer.append  input_audio_buffer.commit  response.create  response.audio.delta  response.audio.done  response.done   `

Show them live in DevTools.

Students love seeing raw events.

7\. Tool Calling (20 min)
=========================

Probably the coolest section.

Architecture

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   User  ↓  "I want to order pizza"  ↓  GPT  ↓  Function Call  ↓  FastAPI  ↓  JSON  ↓  GPT  ↓  Voice Response   `

Create 2–3 simple tools.

Example

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   get_weather()  search_product()  place_order()  get_stock_price()   `

Explain:

*   Tool schema
    
*   Parameters
    
*   JSON
    
*   Returning results
    

This teaches how voice agents become useful.

8\. Prompt Engineering for Voice (10 min)
=========================================

Different from chat.

Teach:

Instead of

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   You are helpful.   `

Use

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   Be concise.  Speak naturally.  Never exceed 2 sentences.  Avoid markdown.  Pause before answering.  Confirm actions.  Ask one question at a time.   `

Explain why.

9\. Advanced Features (5 min)
=============================

Mention without deep diving.

*   Voice selection
    
*   Interruptions (barge-in)
    
*   Voice Activity Detection (VAD)
    
*   Streaming transcripts
    
*   Emotion
    
*   Background noise
    
*   Multi-language
    
*   Context window management
    

10\. Q&A + Next Steps (5 min)
=============================

Show what's possible next.

*   MCP integration
    
*   Calendar booking
    
*   RAG
    
*   CRM
    
*   Twilio phone agent
    
*   SIP calling
    
*   Browser agent
    
*   Customer support agent
    

Live Demo Flow
==============

Keep one exciting end-to-end demo ready:

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   "Hi"  ↓  AI responds  ↓  "What's the weather in Pune?"  ↓  Calls tool  ↓  Returns weather  ↓  "Book me a meeting tomorrow"  ↓  Calls calendar tool  ↓  Confirms booking  ↓  "Summarize today's AI news"  ↓  Calls news tool  ↓  Reads summary   `

This demonstrates conversation, memory, and tool use in one flow.

What NOT to Cover
=================

Avoid these in a 2-hour beginner workshop, as they can consume time without helping attendees build a working agent:

*   Training speech models
    
*   Transformer internals
    
*   Whisper architecture details
    
*   Neural vocoders
    
*   Tokenization
    
*   Audio codecs
    
*   WebRTC internals
    
*   SIP protocol
    
*   LangChain/LangGraph
    
*   Multi-agent orchestration
    
*   Fine-tuning
    

Suggested Agenda
================

| Time | Topic |
|---|---|
| 0–10 min | Why Voice AI & workshop overview |
| 10–20 min | Traditional Voice Pipeline (STT → LLM → TTS) — the naive version |
| 20–35 min | Production Reality: modular (streaming STT/LLM/TTS) vs unified Realtime — why both exist |
| 35–50 min | GPT Realtime API concepts & event model |
| 50–90 min | Hands-on: Build a browser-based voice agent |
| 90–110 min | Add function/tool calling with a FastAPI backend |
| 110–120 min | Prompt engineering, advanced capabilities, Q&A |

Note: your audience is **AI builders**, so don't skip Section 2. Attendees
should leave knowing that GPT Realtime is one valid architecture among
several — not the only way production voice agents are built — and why
today's demo still uses it (simplicity, faster to prototype, good enough
latency for this use case).