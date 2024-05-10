import numpy as np
import pandas
import pprint

import othello

DATA_FILES_NAME = [f"csv/wthor ({i}).csv" for i in range(46)]
DATA_COUNT_PER_FILE = 10000


def convert_line_to_data(transcript: str) -> tuple:
    black_player = othello.Othello(color=othello.OthelloPiece.Black)
    white_player = othello.Othello(color=othello.OthelloPiece.White)
    black_player.initial_board()
    white_player.initial_board()

    loop = 0
    passed = False

    while transcript != "":
        x, y = othello.move_to_pos(transcript[:2])

        if loop % 2 == 0:
            flip_dirs = black_player.can_put(x, y)
            if len(flip_dirs) > 0:
                black_player.put(x, y, black_player.color, flip_dirs)
                white_player.put(x, y, black_player.color, flip_dirs)
                passed = False
            else:
                if passed:
                    print("why ?")
                    break
                else:
                    passed = True

        else:
            flip_dirs = white_player.can_put(x, y)
            if len(flip_dirs) > 0:
                black_player.put(x, y, white_player.color, flip_dirs)
                white_player.put(x, y, white_player.color, flip_dirs)
                passed = False
            else:
                if passed:
                    print("why ?")
                    break
                else:
                    passed = True
        loop += 1
        if not passed:
            transcript = transcript[2:]

    if black_player.judge_winner() == othello.OthelloPiece.Black:
        return black_player.pool_play_board, black_player.pool_move_board
    else:
        return white_player.pool_play_board, white_player.pool_move_board


def main():
    current_data_count = 0
    current_file_count = 0

    save_board_data = []
    save_moves_data = []

    for filename in DATA_FILES_NAME:
        file = pandas.read_csv(filename)

        for transcript in file["transcript"].to_list():
            print(f"converte transcript : {transcript} | count : {current_data_count}")
            current_data_count += 1
            board_data, moves_data = convert_line_to_data(transcript)
            save_board_data += board_data
            save_moves_data += moves_data

            pprint.pprint(board_data[1])
            pprint.pprint(moves_data[1])

            if current_data_count == DATA_COUNT_PER_FILE:
                np.savez(
                    f"data/wthor-{current_file_count}",
                    np.array(save_board_data),
                    np.array(save_moves_data),
                )
                current_data_count = 0
                current_file_count += 1
                save_board_data = []
                save_moves_data = []

    np.savez(
        f"data/wthor-{current_file_count}",
        np.array(save_board_data),
        np.array(save_moves_data),
    )


if __name__ == "__main__":
    main()
