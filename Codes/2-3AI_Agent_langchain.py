def add_tool(input_str : str) -> str:
    try:
        arr = list(map(int, input_str.split()))
        return str(sum(arr))
    except Exception as e:
        return f"에러: {str(e)}"
    
def chat_tool(input_st: str):
    return llm.invoke(input_st)

from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_community.chat_models import ChatOpenAI

api_key = ''
model = 'gpt-4o-mini'

llm = ChatOpenAI(api_key=api_key, model=model)

tools = [
    Tool( name= 'AddTool', func=add_tool, description="두 숫자를 더합니다. 입력은 두 숫자를 공백으로 구분한 문자열로 입력합니다. 입력 형식: 3 5"),
    Tool( name= 'ChatTool', func=chat_tool
         , description="일반적인 질문이나 대화에 답변합니다. 계산, 검색, 도구 실행이 필요하지 않은 경우 사용하세요. 입력 예시: '오늘 기분이 어때?' 또는 'AI는 어떻게 작동해?'")
]

agent = initialize_agent(
    tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
)

response = agent.run("3하고 7을 더해줘.")
print(response)