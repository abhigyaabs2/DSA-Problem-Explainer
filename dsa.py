import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(
    page_title="DSA Problem Explainer Bot",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #555;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown('<p class="main-header">🧠 DSA Problem Explainer Bot</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Input any Data Structures & Algorithms problem and get a clear explanation!</p>', unsafe_allow_html=True)

# Sidebar for API key
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # API Provider Selection
    api_provider = st.selectbox(
        "Choose API Provider:",
        ["Google Gemini (FREE)", "Groq (FREE & Fast)"]
    )
    
    if api_provider == "Google Gemini (FREE)":
        api_key = st.text_input(
            "Enter Google Gemini API Key:", 
            type="password", 
            help="Get your FREE API key from https://makersuite.google.com/app/apikey"
        )
        
        # Model selector for Gemini
        gemini_model = st.selectbox(
            "Select Gemini Model:",
            ["gemini-1.5-flash-latest", "gemini-1.5-pro-latest", "gemini-pro", "gemini-1.5-flash"]
        )
    else:
        api_key = st.text_input(
            "Enter Groq API Key:", 
            type="password", 
            help="Get your FREE API key from https://console.groq.com"
        )
        
        groq_model = st.selectbox(
            "Select Groq Model:",
            ["llama-3.3-70b-versatile", "llama-3.1-8b-instant", "mixtral-8x7b-32768", "gemma2-9b-it"]
        )
    
    st.markdown("---")
    st.markdown("### 📚 How to use:")
    st.markdown("""
    1. Choose your API provider
    2. Enter your API key (FREE!)
    3. Paste or type a DSA problem
    4. Click 'Explain Problem'
    5. Get a detailed explanation!
    """)
    
    st.markdown("---")
    
    if api_provider == "Google Gemini (FREE)":
        st.markdown("### 🔑 Get FREE Gemini API Key:")
        st.markdown("""
        1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
        2. Sign in with Google account
        3. Click **"Create API Key"**
        4. Copy and paste above
        
        **✅ FREE with generous limits!**
        - 60 requests/min
        - 1500 requests/day
        """)
    else:
        st.markdown("### 🔑 Get FREE Groq API Key:")
        st.markdown("""
        1. Visit [Groq Console](https://console.groq.com)
        2. Sign up (free)
        3. Go to API Keys
        4. Create new key
        
        **✅ Super FAST & FREE!**
        - 30 requests/min
        - Fastest inference
        """)

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📝 Input DSA Problem")
    
    # Example problems dropdown
    example_problems = {
        "Select an example...": "",
        "Two Sum": "Given an array of integers nums and an integer target, return indices of the two numbers such that they add up to target. You may assume that each input would have exactly one solution, and you may not use the same element twice.",
        "Reverse Linked List": "Given the head of a singly linked list, reverse the list, and return the reversed list.",
        "Valid Parentheses": "Given a string s containing just the characters '(', ')', '{', '}', '[' and ']', determine if the input string is valid. An input string is valid if: Open brackets must be closed by the same type of brackets. Open brackets must be closed in the correct order.",
        "Binary Search": "Given an array of integers nums which is sorted in ascending order, and an integer target, write a function to search target in nums. If target exists, then return its index. Otherwise, return -1.",
        "Merge Two Sorted Lists": "You are given the heads of two sorted linked lists list1 and list2. Merge the two lists into one sorted list. The list should be made by splicing together the nodes of the first two lists. Return the head of the merged linked list.",
        "Maximum Subarray": "Given an integer array nums, find the subarray with the largest sum, and return its sum."
    }
    
    selected_example = st.selectbox("Choose an example problem:", list(example_problems.keys()))
    
    problem_text = st.text_area(
        "Or paste your own problem:",
        value=example_problems[selected_example],
        height=200,
        placeholder="Paste your DSA problem here..."
    )
    
    explain_button = st.button("🚀 Explain Problem", type="primary", use_container_width=True)

with col2:
    st.subheader("💡 Explanation & Approach")
    
    if explain_button:
        if not api_key:
            st.error(f"⚠️ Please enter your {api_provider} API key in the sidebar!")
        elif not problem_text:
            st.error("⚠️ Please enter a DSA problem to explain!")
        else:
            try:
                with st.spinner("🤔 Analyzing the problem..."):
                    
                    if api_provider == "Google Gemini (FREE)":
                        # Configure Gemini
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel(gemini_model)
                        
                        # Create prompt (encode properly)
                        prompt_text = """You are an expert DSA (Data Structures & Algorithms) tutor. 
Your job is to explain DSA problems in simple, clear language that anyone can understand.

For each problem, provide:
1. Problem Summary: A brief overview in simple words
2. Key Concepts: What data structures or algorithms are involved
3. Approach: Step-by-step explanation of how to solve it
4. Time & Space Complexity: Big O notation with explanation
5. Example Walkthrough: A small example showing the solution
6. Tips: Common pitfalls or edge cases to consider

Use analogies and simple language. Avoid jargon unless you explain it.

Explain this DSA problem:

"""
                        full_prompt = prompt_text + problem_text
                        
                        # Generate response
                        response = model.generate_content(full_prompt)
                        explanation = response.text
                        
                    else:  # Groq
                        try:
                            from groq import Groq
                        except ImportError:
                            st.error("Groq package not installed! Run: pip install groq")
                            st.stop()
                        
                        client = Groq(api_key=api_key)
                        
                        chat_completion = client.chat.completions.create(
                            messages=[
                                {
                                    "role": "system",
                                    "content": """You are an expert DSA (Data Structures & Algorithms) tutor. 
Your job is to explain DSA problems in simple, clear language that anyone can understand.

For each problem, provide:
1. Problem Summary: A brief overview in simple words
2. Key Concepts: What data structures or algorithms are involved
3. Approach: Step-by-step explanation of how to solve it
4. Time & Space Complexity: Big O notation with explanation
5. Example Walkthrough: A small example showing the solution
6. Tips: Common pitfalls or edge cases to consider

Use analogies and simple language. Avoid jargon unless you explain it."""
                                },
                                {
                                    "role": "user",
                                    "content": f"Explain this DSA problem:\n\n{problem_text}"
                                }
                            ],
                            model=groq_model,
                            temperature=0.7,
                        )
                        
                        explanation = chat_completion.choices[0].message.content
                    
                    # Display explanation
                    st.markdown(explanation)
                    
                    st.success("✅ Explanation generated successfully!")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")
                
                if api_provider == "Google Gemini (FREE)":
                    st.info("""
                    **Troubleshooting:**
                    - Make sure your API key is correct
                    - Visit [Google AI Studio](https://aistudio.google.com) to verify your key
                    - Try the Groq option instead (equally FREE & fast!)
                    """)
                else:
                    st.info("""
                    **Troubleshooting:**
                    - Make sure your API key is correct
                    - Visit [Groq Console](https://console.groq.com) to verify your key
                    """)
    else:
        st.info("👈 Enter a problem and click 'Explain Problem' to get started!")

# Footer
st.markdown("---")
st.markdown(f"""
    <div style='text-align: center; color: #888; padding: 1rem;'>
        Built with ❤️ using Streamlit & {api_provider} AI (FREE!)
    </div>
""", unsafe_allow_html=True)