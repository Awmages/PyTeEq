from Gen_8684AD import Agilent_8684


def main():
    sig_gen = Agilent_8684()
    print(sig_gen.name)
    sig_gen.name = "test"
    print(sig_gen.name)

if __name__ == '__main__':
    main()
