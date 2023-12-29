import time
import queue
import threading
import sys

from news_extractor import NewsExtractor

timeout = 300

class NewsQueue(queue.Queue):
    def __init__(self):
        super().__init__()
        self.shown_news = set()

    def put(self, item):
        if item.title not in self.shown_news:
            self.shown_news.add(item.title)
            super().put(item)

def bg_task(extractor, queue):
    while True:
        news = extractor.get_latest_news()
        for item in news:
            queue.put(item)
        time.sleep(timeout)


def main():
    queue = NewsQueue()
    extractor = NewsExtractor()
    bg_thread = threading.Thread(target = bg_task, args = (extractor, queue), daemon = True)
    shown_news = set()

    try:
        bg_thread.start()
        while True:
            if not queue.empty():
                news_item = queue.get()
                if news_item.title not in shown_news:
                    shown_news.add(news_item.title)
                    print(news_item)
                    print("\n")
                    sys.stdout.flush()
            else:
                time.sleep(0.5)
    except (KeyboardInterrupt, SystemExit):
        print("Exiting...")
        sys.exit()

if __name__ == '__main__':
    main()
    