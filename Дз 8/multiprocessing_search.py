import os
import multiprocessing
from multiprocessing import Manager
import time

def search_keywords_in_file(file_path, keywords):
    found_keywords = {keyword: [] for keyword in keywords}
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            print(f"Reading file: {file_path}") 
            for keyword in keywords:
                if keyword in content:
                    found_keywords[keyword].append(file_path)
                    print(f"Found {keyword} in {file_path}")  
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
    return found_keywords

def worker(file_queue, keywords, results):
    while True:
        file_path = file_queue.get()
        if file_path is None:
            break
        found_keywords = search_keywords_in_file(file_path, keywords)
        for keyword, paths in found_keywords.items():
            results.append((keyword, paths))
        file_queue.task_done()

def multi_process_search(files, keywords):
    manager = Manager()
    file_queue = manager.Queue()
    results = manager.list() 
    
    for file in files:
        file_queue.put(file)

    processes = []
    num_processes = min(10, len(files))  
    for _ in range(num_processes):
        process = multiprocessing.Process(target=worker, args=(file_queue, keywords, results))
        process.start()
        processes.append(process)
    
    for _ in range(num_processes):
        file_queue.put(None)
    
    for process in processes:
        process.join()
    
    collected_results = {keyword: [] for keyword in keywords}
    for keyword, paths in results:
        collected_results[keyword].extend(paths)
    
    return collected_results

if __name__ == "__main__":
    files = ["file1.txt", "file2.txt", "file3.txt"]  
    keywords = ["keyword1", "keyword2", "keyword3"]  

    start_time = time.time()
    results = multi_process_search(files, keywords)
    end_time = time.time()
    print("Results:", results)
    print("Execution time:", end_time - start_time, "seconds")
