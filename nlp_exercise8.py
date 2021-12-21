# -*- coding: utf-8 -*-
"""nlp_exercise8.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1aDZP09qW819rt0WtdoJMa0X9KwiSv8ag
"""

import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
doc = "He derives great joy and happiness from cycling"
doc = nltk.word_tokenize(doc)
doc = nltk.pos_tag(doc)
grammar = "NP: {<DT>?<JJ>*<NN>}"
cp = nltk.RegexpParser(grammar)
result = cp.parse(doc)
result

#1st
import spacy
nlp=spacy.load('en_core_web_sm')

text1='watched the comet from the roof with my telescope'
text2='watched the comrt from the park across the street'
text3='watched a video by the BBC about the comet'
text4='watched a video about the expedition to the comet'
text5='watched a video about the comet on my mobile'

for token in nlp(text1):
  print(token.text,'=>',token.dep_,'=>',token.head.text)
from spacy import displacy

displacy.render(nlp(text1),jupyter=True)
displacy.render(nlp(text2),jupyter=True)
displacy.render(nlp(text3),jupyter=True)
displacy.render(nlp(text4),jupyter=True)
displacy.render(nlp(text5),jupyter=True)



import nltk
nltk.download('averaged_perceptron_tagger')

import nltk
nltk.download('punkt')

#2
class State(object):
    def __init__(self, label, rules, dot_idx, start_idx, end_idx, idx, made_from, producer):
        self.label = label
        self.rules = rules
        self.dot_idx = dot_idx
        self.start_idx = start_idx
        self.end_idx = end_idx
        self.idx = idx
        self.made_from = made_from
        self.producer = producer

    def next(self):
        """Returns the tag after the dot"""
        return self.rules[self.dot_idx]

    def complete(self):
        return len(self.rules) == self.dot_idx

    def __eq__(self, other):
        return (self.label == other.label and
                self.rules == other.rules and
                self.dot_idx == other.dot_idx and
                self.start_idx == other.start_idx and
                self.end_idx == other.end_idx)

    def __str__(self):
        rule_string = ''
        for i, rule in enumerate(self.rules):
            if i == self.dot_idx:
                rule_string += '\\bullet '
            rule_string += rule + ' '
        if self.dot_idx == len(self.rules):
            rule_string += '\\bullet'
        return 'S%d %s -> %s [%d, %d] %s %s' % (self.idx, self.label, rule_string, self.start_idx, 
                                                self.end_idx, self.made_from, self.producer)

class Earley:
    def __init__(self, words, grammar, terminals):
        self.chart = [[] for _ in range(len(words) + 1)]
        self.current_id = 0
        self.words = words
        self.grammar = grammar
        self.terminals = terminals

    def get_new_id(self):
        self.current_id += 1
        return self.current_id - 1

    def is_terminal(self, tag):
        return tag in self.terminals

    def is_complete(self, state):
        return len(state.rules) == state.dot_idx

    def enqueue(self, state, chart_entry):
        if state not in self.chart[chart_entry]:
            self.chart[chart_entry].append(state)
        else:
            self.current_id -= 1

    def predictor(self, state):
        for production in self.grammar[state.next()]:
            self.enqueue(State(state.next(), production, 0, state.end_idx, state.end_idx, self.get_new_id(), [], 'predictor'), state.end_idx)

    def scanner(self, state):
        if self.words[state.end_idx] in self.grammar[state.next()]:
            self.enqueue(State(state.next(), [self.words[state.end_idx]], 1, state.end_idx, state.end_idx + 1, self.get_new_id(), [], 'scanner'), state.end_idx + 1)

    def completer(self, state):
        for s in self.chart[state.start_idx]:
            if not s.complete() and s.next() == state.label and s.end_idx == state.start_idx and s.label != 'gamma':
                self.enqueue(State(s.label, s.rules, s.dot_idx + 1, s.start_idx, state.end_idx, self.get_new_id(), s.made_from + [state.idx], 'completer'), state.end_idx)

    def parse(self):
        self.enqueue(State('gamma', ['S'], 0, 0, 0, self.get_new_id(), [], 'dummy start state'), 0)
        
        for i in range(len(self.words) + 1):
            for state in self.chart[i]:
                if not state.complete() and not self.is_terminal(state.next()):
                    self.predictor(state)
                elif i != len(self.words) and not state.complete() and self.is_terminal(state.next()):
                    self.scanner(state)
                else:
                    self.completer(state)

    def __str__(self):
        res = ''
        
        for i, chart in enumerate(self.chart):
            res += '\nChart[%d]\n' % i
            for state in chart:
                res += str(state) + '\n'

        return res


def test(sentence):
    grammar = {
        'S':           [['NP', 'VP'], ['Aux', 'NP', 'VP'], ['VP']],
        'NP':          [['Det', 'Nominal'], ['Proper-Noun']],
        'Nominal':     [['Noun'], ['Noun', 'Nominal']],
        'VP':          [['Verb'], ['Verb', 'NP']],
        'Det':         ['that', 'this', 'a'],
        'Noun':        ['book', 'flight', 'meal', 'money'],
        'Verb':        ['book', 'called', 'prever'],
        'Aux':         ['does'],
        'Prep':        ['from', 'to', 'on'],
        'Proper-Noun': ['Chennai', 'TWA','John','Mary']
    }
    terminals = ['Det', 'Noun', 'Verb', 'Aux', 'Prep', 'Proper-Noun']
    sent=sentence.split(' ') 
    earley = Earley(sent, grammar, terminals)
    earley.parse()
    print (earley)

if __name__ == '__main__':
    test('John called Mary from Chennai')



#3

class Dictlist(dict):
    
    def __setitem__(self, key, value):
        try:
            self[key]
        except KeyError:
            super(Dictlist, self).__setitem__(key, [])
        self[key].append(value)


class production_rule(object):
    
    result = None
    p1 = None
    p2 = None
    
    #Parameters:
    #   Result: String
    #   p1: Production rule (left child of the production rule)
    #   p2: Production rule (right child of the production rule)
    def __init__(self,result,p1,p2):
        self.result = result
        self.p1 = p1
        self.p2 = p2
    
    #Returns the result of the production rule, VP, S, NP... 
    @property
    def get_type(self):
        return self.result
    
    #Returns the left child of the production rule
    @property
    def get_left(self):
        return self.p1
    
    #Returns the right child of the production rule
    @property
    def get_right(self):
        return self.p2

class Cell(object):
    productions = []
    
    
    #Parameters:
    #   Productions: List of production rules
    
    def __init__(self, productions=None):
        if productions is None:
            self.productions = []
        else:
            self.productions = productions
            
    def add_production(self, result,p1,p2):
        self.productions.append(production_rule(result,p1,p2))
    
    def set_productions(self, p):
        self.productions = p
    
    @property
    def get_types(self):
        types = []
        for p in self.productions:
            types.append(p.result)
        return types
    @property
    def get_rules(self):       
        return self.productions


class Grammar(object):
    
    grammar_rules = Dictlist()
    parse_table = None
    length = 0
    tokens = []
    number_of_trees = 0
    
    #Parameters:
    #   Filename: file containing a grammar
    
    def __init__(self, filename):
        self.grammar_rules = Dictlist()
        self.parse_table = None
        self.length = 0
        for line in open(filename):
            a, b = line.split("->")
            self.grammar_rules[b.rstrip().strip()]=a.rstrip().strip()
        
        if len(self.grammar_rules) == 0:
            raise ValueError("No rules found in the grammar file")
        print('')
        print('Grammar file readed succesfully. Rules readed:')
        self.print_rules()
        print('')
    
    #Print the production rules in the grammar
    
    def print_rules(self):
        for r in self.grammar_rules:
            for p in self.grammar_rules[r]:
                print(str(p) + ' --> ' + str(r))
        
    def apply_rules(self,t):
        try:
            return self.grammar_rules[t]
        except KeyError as r:
            return None
            
    #Parse a sentence (string) with the CYK algorithm   
    def parse(self,sentence):
        self.number_of_trees = 0
        self.tokens = sentence.split()
        self.length = len(self.tokens)
        if self.length < 1:
            raise ValueError("The sentence could no be read")
        self.parse_table = [ [Cell() for x in range(self.length - y)] for y in range(self.length) ]
        
         #Process the first line
        
        for x, t in enumerate(self.tokens):
            
            r = self.apply_rules(t)
            if r == None:
                raise ValueError("The word " + str(t) + " is not in the grammar")
            else:
                for w in r: 
                    self.parse_table[0][x].add_production(w,production_rule(t,None,None),None)
        
        
        #Run CYK-Parser
        
        
        for l in range(2,self.length+1):
            for s in range(1,self.length-l+2):
                for p in range(1,l-1+1):
                    
                    t1 = self.parse_table[p-1][s-1].get_rules
                    t2 = self.parse_table[l-p-1][s+p-1].get_rules
                            
                    for a in t1:
                        for b in t2:
                            r = self.apply_rules(str(a.get_type) + " " + str(b.get_type))
                                    
                            if r is not None:
                                for w in r:
                                    print('Applied Rule: ' + str(w) + '[' + str(l) + ',' + str(s) + ']' + ' --> ' + str(a.get_type) + '[' + str(p) + ',' + str(s) + ']' + ' ' + str(b.get_type)+ '[' + str(l-p) + ',' + str(s+p) + ']')
                                    self.parse_table[l-1][s-1].add_production(w,a,b)
                               
        self.number_of_trees = len(self.parse_table[self.length-1][0].get_types)
        if  self.number_of_trees > 0:
            print("----------------------------------------")
            print('The sentence IS accepted in the language')
            print('Number of possible trees: ' + str(self.number_of_trees))
            print("----------------------------------------")
        else:
            print("--------------------------------------------")
            print('The sentence IS NOT accepted in the language')
            print("--------------------------------------------")
        
        
    #Returns a list containing the parent of the possible trees that we can generate for the last sentence that have been parsed
    def get_trees(self):
        return self.parse_table[self.length-1][0].productions
                
                
    #@TODO
    def print_trees(self):
        pass
                      
    #Print the CYK parse trable for the last sentence that have been parsed.             
    def print_parse_table(self):
        try:
            from tabulate import tabulate
        except (ModuleNotFoundError,ImportError) as r:
            import subprocess
            import sys
            import logging
            logging.warning('To print the CYK parser table the Tabulate module is necessary, trying to install it...')
            subprocess.call([sys.executable, "-m", "pip", "install", 'tabulate'])

            try:
                from tabulate import tabulate
                logging.warning('The tabulate module has been instaled succesfuly!')

            except (ModuleNotFoundError,ImportError) as r:
                logging.warning('Unable to install the tabulate module, please run the command \'pip install tabulate\' in a command line')

        
        lines = [] 
        
        
        
        for row in reversed(self.parse_table):
            l = []
            for cell in row:
                l.append(cell.get_types)
            lines.append(l)
        
        lines.append(self.tokens)
        print('')
        print(tabulate(lines))
        print('')

example1.txt
S -> NP VP
PP -> P NP
PP -> A NP
VP -> V NP
VP -> VP PP
NP-> NP PP
NP -> Delhi
NP -> pilot
NP -> plane
NP-> telescope
NP -> stars
P -> to
A -> The
V -> flew

class CollinsSpan:

    def __init__(self, i, j, k, h, score):
        self.i = i
        self.j = j
        self.k = k
        self.h = h
        self.score = score

    def __str__(self):
        return "[%s, %s, %s, %s, %s]" % (self.i, self.j, self.k, self.h, self.score)

pos_tags = ["PR", "V", "DT", "JJ", "N"]
class CollinsParser:

    def __init__(self):
        self.chart = None

    def parse(self, words, pos_tags):
        self.words = words
        self.init_spans(words)
        self.heads = [None for i in range(len(words))]

        # merge spans in a bottom-up manner
        for l in range(1, len(words)+1):
            for i in range(0, len(words)):
                j = i + l
                if j > len(words): break
                for k in range(i+1, j):
                    for h_l in range(i, k):
                        for h_r in range(k, j):
                            span_l = self.chart[i][k][h_l]
                            span_r = self.chart[k][j][h_r]
                            # l -> r
                            score = self.get_score(words, pos_tags, span_l, span_r)
                            span = CollinsSpan(i, j, k, h_l, score)
                            self.add_span(span)
                            # r -> l
                            score = self.get_score(words, pos_tags, span_r, span_l)
                            span = CollinsSpan(i, j, k, h_r, score)
                            self.add_span(span)
        #top layer
        self.best_top_layer_span = self.find_best(0, len(words)) 
        self.backtrace(self.best_top_layer_span)

    def backtrace(self, span):
        # trace back to left
        self.trace_direction(span, 'left')
        # trace back to right
        self.trace_direction(span, 'right')

    def trace_direction(self, upper_span, direction):
        if direction == 'left':
            current_span = self.find_best(upper_span.i, upper_span.k)
        elif direction == 'right':
            current_span = self.find_best(upper_span.k, upper_span.j)

        # dicide heads
        if upper_span.h != current_span.i:
            self.heads[current_span.i] = upper_span.h
        elif upper_span.h != current_span.j - 1:
            self.heads[current_span.j - 1] = upper_span.h

        if current_span.j - current_span.i > 1:
            self.backtrace(current_span)
        else:
            pass

    def print_heads(self):
        head_words = []
        #print(self.heads)
        for i in self.heads:
            try:
                head_words.append(self.words[i])
            except TypeError:
                head_words.append(None)
        print(head_words)

    def init_spans(self, words):
        # initialize chart as 3-dimensional list
        length = len(words) + 1
        chart = []
        for i in range(length):
            chart.append([])
            for j in range(length):
                chart[i].append([None] * length)
        self.chart = chart

        # add 1-length spans to the chart
        for i in range(0, len(words)):
            span = CollinsSpan(i, i+1, i, i, 0.0)
            self.add_span(span)

    def add_span(self, new_span):
        i, j, h = new_span.i, new_span.j, new_span.h
        old_span = self.chart[i][j][h]
        if old_span is None or old_span.score < new_span.score:
            self.chart[i][j][h] = new_span # update chart

    def get_score(self, words, pos_tags, head, dep):
        # currently, use naive scoring function
  
        h_pos = pos_tags[head.h]
        d_pos = pos_tags[dep.h]
        print(h_pos,d_pos)
        if h_pos == 'V' and d_pos == 'N':
            score = 3.0
        elif h_pos == 'N' and d_pos == 'DT':
            score = 1.0
        elif h_pos == 'N' and d_pos == 'JJ':
            score = 1.0
        elif h_pos == 'V' and d_pos == 'PR':
            score = 2.0
        else:
            score = 0.1
        print(score)
        # calculate score based on arc-factored model
        return head.score + dep.score + score

    """ Find the highest-scored span [i, j, h] from [i, j] """
    def find_best(self, i, j):
        best_span = None
        for h in range(i, j):
            span = self.chart[i][j][h]
            if best_span is None or best_span.score < span.score:
                best_span = span
        return best_span

# run
p = CollinsParser()
words = ["She", "went", "to", "temple"]
print(words)
p.parse(words, pos_tags)
print(words)
print(pos_tags)



g = Grammar('example1.txt')
g.parse('The pilot flew The plane to Delhi')
g.print_parse_table()
trees = g.get_trees()
p = trees[0].get_type
l = trees[0].get_left
d = trees[0].get_right
p = trees[1].get_type
l = trees[1].get_left
d = trees[1].get_right

"""# New Section"""

#4.collins parser