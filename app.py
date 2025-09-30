import streamlit as st
import google.generativeai as genai
import os
import re
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def main():
    # Set page configuration with custom theme
    st.set_page_config(
        page_title="AI Paraphrasing Tool",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Remove temporary theme overrides
    
    # Custom CSS styling (same as Alwrity)
    st.markdown("""
        <style>
        ::-webkit-scrollbar-track {
        background: #e1ebf9;
        }

        ::-webkit-scrollbar-thumb {
            background-color: #90CAF9;
            border-radius: 10px;
            border: 3px solid #e1ebf9;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: #64B5F6;
        }

        ::-webkit-scrollbar {
            width: 16px;
        }
        div.stButton > button:first-child {
            background: #1565C0;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 10px 2px;
            cursor: pointer;
            transition: background-color 0.3s ease;
            box-shadow: 2px 2px 5px rgba(0, 0, 0, 0.2);
            font-weight: bold;
        }
        
        /* No checkbox overrides */
        </style>
    """, unsafe_allow_html=True)

    # Hide top header line
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)

    # Hide footer
    hide_streamlit_footer = '<style>#MainMenu {visibility: hidden;} footer {visibility: hidden;}</style>'
    st.markdown(hide_streamlit_footer, unsafe_allow_html=True)

    # Header Section
    st.title("🔄 AI Paraphrasing Tool")

    # API Configuration Section (Expandable - Collapsed by default)
    with st.expander("API Configuration 🔑", expanded=False):
        st.markdown('''If the default Gemini API key is unavailable or exceeds its limits, you can provide your own API key below.<br>
        <a href="https://aistudio.google.com/app/apikey" target="_blank">Get Gemini API Key</a>
        ''', unsafe_allow_html=True)
        user_gemini_api_key = st.text_input("Gemini API Key", type="password", help="Paste your Gemini API Key here if you have one. Otherwise, the tool will use the default key if available.")

    # Main Input Section (Expandable - Open by default)
    with st.expander("**PRO-TIP** - Enter your text and choose paraphrasing style for best results.", expanded=True):
        col1, col2 = st.columns([5, 5])

        with col1:
            input_text = st.text_area(
                '**📄 Enter your text to paraphrase**',
                placeholder="Type or paste your text here (maximum 800 words)...",
                help="Enter the text you want to paraphrase. Maximum 800 words allowed.",
                height=300
            )
            
            # Word count display
            word_count = count_words(input_text)
            if word_count > 0:
                if word_count > 800:
                    st.markdown(f'<p style="color: #ff6b6b; font-weight: bold;">⚠️ Word count: {word_count}/800 (exceeds limit)</p>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<p style="color: #1976D2;">📊 Word count: {word_count}/800</p>', unsafe_allow_html=True)
            
        with col2:
            paraphrasing_style = st.selectbox(
                '🎨 Paraphrasing Style', 
                ('Balanced', 'Formal', 'Casual', 'Concise', 'Detailed'),
                index=0,
                help="Choose how you want the text to be paraphrased"
            )
            
            # Additional options
            st.markdown('<h4 style="color:#1976D2;">Additional Options</h4>', unsafe_allow_html=True)
            
            preserve_tone = st.checkbox(
                '🎯 Preserve Original Tone',
                value=True,
                help="Keep the original emotional tone of the text"
            )
            
            maintain_length = st.checkbox(
                '📏 Maintain Similar Length',
                value=True,
                help="Keep the paraphrased text similar in length to original"
            )
            
            # Paraphrase button on the right side below additional options
            st.markdown('<br>', unsafe_allow_html=True)
            paraphrase_clicked = st.button('**🔄 Paraphrase Text**', use_container_width=True)

    # Button logic moved outside the expander but still accessible
    if paraphrase_clicked:
        # Validation
        if not input_text.strip():
            st.error('**🫣 Please enter some text to paraphrase!**')
        elif word_count > 800:
            st.error('**⚠️ Text exceeds 800 words. Please shorten your text.**')
        else:
            with st.spinner("Paraphrasing your text..."):
                paraphrased_text = generate_paraphrase(
                    input_text, paraphrasing_style, user_gemini_api_key, preserve_tone, maintain_length
                )
                
                if paraphrased_text:
                    st.session_state['paraphrased_text'] = paraphrased_text
                    st.markdown('<h4 style="margin-top:1.5rem; color:#1976D2;">✨ Paraphrased Text</h4>', unsafe_allow_html=True)
                    st.markdown(paraphrased_text)
                    
                    # Copy button
                    if st.button("📋 Copy to Clipboard", help="Click to copy the paraphrased text"):
                        st.write("💡 Use Ctrl+C to copy the text above")
                else:
                    st.error("💥 **Failed to paraphrase text. Please try again!**")

def count_words(text):
    """Count words in the given text"""
    if not text.strip():
        return 0
    words = re.findall(r'\b\w+\b', text)
    return len(words)

def generate_paraphrase(text, style, api_key=None, preserve_tone=True, maintain_length=True):
    """Generate paraphrased text using Gemini"""
    try:
        # Get API key
        gemini_api_key = api_key or os.getenv('GEMINI_API_KEY')
        if not gemini_api_key:
            st.error("GEMINI_API_KEY is missing. Please provide it in the API Configuration section or set it in the environment.")
            return None
        
        # Configure Gemini
        genai.configure(api_key=gemini_api_key)
        
        # Create prompt based on style and options
        style_prompts = {
            'Balanced': 'Paraphrase this text naturally while keeping the same meaning:',
            'Formal': 'Rewrite this text in a formal, professional tone:',
            'Casual': 'Rewrite this text in a casual, conversational style:',
            'Concise': 'Make this text shorter and more direct:',
            'Detailed': 'Expand this text with more detail:'
        }
        
        prompt = style_prompts[style]
        
        if preserve_tone:
            prompt += " Maintain the original emotional tone."
        if maintain_length:
            prompt += " Keep the length similar to the original."
        
        prompt += f"\n\n{text}"
        
        # Generate content
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content(prompt)
        
        return response.text
        
    except Exception as e:
        if 'quota' in str(e).lower() or 'rate limit' in str(e).lower():
            st.warning('⚠️ Gemini API rate limit or quota exceeded. Please try again later or use a different API key.')
        else:
            st.error(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    main()
