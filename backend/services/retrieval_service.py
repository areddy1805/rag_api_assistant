from backend.services.chat_service import ask_stream


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

            print("\n" + "-"*60)
            print("ANSWER")
            print("-"*60)

            for token in ask_stream(question):
                print(token, end="", flush=True)

            print("\n" + "-"*60)

        except Exception as e:

            print("\nERROR:", e)


if __name__ == "__main__":
    run()