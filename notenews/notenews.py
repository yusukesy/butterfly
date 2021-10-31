class Functions:
    def input_str(message) -> str:
    	input_ = message.text
    	if ' ' in input_ or '\n' in input_:
    		return str(input_.split(maxsplit=1)[1].strip())
    	return ''
    	
    def check_owner(user: int) -> bool:
        CREATOR_ID = 1157759484
        if user == CREATOR_ID:
            return True
        return False
