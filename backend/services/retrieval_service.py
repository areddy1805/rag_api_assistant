from backend.services.chat_service import ask


def run():

    print("\nRAG SYSTEM READY")
    print("Type 'exit' to quit\n")

    while True:

        question = input("Ask: ").strip()

        if question.lower() in ["exit", "quit"]:
            print("\nExiting...")
            break

        if not question:
            continue

        try:

            answer = ask(question)

            print("\n" + "-"*60)
            print("ANSWER")
            print("-"*60)
            print(answer)
            print("-"*60)

        except Exception as e:

            print("\nERROR:", e)


if __name__ == "__main__":
    run()