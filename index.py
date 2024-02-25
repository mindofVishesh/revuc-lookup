from taipy import Gui
import next 
import main_file

title = "Query Pages"
user_input = ""  
display_text = "" 
output_text = "" 
Lits_items = ""

def button_pressed(gui):
    items = ' '.join(map(str, next.get_list()))
    gui.Lits_items = items
    gui.display_text = gui.user_input  
    print(gui.display_text)
    answer = main_file.main(user_session,gui.display_text)

    gui.output_text = answer
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
    user_session = main_file.start()
    app.run()

