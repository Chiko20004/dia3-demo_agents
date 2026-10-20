import streamlit as st 
from llm_agent import ConversationAgent


class UserInterface:
	def __init__(self):
		st.set_page_config(page_title="Jarvis")
		st.title("Barbe-Quasar")
		self.conversation_agent_object = self.get_persistant_conversation_agent()


	def get_persistant_conversation_agent(self):
		
		if "conversation_agent_object" not in st.session_state:
			st.session_state.conversation_agent_object = ConversationAgent()

		return st.session_state.conversation_agent_object


	def show_discussion_history(self):
		for message in self.conversation_agent_object.get_conversation_history():
			with st.chat_message(message["role"]):
				st.markdown(message["content"])


	def get_text_interaction(self):
		chat_interaction = st.chat_input(
			"Que veux tu moussaillon ?",
			accept_file=False,
			accept_audio=True
			)

		if not chat_interaction:
			return None

		if chat_interaction.audio:
			return self.transcribe_audio(chat_interaction.audio)

		return chat_interaction.text


	def transcribe_audio(self, audio_interaction):
		transcription = self.conversation_agent_object.groq_client.audio.transcriptions.create(
			file=("audio.wav", audio_interaction.getvalue()),
			model="whisper-large-v3-turbo",
			language="fr",
		)
		return transcription.text




	def run(self):
		text_interaction = self.get_text_interaction()

		if text_interaction :
			self.conversation_agent_object.ask_llm(text_interaction)

		self.show_discussion_history()





if __name__ == "__main__":
	user_interface_object = UserInterface()
	user_interface_object.run()








































	# response = ask_llm(user_input)
	# with st.chat_message("user"):
	# 	st.markdown(user_input)

	# with st.chat_message("system"):
	# 	st.markdown(response)


