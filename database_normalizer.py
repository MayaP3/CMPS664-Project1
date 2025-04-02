import pandas as pd
import itertools


# Import csv
def display_data(csv_path):
    csv_path = csv_path.replace('"', "").replace("\\", "/")
    data = pd.read_csv(csv_path)
    df = pd.DataFrame(data)

    print(df.head)
    print(df.dtypes)


# Functional Dependency Identifcation
def database_fds(functional_dependencies: list):

    relation = set()
    determinants = []
    dependents = []

    FD_list = []

    for i in range(len(functional_dependencies)):
        left, right = functional_dependencies[i].split('->')
        determinants.append(left)
        dependents.append(right)
        FD_list.append((left, right))
        relation.update(list({left}))
        relation.update(list({right}))

    print("Relation: ", relation)
    print("")
    print("Deteminants: ", determinants)
    print("")
    print("Dependents: ", dependents)
    print("")
    print("Functional Dependencies: ", FD_list)

    return relation, determinants, dependents, FD_list


def attribute_combos(determinants: list, dependents: list):

    combined_list = list(set(determinants + dependents))

    combinations = []

    for r in range(1, len(combined_list) + 1):
        for combo in itertools.combinations(combined_list, r):
            combinations.append('/'.join(combo))

    return combinations


def compute_closure(FD_list: list):
    closure_dict = {}
    determinants = []
    dependents = []
    for determinant, dependent in FD_list:
        determinants.append(determinant)
        dependents.append(dependent)

    for determinant, dependent in FD_list:
        if determinant not in closure_dict.keys():
            closure_dict[determinant] = {determinant}
            closure_dict[determinant].update({dependent})

    if dependent not in closure_dict.keys():
        closure_dict[dependent] = {dependent}

    if determinant in closure_dict.keys():
        closure_dict[determinant].update({dependent})

    for determinant in closure_dict.keys():
        for key, value in closure_dict.items():
            if determinant in value:
                closure_dict[key].update(closure_dict[determinant])

    attribute_combos_results = attribute_combos(determinants, dependents)

    for attr_combo in attribute_combos_results:
        if attr_combo not in closure_dict.keys():
            closure_dict[attr_combo] = set()
            attrs = [attrs for attrs in attr_combo.split('/')]
            for attr in attrs:
                closure_dict[attr_combo].update(closure_dict[attr])

    print("")
    print("Closure Dict: ", closure_dict)

    return closure_dict


def find_partial_dependencies(primary_keys: list, closure_dict: dict) -> list:
    possible_partial_dependencies = []

    if len(primary_keys) > 1:
        for i in primary_keys:
            for j in primary_keys:
                if closure_dict[i] != closure_dict[j]:
                    for dependency in closure_dict[i]:
                        if (dependency not in closure_dict[j]) & (i != dependency):
                            possible_partial_dependencies.append((i, dependency))

    print("")
    print("With primary keys: ", primary_keys)
    print("Possible Partial Dependencies: ", possible_partial_dependencies)
    if len(possible_partial_dependencies) > 0:
        satisfies_2nf = False
    else:
        satisfies_2nf = True
    return satisfies_2nf, possible_partial_dependencies


def find_transitive_dependencies(closure_dict: dict, determinants: list, FD_list: list):
    transitive_dependencies = []

    for key, closure_set in closure_dict.items():
        for attribute in closure_set:
            if (attribute in determinants) & (attribute != key):
                for determinant, dependent in FD_list:
                    if determinant == attribute:
                        transitive_dependencies.append((key, dependent))

    print("")
    print("Possible Transitive Dependencies: ", transitive_dependencies)

    if len(transitive_dependencies) > 0:
        satisfies_3nf = False
    else:
        satisfies_3nf = True

    return satisfies_3nf, transitive_dependencies


def suggest_candidate_key(relation: set, closure_dict: dict):
    superkeys = {}
    candidate_keys = {}

    # If closure as all the attributes, the attribute is a superkey
    for attribute, closure in closure_dict.items():
        if len(closure) == len(relation):
            superkeys[attribute] = closure

    # If no subset of the superkey is superkey, the attribute is a candidate key
    for superkey, closure in superkeys.items():
        attrs = superkey.split('/')

        # If there's only one attr, its subset if null, to it's a C key
        if len(attrs) == 1:
            candidate_keys[superkey] = closure
        else:
            combinations = []
            for r in range(1, len(attrs) + 1):
                for combo in itertools.combinations(attrs, r):
                    combinations.append('/'.join(combo))

            is_candidate_key = True
            for combo in combinations:
                if combo in superkeys:
                    is_candidate_key = False
                    break

            if is_candidate_key:
                candidate_keys[superkey] = closure

    return candidate_keys


def main():

    csv_path = input("Give path to csv file: ")
    display_data(csv_path)

    # relation_name = input("Enter relation name: ")
    functional_dependencies = [fd.strip() for fd in input("Enter functional dependencies (e.g., A->B, C->D): ").split(',')]
    primary_keys = [key.strip() for key in input("Enter primary key(s): ").split(',')]

    print(functional_dependencies)

    determinants, dependents, FD_list = database_fds(functional_dependencies)

    closure_dict = compute_closure(FD_list)

    find_partial_dependencies(primary_keys, closure_dict)

    find_transitive_dependencies(closure_dict, determinants, FD_list)


if __name__ == '__main__':
    main()
