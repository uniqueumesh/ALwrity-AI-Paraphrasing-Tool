# AI Paraphrasing Tool

A fast, accessible paraphrasing tool built with Streamlit and Google Gemini. It now uses a secure backend key (no BYOK in the UI) and includes a one‑click “Listen” feature to read results aloud.

## Features

- 🔄 **AI Paraphrasing**: Gemini‑powered rephrasing
- 📝 **800‑Word Limit**: Live counter + validation
- 🎨 **5 Styles**: Balanced, Formal, Casual, Concise, Detailed
- 🎯 **Options**: Preserve tone, maintain similar length
- 🔊 **Listen**: Text‑to‑Audio via AssemblyAI (no download); browser TTS fallback
- 📋 **Copy Text**: One‑click copy
- 🔐 **Secure**: Server‑side API keys only (no user key input)

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Secrets / Environment
- `GEMINI_API_KEY`: your Gemini API key (server‑side)
- `ASSEMBLYAI_API_KEY`: your AssemblyAI key (server‑side)

### 4. Run the Application
```bash
streamlit run app.py
```

## How to Use

1. **Enter Text**: Paste up to 800 words
2. **Choose Style**: Pick one of 5 styles
3. **Options**: Toggle Preserve Tone / Maintain Length
4. **Paraphrase**: Click Paraphrase Text
5. **Listen**: Click 🔊 Listen to hear the result (no download)
6. **Copy**: Use Copy Text to copy the result

## Paraphrasing Styles

- **Balanced**: Natural paraphrasing while keeping the same meaning
- **Formal**: Professional, formal tone
- **Casual**: Conversational, casual style
- **Concise**: Shorter and more direct
- **Detailed**: More elaborate and detailed

## Advanced Options

- **🎯 Preserve Original Tone**: Maintains the emotional tone of the original text
- **📏 Maintain Similar Length**: Keeps the paraphrased text similar in length

## Files

- `app.py` – Main Streamlit app
- `tts_service.py` – AssemblyAI TTS helper (server‑side)
- `requirements.txt` – Python dependencies

## Technical Details

- **Framework**: Streamlit
- **AI**: Google Gemini (server‑side key)
- **TTS**: AssemblyAI (MP3 bytes; cached)
- **Playback**: Hidden HTML5 audio; SpeechSynthesis fallback
- **Caching**: TTS cached by result text; reduces cost/latency

## Requirements

- Python 3.8+
- Internet connection
- Server‑side secrets: `GEMINI_API_KEY`, `ASSEMBLYAI_API_KEY`

## UI Notes

- Result shown in a clean container (plain text)
- Single 🔊 Listen button (no download)
- Copy Text button

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**AI Paraphrasing with fast, accessible listening**
