def sum(x, y) :
    return x + y


def main():
    x = int(input("Enter positive number: "))
    while True:
        if x > 0:
            break
        print("Number must be positive!")
        x = int(input("Enter positive number: "))
    y = int(input("Enter positive number: "))
    while True:
        if y > 0 and y != x:
            break
        msg = "Numbers can't be equal" if y == x else "Number must be positive!"
        print(msg)
        y = int(input("Enter positive number: "))
    print(f"{x} + {y} = {sum(x, y)}")


if __name__ == '__main__': main()