# coding: utf-8

import random


def rand_num():
    # 生成一个不重复的四位数字List
    rand_list = random.sample(range(10), 4)

    while rand_list[0] == 0:
        rand_list = random.sample(range(10), 4)

    return rand_list


def user_num():
    while True:
        user = input("输入一个首位不为零，且各位不重复的 4 位数字：").strip()
        # 1. 输入的不是纯数字
        if not user.isdigit():
            print("请输入纯数字！！\n")
        # 2. 输入的是纯数字
        else:
            # 2.1 长度不正确
            if not len(user) == 4:
                print("输入字符串长度不正确！！\n")

            # 2.2 输入的首位为 0
            elif user[0] == '0':
                print("首位不为零！！\n")

            # 2.3 输入的数字带重复
            elif not len(set(user)) == 4:
                print("输入 4 位不重复的数字！！\n")

            # 2.4 剩下的应该就是合乎要求的user_string了
            else:
                lst = []
                for i in range(len(user)):
                    lst.append(int(user[i]))
                return lst


def compare(user_list, target_list):
    a = 0
    b = 0
    for i in range(len(user_list)):
        if user_list[i] == target_list[i]:
            a += 1
        if user_list[i] in target_list:
            b += 1
    return a, b-a


def main():

    answer = rand_num()
    print("Random number is: ", answer)

    guess = 0
    max_guess = 10

    while guess <= max_guess:
        print('--------------------{}/{} Guessing--------------------'.format(guess+1, max_guess))
        user = user_num()
        guess_A, guess_B = compare(user, answer)
        if guess_A == 4:
            print("\nCool, you got it!!")
            break
        else:
            print('Your guessing is: {} A {} B\n'.format(guess_A, guess_B))

        guess += 1
        if guess == max_guess:
            print("G A M E     O V E R!!")
            print("Random number is: ", answer)
            break

    return 0


if __name__ == "__main__":
    main()
