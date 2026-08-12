import json
from openai import OpenAI
from app.core import settings
from app.agent.tool_parser import parse_function_to_json_schema
from app.repositories.item_repository import ItemRepository
from app.schemas.item import ItemCreate

class AgentService:
    def __init__(self, repo: ItemRepository):
        self.repo = repo

    def add_item_tool(self, title: str, price: float, description: str = None) -> str:
        """
        新增商品到資料庫， price 一定要大於 0。
        Args:
            title: 商品的標題或名稱
            price: 商品價格 (必須大於 0)
            description: 商品的詳細描述 (選填)
        """
        item_data = ItemCreate(
            title=title,
            price=price,
            description=description
        )

        created_item = self.repo.create(item_data)

        return f"【資料庫訊息】成功建立商品：{created_item.title}，價格：{created_item.price} 元！"

    def run_agent_with_tool(self, user_prompt: str) -> str:
        """
        建立OpenRouter 呼叫流程
        """
        # 初始化 OpenAI Client (指向 OpenRouter)
        client = OpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url=settings.OPENROUTER_BASE_URL
        )

        tool_schema = parse_function_to_json_schema(self.add_item_tool)

        # 工具映射表 (讓程式知道 AI 說要呼叫 "add_item_tool" 時該跑哪一個 Python function)
        tool_map = {"add_item_tool": self.add_item_tool}

        print(f"🤖 發送請求給 OpenRouter, Prompt: '{user_prompt}'...")

        response = client.chat.completions.create(
            model="openai/gpt-5.6-luna",
            messages=[
                {"role": "user", "content": user_prompt}
            ],
            tools=[tool_schema],
        )

        message = response.choices[0].message

        if message.tool_calls:
            tool_call = message.tool_calls[0]
            func_name = tool_call.function.name
            func_args = json.loads(tool_call.function.arguments)

            print(f"🎯 AI 決定呼叫工具: {func_name}")
            print(f"📦 AI 拆解出的參數: {func_args}")

            if func_name in tool_map:
                execution_result = tool_map[func_name](**func_args)
                return execution_result
            else:
                return f"錯誤：找不到對應的工具 {func_name}"
        else:
            # 如果 AI 覺得不需要呼叫 Tool，就直接回傳文字
            return message.content



if __name__ == "__main__":
   # 1. 建立 Repo 實例
    repo = ItemRepository()
    
    # 2. 實例化 AgentService 物件，並把 repo 丟進去（呼叫 __init__）
    agent_service = AgentService(repo)
    
    # 3. 透過實例物件呼叫裡面的方法
    result = agent_service.run_agent_with_tool(
        "你好，我想建立一個新的商品，名稱是滑鼠，價格是300元，描述是這個滑鼠很好用"
    )
    print(result)