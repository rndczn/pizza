"""Main for hashcode test."""

FILE = 'small.in'

def parse(file):
    with open(file) as f:
        for i, line in enumerate(f):
            print(i, line)

if __name__ == '__main__':
    parse(FILE)
