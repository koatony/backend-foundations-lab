import sys
class InsufficientFundsError(Exception):
    pass




def withdraw_money(balance:float, amount:float) -> float:
    if amount<0:
        raise ValueError("提款金額不得為負數")
    
    if amount>balance:
        raise InsufficientFundsError(f"餘額:{balance}，提款金額:{amount},餘額不足")
    return balance - amount




try:
    print(withdraw_money(100, 200))
except InsufficientFundsError as error:
    print(error)

print(sys.path)