from itertools import combinations
import numpy as np
import networkx as nx
import random
import pandas as pd

from simulation import create_graph, get_influencers_cost, change_network, buy_products


def optimize_influencers_selection(edges_path: str, cost_path: str, max_influencers: int):
    """
    Finds and prints the optimal selection of influencers to maximize the score
    :param edges_path: A csv file that contains information about "friendships" in the network
    :param cost_path: A csv file containing the information about the costs
    :param max_influencers: The maximum number of influencers to consider in a combination
    :return: None
    """
    chic_choc_network = create_graph(edges_path)
    costs = pd.read_csv(cost_path)
    all_users = list(chic_choc_network.nodes)
    all_influencers = list(costs['user'])

    best_score = -float('inf')
    best_influencers = []

    for num_influencers in range(1, max_influencers + 1):
        for influencers in combinations(all_influencers, num_influencers):
            influencers_cost = get_influencers_cost(cost_path, influencers)
            purchased = set(influencers)

            for i in range(6):
                chic_choc_network = change_network(chic_choc_network)
                purchased = buy_products(chic_choc_network, purchased)

            score = len(purchased) - influencers_cost

            if score > best_score:
                best_score = score
                best_influencers = influencers

    print("*************** The optimal selection of influencers is", best_influencers, "with a score of", best_score, "***************")

# Example usage
optimize_influencers_selection('chic_choc_data.csv', 'costs.csv', 3)
