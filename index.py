
import os
import sys
from taipy import Gui
import next 
from taipy.gui import State, notify 

title = "Query Pages"
user_input = ""  
display_text = "" 
output_text = "" 
Lits_items = ""

def button_pressed(gui):
    items = ' '.join(map(str, next.get_list()))
    gui.Lits_items = items
    gui.display_text = gui.user_input  

    gui.output_text = next.display_out_put(gui.display_text)
    gui.user_input = ""


page = """
<|text-center |
<|{title}|id=display-title-color|>

<|container container1|
<|container hidden_container|
<|{Lits_items}|>
|>
<|container container_text_1|
<|{display_text}|>
|>

<|container container_text_2|
<|{output_text}|id=display-text|>  
|>
|>

<|container container2|
<|{user_input}|input|> <|Send|button|on_action=button_pressed|>
|>
"""


if __name__ == "__main__":
    app = Gui(page=page)
    app.run()
