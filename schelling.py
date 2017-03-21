import numpy as np
import random
import matplotlib.pylab as plt
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# create a file handler
handler = logging.FileHandler('schelling.log')
handler.setLevel(logging.DEBUG)

# create a logging format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# add the handlers to the logger
logger.addHandler(handler)


class Schelling:
    def __init__(self, height, width, empty_percentage, pop_percentage, sim_thresold, iterations):
        self.height = height
        self.width = width
        self.empty_percentage = empty_percentage
        self.pop_percentage = np.array(pop_percentage)
        processed_thresold = list()
        for val in sim_thresold:
            processed_thresold.append(float(val))
        self.sim_thresold = processed_thresold
        self.iterations = iterations
        self.agent_matrix = np.zeros((self.iterations, self.height, self.width))

    def generate_grid(self):
        filled_cells = self.width * self.height - self.width * self.height * self.empty_percentage
        populated_cells = self.pop_percentage * filled_cells
        print populated_cells
        print self.sim_thresold
        self.agents = np.zeros((1, self.height * self.width - round(sum(populated_cells))))
        for index, value in enumerate(populated_cells):
            self.agents = np.append(self.agents, np.ones((1, value), dtype=np.int16) * (index + 1))
        if self.agents.size != self.height * self.width:
            self.agents = np.append(self.agents, np.zeros((1, self.height * self.width - self.agents.size)))
        print self.agents.size
        self.agents = self.agents.reshape(self.height, self.width)
        np.random.shuffle(self.agents.flat)
        return self.agents

    def get_neighbour_races(self, x, y):
        races = list()
        x = int(x)
        y = int(y)
        if x > 0:
            races.append(self.agents[x - 1, y])
            if y > 0:
                races.append(self.agents[x - 1, y - 1])
            if y < self.height - 1:
                races.append(self.agents[x - 1, y + 1])

        if x < self.width - 1:
            races.append(self.agents[x + 1, y])
            if y > 0:
                races.append(self.agents[x + 1, y - 1])
            if y < self.height - 1:
                races.append(self.agents[x + 1, y + 1])

        if y < self.height - 1:
            races.append(self.agents[x, y + 1])

        if self.height - 1 > y > 0:
            races.append(self.agents[x, y - 1])

        return races

    def is_similar(self, x, y):
        self.counter = 0
        current_agent = self.agents[x, y]
        logger.debug('')
        logger.debug('Current agent = %s' % str(current_agent))
        count_similar = count_different = 0
        neighbour_races = self.get_neighbour_races(x, y)
        logger.debug('Neighbour races = ' + str(neighbour_races))
        for neighbour_race in neighbour_races:
            if current_agent == neighbour_race:
                count_similar += 1
            else:
                count_different += 1
        logger.debug('count_similar = %d, count_different = %d' % (count_similar, count_different))
        logger.debug('types = ' + str(type(count_similar)) + str(type(count_different)))
        percentage_similarity = float(count_similar) / float(count_similar + count_different)
        logger.debug('percentage_similarity = %s' % str(percentage_similarity))
        if count_different + count_similar == 0:
            logger.debug('count_similar and different are zero. agent is lonely.')
            return False
        elif current_agent == 1:
            logger.debug('Agent: 1. Value = %s' % str(percentage_similarity < self.sim_thresold[0]))
            return percentage_similarity < self.sim_thresold[0]
        elif current_agent == 2:
            logger.debug('Agent: 2. Value = %s' % str(percentage_similarity < self.sim_thresold[1]))
            return percentage_similarity < self.sim_thresold[1]
        elif current_agent == 3:
            logger.debug('Agent: 3. Value = %s' % str(percentage_similarity < self.sim_thresold[2]))
            return percentage_similarity < self.sim_thresold[2]

    def process_grid(self):
        self.agent_matrix[0] = self.agents
        for i in xrange(1, self.iterations - 1):
            changes = 0
            for x in xrange(0, self.height - 1):
                for y in xrange(0, self.width - 1):
                    if self.agents[x, y] == 0:
                        # logger.info('current_agent is zero')
                        continue
                    if self.is_similar(x, y):
                        # logger.info('similarity found')
                        selected_lot = random.sample(np.argwhere(self.agents == 0), 1)[0]
                        self.agents[selected_lot[0], selected_lot[1]] = self.agents[x, y]
                        self.agents[x, y] = 0
                        changes += 1
            self.agent_matrix[i] = self.agents
            if changes == 0:
                print 'System Stabilized'
                logger.info('System Stabilized')
                break
                # print self.agent_matrix[-1]

    def plot(self, title, file_name):
        fig, ax = plt.subplots()
        agent_colors = {0: 'w', 1: 'r', 2: 'g', 3: 'c'}

        for i in xrange(0, self.height - 1):
            for j in xrange(0, self.width - 1):
                ax.scatter(i + 0.5, j + 0.5, color=agent_colors[int(self.agents[i, j])])

        ax.set_title(title, fontsize=10, fontweight='bold')
        ax.set_xlim([0, self.width])
        ax.set_ylim([0, self.height])
        ax.set_xticks([])
        ax.set_yticks([])

        plt.savefig(file_name)


# Q1.a: k = 1/8, 40, 40, 0.15, [0.5, 0.5], [0.125, 0.125], 2000
sch = Schelling(40, 40, 0.15, [0.5, 0.5], [0.125, 0.125], 2000)
logger.info(sch.generate_grid())
sch.plot('Initial Grid - 40, 40, 0.15, [0.5, 0.5], [0.125, 0.125], 2000', 'initial_grid_test1.png')
sch.process_grid()
sch.plot('Final Grid - 40, 40, 0.15, [0.5, 0.5], [0.125, 0.125], 2000', 'test1.png')

# Q1.b: k = 2/8, 40, 40, 0.15, [0.5, 0.5], [0.25, 0.25], 2000
sch = Schelling(40, 40, 0.15, [0.5, 0.5], [0.25, 0.25], 2000)
logger.info(sch.generate_grid())
sch.plot('Initial Grid - 40, 40, 0.15, [0.5, 0.5], [0.25, 0.25], 2000', 'initial_grid_test2.png')
sch.process_grid()
sch.plot('Final Grid - 40, 40, 0.15, [0.5, 0.5], [0.25, 0.25], 2000', 'test2.png')

# Q1.c: k = 3/8, 40, 40, 0.15, [0.5, 0.5], [0.375, 0.375], 2000
sch = Schelling(40, 40, 0.15, [0.5, 0.5], [0.375, 0.375], 2000)
logger.info(sch.generate_grid())
sch.plot('Initial Grid - 40, 40, 0.15, [0.5, 0.5], [0.375, 0.375], 2000', 'initial_grid_test3.png')
sch.process_grid()
sch.plot('Final Grid - 40, 40, 0.15, [0.5, 0.5], [0.375, 0.375], 2000', 'test3.png')

# Q1.d: k = 4/8, 40, 40, 0.15, [0.5, 0.5], [0.5, 0.5], 2000
sch = Schelling(40, 40, 0.15, [0.5, 0.5], [0.5, 0.5], 2000)
logger.info(sch.generate_grid())
sch.plot('Initial Grid - 40, 40, 0.15, [0.5, 0.5], [0.5, 0.5], 2000', 'initial_grid_test4.png')
sch.process_grid()
sch.plot('Final Grid - 40, 40, 0.15, [0.5, 0.5], [0.5, 0.5], 2000', 'test4.png')

# Q1.e: k = 5/8, 40, 40, 0.15, [0.5, 0.5], [0.625, 0.625], 2000
sch = Schelling(40, 40, 0.15, [0.5, 0.5], [0.625, 0.625], 2000)
logger.info(sch.generate_grid())
sch.plot('Initial Grid - 40, 40, 0.15, [0.5, 0.5], [0.625, 0.625], 2000', 'initial_grid_test5.png')
sch.process_grid()
sch.plot('Final Grid - 40, 40, 0.15, [0.5, 0.5], [0.625, 0.625], 2000', 'test5.png')

# Q2. k=3/8,5/8: 40, 40, 0.15, [0.5, 0.5], [0.375, 0.625], 2000
sch = Schelling(40, 40, 0.15, [0.5, 0.5], [0.375, 0.625], 2000)
logger.info(sch.generate_grid())
sch.plot('Initial Grid - 40, 40, 0.15, [0.5, 0.5], [0.375, 0.625], 2000', 'initial_grid_test6.png')
sch.process_grid()
sch.plot('Final Grid - 40, 40, 0.15, [0.5, 0.5], [0.375, 0.625], 2000', 'test6.png')

# Q3.a: 45% of a & b + 10% c and k=1/8
# 40, 40, 0.15, [0.45, 0.45, 0.10], [0.375, 0.375, 0.375], 2000
sch = Schelling(40, 40, 0.15, [0.45, 0.45, 0.10], [0.375, 0.375, 0.375], 2000)
logger.info(sch.generate_grid())
sch.plot('Initial Grid - 40, 40, 0.15, [0.45, 0.45, 0.10], [0.375, 0.375, 0.375], 2000', 'initial_grid_test7.png')
sch.process_grid()
sch.plot('Final Grid - 40, 40, 0.15, [0.45, 0.45, 0.10], [0.375, 0.375, 0.375], 2000', 'test7.png')

# Q3.b: 45% of a & b + 10% c and k=5/8, 5/8, 3/8
# 40, 40, 0.15, [0.45, 0.45, 0.10], [0.625, 0.625, 0.375], 2000
sch = Schelling(40, 40, 0.15, [0.45, 0.45, 0.10], [0.625, 0.625, 0.375], 2000)
logger.info(sch.generate_grid())
sch.plot('Initial Grid - 40, 40, 0.15, [0.45, 0.45, 0.10], [0.625, 0.625, 0.375], 2000', 'initial_grid_test8.png')
sch.process_grid()
sch.plot('Final Grid - 40, 40, 0.15, [0.45, 0.45, 0.10], [0.625, 0.625, 0.375], 2000', 'test8.png')

# Q3.c: 45% of a & b + 10% c and k=3/8, 3/8, 5/8
# 40, 40, 0.15, [0.45, 0.45, 0.10], [0.375, 0.375, 0.625], 2000
sch = Schelling(40, 40, 0.15, [0.45, 0.45, 0.10], [0.375, 0.375, 0.625], 2000)
logger.info(sch.generate_grid())
sch.plot('Initial Grid - 40, 40, 0.15, [0.45, 0.45, 0.10], [0.375, 0.375, 0.625], 2000', 'initial_grid_test9.png')
sch.process_grid()
sch.plot('Final Grid - 40, 40, 0.15, [0.45, 0.45, 0.10], [0.375, 0.375, 0.625], 2000', 'test9.png')
