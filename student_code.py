import math
import re

class Bayes_Classifier:

    def __init__(self):
        self.allwords = {}
        self.positive = 0
        self.negative = 0
       



    def train(self, lines):
        
        for line in lines:
            line = line.replace('\n', '')
            scheme = line.split('|')
            label = scheme[0]
            ID = scheme[1]            
            reviews = scheme[2]
            review_words = reviews.split()
            
            for word in review_words:
                if word not in self.allwords:
                    if label == '5':
                        self.allwords[word] = {'5':1,'1':0}
                    else:
                        self.allwords[word] = {'1':1,'5':0}                    
                else:
                    self.allwords[word][label] += 1

            if label == '5':
                self.positive += len(review_words)
            else:
                self.negative += len(review_words)

    def classify(self, lines):
        
        punctuation = ['.', ',', '?', '\'', '/', '-', '\"', '*', '#', '!', '@', \
                       '$', '%', '^', '&', '(', ')', '+', '=', '<', '>', '~', '[', \
                       ']', '{', '}', '`']
        stop_words = ['i','you','he','she','it','we','they','if','in','into', \
                      'is','itself','let','me','more','most','my','myself','nor', \
                      'of','on','once','only','or','other','ought','our','ours', \
                      'ourselves','out','over','own','same','should','so','some', \
                      'such','than','that','the','their','theirs','them','themselves', \
                      'then','there','this','those','through','to','too','under','until', \
                      'up','very','was','were','what','when','where','which','while', \
                      'who','whom','why','with','would','your','yours','yourself']
        

        predict = []
        num_words = len(self.allwords)

        for line in lines:
            line = line.replace('\n', '')
            scheme = line.split('|')
            reviews = scheme[2]
            review_words = reviews.split()
            Pp = 0
            Pn = 0
            
            for word in review_words:
                if word in stop_words or word in punctuation:
                    continue
                if word not in self.allwords:
                    P = math.log(float(1)/len(self.allwords))
                else:
                    Pp += math.log(float(1+self.allwords[word]['5'])/(num_words+self.positive))
                    Pn += math.log(float(1+self.allwords[word]['1'])/(num_words+self.negative))

            if Pp >= Pn:
                predict.append('5')
            else:
               predict.append('1')                
    
        return predict
    
