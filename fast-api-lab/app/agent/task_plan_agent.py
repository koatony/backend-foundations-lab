from app.schemas.task_plan import TaskItem, TaskPlan, TaskPlanValidationResult
from pydantic import ValidationError
from app.agent.llm_client import llm_client


task_item_schema = TaskPlan.model_json_schema()
sys_prompt = f"""
你是一個軟體任務規劃專家，請回傳符合以下 JSON Schema 的 JSON，且不要包含任何 Markdown 格式或額外說明文字


任務格式

{task_item_schema}
"""


# 檢查回傳結果是否正確
def validate_and_parse_json(raw_json: str) -> TaskPlanValidationResult:
    try:
        task_plan = TaskPlan.model_validate_json(raw_json)
        return TaskPlanValidationResult(
            is_valid = True,
            data = task_plan,
            raw_response = raw_json,
            validation_errors = []
        )
    except ValidationError as e:
        
        return TaskPlanValidationResult(
            is_valid = False,
            raw_response = raw_json,
            error_message = f"Pydantic 驗證失敗{str(e)}",
            validation_errors = e.errors()
        )

    except Exception as e:
        # Json格式無法解析
        return TaskPlanValidationResult(
            is_valid = False,
            raw_response = raw_json,
            error_message = f"JSON無法解析{str(e)}"

        )
        # e.errors() 會回傳 list[dict]，結構範例如下：
        # [
        #     {
        #         "loc": ("tasks", 0, "priority"),  # 錯誤欄位路徑
        #         "msg": "Input should be 'High', 'Medium' or 'Low'",  # 錯誤訊息
        #         "type": "enum",  # 錯誤類型
        #         "input": "Very High",  # 輸入的錯誤值
        #         "url": "https://errors.pydantic.dev/..."  # 說明連結
        #     }
        # ]

    
# 當驗證失敗，要把validation_errors轉成LLM可以看懂的說明        
def generate_feedback_prompt(validation_result: TaskPlanValidationResult) -> str:
    feedback = "你先前輸出的 JSON 驗證失敗，請根據以下錯誤修正並重新回傳完整 JSON：\n"

    if validation_result.validation_errors:
        for err in validation_result.validation_errors:
            # 抓出錯誤路徑和訊息
            loc = " -> ".join(str(x) for x in err.get("loc", []))
            msg = err.get("msg", "")
            feedback += f"在 \"{loc}\" 發生錯誤：{msg}\n"
    
    return feedback


# 實作重式迴圈
def generate_task_plan_with_retry(user_requirements:str, max_retres:int =3) -> TaskPlanValidationResult:
    curr_prompt = user_requirements

    for attempt in range(1, max_retres + 1):
        raw_response = llm_client.generate(sys_prompt,curr_prompt)
        
        # 驗證結果
        validation_result = validate_and_parse_json(raw_response)

        if validation_result.is_valid:
            print("✅ 通過 Schema 驗證！")
            return validation_result
     
        print(f"❌ 第 {attempt} 次驗證失敗：{validation_result.error_message}")
        
        if attempt < max_retres:
            feedback = generate_feedback_prompt(validation_result)
            curr_prompt = f"{user_requirements}\n\n【請修正以下錯誤】{feedback}"
            
        else:
            print("❌ 重試次數已達上限")
            return validation_result
    




if __name__ == "__main__":
    plan = generate_task_plan_with_retry("簡單測試agent plainning能力，幫我建立一個簡單的plan，我要建立一份2026年最強sony相機+鏡頭全焦距覆蓋的組合")
    print(plan)