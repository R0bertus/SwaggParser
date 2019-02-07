from swaggparser.parser import SwaggParser


def main():
    sp = SwaggParser()
    #sp.preparse()
    #sp.create_pojos()
    #sp.sufparse()
    sp.apify()


if __name__ == '__main__':
    main()
