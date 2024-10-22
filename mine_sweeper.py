from random import uniform
import os


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def make_map(mines: int, rows: int, cols: int):
    heat_map = [[uniform(0, 1) for _ in range(cols)] for _ in range(rows)]
    veiw_map = [[None for _ in range(cols)] for _ in range(rows)]
    mine_locs = []

    for line in heat_map:
        mine_locs.extend(line)
    mine_locs.sort(reverse=True)
    mine_locs = mine_locs[:mines]

    for row in range(rows):
        for col in range(cols):
            if heat_map[row][col] not in mine_locs:
                heat_map[row][col] = 0
    for row in range(rows):
        for col in range(cols):
            if heat_map[row][col] in mine_locs:
                rs = row - 1 if row - 1 >= 0 else 0
                re = row + 2 if row + 2 <= rows else rows
                cs = col - 1 if col - 1 >= 0 else 0
                ce = col + 2 if col + 2 <= cols else cols
                for ri in range(rs, re):
                    for ci in range(cs, ce):
                        if not heat_map[ri][ci] == -1 and not type(heat_map[ri][ci]) == float:
                            heat_map[ri][ci] += 1
                heat_map[row][col] = -1
    return heat_map, veiw_map


def start_input():
    r, c, m = 0, 0, 0
    try:
        ans = input("choose between 1: easy, 2: medium, 3: hard, 4: custom.")
        match ans:
            case "1":
                print()
                r = 9
                c = 9
                m = 10
            case "2":
                r = 15
                c = 15
                m = 25
            case "3":
                r = 30
                c = 15
                m = 99
            case "4":
                r, c, m = custom_start_input(r, c, m)
        return r, c, m
    except ValueError as e:
        raise e
    except Exception as e:
        print(e)


def custom_start_input(r: int, c: int, m: int):
    for i in range(5):
        ar = input("how many rows wide will your board be?")
        if ar.isdigit():
            r = int(ar)
        ac = input("how many columns long will your board be?")
        if ac.isdigit():
            c = int(ac)
        am = input("how many mines will be hidden on your board?")
        if am.isdigit():
            m = int(am)
        if r > 0 and c > 0 and 0 < m < r * c:
            return r, c, m
        else:
            print("please input numbers larger then zero for rows and columns, "
                  "and leave some room for play with the number of mines")
    if r <= 0 or c <= 0 or m <= 0:
        raise ValueError


def player_input(rows: int, cols: int):
    r = ""
    c = ""
    flag = False
    for i in range(3):
        print("input number from 1 to n, if you wish to flag a spot add -f to the input, to remove a flag -rf")
        R_ans = input('input row. for example 5 to reveal somthing in the 5th row: ')
        C_ans = input('input column. for example 5 to reveal somthing in the 5th column: ')
        F_ans = input('input flag. leave empty for non flag reveals: ')
        if '-f' in F_ans:
            flag = 'f'
        if '-rf' in F_ans:
            flag = 'rf'
        for char in R_ans:
            if char.isdigit():
                r += char
                print(r)
        if r.isnumeric() and int(r) <= rows:
            r = int(r) - 1

        for char in C_ans:
            if char.isdigit():
                c += char
                print(c)
        if c.isnumeric() and int(c) <= cols:
            c = int(c) - 1
        if (type(r) == str or type(c) == str) or (c > cols or r > rows) or (r < 0 or c < 0):
            print("there was some other problem with your input")
            print(f"you have {3 - (i + 1)} more tries")
            r = ""
            c = ""
            flag = False
        else:
            break
    if (type(r) == str or type(c) == str) or (c > cols or r > rows) or (r < 0 or c < 0):
        print("so you don't want to play? that's fine")
        quit(1)
    return r, c, flag


def print_map(clint_map, cols: int, mines: int, flags: int):
    index_str = ' ' * 6 + "|"
    for i in range(cols):
        if i < 9:
            index_str += f"  {i + 1}  |"
        else:
            index_str += f"  {i + 1} |"
    print(index_str)
    for i, line in enumerate(clint_map):
        line_str = f"|"
        if i < 9:
            line_str += f"  {i + 1}  | "
        else:
            line_str += f" {i + 1}  | "
        for item in line:
            item_str = str(item) + ', '
            i_str_len = len(item_str)
            match i_str_len:
                case 6:
                    line_str += item_str
                case 4:
                    line_str += ' ' + item_str + ' '
                case 3:
                    line_str += ' ' * 2 + item_str + ' '
            # line_str += ' ' * ((3 - (1 + len(str(item))))) + str(item) + ', ' + ' ' * ((3 - (2 + len(str(item)))))
        print(line_str)
    print(f"mines: {mines} |\t\t\t\t\t| flags: {flags}")


def game_over(server_map, clint_map, rows, cols, mines, flags):
    print("game over")
    for row in range(rows):
        for col in range(cols):
            if server_map[row][col] == -1:
                clint_map[row][col] = -1
    print_map(clint_map, cols, mines, flags)
    print("see you next time!")
    return False


def reveal_empty(server_map, clint_map, rows, cols, start_row, start_col):
    points_to_check: list[tuple[int, int]] = [(start_row, start_col)]
    checked_points: set[tuple[int, int]] = {(start_row, start_col)}
    for point_check in points_to_check:
        row, col = point_check
        check_point(server_map, rows, cols, row, col, points_to_check, checked_points)
    for row in range(rows):
        for col in range(cols):
            if (row, col) in checked_points:
                clint_map[row][col] = server_map[row][col]


def check_point(server_map, rows, cols, row, col, points_to_check, checked_points):
    rs = row - 1 if row - 1 >= 0 else 0
    re = row + 2 if row + 2 <= rows else rows
    cs = col - 1 if col - 1 >= 0 else 0
    ce = col + 2 if col + 2 <= cols else cols
    for ri in range(rs, re):
        for ci in range(cs, ce):
            point = (ri, ci)
            if server_map[ri][ci] == 0:
                if point not in points_to_check:
                    points_to_check.append(point)
                checked_points.add(point)
            else:
                checked_points.add(point)


def check_point1(server_map, rows, cols, start_row, start_col, points_to_check, checked_points):
    for r in range(start_row, 0, -1):
        point = (r, start_col)
        if server_map[r][start_col] == 0:
            if point not in points_to_check:
                points_to_check.append(point)
            checked_points.add(point)
        else:
            checked_points.add(point)
            break
    for r in range(start_row, rows):
        point = (r, start_col)
        if server_map[r][start_col] == 0:
            if point not in points_to_check:
                points_to_check.append(point)
            checked_points.add(point)
        else:
            checked_points.add(point)
            break
    for c in range(start_col, 0, -1):
        point = (start_row, c)
        if server_map[start_row][c] == 0:
            if point not in points_to_check:
                points_to_check.append(point)
            checked_points.add(point)
        else:
            checked_points.add(point)
            break
    for c in range(start_col, cols):
        point = (start_row, c)
        if server_map[start_row][c] == 0:
            if point not in points_to_check:
                points_to_check.append(point)
            checked_points.add(point)
        else:
            checked_points.add(point)
            break


def check_victory(flaged_points, server_map, mines, cols, clint_map):
    good = False
    if len(flaged_points) < mines:
        return True
    for point in flaged_points:
        r, c = point
        if server_map[r][c] == -1:
            good = True
        else:
            good = False
    if good:
        print_map(clint_map, cols, mines, len(flaged_points))
        print("hooray, you won!")
    return not good


def main():
    # rows, cols, mines = 5, 5, 3
    rows, cols, mines = start_input()
    server_map, clint_map = make_map(mines, rows, cols)
    # for line in server_map:
    #     print(line)
    flaged_points: list[tuple[int, int]] = []
    alive = True
    while alive:
        clear()
        print_map(clint_map, cols, mines, len(flaged_points))
        r, c, flag = player_input(rows, cols)
        if flag:
            match flag:
                case 'f':
                    if len(flaged_points) < mines:
                        if (r, c) not in flaged_points:
                            flaged_points.append((r, c))
                            clint_map[r][c] = "flag"
                    else:
                        print("you got as many flags as mines, you can't flag all of the map."
                              " you have to remove a flag before you use it")
                case 'rf':
                    if (r, c) in flaged_points:
                        flaged_points.pop(-1)
                        clint_map[r][c] = None
        else:
            res = server_map[r][c]
            match res:
                case -1:
                    game_over(server_map, clint_map, rows, cols, mines, len(flaged_points))
                    break
                case 0:
                    reveal_empty(server_map, clint_map, rows, cols, r, c)
                case _:
                    clint_map[r][c] = res
        alive = check_victory(flaged_points, server_map, mines, cols, clint_map)


if __name__ == '__main__':
    main()
