from mesa import Agent
import random

class Nation(Agent):
    def __init__(self, unique_id, model, region = None):
        super().__init__(unique_id, model)

        try:
            self.region = region
        except:
            

    def random_move(self):
        '''
        This method should get the neighbouring cells (Moore's neighbourhood), select one, and move the agent to this cell.
        '''
        neighbourhood = self.model.grid.get_neighborhood(self.pos, True, False, 1)
        new_pos = random.choice(neighbourhood)
        self.model.grid.move_agent(self, new_pos)


class PeaceFullNation(Nation):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)

    def step(self):
        '''
        This method should move the Sheep using the `random_move()` method implemented earlier, then conditionally reproduce.
        '''
        # YOUR CODE HERE
        self.random_move()
        if random.random() < self.model.sheep_reproduction_chance:
            self.model.new_agent(PeaceFullNation, self.pos)

class WarringNation(Nation):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)

    def step(self):
        '''
        This method should move the Sheep using the `random_move()` method implemented earlier, then conditionally reproduce.
        '''
        # YOUR CODE HERE
        self.random_move()
        if random.random() < self.model.sheep_reproduction_chance:
            self.model.new_agent(Sheep, self.pos)

class WarringNation(Nation):
    def __init__(self, unique_id, model, pos):
        super().__init__(unique_id, model, pos)

    def step(self):
        '''
        This method should move the Sheep using the `random_move()` method implemented earlier, then conditionally reproduce.
        '''
        # YOUR CODE HERE
        self.random_move()
        if random.random() < self.model.sheep_reproduction_chance:
            self.model.new_agent(Sheep, self.pos)