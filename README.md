# AI Paraphrasing Tool

A professional AI paraphrasing tool built with Streamlit and Google Gemini AI. Features the same clean design as Alwrity with advanced paraphrasing capabilities.

## Features

- 🔄 **AI Paraphrasing**: Powered by Google Gemini 2.0 Flash
- 📝 **800-Word Limit**: Real-time word counting with validation
- 🎨 **5 Paraphrasing Styles**: Balanced, Formal, Casual, Concise, Detailed
- 🎯 **Advanced Options**: Preserve tone, maintain length
- 📊 **Professional UI**: Clean design matching Alwrity style
- 🔐 **Secure API**: Password-protected API key input
- 📋 **Easy Copy**: One-click copy to clipboard

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Get Gemini API Key
- Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
- Create a free API key

### 3. Set Up Environment
Create `.env` file:
```
GEMINI_API_KEY=your_api_key_here
```

### 4. Run the Application
```bash
streamlit run app.py
```

## How to Use

1. **Enter Text**: Type or paste your text (max 800 words)
2. **Choose Style**: Select from 5 paraphrasing styles
3. **Configure Options**: Preserve tone and maintain length
4. **Add API Key**: Enter your Gemini API key in the expandable section
5. **Click Paraphrase**: Get your paraphrased text instantly
6. **Copy Results**: Use the copy button to copy the paraphrased text

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

- `app.py` - Main Streamlit application
- `requirements.txt` - Python dependencies
- `env_example.txt` - Environment variables template
- `TOOL_CREATION_PLAN.md` - Development plan and specifications

## Technical Details

- **Framework**: Streamlit with wide layout
- **AI Model**: Google Gemini 2.0 Flash Experimental
- **Styling**: Custom CSS matching Alwrity design
- **Dependencies**: Minimal (3 packages only)
- **Error Handling**: Comprehensive error management

## Requirements

- Python 3.7 or higher
- Internet connection
- Google Gemini API key (free tier available)

## UI Features

- **Custom Scrollbars**: Blue-themed scrollbars
- **Professional Buttons**: Styled buttons with shadows
- **Expandable Sections**: Clean organization
- **Real-time Validation**: Word count and limit checking
- **Responsive Design**: Works on all screen sizes

---

**Professional AI Paraphrasing with Alwrity-Style Design**
