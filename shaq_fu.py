#!/usr/bin/env python
from markov import Chain
import re
import random

rm_list = [',', ', ', '\n\n', '*', '**', ' ']

def tokens(text):
    text = text.replace('(', '')
    text = text.replace(')', '')
    return [x.lower() for x in re.split(r'(\s+)', text) if x not in rm_list]

class ShaqFu(object):
    def __init__(self):
        
        data = open('training_data.txt').read()
        self.chain = Chain(tokens(data), 5)
    
    def generate_line(self, rhymes):
        words = self.chain.generate(100)
        lines = ' '.join([x for x in words]).splitlines(False)
        return random.choice(lines)
    
    def generate_chorus(self):
        return ['[CHORUS]'] + [self.generate_line(True) for x in xrange(5)] + ['\n']
    
    def generate_verse(self, min_length, max_length):
        length = random.randint(min_length, max_length)
        return ['[VERSE]'] + [self.generate_line(False) for x in xrange(length)] + ['\n']
        
    def generate_song(self):
        chorus = self.generate_chorus()
        verses = [self.generate_verse(5, 10) for x in xrange(3)]
        return verses[0] + chorus + verses[1] + chorus + verses[2]

def main():
    song = ShaqFu().generate_song()
    for x in song:
        print x
    #for x in xrange(5):
    #    print generate_line_from(chain)
    #words = chain.generate(100)
    #print ' '.join([x for x in words])

main() if __name__=='__main__' else None


#data = open('training_data.txt').read()
#print tokens(data)