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


if __name__ == '__main__':
    main()
