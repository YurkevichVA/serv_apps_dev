def create_file2() -> None:
    fname = "file2.txt"
    try:
        with open(fname, mode='w', encoding='utf-8') as f:
            f.write( "Host: localhost\r\n" )
            f.write( "Connection: close\r\n" )      
            f.write( "Content-Type: text/html" ) 
    except OSError as err:
        print("File 2 creation error", err)     


def read_lines(fname):
    f = None
    try:
        f = open(fname, mode='r', encoding='utf-8')
        return f.readlines()
    except OSError as err:
        print("Reading err", err )
    finally:
        if f is not None:
            f.close()


def parse_headers(fname) -> dict:
    return { k: v for k, v in ( map( str.strip, line.split( ':' ) ) for line in read_lines( fname ) if ':' in line ) }


def main() -> None:
    create_file2()
    for k, v in parse_headers("file2.txt").items():
        print("> %s: %s" % (k, v))


if __name__ == "__main__":
    main()