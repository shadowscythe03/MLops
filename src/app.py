
import streamlit as st
import os

st.set_page_config(page_title="RAG Chatbot", layout="wide")
st.title("📰 News RAG Chatbot (Local)")
st.markdown("Ask questions about your processed news articles. Powered by local embeddings and T5.")

@st.cache_resource(show_spinner=True)
def load_bot():
	try:
		from src.rag.chatbot import RAGChatbot
	except ImportError:
		from rag.chatbot import RAGChatbot
	return RAGChatbot(k=5)

bot = load_bot()


# Session state for chat history and input
if "history" not in st.session_state:
	st.session_state.history = []
if "user_input" not in st.session_state:
	st.session_state.user_input = "What are the main topics in these articles?"

col1, col2 = st.columns([4,1])
with col2:
	if st.button("Reset", use_container_width=True):
		st.session_state.user_input = "What are the main topics in these articles?"
		st.session_state.history = []

with st.form("chat_form", clear_on_submit=False):
	user_input = st.text_area("Your question:", st.session_state.user_input, height=60, key="user_input_area")
	submitted = st.form_submit_button("Ask")

if submitted and user_input.strip():
	with st.spinner("Thinking..."):
		answer, sources = bot.ask(user_input.strip())
	st.session_state.history.append((user_input.strip(), answer, sources))
	st.session_state.user_input = user_input.strip()

for q, a, sources in reversed(st.session_state.history):
	st.markdown(f"**You:** {q}")
	st.markdown(f"**Bot:** {a}")
	if sources:
		with st.expander("Show sources"):
			for s in sources:
				st.write(f"- {s.get('title','[untitled]')} (score: {s.get('score',0):.3f})")
