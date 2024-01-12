x = 10

def change_x()-> None:
    global x
    x = 20


def pair() :
    return 1, 2


def hello() -> str:
    x = 20
    return "Hello, World %d" %(x)


def main() -> None :
    print( hello() )
    x, y = pair()
    print(make(x, y))


def make(x, y) -> str:
    return f"x={x}, y={y}\n"


if __name__ == '__main__': main()