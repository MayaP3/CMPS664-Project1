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

    FD_dict = {}

    for i in range(len(functional_dependenices)):
        left, right = functional_dependenices[i].split('->')
        determinants.append(left)
        dependents.append(right)
        FD_dict[left] = right

    print("Deteminants: ", determinants)
    print("")
    print("Dependents: ", dependents)
    print("")
    print("Functional Dependencies: ", FD_dict)


def main():

    csv_path = input("Give path to csv file: ")
    display_data(csv_path)

    # relation_name = input("Enter relation name: ")
    functional_dependencies = list(input("Enter functional dependencies (e.g., A->B, C->D): ").split(','))
    primary_keys = list(input("Enter primary key(s): ").split(','))

    database_fds(functional_dependencies, primary_keys)


if __name__ == '__main__':
    main()
