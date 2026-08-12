import inspect
from typing import Any, Callable

def parse_function_to_json_schema(func: Callable[..., Any]) -> dict:
    func_name = func.__name__
    func_doc = func.__doc__.strip() if func.__doc__  else ""

    type_map = {
        str: "string",
        int: "integer",
        float: "number",
        bool: "boolean"
    }

    sig = inspect.signature(func)
    properties = {}
    required = []

    # inspect.signature(func) 會回傳一個 Signature 物件，代表該函式的定義（包含參數與回傳值型別）
    # sig.parameters 是一個 OrderedDict-like 的字典，Key 是參數名稱，Value 是 Parameter 物件
    # sig.parameters.items() 迭代時會得到 (參數名稱, Parameter 物件)
    for param_name, param in sig.parameters.items():
        # param.annotation 取得參數的型別標註（例如 str, float, bool）
        # 如果參數沒有寫型別標註，其值會是 inspect.Parameter.empty
        json_type = param.annotation
        if json_type not in type_map:
            json_type = "string"
        else:
            json_type = type_map.get(json_type)
        
        properties[param_name] = {"type": json_type}

        # param.default 取得參數的預設值
        # 如果該參數是必填（沒有預設值），其值會等於 inspect.Parameter.empty
        if param.default == inspect.Parameter.empty:
            required.append(param_name)
    
    return {
        "type": "function",
        "function":{
            "name": func_name,
            "description": func_doc,
            "parameters": {
            "type": "object",
            "properties": properties,
            "required": required
            }
        }
    }


def add_item(name:str, price:float, is_active:bool = True) -> str:
    """新增商品到資料庫"""
    return f"新增商品{name}，價格為{price}，狀態為{is_active}已加入資料庫"

if __name__ == "__main__":
    import json

    schema = parse_function_to_json_schema(add_item)
    print(json.dumps(schema, ensure_ascii=False))