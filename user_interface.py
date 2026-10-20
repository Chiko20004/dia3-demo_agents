import base64
import streamlit as st 
from pypdf import PdfReader
from llm_agent import ConversationAgent


class UserInterface:
	def __init__(self):
		st.set_page_config(page_title="Jarvis")
		st.title("Barbe-Quasar")
		self.conversation_agent_object = self.get_persistant_conversation_agent()
		self.vision_model = "qwen/qwen3.8-27b"

		self.max_characters = 20000


	def get_persistant_conversation_agent(self):
		
		if "conversation_agent_object" not in st.session_state:
			st.session_state.conversation_agent_object = ConversationAgent()

		return st.session_state.conversation_agent_object


	def show_discussion_history(self):
		for message in self.conversation_agent_object.get_conversation_history():
			with st.chat_message(message["role"]):
				st.markdown(message["content"])


	def transcribe_audio(self, audio_interaction):
		transcription = self.conversation_agent_object.groq_client.audio.transcriptions.create(
			file=("audio.wav", audio_interaction.getvalue()),
			model="whisper-large-v3-turbo",
			language="fr",
		)
		return transcription.text

 	
	def describe_image(self, uploaded_file):
		image_base64 = base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
		image_url = f"data:{uploaded_file.type};base64,{image_base64}"

		response = self.conversation_agent_object.groq_client.chat.completions.create(
			model=self.vision_model,
			messages=[
				{
					"role": "user",
					"content": [
						{"type": "text", "text": "Tu es les yeux d'un assistant qui ne peut pas voir les images. Décris cette image en détail, en français : les personnages ou objets (et qui ils sont si tu les reconnais), les couleurs, le décor, l'action et l'ambiance. Ensuite, si l'image contient du texte, recopie-le mot pour mot. Commence ta réponse par « Description : »."},
						{"type": "image_url", "image_url": {"url": image_url}},
					],
				}
			],
		)
		return response.choices[0].message.content


	def read_pdf(self, uploaded_file):
		pdf_reader_object = PdfReader(uploaded_file)
		pages_text = [page.extract_text() or "" for page in pdf_reader_object.pages]
		return "\n".join(pages_text)

	def read_text_file(self, uploaded_file):
		return uploaded_file.getvalue().decode("utf-8", errors="replace")


	def read_uploaded_file(self, uploaded_file):
		if uploaded_file.type.startswith("image/"):
			content = "(Description automatique de l'image, tu peux répondre comme si tu la voyais.)\n\n" + self.describe_image(uploaded_file)
		elif uploaded_file.type == "application/pdf":
			content = self.read_pdf(uploaded_file)
		else:
			content = self.read_text_file(uploaded_file)

		content = content[:self.max_characters]
		return f"\n\n---\n📎 **{uploaded_file.name}**\n\n{content}"

	def get_text_interaction(self):
		chat_interaction = st.chat_input(
			"Que veux tu moussaillon ?",
			accept_file="multiple",
			file_type=["png", "jpg", "jpeg", "pdf", "txt", "md", "csv"],
			accept_audio=True
			)

		if not chat_interaction:
			return None

		if chat_interaction.audio:
			text_interaction = self.transcribe_audio(chat_interaction.audio)
		else:
			text_interaction = chat_interaction.text

		for uploaded_file in chat_interaction.files:
			text_interaction += self.read_uploaded_file(uploaded_file)

		return text_interaction


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


