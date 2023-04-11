import numpy as np
import networkx as nx
import random
import pandas as pd

# CHANGE ################################
influencers = [0, 1, 2, 3, 4]
# CHANGE ################################

p = 0.01
chic_choc_path = 'chic_choc_data.csv'
cost_path = 'costs.csv'


def create_graph(edges_path: str) -> nx.Graph:
    """
    Creates the Chic Choc social network
    :param edges_path: A csv file that contains information obout "friendships" in the network
    :return: The Chic Choc social network
    """
    edges = pd.read_csv(edges_path).to_numpy()
    net = nx.Graph()
    net.add_edges_from(edges)
    return net


def change_network(net: nx.Graph) -> nx.Graph:
    """
    Gets the network at staged t and returns the network at stage t+1 (stochastic)
    :param net: The network at staged t
    :return: The network at stage t+1
    """
    edges_to_add = []
    for user1 in sorted(net.nodes):
        for user2 in sorted(net.nodes, reverse=True):
            if user1 == user2:
                break
            if (user1, user2) not in net.edges:
                neighborhood_size = len(set(net.neighbors(user1)).intersection(set(net.neighbors(user2))))
                prob = 1 - ((1 - p) ** (np.log(neighborhood_size))) if neighborhood_size > 0 else 0  # #################
                if prob >= random.uniform(0, 1):
                    edges_to_add.append((user1, user2))
    net.add_edges_from(edges_to_add)
    return net


def buy_products(net: nx.Graph, purchased: set) -> set:
    """
    Gets the network at the beginning of stage t and simulates a purchase round
    :param net: The network at stage t
    :param purchased: All the users who bought a doll up to and including stage t-1
    :return: All the users who bought a doll up to and including stage t
    """
    new_purchases = set()
    for user in net.nodes:
        neighborhood = set(net.neighbors(user))
        b = len(neighborhood.intersection(purchased))
        n = len(neighborhood)
        prob = b / n
        if prob >= random.uniform(0, 1):
            new_purchases.add(user)

    return new_purchases.union(purchased)


def get_influencers_cost(cost_path: str, influencers: list) -> int:
    """
    Returns the cost of the influencers you chose
    :param cost_path: A csv file containing the information about the costs
    :param influencers: A list of your influencers
    :return: Sum of costs
    """
    costs = pd.read_csv(cost_path)
    return sum([costs[costs['user'] == influencer]['cost'].item() if influencer in list(costs['user']) else 0 for influencer in influencers])



def optimize_influencers_selection_greedy(edges_path: str, cost_path: str, max_influencers: int):
    """
    Finds and prints the approximate optimal selection of influencers using a Greedy Algorithm
    :param edges_path: A csv file that contains information about "friendships" in the network
    :param cost_path: A csv file containing the information about the costs
    :param max_influencers: The maximum number of influencers to consider in a combination
    :return: None
    """
    chic_choc_network = create_graph(edges_path)
    costs = pd.read_csv(cost_path)
    all_influencers = list(costs['user'])

    selected_influencers = set()
    best_score = -float('inf')
    total_influencers_cost = 0

    for _ in range(max_influencers):
        best_improvement = -float('inf')
        best_influencer = None

        for influencer in all_influencers:
            if influencer in selected_influencers:
                continue

            influencers_cost = get_influencers_cost(cost_path, selected_influencers | {influencer})
            purchased = set(selected_influencers | {influencer})

            for i in range(6):
                chic_choc_network = change_network(chic_choc_network)
                purchased = buy_products(chic_choc_network, purchased)

            score = len(purchased) - influencers_cost

            improvement = score - best_score

            if improvement > best_improvement:
                best_improvement = improvement
                best_influencer = influencer

        if best_improvement <= 0:
            break

        selected_influencers.add(best_influencer)
        best_score += best_improvement
        total_influencers_cost += get_influencers_cost(cost_path, {best_influencer})

    print("*************** The approximate optimal selection of influencers using a Greedy Algorithm is",
          selected_influencers, "with a score of", best_score, "***************")

# Example usage


if __name__ == '__main__':

    print("STARTING")

    chic_choc_network = create_graph(chic_choc_path)
    influencers_cost = get_influencers_cost(cost_path, influencers)
    purchased = set(influencers)

    for i in range(6):
        chic_choc_network = change_network(chic_choc_network)
        purchased = buy_products(chic_choc_network, purchased)
        print("finished round", i + 1)

    score = len(purchased) - influencers_cost

    print("*************** Your final score is " + str(score) + " ***************")
    optimize_influencers_selection_greedy('chic_choc_data.csv', 'costs.csv', 3)


