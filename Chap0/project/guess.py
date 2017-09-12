# coding: utf-8

import random


def check_valid(min_num, max_num):
    while True:
        string = input("Please enter a number between {} and {}: ".format(min_num, max_num)).strip()

        if string.isdigit():
            if min_num <= int(string) <= max_num:
                return int(string)
            else:
                print("Number out of range!!\n")
        else:
            print("Please input a number, not characters!!\n")


def main():
    max_num = 50
    min_num = 1
    rand_num = random.randint(min_num, max_num)
#    print(rand_num)
    max_guess = 10
    guess = 0

    while guess <= max_guess:
        print("-------------------- {} / {} Guessing --------------------".format(guess+1, max_guess))
        user_num = check_valid(min_num, max_num)
        if user_num > rand_num:
            print("Too big\n")
        elif user_num < rand_num:
            print("Too little\n")
        else:
            print("Good job!!")
            break

        guess += 1
        if guess == max_guess:
            print("Game over\nThe RANDOM number is: ", rand_num)
            break

    return 0


if __name__ == "__main__":
    main()
