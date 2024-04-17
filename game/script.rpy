define me =  Character("Elyssia",color="#0088ff")
define Aiden = Character("Aiden",color="#ffffff")
define Lyra = Character("Lyra",color="#ffffff")
define Eldric = Character("Eldric",color="#ffffff")
define Fiona = Character("Fiona",color="#ffffff")

label start:
    scene playground:
        size(1920,1080)
    #here the main character is playing with her friends in the twilight. The light is just fading away.
    show aiden_worried at right,
    show lyra_smiling at left,
    show eldric_neutral
    Aiden "It's already dark guys. Mom says we must not be out during the dark.{w} She says queer things haunt the streets at night"
    #lyra taunts Aiden
    Eldric "Come on Aiden, don't be such a bore."
    "would you like to play a game"
    menu:
        "sure":
            jump yes_memoria_game
        "no":
            jump no_memoria_game

label yes_memoria_game:
    "here we go"
    jump memoria_game

label no_memoria_game:
    "I knew you were a coward"
    jump post_memoria

label memoria_won:
    "well done you won"
    jump post_memoria

label post_memoria:
    "the story progresses"
return