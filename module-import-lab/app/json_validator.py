class MissingFieldError(Exception):
    pass

class InvalidTypeError(Exception):
    pass


def validate_json_data(data:dict, schema:dict):
    for k,v in schema.items():
        if(k not in data):
            raise MissingFieldError(f"缺少必填欄位{k}")
        
        value = data[k]
        if type(value) is not v:
            raise InvalidTypeError(f"欄位{k}型別不符合 預期為{v.__name__}")
    return True



    