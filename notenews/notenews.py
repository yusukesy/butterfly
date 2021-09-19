# from pyrogram import Client, filters
from pyrogram.types import Message
# from client import NoteMusic
from typing import Union


class Functions:
    def input_str(message: Message) -> str:
    	input_ = message.text
    	if ' ' in input_ or '\n' in input_:
    		return str(input_.split(maxsplit=1)[1].strip())
    	return ''
    	
    def check_owner(user: Union[int, str]) -> bool:
        CREATOR_ID = 1157759484
        if user == CREATOR_ID:
            return True
        return False
