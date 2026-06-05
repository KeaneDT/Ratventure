from game import run_game


def main():
    while True:
        run_game()
        again = input("\n  Play again? (y/n): ").strip().lower()
        if again != "y":
            print("  Thanks for playing!\n")
            break


if __name__ == "__main__":
    main()
