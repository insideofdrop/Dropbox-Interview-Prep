"""
Given a URL, crawl that webpage for URLs, and then continue crawling until you've visited all URLs
Assume you have an API with two methods:
get_html_content(url) -> returns html of the webpage of url
get_links_on_page(html) -> returns array of the urls in the html

Do this in a breadth-first style manner (it's just easier).
"""

class Webcrawler:

    def __init__(self, url):
        self.visited_urls = set()
        self.url_queue = collections.deque()
        self.url_queue.appendleft(url)
    
    def process_url(self, url):
        try:
            html = get_html_content(url) #Interviewer asks which line is the bottleneck. IT'S THIS ONE!
        except ConnectionError:
            return #talk about retries, what to do in this case
        links = get_links_on_page(html)
        for link in links:
            if link not in self.visited_urls:
                self.visited_urls.add(link)
                self.url_queue.appendleft(link)

    def run(self):
        while self.url_queue:
            current_url = self.url_queue.pop()
            self.process_url(current_url)
        return list(self.visited)

"""
Now you are asked what the bottleneck is. See the above comment.
How do you fix the bottleneck?
Use multithreading!
Some interviewers let you use the ThreadPoolExecutor (lets you queue the work and self-manages the threads)
"""

from concurrent.futures import ThreadPoolExecutor

class MultiThreadedWebcrawler:

    def __init__(self, url):
        self.visited_urls = set()
        self.lock = threading.Lock()
        self.url_queue = collections.deque()
        self.url_queue.appendleft_(url)
        self.active_futures = []
        self.max_active_jobs_in_pool = 50
    
    def process_url(self, url):
        try:
            html = get_html_content(url) #Interviewer asks which line is the bottleneck. It's this one!
        except ConnectionError:
            return #talk about retries, what to do in this case
        links = get_links_on_page(html)
        with self.lock: #this is the same as calling self.lock.acquire()
            for link in links:
                if link not in self.visited_urls:
                    self.visited_urls.add(link)
                    self.url_queue.appendleft(link)
        #and then calling self.lock.release()

    def run(self):
        with pool as ThreadPoolExecutor(max_workers=20):
            while True:
                with lock:
                    num_active_jobs = len(self.active_futures)
                    num_urls_to_crawl = len(self.url_queue)
                    if num_urls_to_crawl == 0 and num_active_jobs == 0:
                        #Termination - you have no urls left to crawl, and all of your 
                        #jobs in the pool are complete.
                        break
                    
                    #If you have too many jobs still running in the pool, then just let them run again
                    #Otherwise, if you have a manageable amount, then you can submit more. 
                    if num_active_jobs <= self.max_active_jobs_in_pool:
                        number_of_jobs_to_submit = min(
                            num_urls_to_crawl, 
                            self.max_active_jobs_in_pool - num_active_jobs
                        )
                        for _ in range(number_of_jobs_to_submit):
                            future = pool.submit(self.process_url, self.url_queue.pop())
                            self.active_futures.append(future)
                #Outside of the lock, you can remove completed futures from the active_futures
                self.active_futures = [future for future in self.active_futures if not future.done()]
                time.sleep(1) #Let someone else take the lock. 
                
        return list(self.visited_urls)
