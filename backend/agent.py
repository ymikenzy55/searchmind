import os
import certifi
from dotenv import load_dotenv 

from langchain_groq import ChatGroq
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate
from memory import ConversationMemory

os.environ["SSL_CERT_FILE"] = certifi.where()
load_dotenv()

# Initialize persistent memory
memory = ConversationMemory()

def create_agent():
    """Initialize and return the agent executor"""
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    YOUR_NAME = os.getenv("CREATOR_NAME", "Mike")
    
    # Initialize tools
    search_tool = TavilySearchResults(max_results=2)
    tools = [search_tool]
    
    # Initialize LLM with faster model
    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        temperature=0.3,
        api_key=GROQ_API_KEY,
        streaming=True
    )
    
    # Create custom prompt - simple and clean
    prompt = ChatPromptTemplate.from_messages([
        ("system", f'''You are SearchMind, an intelligent AI research assistant created by {YOUR_NAME}.

Your capabilities:
- Real-time web search for current information
- Intelligent reasoning and analysis  
- Natural, friendly conversation
- Multi-step problem solving
- Memory of past conversations

When users greet you or introduce themselves, respond naturally and warmly.
When asked about your creator, mention that you were created by {YOUR_NAME}.
Use past conversation history to provide contextual responses.
Be conversational, helpful, and concise.'''),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    
    # Create agent
    agent = create_tool_calling_agent(llm, tools, prompt)
    
    # Create agent executor with optimized settings
    agent_executor = AgentExecutor(
        agent=agent, 
        tools=tools, 
        verbose=True,
        handle_parsing_errors=True,
        max_execution_time=30
    )
    
    return agent_executor

def query_agent(agent_executor, question, session_id="default"):
    """Query the agent with a question and persistent memory"""
    try:
        # Get recent conversation context (last 6 messages for speed)
        context = memory.get_recent_context(session_id, num_messages=6)
        
        # If there's context, add it naturally to the question
        if context.strip():
            full_input = f"[Previous conversation:\n{context}]\n\nUser: {question}"
        else:
            full_input = question
        
        # Query the agent
        response = agent_executor.invoke({"input": full_input})
        answer = response["output"]
        
        # Save to permanent memory
        memory.add_message("user", question, session_id)
        memory.add_message("assistant", answer, session_id)
        
        return answer
    except Exception as e:
        return f"Error: {str(e)}"
