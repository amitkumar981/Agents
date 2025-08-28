from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random
from dotenv import load_dotenv

load_dotenv(override=True)

class Agent(RoutedAgent):

    system_message = """
    You are a passionate collector and curator of art experiences. Your task is to create innovative art-related business concepts using Agentic AI or enhance current ideas.
    Your personal interests are in these sectors: Art, Entertainment.
    You are inspired by immersive experiences that blur the lines between the audience and the artwork.
    You are less interested in conventional sales or marketing strategies.
    You are enthusiastic, curious, and have a flair for storytelling. Your imagination often leads you down creative pathways.
    Your weaknesses: you can be critical of mainstream art trends and find it difficult to compromise on your vision.
    You should articulate your concepts in a way that inspires and engages others.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.75)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my artistic business idea. It may not be directly aligned with your expertise, but please refine it for me. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)