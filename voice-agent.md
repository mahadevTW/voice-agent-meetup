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

1\. How Voice AI Works (15 min)
===============================

This section should explain the pipeline.

Traditional Architecture

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   User  ↓  Speech To Text  (Whisper)  ↓  LLM  (GPT)  ↓  Tool Calls  (Database/API)  ↓  LLM  ↓  Text To Speech  ↓  Audio   `

Explain:

*   STT converts speech into text
    
*   LLM reasons
    
*   Tool calls fetch data
    
*   TTS converts answer into speech
    

Discuss drawbacks:

*   Multiple network calls
    
*   Latency
    
*   Voice interruptions
    
*   No streaming
    
*   Robotic feeling
    

2\. Why Realtime APIs Exist (10 min)
====================================

Explain the problems.

Without realtime

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   Speak  Wait  Upload audio  Transcribe  LLM  Generate response  Convert to speech  Download speech  Play   `

Latency:

2–6 seconds

Realtime

Plain textANTLR4BashCC#CSSCoffeeScriptCMakeDartDjangoDockerEJSErlangGitGoGraphQLGroovyHTMLJavaJavaScriptJSONJSXKotlinLaTeXLessLuaMakefileMarkdownMATLABMarkupObjective-CPerlPHPPowerShell.propertiesProtocol BuffersPythonRRubySass (Sass)Sass (Scss)SchemeSQLShellSwiftSVGTSXTypeScriptWebAssemblyYAMLXML`   Mic  ↓  Streaming Audio  ↓  GPT  ↓  Streaming Audio Back   `

Talk about:

*   Low latency
    
*   Interruptions
    
*   Natural conversation
    
*   Emotion
    
*   Turn detection
    

This is the biggest conceptual difference.

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

TimeTopic0–10 minWhy Voice AI & workshop overview10–25 minTraditional Voice Pipeline (STT → LLM → TTS)25–35 minWhy Realtime APIs & Agentic Voice Architecture35–50 minGPT Realtime API concepts & event model50–90 minHands-on: Build a browser-based voice agent90–110 minAdd function/tool calling with a FastAPI backend110–120 minPrompt engineering, advanced capabilities, Q&A

One addition I'd strongly recommend
-----------------------------------

Since your audience is **AI builders**, add a **5-minute comparison slide** early in the session:

Traditional PipelineGPT Realtime APISeparate STT, LLM, TTS servicesUnified multimodal modelHigher latencyLow-latency streamingMultiple API integrationsSingle session APIText-first interactionNative audio interactionComplex orchestrationSimpler architecture

This helps attendees immediately understand _why_ they're using the Realtime API instead of assembling Whisper + GPT + TTS, making the rest of the workshop much easier to follow.