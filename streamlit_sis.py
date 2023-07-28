# Import python packages
import streamlit as st
import pandas as pd
from snowflake.snowpark.context import get_active_session

st.set_page_config(
    page_title="Generative AI using Snowflake External Functions and OpenAI",
    layout='wide'
)

st.title("Generative AI using Snowflake External Functions and OpenAI")

# Get the current credentials
session = get_active_session()
model = "gpt4"

@st.cache_data()
def load_prompts():
    df_prompts = session.sql('SELECT prompt:prompt from llm_prompts').to_pandas()
    return df_prompts

@st.cache_data()
def get_openai_response(prompt):
    df_query = session.sql(f"SELECT llm_external_function(parse_json('{prompt}')) as llm_query").to_pandas()
    return df_query.iloc[0][0][1:-1]
    
def sentiment_analysis():
    st.subheader("Sentiment Analysis")
    entered_phrase = st.text_input("Enter a sentiment",label_visibility="hidden",placeholder='For example: My puppy is adorable ❤️❤️')
    if entered_phrase:
        st.caption(f"OpenAI (model: {model}) LLM Response")
        st.write(get_openai_response(f"\"Classify this sentiment: {entered_phrase}\""))

def share_knowledge():
    st.subheader("Share Knowledge")
    entered_question = st.text_input("Enter a sentiment",label_visibility="hidden",placeholder='For example: Thoughts on OpenAI')
    if entered_question:
        st.caption(f"OpenAI (model: {model}) LLM Response")
        st.write(get_openai_response(f"\"Share your knowledge: {entered_question}\""))

def text_to_sql():
    st.subheader("Select a SQL prompt")
    df_prompts = load_prompts()
    selected_prompt = st.selectbox("Select a prompt",df_prompts,label_visibility="hidden")    
    if selected_prompt:
        st.caption("Selected SQL Prompt")
        st.write(selected_prompt)
        st.caption(f"OpenAI (model: {model}) LLM Response")
        st.write(get_openai_response(f"{selected_prompt}"))

page_names_to_funcs = {
    "Sentiment Analysis": sentiment_analysis,
    "Share Knowledge": share_knowledge,
    "Text-to-SQL": text_to_sql
}

selected_page = st.sidebar.selectbox("Select", page_names_to_funcs.keys())
page_names_to_funcs[selected_page]()