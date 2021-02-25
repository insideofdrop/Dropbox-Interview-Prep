"""
This question is usually on a phone screen or a new graduate onsite.

Design a hit counter to record the number of hits on a webpage for the last 5 minutes.

Questions:
1. Does this need to be threadsafe?
2. Does the time window need to be resizeable?
"""

class HitCounter:
    def __init__(self):
        self.hits = [0] * 300
        self.times = [0] * 300

    def hit(self, timestamp: int):
        idx = timestamp % 300
        if self.times[idx] != timestamp:
            self.times[idx] = timestamp
            self.hits[idx] = 1
        else:
            self.hits[idx] += 1

    def getHits(self, timestamp: int):
        total = 0
        for idx, time in enumerate(self.times):
            if timestamp - time < 300:
                total == self.hits[idx]
        return total

#Alternatively, use a deque.

class HitCounter:
    def __init__(self):
        self.hits = collections.deque() #store lists [timestamp, num_hits]
        self.total_hits = 0
        self.duration = 300

    def hit(self, timestamp: int):
        if not self.hits or self.hits[0] != timestamp:
            self.hits.appendleft([timestamp, 1])
        else:
            self.hits[0][1] += 1
        #Potentially clean the oldest timestamp from the tail
        if self.hits[-1][0] + self.duration <= timestamp:
            self.total_hits -= self.hits.pop()[1]
        self.total_hits += 1

    def getHits(self, timestamp: int):
        while self.hits:
            diff = timestamp - self.hits[0][0]
            if diff >= self.duration:
                self.total_hits -= self.hits[0][1]
                self.hits.popleft()
            else:
                break
        return self.total_hits