# hello
import hashpumpy
import urllib.parse

def main():
    # admi / '4dd28ad0560441245de6fda3973890eeb41b702d' / variable key length
    results = []
    for i in range(6, 30):
        data = hashpumpy.hashpump('4dd28ad0560441245de6fda3973890eeb41b702d', "admi", 'n', i)
        results.append(data)

    for r in results:
        print("{} => {}".format(r[0], urllib.parse.quote_from_bytes(r[1])))

if __name__ == "__main__":
    main()