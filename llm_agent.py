from groq import Groq

from dotenv import load_dotenv
import os


class ConversationAgent:
    def __init__(self):
        load_dotenv()
        self.groq_client = Groq(api_key=os.environ["GROQ_KEY"])
        self.conversation_history = [
                {
                    "role": "system",
                    "content": read_file(file_path="./context.txt")
                }
            ]


    @staticmethod
    def read_file(file_path):
        with open(file_path, "r") as file:
            return file.read()


<<<<<<< HEAD
def ask_llm(question, history=None):
    
    client = Groq(api_key=os.environ["GROQ_KEY"])

    messages = [
        {
            "role": "system",
            "content": read_file(file_path="./context.txt")
        }
    ]
    messages += history or []
    messages.append({"role": "user", "content": question})

    chat_completion = client.chat.completions.create(
        messages=messages,
        model="openai/gpt-oss-120b",
        include_reasoning=False,
    )
=======
    def update_conversation_history(self, role, content):
        self.conversation_history.append(
            {
            "role": role,
            "content": content,
            }
        )


    def ask_llm(self, question):

        self.update_conversation_history(role="user", content=question)

        response = self.groq_client.chat.completions.create(
            messages=self.conversation_history,
            model="openai/gpt-oss-120b",
            include_reasoning=False,
        ).choices[0].message.content


        self.update_conversation_history(role="assistant", content=response)

























>>>>>>> db8c2d9a74dc9d5c6911d22d4705122631835795




if __name__ == "__main__":
    question = input("Pose ta question :\n")
    response = ask_llm(question)
    print("\n")
    print(response)
