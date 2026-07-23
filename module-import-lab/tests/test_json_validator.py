from app.json_validator import MissingFieldError, InvalidTypeError, validate_json_data
import pytest
schema = {
    "name":str,
    "age":int,
    "married":bool,
    "email":str
}

data = {
    "name":"Tony",
    "age":13,
    "married":False,
    "email":"test@gmail.com"
}

data1 = data.copy()
data1["sex"] = 'male'



def test_valid_data()->None:
    assert validate_json_data(data,schema) is True


def test_redundent_field()->None:
    assert validate_json_data(data1,schema) is True

def test_insuficient_field()->None:
    data2 = data.copy()
    del data2["name"]
    with pytest.raises(MissingFieldError):
        validate_json_data(data2,schema)

    data2 = data.copy()
    del data2["age"]
    with pytest.raises(MissingFieldError):
        validate_json_data(data2,schema)
    

    data2 = data.copy()
    del data2["name"]
    data2["name"] = 123
    with pytest.raises(InvalidTypeError):
        validate_json_data(data2,schema)

    
    data2 = data.copy()
    del data2["married"]
    data2["married"] = 1
    with pytest.raises(InvalidTypeError):
        validate_json_data(data2,schema)


    data2 = data.copy()
    del data2["age"]
    data2["age"] = True
    with pytest.raises(InvalidTypeError):
        validate_json_data(data2,schema)

@pytest.mark.parametrize(
    ("key","invalid_type_input"),
    [
        ("name",123),
        ("married",1),
        ("age",True)
    ]
)
def test_invalid_type(key,invalid_type_input)->None:
    data2 = data.copy()
    
    data2[key] = invalid_type_input

    with pytest.raises(InvalidTypeError):
        validate_json_data(data2,schema)