from pydantic import BaseModel, field_validator, model_validator

class Taxpayer(BaseModel):
    name:str
    id_number:str
    
class Expense(BaseModel):
    category:str
    amount:float
    

class TaxReport(BaseModel):
    taxpayer:Taxpayer
    expenses:list[Expense]

    @model_validator(mode='after')
    def check_total_limit(self)->'TaxReport':
        total = sum(e.amount for e in self.expenses)
        if total > 100000: 
            if not self.taxpayer.name or self.taxpayer.name.strip() == "":
                raise ValueError('Taxpayer name is required for reports exceeding 100000')

        return self
    


bad_data = {
    "taxpayer":{
        "name":"",
        "id_number":"12345"
    },
    "expenses":[
        {
            "category":"salary",
            "amount":2000000
        }
    ]
}

try:
    report = TaxReport.model_validate(bad_data)
except ValueError as e:
    for error in e.errors():
        location = " -> ".join(map(str, error['loc']))
        message = error['msg']
        print(f"❌ 錯誤路徑: [{location if location else 'Root Object'}]")
        print(f"   錯誤訊息: {message}")