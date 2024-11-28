<a href="https://livekit.io/">
  <img src="./.github/assets/livekit-mark.png" alt="LiveKit logo" width="100" height="100">
</a>

# Guided Meditation Voice Assistant

A voice-interactive meditation assistant that creates personalized guided meditation sessions using AI. The assistant asks for your desired meditation duration, generates a custom meditation script, and guides you through the session with calming background music.

## Features

- **Voice Interaction**: Natural voice commands to set up your meditation session
- **AI-Generated Meditations**: Custom meditation scripts generated using Cerebras LLaMA 3.1 70B model
- **Background Audio**: Calming background music during meditation sessions
- **Dynamic Timing**: Automatically paces meditation instructions based on session length
- **High-Quality Voice**: Uses Cartesia TTS for natural-sounding meditation guidance
- **Accurate Speech Recognition**: Leverages Deepgram for reliable voice command interpretation

## Requirements

- Python 3.8+
- LiveKit Agents Framework
- Required API Keys:
  - Cerebras API key
  - LiveKit credentials
  - Cartesia API key
  - Deepgram API key

## Installation

### Clone the Repository

```bash
git clone <repository-url>
cd guided-meditation-assistant
```

### Set Up Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
```

### Install Dependencies

```bash
pip install livekit-agents
pip install livekit-plugins-openai
pip install livekit-plugins-silero
pip install livekit-plugins-cartesia
pip install livekit-plugins-deepgram
```

### Environment Variables

Create a `.env` file with the following:

```bash
LIVEKIT_URL=your-livekit-url
LIVEKIT_API_KEY=your-livekit-api-key
LIVEKIT_API_SECRET=your-livekit-api-secret
CEREBRAS_API_KEY=your-cerebras-api-key
CARTESIA_API_KEY=your-cartesia-api-key
DEEPGRAM_API_KEY=your-deepgram-api-key
```

## Project Structure

- **`agent.py`**: Main application entry point and meditation session orchestration
- **`audio_handler.py`**: Manages background audio playback during meditation
- **`assistant_functions.py`**: Contains meditation script generation logic using Cerebras inference

## Usage

### Start the Meditation Assistant

```bash
python agent.py start
```

### Development Mode

```bash
python agent.py dev
```

### Connect to a Specific Room

```bash
python agent.py connect --room <room-name>
```

## How It Works

1. The assistant greets you and asks for your desired meditation duration
2. Using the Cerebras LLaMA 3.1 70B model, it generates a custom meditation script
3. The script is delivered through high-quality Cartesia text-to-speech
4. Soothing background music plays throughout your session
5. The assistant guides you through the meditation with perfectly timed instructions
6. The session concludes with a gentle closing message

## Testing

You can test the meditation assistant using the LiveKit Agents Playground:
- Visit [agents-playground.livekit.io](https://agents-playground.livekit.io/)
- Connect to your LiveKit server
- Join a room where your meditation assistant is running

## Background Audio

The application includes a `serene_waters.wav` file for background ambiance. You can replace this with your own audio file by:
1. Ensuring your audio file is in WAV format
2. Updating the filename in `agent.py`
3. Adjusting volume levels in `audio_handler.py` if needed.

---

For support or questions, please open an issue in the repository.
