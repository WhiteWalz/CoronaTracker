
# coding: utf-8
import heapq
from datetime import date, timedelta
# In[2]:


testDNA1 = 'ACCAGTATGG'
testDNA2 = 'ACGATGG'


# In[ ]:


import enum

class Types(enum.Enum):
    one_to_one = 0
    match = -5
    mismatch = 2
    gap_open = 10
    gap_extension = 2
    root = 0


# In[7]:


class Node:

    def __init__(self, string_i, string_y, index_i, index_y, parent_present_score, typ=Types.one_to_one):
        self.string_i = string_i
        self.string_y = string_y
        self.index_i = index_i
        self.index_y = index_y
        self.children = []
        if typ == Types.one_to_one:
            self.typ = self.determineMatch()
        else:
            self.typ = typ
        self.present_score = parent_present_score + self.typ.value
        self.future_scores = self.calculateFutureScores()
        self.fitness_scores = self.calculateFitnessScores()
            
    def determineMatch(self):
        if self.string_i[self.index_i] == self.string_y[self.index_y]:
            return Types.match
        else:
            return Types.mismatch
        
    def calculateFutureScores(self):
        x = len(self.string_i) - self.index_i
        y = len(self.string_y) - self.index_y
        
        if y < x:
            fut_min = (y*Types.mismatch.value) + ((Types.gap_open.value  + Types.gap_extension.value) * (x - y))
            fut_max = (y*Types.match.value) + ((Types.gap_open.value + Types.gap_extension.value) * (x - y))
        else:
            fut_min = (x*Types.mismatch.value) + ((Types.gap_open.value + Types.gap_extension.value) * (y - x))
            fut_max = (x*Types.match.value) + ((Types.gap_open.value + Types.gap_extension.value) * (y - x))
        
        return (fut_min, fut_max)

    def generateChildren(self):
        if not self.children:
            if len(self.string_i) - (self.index_i + 1):
                if self.typ in [Types.gap_extension, Types.gap_open]:
                    self.children.append(Node(string_i=self.string_i, string_y=self.string_y,
                    index_i=self.index_i+1, index_y=self.index_y, parent_present_score=self.present_score,
                    typ=Types.gap_extension))
                else: self.children.append(Node(string_i=self.string_i, string_y=self.string_y,
                    index_i=self.index_i+1, index_y=self.index_y, parent_present_score=self.present_score,
                    typ=Types.gap_open))
            if len(self.string_y) - (self.index_y + 1):
                if self.typ in [Types.gap_extension, Types.gap_open]:
                    self.children.append(Node(string_i=self.string_i, string_y=self.string_y,
                    index_i=self.index_i, index_y=self.index_y+1, parent_present_score=self.present_score,
                    typ=Types.gap_extension))
                else: self.children.append(Node(string_i=self.string_i, string_y=self.string_y,
                    index_i=self.index_i, index_y=self.index_y+1, parent_present_score=self.present_score,
                    typ=Types.gap_open))
            if not (len(self.string_i) == self.index_i + 1 and len(self.string_y) == self.index_y + 1):
                self.children.append(Node(string_i=self.string_i, string_y=self.string_y,
                index_i=self.index_i+1, index_y=self.index_y+1, parent_present_score=self.present_score))

    def getChildren(self):
        if not self.children:
            self.generateChildren()
        return self.children
    
    def __eq__(self, other):
        return self.fitness_scores[1] == other.fitness_scores[1]
    def __ne__(self, other):
        return not (self == other)
    def __lt__(self, other):
        return self.fitness_scores[1] < other.fitness_scores[1]
    def __gt__(self, other):
        return self.fitness_scores[1] > other.fitness_scores[1]
    def __le__(self, other):
        return self.fitness_scores[1] <= other.fitness_scores[1]
    def __ge__(self, other):
        return self.fitness_scores[1] >= other.fitness_scores[1]
    
    def calculateFitnessScores(self):
        return (self.present_score + self.future_scores[0], self.present_score + self.future_scores[1])


# In[11]:


class Sequence:
    def __init__(self, seq_id, location):
        self.seq_id = seq_id
        self.location = location
        # self.date = date
    '''
    def __eq__(self, other):
        return self.date == other.date
    def __ne__(self, other):
        return not self.date == other.date
    def __lt__(self, other):
        return self.date < other.date
    def __gt__(self, other):
        return self.date > other.date
    def __ge__(self, other):
        return self.date >= other.date
    def __le__(self, other):
        return self.date <= other.date
    '''

# In[14]:


class Spread:
    def __init__(self, start_seq, end_seq, strength=1):
        self.start_id = start_seq.seq_id
        self.end_id = end_seq.seq_id
        self.start_loc = start_seq.location
        self.end_loc = end_seq.location
        self.strength = strength

    def __str__(self):
        return str(self.start_id) + " infected " + str(self.end_id)

# In[ ]:


class Edge:
    def __init__(self, start_loc, end_loc, strength=0):
        self.start_loc = start_loc
        self.end_loc = end_loc
        self.strength = strength
        self.spreads = []
        
    def addSpread(self, spread):
        self.spreads.append(spread)
        self.strength += spread.strength


# In[1]:


class Location:
    def __init__(self, location):
        self.location = location
        self.edges = []
        
    def addSpread(self, case_id, end_location, strength=1):
        edge = (case_id, end_location, strength)
        self.edges.append(edge)


# In[6]:

'''
import heapq
heap = []
data = [1,2,3,4,5,6,7,8,9,0]

for item in data:
    heapq.heappush(heap, item)
while heap:
    print(heapq.heappop(heap))
'''

# In[ ]:


class ComparisonUtility():

    @staticmethod
    def getStopDate(date_str, days=30):
        date_str_arr = date_str.split("-")
        if len(date_str_arr) == 1:
            date_str_arr.append('01')
        if len(date_str_arr) == 2:
            date_str_arr.append('01')
        dat = date(year=int(date_str_arr[0]), month=int(date_str_arr[1]), day=int(date_str_arr[2]))
        td = timedelta(days=days)
        stop_date = dat - td
        return str(stop_date)

    @staticmethod
    def compareSequences(string1, string2):
        expand = Node(string_i=string1, string_y=string2, parent_present_score=0, index_i=-1, index_y=-1, typ=Types.root)
        current_best = 10000
        alternatives = []
        heapq.heapify(alternatives)
        for child in expand.getChildren():
            heapq.heappush(alternatives, child)
        while alternatives[0].fitness_scores[1] <= current_best:
            expand = heapq.heappop(alternatives)
            while expand.getChildren():
                for child in expand.getChildren():
                    heapq.heappush(alternatives, child)
                expand = heapq.heappop(alternatives)
            if expand.present_score < current_best:
                current_best = expand.present_score
        return -1 * current_best
        