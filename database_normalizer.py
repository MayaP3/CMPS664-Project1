import pandas as pd


# Import csv
def display_data(csv_path):
    csv_path = csv_path.replace('"', "").replace("\\", "/")
    data = pd.read_csv(csv_path)
    df = pd.DataFrame(data)

    print(df.head)
    print(df.dtypes)


# Functional Dependency Identifcation
def database_fds(functional_dependenices: list, primary_keys: list):

    determinants = []
    dependents = []

    FD_list = []

    for i in range(len(functional_dependenices)):
        left, right = functional_dependenices[i].split('->')
        determinants.append(left)
        dependents.append(right)
        FD_list.append((left, right))

    print("Deteminants: ", determinants)
    print("")
    print("Dependents: ", dependents)
    print("")
    print("Functional Dependencies: ", FD_list)

    return determinants, dependents, FD_list


def compute_closure(FD_list: list) -> dict:
    closure_dict = {}

    for determinant, dependent in FD_list:
        if determinant not in closure_dict.keys():
            closure_dict[determinant] = set(determinant)
            closure_dict[determinant].update(dependent)

    if determinant in closure_dict.keys():
        closure_dict[determinant].update(dependent)

    for determinant in closure_dict.keys():
        for key, value in closure_dict.items():
            if determinant in value:
                closure_dict[key].update(closure_dict[determinant])

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

    return possible_partial_dependencies


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

    return transitive_dependencies


def suggest_candidate_key(determinants, closure_dict):
    largest_length = -1
    largest_set = {}
    best_i = None
    best_j = None

    for i in determinants:
        for j in determinants:
            if j not in i:
                combined_set = set(closure_dict[i]) | set(closure_dict[j])

                if len(combined_set) > largest_length:
                    largest_length = len(combined_set)
                    largest_set = combined_set
                    best_i = i
                    best_j = j

    print("")
    print(best_i, "and", best_j, "creates", largest_set, "the largest set")

    return best_i, best_j, largest_set


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
