# Pipecat

## Overview
Pipecat is an open-source framework for building real-time, streaming AI voice applications with LLM-powered voice assistants.

## Purpose
Pipecat enables developers to create voice AI agents that can speak and listen in real-time, integrating LLMs with telephony systems for intelligent voice interactions.

## Key Concepts

- **Core Function**: Real-time AI voice assistant framework
- **Role**: Voice AI processing engine connecting LLMs to telephony infrastructure
- **Dependencies**: LLM provider (OpenAI, Ollama, etc.), WebSocket/SIP transport, audio processing libraries
- **Integration Points**: Kamailio, FreeSWITCH, WebRTC, external APIs

## Architecture

Pipecat operates as a streaming audio processing pipeline with built-in LLM integration.

### Components

- **Audio Engine**: Real-time audio capture, processing, and playback
- **LLM Connector**: Interface with language models for conversational AI
- **Transport Layer**: WebSocket/SIP transport for telephony integration
- **Pipeline Architecture**: Composable nodes for modular processing
- **Context Manager**: Conversation history and context management

## Configuration

### Essential Settings

```python
# Basic Pipecat setup
import asyncio
from pipecat.audio.vad.silero import SileroVADSettings
from pipecat.transports.services.twilio import TwilioTransports
from pipecat.llm.llm import PromptMode
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner

async def main():
    # Initialize LLM
    llm = OpenAILLM(
        model="gpt-4o",
        system_prompt="You are a voice assistant..."
    )
    
    # Create pipeline
    pipeline = Pipeline([...])
    
    # Run
    runner = PipelineRunner()
    await runner.run(pipeline)
```

### Common Configurations

**VAD (Voice Activity Detection)**:
```python
vad_settings = SileroVADSettings(
    min_silence_duration_ms=500,
    min_speech_duration_ms=250
)
```

**System Prompt**:
```python
system_prompt = """
You are a helpful voice assistant for telecom support.
You can answer questions about SIP, Kamailio, FreeSWITCH, and related topics.
Speak clearly and concisely.
"""
```

**LLM Configuration**:
```python
llm = OllamaLLM(
    model="qwen3.5:35b",
    base_url="http://localhost:11434/v1"
)
```

## Usage Patterns

### Typical Workflows

1. Voice input captured -> VAD detects speech -> audio sent to LLM
2. LLM generates response -> TTS synthesizes speech -> audio played
3. Continuous streaming -> low latency interaction

### Use Cases

- **Voice Assistant**: Interactive voice support for telecom topics
- **Call Routing**: AI-powered IVR with natural language understanding
- **Conversational CRM**: Voice-based customer interaction system
- **Real-time Transcription**: Live speech-to-text with LLM processing

## Protocols Supported

- WebSocket (primary transport)
- SIP (via integration with Kamailio/FreeSWITCH)
- WebRTC (via Pipecat's WebRTC transport)

## Integration

This package integrates with:
- [[Kamailio]] - SIP signaling for voice routing
- [[FreeSWITCH]] - Media server for telephony integration
- [[WebRTC]] - Browser-based voice clients
- LLM providers (OpenAI, Ollama, etc.)

## Troubleshooting

### Common Issues

1. **Issue**: High latency in voice response
   **Solution**: Optimize network, use smaller model, or enable streaming

2. **Issue**: Audio cutting out
   **Solution**: Check VAD settings and bandwidth

3. **Issue**: LLM timeout errors
   **Solution**: Increase timeout values or optimize prompts

## Best Practices

- Use streaming responses for lower perceived latency
- Configure appropriate VAD sensitivity for your environment
- Implement fallback error handling for LLM failures
- Use system prompts to constrain output format
- Monitor token usage and costs

## Related Documents

- [[Core-Packages/Kamailio]]
- [[Core-Packages/FreeSWITCH]]
- [[Protocols/WebRTC]]

---
*Created: 2026-03-06*
*Last Updated: 2026-03-06*
