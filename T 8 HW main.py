import os
import time
import threading
import multiprocessing
from queue import Queue
# Список ключових слів для пошуку
KEYWORDS = ['Python', 'programming', 'multiprocessing', 'threading']
# Список текстових файлів для обробки
FILES_DIR = 'path/to/your/text/files'
files = [os.path.join(FILES_DIR, f) for f in os.listdir(FILES_DIR) if f.endswith('.txt')]
def search_keywords_in_file(file_path, keywords, results_queue):
    """Шукає ключові слова в заданому файлі та додає результати до черги."""
    results = {}
    for keyword in keywords:
        occurrences = []
        with open(file_path, 'r') as file:
            for line_num, line in enumerate(file, start=1):
                if keyword.lower() in line.lower():
                    occurrences.append(line_num)
        if occurrences:
            results[keyword] = occurrences
    results_queue.put(results)
def multithread_search(files, keywords):
    """Паралельний пошук ключових слів у файлах, використовуючи threading."""
    start_time = time.time()
    results = {}
    threads = []
    results_queue = Queue()
    for file_path in files:
        thread = threading.Thread(target=search_keywords_in_file, args=(file_path, keywords, results_queue))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    while not results_queue.empty():
        partial_results = results_queue.get()
        for keyword, occurrences in partial_results.items():
            if keyword in results:
                results[keyword].extend(occurrences)
            else:
                results[keyword] = occurrences
    print(f"Багатопотоковий пошук завершено за {time.time() - start_time:.2f} секунд.")
    return results
def multiprocess_search(files, keywords):
    """Паралельний пошук ключових слів у файлах, використовуючи multiprocessing."""
    start_time = time.time()
    results = {}
    processes = []
    results_queue = Queue()
    for file_path in files:
        process = multiprocessing.Process(target=search_keywords_in_file, args=(file_path, keywords, results_queue))
        process.start()
        processes.append(process)
    for process in processes:
        process.join()
    while not results_queue.empty():
        partial_results = results_queue.get()
        for keyword, occurrences in partial_results.items():
            if keyword in results:
                results[keyword].extend(occurrences)
            else:
                results[keyword] = occurrences
    print(f"Багатопроцесорний пошук завершено за {time.time() - start_time:.2f} секунд.")
    return results
# Тестування багатопотокового та багатопроцесорного пошуку
print("Багатопотоковий пошук:")
multithread_search(files, KEYWORDS)
print("\nБагатопроцесорний пошук:")
multiprocess_search(files, KEYWORDS)
