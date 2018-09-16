def calcProbabilityGE(target_dice, out_of_dice, symbol):
    # print "target", target_dice, " outof", outofDice, " symb ", symbol
    prob = 0
    if target_dice <= 0:
        return 1
    for i in range(target_dice, out_of_dice + 1):
        prob += calcProbabilityE(i, out_of_dice, symbol)

    return prob


def calcProbabilityE(target_dice, out_of_dice, symbol):
    """
    Return the probability that exactly "target_dice" exist
    within the total number of dice ("outofDice").
    Parameter "symbol", refers to the desired number (or if is sta!)

    :param target_dice:
    :param out_of_dice:
    :param symbol:
    :return:
    """
    # TODO: it's not the best way to do the calculations (factorial does not scale well)

    if target_dice > out_of_dice:
        return 0

    if target_dice < 0:
        return 0

    if symbol == 0:
        return float(shitOperation(out_of_dice, target_dice) * pow(1, target_dice) * pow(5, (
                out_of_dice - target_dice))) / pow(6, out_of_dice)

    return float(
        shitOperation(out_of_dice, target_dice) * pow(2, target_dice) * pow(4,
                                                                            (
                                                                                    out_of_dice - target_dice))) / pow(
        6,
        out_of_dice)


def shitOperation(N, x):
    """
    :param N:
    :param x:
    :return:
    """
    a = max([x, N - x])
    b = min([x, N - x])

    factorial = 1

    for i in range(a + 1, N + 1):
        factorial *= i

    for i in range(1 + 1, b + 1):
        factorial /= i

    return factorial


if __name__ == "__main__":
    from Tkinter import *
    import tkMessageBox


    def callback():
        print "click!"
        tkMessageBox.showinfo(
            title="Help",
            message="To play the game..."
        )


    root = Tk()

    root.title("Calculate Bluff probabilities")

    frame = Frame(root, width=350)
    frame.pack()

    info_label = Label(root, text="this is an intro? is it unecessary?")
    info_label.pack()

    symbol_label = Label(root, text="Select symbol:")
    symbol_label.pack()

    symbol_spinny = Spinbox(root, values=(1, 2, 3, 4, 5, "*"))
    symbol_spinny.pack()

    # print(symbol_spinny.get())

    target_label = Label(root, text="Targeted number of dice:")
    target_label.pack()

    target_spinny = Spinbox(root, from_=0, to=30)
    target_spinny.pack()

    total_label = Label(root, text="Total number of dice:")
    total_label.pack()

    total_spinny = Spinbox(root, from_=0, to=30)
    total_spinny.pack()


    def calculate():
        symbol = symbol_spinny.get()
        if symbol not in {"1", "2", "3", "4", "5", "*"}:
            var_ge.set("")
            var_e.set("symbol is not valid, needs to be one of {1,2,3,4,5,*}")
            return
        symbol = int(symbol) if symbol != "*" else 0
        target = int(target_spinny.get())
        total = int(total_spinny.get())
        print symbol, target, total
        print "calculate"
        cpe = calcProbabilityE(target_dice=target, out_of_dice=total, symbol=symbol)
        print "probability equal:", cpe
        cpge = calcProbabilityGE(target_dice=target, out_of_dice=total, symbol=symbol)
        print "probability greater or equal:", cpge
        var_e.set("Probability exactly " + str(target) + " out of " + str(total) + " of symbol " + str(
            symbol if symbol != 0 else "*") + " = " + str(round(cpe, 3) * 100) + "%")
        var_ge.set("Probability at least " + str(target) + " out of " + str(total) + " of symbol " + str(
            symbol if symbol != 0 else "*") + " = " + str(round(cpge, 3) * 100) + "%")


    result_button = Button(root, text="Calculate", command=calculate)
    result_button.pack()

    var_e = StringVar()
    e_label = Label(root, textvariable=var_e)
    e_label.pack()
    var_e.set("")

    var_ge = StringVar()
    ge_label = Label(root, textvariable=var_ge)
    ge_label.pack()
    var_ge.set("")

    b = Button(root, text="Help", command=callback)
    b.pack()

    root.mainloop()
