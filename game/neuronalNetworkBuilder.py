import neat
import pickle

class NeuronalNetworkBuilder:
    def __init__(self, config_file, genome_file):
        self.config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

        with open(genome_file, "rb") as f:
            self.genome = pickle.load(f)

        self.net = neat.nn.FeedForwardNetwork.create(self.genome, self.config)

    def get_nn(self):
        return self.net