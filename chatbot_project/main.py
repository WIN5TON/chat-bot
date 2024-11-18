from knowledge_base import KnowledgeBase
from response_generator import ResponseGenerator
from chatbot import Chatbot

if __name__ == "__main__":
    knowledge_base = KnowledgeBase()
    response_generator = ResponseGenerator(knowledge_base)
    chatbot = Chatbot(response_generator)
    chatbot.run()
