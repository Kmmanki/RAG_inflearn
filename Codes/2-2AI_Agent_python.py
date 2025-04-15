from langchain_community.chat_models import ChatOpenAI
import re

api_key = 'api_key'
model = 'gpt-4o-mini'
llm = ChatOpenAI(api_key=api_key, model=model)



######## prompt
# 도구 선택 프롬프트
tool_prompt_disc="""
당신은 다음 도구를 사용할 수 있습니다:

도구 이름: AddTool
기능: 두 숫자를 더합니다.
입력 예시: "3 5"


도구 이름: ChatTool
기능: 일반적인 질문이나 대화에 답변합니다. 계산, 검색, 도구 실행이 필요하지 않은 경우 사용하세요.
입력 예시: "오늘 기분이 어때?" 또는 "AI는 어떻게 작동해?"

사용자가 질문하면, 어떤 도구를 사용할지 판단하고 다음 형식으로 대답하세요:

사용할 도구: <도구 이름>
입력값: <도구에 줄 입력값>

사용자의 질문: "{question}"
"""

final_prompt_disc="""
사용자의 질문: "{question}"
도구 실행 결과: {result}
이제 사용자에게 자연어로 대답하세요.
"""

########

def add_tool(input_str : str) -> str:
    try:
        arr = list(map(int, input_str.split()))
        return str(sum(arr))
    except Exception as e:
        return f"에러: {str(e)}"
    
def run_agent(query: str):
    tool_prompt = tool_prompt_disc.format(question=query)
    tool_result = llm.invoke(tool_prompt)

    match = re.search(r"사용할 도구:\s*(\w+)\s*입력값:\s*[\"']?(.+?)[\"']?$", tool_result.content.strip(), re.DOTALL)
    tool = match.group(1)
    tool_input = match.group(2)
    print(tool_result.content)
    if tool == "AddTool":
        add_result = add_tool(tool_input)
        final_prompt = final_prompt_disc.format(question = query, result=add_result)
        return llm.invoke(final_prompt).content
    elif tool == "ChatTool":
        final_prompt = final_prompt_disc.format(question = query, result=tool_input)
        return llm.invoke(final_prompt).content
    
if __name__ == '__main__':
    query="오늘 저녁메뉴는 뭘 먹는게 좋을까?"
    print("사용자 질문 :", query)
    result = run_agent(query)
    print("llm 답변: ",result)
