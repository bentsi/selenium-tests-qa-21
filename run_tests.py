import argparse
import pytest


def parse_args():
    parser = argparse.ArgumentParser(description="Tests runner")
    parser.add_argument("-a", "--all", action="store_true",
                        help="runs all the tests in the framework")
    parser.add_argument("-s", "--security", action="store_true",
                        help="runs all the security tests in the framework")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.all:
        pytest.main(args=["-v"])
    elif args.security:
        pytest.main(args=["-v", "-m", "security"])
    else:
        print(f"Error unknown  args {args}")
        exit(1)


if __name__ == '__main__':
    main()
