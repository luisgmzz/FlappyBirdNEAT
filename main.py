import os
import sys
import pickle

from game.game import Game
from game.neatGame import run_neat
import neat
from game.neuronalNetworkBuilder import NeuronalNetworkBuilder


def run(config_file):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction,
                         neat.DefaultSpeciesSet, neat.DefaultStagnation,
                         config_file)

    # Create the population, which is the top-level object for a NEAT run.
    p = neat.Population(config)

    # Add a stdout reporter to show progress in the terminal.
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    #p.add_reporter(neat.Checkpointer(5))

    # Run for up to 50 generations.
    winner = p.run(run_neat, 50)
    # show final stats
    print("\nBest genome:\n{!s}".format(winner))

    with open("neat/best_genome.pkl", "wb") as f:
        pickle.dump(winner, f)

def neat_runner():
    # Determine path to configuration file. This path manipulation is
    # here so that the script will run successfully regardless of the
    # current working directory.
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat/neat_config.txt")
    run(config_path)

def game_runner():
    game_instance = Game()
    game_instance.run()
    quit()

def ai_runner():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "neat/neat_config.txt")
    genome_path = os.path.join(local_dir, "neat/best_genome.pkl")

    nnb = NeuronalNetworkBuilder(config_path, genome_path)

    game_instance = Game(nnb.get_nn())
    game_instance.run()
    quit()

def main():
    if len(sys.argv) < 2:
        print("Introduce un argumento")
        return
    option = int(sys.argv[1])

    if option == 1:
        game_runner()
    elif option == 2:
        neat_runner()
    elif option == 3:
        ai_runner()
    else:
        print("El argumento debe ser 1 (para jugar) o 2 (para correr NEAT)")

if __name__ == "__main__":
    main()