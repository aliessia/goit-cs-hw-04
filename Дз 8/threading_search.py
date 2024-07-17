import os
import threading
from queue import Queue
import time

def search_keywords_in_file(file_path, keywords):
    found_keywords = {keyword: [] for keyword in keywords}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            for keyword in keywords:
                if keyword in content:
                    found_keywords[keyword].append(file_path)
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return found_keywords

def worker(file_queue, keywords, results):
    while not file_queue.empty():
        file_path = file_queue.get()
        if file_path is None:
            break
        found_keywords = search_keywords_in_file(file_path, keywords)
        with results_lock:
            for keyword, paths in found_keywords.items():
                results[keyword].extend(paths)
        file_queue.task_done()

def multi_threaded_search(files, keywords):
    file_queue = Queue()
    results = {keyword: [] for keyword in keywords}
    
    for file in files:
        file_queue.put(file)

    global results_lock
    results_lock = threading.Lock()
    
    threads = []
    num_threads = min(10, len(files)) 
    for _ in range(num_threads):
        thread = threading.Thread(target=worker, args=(file_queue, keywords, results))
        thread.start()
        threads.append(thread)
    
    file_queue.join()
    
    for thread in threads:
        thread.join()
    
    return results

if __name__ == "__main__":
    files = ["file1.txt", "file2.txt", "file3.txt"]  
    keywords = ["keyword1", "keyword2", "keyword3"]  

    start_time = time.time()
    results = multi_threaded_search(files, keywords)
    end_time = time.time()
    print("Results:", results)
    print("Execution time:", end_time - start_time, "seconds")
