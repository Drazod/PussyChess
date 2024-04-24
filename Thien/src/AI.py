from Game import Game

class AI(Game): 
    def __init__(self,engine,depth,color,boards_explored):
        __super__.__init__(engine,depth,color,boards_explored)
        self.engine = engine
        self.depth = depth
        self.color = color 
        self.boards_explored = boards_explored
        self.book = Book()
    def eval(self):
        pass
    def minimax(self, depth, maximizing_player):
        pass
    def heatmap(self):
        pass 
    def threats(self):
        pass 
    def book_move(self):
        pass 
    def get_mover(self):
        pass

class Book():
    def __init__(self):
        self.node = Node()
    def _create(self):
        pass
    def next_move(self):
        pass                    

class Node():
    def __init__(self,value,weight,prob):
        self.value = value 
        self.weight = weight
        self.prob = prob
        self.node = [Node()]
    def add_child(self):
        pass
    def add_children(self):
        pass
    def calc_prob(self):
        pass
    def get_child(sefl):
        pass 
    def choose_child(self):
        pass