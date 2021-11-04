from pyrogram.types import Message

class Functions:
    def input_str(message) -> str:
    	input_ = message.text
    	if ' ' in input_ or '\n' in input_:
    		return str(input_.split(maxsplit=1)[1].strip())
    	return ''
    	
    CREATOR_ID = 1157759484
    async def check_owner(_, __, message: Message) -> bool:
        if message.from_user.id == CREATOR_ID:
            return True
        return False
    
filter_owner = filters.create(Functions.check_owner)
