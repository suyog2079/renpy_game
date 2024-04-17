init python:

    # DEFAULT GAME SETTINGS:

    # Default set of card types
    all_cards = ['A', 'B', 'C']
    # Width and height of the game field
    ww = 2
    hh = 2
    # Maximum number of cards that can be opened in one move
    max_c = 2
    # Text size on the card for text mode
    card_size = 48
    # Time allocated for gameplay
    max_time = 45
    # Pause before cards disappear
    wait = 0.5
    # Card mode with images instead of text
    img_mode = True

    values_list = []
    temp = []
    # Declare card images
    # Images should be in the format "images/card_*.png"
    # "card_back.png" and "card_empty.png" are mandatory
    for fn in renpy.list_files():
        if fn.startswith("images/card_") and fn.endswith((".png")):
            name = fn[12:-4]
            renpy.image("card " + name, fn)
            if name != "empty" and name != "back":
                temp.append(str(name))
    # If more than 1 image is found, change the set of card types
    # but keep the file names
    if len(temp) > 1:
        all_cards = temp
    else:
        # Otherwise, switch to text mode
        # since there are very few images
        img_mode = False

    # Function to initialize the game field
    def cards_init():
        global values_list
        values_list = []
        while len(values_list) + max_c <= ww * hh:
            current_card = renpy.random.choice(all_cards)
            for i in range(0, max_c):
                values_list.append(current_card)
        renpy.random.shuffle(values_list)
        while len(values_list) < ww * hh:
            values_list.append('empty')

# Game screen
screen memo_scr:
    # Timer
    timer 1.0 action If (memo_timer > 1, SetVariable("memo_timer", memo_timer - 1), Jump("memo_game_lose") ) repeat True
    # Game field
    grid ww hh:
        align (.5, .5) # Centered
        for card in cards_list:
            button:
                left_padding 0
                right_padding 0
                top_padding 0
                bottom_padding 0
                background None
                if card["c_value"] == 'empty':
                    if img_mode:
                        add "card empty"
                    else:
                        text " " size card_size
                else:
                    if card["c_chosen"]:
                        if img_mode:
                            add "card " + card["c_value"]
                        else:
                            text card["c_value"] size card_size
                    else:
                        if img_mode:
                            add "card back"
                        else:
                            text "#" size card_size
                # Clicking on the card button
                action If ( (card["c_chosen"] or not can_click), None, [SetDict(cards_list[card["c_number"]], "c_chosen", True), Return(card["c_number"]) ] )
    text str(memo_timer) xalign .5 yalign 0.0 size card_size

# The actual game
label memoria_game:
    $ cards_init()
    $ cards_list = []
    python:
        for i in range (0, len(values_list) ):
            if values_list[i] == 'empty':
                cards_list.append ( {"c_number":i, "c_value": values_list[i], "c_chosen":True} )   
            else:
                cards_list.append ( {"c_number":i, "c_value": values_list[i], "c_chosen":False} )   
    $ memo_timer = max_time
    # Show the game screen
    show screen memo_scr
    # Main game loop
    label memo_game_loop:
        $ can_click = True
        $ turned_cards_numbers = []
        $ turned_cards_values = []
        $ turns_left = max_c
        label turns_loop:
            if turns_left > 0:
                $ result = ui.interact()
                $ memo_timer = memo_timer
                $ turned_cards_numbers.append (cards_list[result]["c_number"])
                $ turned_cards_values.append (cards_list[result]["c_value"])
                $ turns_left -= 1
                jump turns_loop
        # Prevent opening extra cards
        $ can_click = False
        if turned_cards_values.count(turned_cards_values[0]) != len(turned_cards_values):
            $ renpy.pause (wait, hard = True)
            python:
                for i in range (0, len(turned_cards_numbers) ):
                    cards_list[turned_cards_numbers[i]]["c_chosen"] = False
        else:
            $ renpy.pause (wait, hard = True)
            python: 
                for i in range (0, len(turned_cards_numbers) ):
                    cards_list[turned_cards_numbers[i]]["c_value"] = 'empty'
                for j in cards_list:
                    if j["c_chosen"] == False:
                        renpy.jump ("memo_game_loop")
                renpy.jump ("memo_game_win")
        jump memo_game_loop

# Loss
label memo_game_lose:
    hide screen memo_scr
    $ renpy.pause (0.1, hard = True)
    "you lost kiddo, try again"
    jump memoria_game

# Win
label memo_game_win:
    hide screen memo_scr
    $ renpy.pause (0.1, hard = True)
    jump memoria_won