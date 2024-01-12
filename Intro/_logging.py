# Логування

import logging

logging.basicConfig(filename="log.txt", 
                    level=logging.INFO, 
                    datefmt="%Y-%m-%d %H:%M:%S", 
                    format="%(asctime)s %(levelname)s [%(filename)s::%(lineno)d] %(message)s %(args)s")

import module

def main() -> None:
    
    logging.info('Logger info')
    logging.error('Querry error', {'sql' : 'SELECT *', 'err' : 'Syntax error'})


if __name__ == "__main__":
    main()