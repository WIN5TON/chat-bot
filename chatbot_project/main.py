from KnowledgeBase import KnowledgeBase
from ResponseGenerator import ResponseGenerator
from Chatbot import Chatbot


if __name__ == "__main__":
    knowledge_base = KnowledgeBase()
    response_generator = ResponseGenerator(knowledge_base)
    chatbot = Chatbot(response_generator)
    chatbot.run()
