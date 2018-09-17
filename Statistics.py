from Tkinter import *


def _get_streak(games):
    if len(games) == 0:
        return 0
    games = games[::-1]
    t = []
    for i in games:
        if len(t) == 0 or i[1] == t[-1]:
            t.append(i[1])
        else:
            break
    return len(t) if t[0] == "win" else -1 * len(t)


def _get_stats(games):
    wins = len([l for l in games if l[1] == "win"])
    losses = len(games) - wins
    streak = _get_streak(games)
    return wins, losses, streak


def show_stats(file_path=None):
    if file_path is None:
        file_path = "./stats.csv"
    with open(file_path) as f:
        lines = f.readlines()

    lines = [l.strip() for l in lines]

    # omit the timestamp and split the comas
    lines = [l.split(",")[1:] for l in lines]

    print lines

    lines_t1 = []
    lines_t2 = []
    lines_mixed = []
    for l in lines:
        if int(l[2]) > 0 and int(l[3]) > 0:
            lines_mixed.append(l)
        elif int(l[2]) > 0 and int(l[3]) == 0:
            lines_t1.append(l)
        elif int(l[2]) == 0 and int(l[3]) > 0:
            lines_t2.append(l)

    total_wins, total_losses, total_streak = _get_stats(lines)

    # print "total win/losses:", total_wins, total_losses, round(total_wins * 1.0 / total_losses, 3) * 100, "%"
    # print "streak:", total_streak

    wins_t1, losses_t1, streak_t1 = _get_stats(lines_t1)
    # print "type 1:", get_stats(lines_t1)

    wins_t2, losses_t2, streak_t2 = _get_stats(lines_t2)
    # print "type 2:", get_stats(lines_t2)

    wins_mixed, losses_mixed, streak_mixed = _get_stats(lines_mixed)
    # print "type mixed:", get_stats(lines_mixed)

    root = Tk()

    root.title("Statistics")

    label_total = Label(root,
                        text="Against ANYONE (w%) = " + str(total_wins) + "/" + str(
                            total_losses + total_wins) + " = " + str(round(
                            total_wins * 1.0 / (total_losses + total_wins), 3) * 100) + "%\nCurrent streak: " + str(
                            total_streak))
    label_total.pack()

    Frame(root, width="150", height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)

    label_t1 = Label(root,
                     text="Against TYPE 1 opponents (w%) = " + str(wins_t1) + "/" + str(
                         losses_t1 + wins_t1) + " = " + str(round(
                         wins_t1 * 1.0 / (losses_t1 + wins_t1), 3) * 100) + "%\nCurrent streak: " + str(streak_t1))
    label_t1.pack()

    Frame(root, width="150", height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)

    label_t2 = Label(root,
                     text="Against TYPE 2 opponents (w%) = " + str(wins_t2) + "/" + str(
                         losses_t2 + wins_t2) + " = " + str(round(
                         wins_t2 * 1.0 / (losses_t2 + wins_t2), 3) * 100) + "%\nCurrent streak: " + str(streak_t2))
    label_t2.pack()

    Frame(root, width="150", height=2, bd=1, relief=SUNKEN).pack(fill=X, padx=5, pady=5)

    label_mixed = Label(root,
                        text="Against MIXED (w%) = " + str(wins_mixed) + "/" + str(
                            losses_mixed + wins_mixed) + " = " + str(round(
                            wins_mixed * 1.0 / (losses_mixed + wins_mixed), 3) * 100) + "%\nCurrent streak: " + str(
                            streak_mixed))
    label_mixed.pack()

    root.mainloop()


if __name__ == "__main__":
    show_stats(file_path="./GUI/stats.csv")
