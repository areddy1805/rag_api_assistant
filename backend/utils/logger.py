import time


class StageLogger:

    def __init__(self):
        self.start_time = None


    def start(self, stage):
        print("\n")
        print("="*60)
        print(f"START: {stage}")
        print("="*60)
        self.start_time = time.time()


    def end(self, stage):
        elapsed = time.time() - self.start_time
        print(f"END: {stage}")
        print(f"Time: {round(elapsed,3)} sec")
        print("="*60)


    def log(self, title, data, limit=3):

        print("\n---", title, "---")

        if isinstance(data, list):

            print("count:", len(data))

            for item in data[:limit]:
                print(item)

        else:
            print(data)