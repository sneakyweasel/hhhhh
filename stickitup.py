# hello
import hashpumpy

def main():
    # admi / '4dd28ad0560441245de6fda3973890eeb41b702d' / variable key length
    for i in range(6, 30):
        data = hashpumpy.hashpump('4dd28ad0560441245de6fda3973890eeb41b702d', "admi", 'n', i)
        print("{}: {}".format(i, data))

if __name__ == "__main__":
    main()