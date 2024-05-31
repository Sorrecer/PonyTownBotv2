import random

# Function to play the game
def play_game():
    # Randomly place the bomb in one of the four boxes
    bomb_position = random.randint(1, 4)
    
    # Show the boxes to the player
    print("Boxes: [1] [2] [3] [4]")
    
    # Ask the player to pick a box
    player_choice = int(input("Pick a box (1-4): "))
    
    # Initialize the boxes
    boxes = ["[ ]", "[ ]", "[ ]", "[ ]"]
    
    # Check if the player picked the box with the bomb
    if player_choice == bomb_position:
        result = "Boom! You picked the box with the bomb. You lose!"
        boxes[bomb_position - 1] = "[💣]"
    else:
        result = "Quack! You picked a box with a duck. You win!"
        boxes[player_choice - 1] = "[🦆]"
        boxes[bomb_position - 1] = "[💣]"
    
    # Print the final state of the boxes
    print(" ".join(boxes))
    print(result)

# Run the game
play_game()
