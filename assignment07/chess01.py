import time

my_computer_time = 0.1
opponet_computer_time = 0.5
opponents = 3
move_pairs = 30

def game(x):
    #Loops 30 times to simulate both players making a move
    board_start_time = time.perf_counter()
    for i in range(move_pairs):
        #print(f"BOARD-{x} {i+1} Judit thinking of making a move.")
        #we think for 5 seconds
        time.sleep(my_computer_time)
        print(f"BOARD-{x+1} {i+1} Judit made a move.")
        #the opponet thinks for 5 seconds.
        time.sleep(opponet_computer_time)
        print(f"BOARD-{x-1} {i+1} Judit made a move.")
    print(f"BOARD-{x+1} - >>>>>>>>>>>>>>>> Finished move in {round(time.perf_counter() - board_start_time)} secs\n")
    return round(time.perf_counter() - board_start_time)

if __name__ == "__main__":
    start_time = time.perf_counter()
    #Loops 24 time because we are playing 24 opponets.
    board_time = 0
    for board in range(opponents):
        board_time += game(board)

print(f"board exhibition finished in {board_time} secs.")
print(f"Finished in {round(time.perf_counter() - start_time)} secs.")
