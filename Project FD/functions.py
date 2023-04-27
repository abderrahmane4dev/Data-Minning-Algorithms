import pandas as pd
import numpy as np
from itertools import combinations
import time
import collections
from collections import defaultdict
from collections import Counter, defaultdict
from itertools import combinations
import time



def support(itemset, dataset):
    """
    Calculate the support value of an itemset in a dataset
    """
    count = 0
    for transaction in dataset:
        if itemset.issubset(transaction):
            count += 1
    return count / len(dataset)



def generate_frequent_itemsets(transactions, min_support):
    
    # Count the occurrence of each item in the transactions
    # in other hand , we are regrouping the unique items in the transactions
    item_counts = {}

    for transaction in transactions:
        for item in transaction:
            if item in item_counts:
                item_counts[item] += 1
            else:
                item_counts[item] = 1
                
    frequent_itemsets_1 = [frozenset({item}) for item, count in item_counts.items()
                            if count / len(transactions) >= min_support]
    

    # Generate frequent k-itemsets, k >= 2
    k = 2
    frequent_itemsets = frequent_itemsets_1
    while True:
        # Generate candidate itemsets of size k
        candidate_itemsets = set()
        for itemset in combinations(frequent_itemsets, 2):
            intersection = set(itemset[0]).intersection(itemset[1])
            if len(intersection) == k - 2:
                candidate_itemsets.add(frozenset(itemset[0]).union(itemset[1]))

        # Count the support of each candidate itemset
        itemset_counts = {itemset: 0 for itemset in candidate_itemsets}
        for transaction in transactions:
            for itemset in candidate_itemsets:
                if itemset.issubset(transaction):
                    itemset_counts[itemset] += 1

        # Filter out infrequent itemsets
        frequent_itemsets_k = [set(itemset) for itemset, count in itemset_counts.items()
                            if count / len(transactions) >= min_support]

        # Exit if no frequent itemsets of size k were found
        if not frequent_itemsets_k:
            break

        # Add the frequent k-itemsets to the list of frequent itemsets
        frequent_itemsets.extend(frequent_itemsets_k)

        # Increment k
        k += 1

    # Display the frequent itemsets by size
    print("Frequent dzd 1-itemsets:")
    print(frequent_itemsets_1)
    for itemset in frequent_itemsets_1:
        print(itemset)
    print('fin')

    for i in range(2, k):
        print("Frequent", i, "-itemsets:")
        for itemset in frequent_itemsets:
            if len(itemset) == i:
                print(itemset)
        print()

    return frequent_itemsets


def generate_association_rules(frequent_itemsets, min_confidence,dataset):
    # Generate association rules from frequent itemsets
    association_rules = []
    for itemset in frequent_itemsets:
        if len(itemset) >= 2:
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    consequent = itemset.difference(antecedent)
                    antecedent = frozenset(antecedent)
                    consequent = frozenset(consequent)
                    if support(consequent,dataset) >0 and support(antecedent,dataset)>0 : 
                       confidence = support(itemset,dataset) / support(antecedent,dataset)
                    
                       lift = confidence / support(consequent,dataset)
                       if confidence >= min_confidence:
                          association_rules.append((antecedent, consequent, confidence, lift))

    # Display the generated association rules
    print("Association rules with confidence >= ", min_confidence, ":")
    for rule in association_rules:
        print(set(rule[0]), "=>",set(rule[1]), "confidence:", rule[2]*100, "lift:", rule[3])

    # Return the generated association rules
    return association_rules




def Apriori_classique(transactions, min_support, min_confidence):
    start_time = time.time()
    # Step 1: Generate frequent itemsets
    freq_itemsets = generate_frequent_itemsets(transactions, min_support)

        # Step 2: Generate association rules and evaluate the strength of the association between two items in a dataset
    association_rules = generate_association_rules(freq_itemsets, min_confidence, transactions)

    end_time = time.time()
    total_time = end_time - start_time
    print("Time taken:", total_time)
    return freq_itemsets, association_rules






def generate_frequent_itemsets_reduction(transactions, min_support, min_item_occurrence):
    
    # Count the occurrence of each item in the transactions
    # in other hand , we are regrouping the unique items in the transactions
    item_counts = {}

    for transaction in transactions:
        for item in transaction:
            if item in item_counts:
                item_counts[item] += 1
            else:
                item_counts[item] = 1
    
    # Filter out infrequent items
    frequent_items = {item for item, count in item_counts.items()
                      if count >= min_item_occurrence}
    transactions = [{item for item in transaction if item in frequent_items}
                    for transaction in transactions]
    
    frequent_itemsets_1 = [frozenset({item}) for item in frequent_items
                            if item_counts[item] / len(transactions) >= min_support]
    
    # Generate frequent k-itemsets, k >= 2
    k = 2
    frequent_itemsets = frequent_itemsets_1
    while True:
        # Generate candidate itemsets of size k
        candidate_itemsets = set()
        for itemset in combinations(frequent_itemsets, 2):
            intersection = set(itemset[0]).intersection(itemset[1])
            if len(intersection) == k - 2:
                candidate_itemsets.add(frozenset(itemset[0]).union(itemset[1]))

        # Count the support of each candidate itemset
        itemset_counts = {itemset: 0 for itemset in candidate_itemsets}
        for transaction in transactions:
            for itemset in candidate_itemsets:
                if itemset.issubset(transaction):
                    itemset_counts[itemset] += 1

        # Filter out infrequent itemsets
        frequent_itemsets_k = [set(itemset) for itemset, count in itemset_counts.items()
                            if count / len(transactions) >= min_support]

        # Exit if no frequent itemsets of size k were found
        if not frequent_itemsets_k:
            break

        # Add the frequent k-itemsets to the list of frequent itemsets
        frequent_itemsets.extend(frequent_itemsets_k)

        # Increment k
        k += 1

    # Display the frequent itemsets by size
    print("Frequent 1-itemsets:")
    for itemset in frequent_itemsets_1:
        print(itemset)
    print()

    for i in range(2, k):
        print("Frequent", i, "-itemsets:")
        for itemset in frequent_itemsets:
            if len(itemset) == i:
                print(itemset)
        print()

    return frequent_itemsets



def apriori_reduce_transactions(transactions, min_support, min_confidence):
    start_time = time.time()
    # Step 1: Generate frequent itemsets
    freq_itemsets = generate_frequent_itemsets_reduction(transactions, min_support,2)

        # Step 2: Generate association rules and evaluate the strength of the association between two items in a dataset
    association_rules = generate_association_rules(freq_itemsets, min_confidence, transactions)

    end_time = time.time()
    total_time = end_time - start_time
    print("Time taken:", total_time)
    return freq_itemsets, association_rules

"""""
def apriori_reduce_transactions(data, minsup):
    # Phase 1: Find frequent single items and support
    singletons = {}
    for transaction in data:
        for item in transaction:
            if item in singletons:
                singletons[item] += 1
            else:
                singletons[item] = 1

    nb_elements = sum(len(transaction) for transaction in data)

    for key in singletons:
        singletons[key] = singletons[key] / nb_elements
    
    # Filter infrequent singletons and calculate support
    freq_items = {frozenset([item]): supp for item, supp in singletons.items() if supp >= minsup}
    
    # Phase 2: Generate candidate itemsets of size k
    k = 2
   
    while freq_items:
        # Generate candidate itemsets of size k
        candidates = set()
        for itemset1 in freq_items.keys():
            for itemset2 in freq_items.keys():
                if len(itemset1.union(itemset2)) == k:
                    candidate = itemset1.union(itemset2)
                    if candidate not in candidates:
                        candidates.add(candidate)

        # Count supports of candidate itemsets
        item_counts = {itemset: 0 for itemset in candidates}
        for transaction in data:
            for candidate in candidates:
                if candidate.issubset(set(transaction)):
                    item_counts[candidate] += 1
       
        # Reduce transactions
        reduced_data = []
        for transaction in data:
            reduced_transaction = set()
            for item in transaction:
                if frozenset([item]) in freq_items:
                    reduced_transaction.add(item)
            if len(reduced_transaction) > 0:
                reduced_data.append(list(reduced_transaction))
        
        #le support
        nb_elements_reduced = sum(len(transaction) for transaction in reduced_data)
        for key in item_counts:
            if(nb_elements_reduced)>0:
               item_counts[key] = item_counts[key] / nb_elements_reduced
        
        # Filter infrequent itemsets and calculate support
        #freq_items = {itemset: supp for itemset, supp in item_counts.items() if supp >= minsup}

        k += 1
        
    # Generate association rules from frequent itemsets
    rules = []
    print(rules)
    for itemset in freq_items.keys():
        if len(itemset) > 1:
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = frozenset(antecedent)
                    consequent = itemset.difference(antecedent)
                    if(freq_items[antecedent])>0 and  (freq_items[antecedent] * freq_items[consequent]) >0 : 
                       conf = freq_items[itemset] / freq_items[antecedent]
                       lift = freq_items[itemset] / (freq_items[antecedent] * freq_items[consequent])
                       rule = (antecedent, consequent, conf, lift)
                       rules.append(rule)
  
    # Return frequent itemsets and association rules
    return freq_items, rules


"""
















def apriori_Close(data, minsup, lift_choix):
    # Phase 1: Find frequent single items and support
    singletons = {}
    for transaction in data:
        for item in transaction:
            if item in singletons:
                singletons[item] += 1
            else:
                singletons[item] = 1

    nb_elements = len(data)

    for key in singletons:
       singletons[key] = singletons[key] / nb_elements  

    # Filter infrequent singletons and calculate support
    freq_items = {frozenset([item]): supp for item, supp in singletons.items() if supp >= minsup}
    closed_items = freq_items.copy()
  
    # Phase 2: Generate candidate itemsets of size k
    k = 2
    while freq_items:
        # Generate candidate itemsets of size k
        candidates = set()
        for itemset1 in freq_items.keys():
            for itemset2 in freq_items.keys():
                if len(itemset1.union(itemset2)) == k:
                    candidate = itemset1.union(itemset2)
                    if candidate not in candidates:
                        candidates.add(candidate)

        # Count supports of candidate itemsets
        item_counts = {itemset: 0 for itemset in candidates}
        for transaction in data:
            for candidate in candidates:
                if candidate.issubset(set(transaction)):
                    item_counts[candidate] += 1

        # Filter infrequent itemsets and calculate support
        freq_items = {itemset: supp for itemset, supp in item_counts.items() if supp >= minsup}

        # Check if itemset is closed
        for itemset in freq_items:
            is_closed = True
          
            for itemset2, supp2 in closed_items.items():
                if itemset.issubset(itemset2) and freq_items[itemset] == supp2:
                    is_closed = False
                    
            if is_closed:
                closed_items[itemset] = freq_items[itemset]

        k += 1
    
    # Generate association rules from frequent itemsets
    rules = []
    for itemset in closed_items.keys():
        if len(itemset) > 1:
            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = frozenset(antecedent)
                    consequent = itemset.difference(antecedent)
                    # Check if antecedent is closed
                    if antecedent in closed_items:
                        lift = closed_items[itemset] / (closed_items[antecedent] * closed_items[consequent])
                        conf = closed_items[itemset] / closed_items[antecedent]
                        if lift_choix == "1" and lift > 1:
                            rule = (antecedent, consequent, conf, lift)
                            rules.append(rule)
                        elif lift_choix == "2" and lift < 1:
                            rule = (antecedent, consequent, conf, lift) 
                            rules.append(rule)
                        elif lift_choix == "3" and conf == 1:
                            rule = (antecedent, consequent, conf, lift) 
                            rules.append(rule)  
    return closed_items, rules