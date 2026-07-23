CLEANUP_COUNTER = 0


def append_log_safely(file_path:str, message:str)->None:
    global CLEANUP_COUNTER
    try:
        with open(file_path,"a",encoding = "utf-8") as file:
            file.write(message+ '\n')
    except FileNotFoundError as e:
        print(f"找不到檔案{e}")
        raise e
        
    except PermissionError as e:
        print(f"無法寫入{e}")
        raise e
    
    finally:
        CLEANUP_COUNTER+=1


