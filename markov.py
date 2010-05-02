#!/usr/bin/env python
import random

class Chain(object):
    def __init__(self, input, window_size):
        self.root = Link(None)
        self.window_size = window_size
        self.root.process(input, window_size)
        
    def generate(self, max, start_word=None):
        if not start_word:
            start_word = self.root.select_random_link().data
        return [x.data for x in
                self.root.generate(start_word, self.window_size, max)
                if x.data]

class Window(object):
    def __init__(self, window_size):
        self.data = []
        self.window_size = window_size
    
    def add(self, thing):
        if len(self.data) >= self.window_size:
            del self.data[0]
        self.data.append(thing)


class Link(object):
    def __init__(self, data):
        self.data = data
        self.links = {}
        self.count = 0
    
    @property
    def times_seen(self):
        return self.count
    
    @property
    def times_links_seen(self):
        return sum((x.times_seen for x in self.links.values()))
    
    def seen(self):
        self.count += 1

    def process(self, input, window_size):
        current_window = Window(window_size)
        for x in input:
            current_window.add(x)
            self.process_window(current_window)
    
    def process_window(self, window):
        link = self
        for x in window.data:
            link = link.process_word(x)
    
    def process_word(self, part):
        link = self.links.get(part)
        if not link:
            link = Link(part)
            self.links[part] = link
        link.seen()
        return link
    
    def select_random_link(self):
        universe = self.times_links_seen
        rnd = random.randint(1, universe+1)
        total = 0
        for child in self.links.values():
            total += child.times_seen
            if total >= rnd:
                return child
        return None
    
    def follow(self, w):
        return self.links.get(w)
    
    def follow_window(self, window):
        link = self
        for w in window.data:
            link = link.follow(w)
            if not link: return None
        return link
    
    def generate(self, start, window_size, max):
        rval = []
        window = Window(window_size-1)
        window.add(start)
        link = self.follow_window(window)
        
        while link != None and max != 0:
            next = link.select_random_link()
            if next:
                rval.append(link)
                window.add(next.data)
            link = self.follow_window(window)
            max -= 1
        return rval
                
    def __repr__(self):
        return "<%s, %d>" % (self.data, self.count)


