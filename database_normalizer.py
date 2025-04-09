import pandas as pd
import mysql.connector
import itertools


def display_data(csv_path):
    """Takes in csv path, cleans the input by removing '"' and replacing '\'
    with '/'. Then reads in the csv, printing a sample of the dataframe and
    the datae types ofeach columns."""

    csv_path = csv_path.replace('"', "").replace("\\", "/")
    data = pd.read_csv(csv_path)
    df = pd.DataFrame(data)

    print("Given Dataframe: ")
    print("")
    print(df.head())
    print("")
    print("DataFrame Column DataTypes: ")
    print("")
    print(df.dtypes)
    print("")

    return df


def database_fds(functional_dependencies: list):

    """
    Analyzes a list of functional dependencies given as
    (i.e. ["A->B,C", "B->C"]) and extracts the relation, determinants,
    dependents, and the list of functional dependencies in the form
    of a list of tuples.
    """

    relation = set()
    determinants = []
    dependents = []

    FD_list = []

    for i in range(len(functional_dependencies)):
        # Split each FD on '->' (i.e "A|B->C,D" --> (A|B), (C,D))
        left, right = functional_dependencies[i].split('->')

        # Remove spaces and split right into a list on ',' (i.e. r = [C, D])
        right = [item.replace(" ", "") for item in right.split(',')]

        # For every dependent per determinant, add the deter x times to
        # the deter list
        for i in range(len(right)):
            determinants.append(left)

        # Add each dependent to dependent list
        for dependent in right:
            dependents.append(dependent)

        # Add a tuple of the deter and the dep to the FD_list st. dep is a
        # list of all the deps the deter has
        FD_list.append((left, right))

        # Update the set (for uniqueness) of the relation by adding the
        # deter to it. Spliting by '|' if needed
        relation.update(list(left.split('|')))

        # Update the relation by adding the dependent to it
        for r in right:
            relation.update(list({r}))

    print("Relation: ", relation)
    print("")
    print("Deteminants: ", determinants)
    print("")
    print("Dependents: ", dependents)
    print("")
    print("Functional Dependencies: ", FD_list)

    # Relation is a set, deter and deps as a list and FD_List is a list
    # of tuples. The first index being the deter and the second being
    # a list of all the deps the deter leads to
    return relation, determinants, dependents, FD_list


def attribute_combos(determinants: list, dependents: list):

    """
    Helper function for compute_closure that creates a list of every
    possible combo between the deters and the deps, dividing each
    combo with a '/'

    i.e Deter = [A,B] Deps = [C,D]
    Combos =  ['A', 'B', 'C', 'D', 'A/B', 'A/C', 'A/D', 'B/C', 'B/D',
    'C/D', 'A/B/C', 'A/B/D', 'A/C/D', 'B/C/D', 'A/B/C/D']
    """

    # Combine the two lists (unique)
    for dep in dependents:
        combined_list = list(set(determinants + dep))

    combinations = []

    # Generate combinations of different lengths (1 to the length of
    # the combined list)
    for combo_size in range(1, len(combined_list) + 1):
        # combo is a tuple of attrs based on the combo size.
        # combined_list = ['A', 'B', 'C'], combo_size = 2
        # combo will be one of: [('A', 'B'), ('A', 'C'), ('B', 'C')]
        for combo in itertools.combinations(combined_list, combo_size):
            # combo ('A', 'B') becomes "A/B"
            combinations.append('/'.join(combo))

    return combinations


def compute_closure(FD_list: list):
    """
    Computes closure of every attribute and attribute combo give a list of
    tuples of the FDs
    i.e. FD_list = [('StudID|CourID', ['StudName', 'CourName', 'InstrName']),
            ('StudID', ['StudName']), ('CourID', ['CourName', 'InstrName'])]
    """

    closure_dict = {}
    determinants = []
    dependents = []

    # Seperate the FDs into determinants and dependents
    for determinant, dependent in FD_list:
        determinants.append(determinant)
        dependents.append(dependent)

    # Adding determinants into closure dict
    for determinant, dependent in FD_list:
        if determinant not in closure_dict.keys():
            # Determinant is a composition of two attrs, split via '|'
            composite = tuple(determinant.split('|'))
            closure_dict[determinant] = set()
            # if deter = A|B, closure of A|B should start with {A,B}
            for c in composite:
                closure_dict[determinant].add(c)
                # Closure of A and B seperately should include themselves
                if c not in closure_dict:
                    closure_dict[c] = {c}

        # Adding Dependents to closure set of determinants
        for dep in dependent:
            closure_dict[determinant].update({dep})

        # Closure of a Dependent is itself
        for dep in dependent:
            if dep not in closure_dict.keys():
                closure_dict[dep] = {dep}

        # if determinant is already in closure.keys, add it's dep to its
        # closure set
        if determinant in closure_dict.keys():
            for dep in dependent:
                closure_dict[dep].update({dep})

    # If any determinant's dependent is also a determinant (Transitive),
    # add the dependent's dependents to the original deter's closure set
    # i.e A->B, C; B->D ---> A+ = [A, B, C, D]
    for determinant in closure_dict.keys():
        for key, value in closure_dict.items():
            if determinant in value:
                closure_dict[key].update(closure_dict[determinant])

    # attribute_combos_results is a list of every combo between the deters
    # and deps
    # ['A', 'B', 'C', 'A|B', 'A/B', 'A/B', 'A/C', 'A/A|B', ..., 'A/B/C/A|B']
    attribute_combos_results = attribute_combos(determinants, dependents)
    print("Attribute_Combos: ", attribute_combos_results)

    # Finding closure of every possible attr combo
    for attr_combo in attribute_combos_results:
        if attr_combo not in closure_dict.keys():
            closure_dict[attr_combo] = set()
            # Seperate the combos by '/' and combine their individual closure
            # sets into
            # a unique set of their closures
            attrs = [attrs for attrs in attr_combo.split('/')]
            for attr in attrs:
                closure_dict[attr_combo].update(closure_dict[attr])

    print("")
    print("Closure Dict: ", closure_dict)

    return closure_dict


def find_partial_dependencies(primary_keys: list, closure_dict: dict) -> list:
    """
    Creates a list of partial dependents given a list of the primary keys and
    a complete closure dict of every attribute and attribute combo's closure
    set
    """

    possible_partial_dependencies = {}

    # partial_deps only occur if the primary key is a composite key
    if len(primary_keys) > 1:
        # Comparing each primary key
        for i in primary_keys:
            for j in primary_keys:
                # If their closure sets aren't the same, hence they're
                # differnt attrs with different deps despite being a primary
                # key
                if closure_dict[i] != closure_dict[j]:
                    # For all the denpendencies from primary key i that aren't
                    # a dep of primary key j, add that dependency to
                    # possible_partial_deps as the value with primary key i as
                    # the key
                    for dependency in closure_dict[i]:
                        if (dependency not in closure_dict[j]) & (i != dependency):
                            if i not in possible_partial_dependencies:
                                possible_partial_dependencies[i] = [dependency]
                            else:
                                possible_partial_dependencies[i].append(dependency)

    print("")
    print("With primary keys: ", primary_keys)
    print("Possible Partial Dependencies: ", possible_partial_dependencies)

    # If the possible_partial_dependencies list length is > 0, a partial_dep
    # was found and hence the dataframe does not satisfy 2NF
    if len(possible_partial_dependencies) > 0:
        satisfies_2nf = False
    else:
        satisfies_2nf = True

    return satisfies_2nf, possible_partial_dependencies


def find_transitive_dependencies(closure_dict: dict, determinants: list, dependents: list, FD_list: list):
    """
    Creates a list of the transitive_dependencies
    (i.e A->B, B->C ---> [(A, C)]) given the closure dictionary of every
    attribute and attribute combo's closure sets, a list of the
    determinants and the list of tuples of Functional Dependencies

    Goal: If a determinant has a dependent that is also a determinant with
    its own dependents, a transitive connection is found
    """
    transitive_dependencies = {}

    # For each attribute and it's closure set
    for key, closure_set in closure_dict.items():
        # For each attribute in that closure set
        for attribute in closure_set:
            # If the attribute in the set is a determinant and isn't itself
            # (As closure of A will include A itself)
            if (attribute in determinants) & (attribute != key):
                # For deter and dep list in FD_list
                for determinant, dependent in FD_list:
                    # If the attribute that is both a dep and a deter,
                    # add that attribute as the key and this attribute's
                    # dependents unique set as the value to
                    # transitive_dependencies
                    if (determinant == attribute) & (attribute in dependents):
                        if key not in transitive_dependencies:
                            transitive_dependencies[attribute] = set()
                        for dep in dependent:
                            transitive_dependencies[attribute].add(dep)

    # Convert transitive_deps' values from a set to a list
    transitive_dependencies = {key: list(value) for key, value in transitive_dependencies.items()}

    print("")
    print("Possible Transitive Dependencies: ", transitive_dependencies)

    # If the transitive_dependencies list length is > 0, a transitive_dep was
    # found and hence the dataframe does not satisfy 3NF
    if len(transitive_dependencies) > 0:
        satisfies_3nf = False
    else:
        satisfies_3nf = True

    return satisfies_3nf, transitive_dependencies


def suggest_candidate_key(relation: set, closure_dict: dict):
    """
    Returns a dict of candidate_keys given the relation set and the closure
    dict.
    Goal: Candidate Keys are minimal superkeys, hence return a dict with keys
    with the least amount of attributes that lead to every attribute in the
    relation
    """

    superkeys = {}
    candidate_keys = {}

    # If closure as all the attributes, the attribute is a superkey
    for attribute, closure in closure_dict.items():
        if len(closure) == len(relation):
            superkeys[attribute] = closure

    # If no subset of the superkey is superkey, the attribute is a
    # candidate key
    for superkey, closure in superkeys.items():
        attrs = superkey.split('/')

        # If there's only one attr, its subset is null, so it's a Candidate key
        if len(attrs) == 1:
            candidate_keys[superkey] = closure
        else:
            combinations = []
            # After seperating the composite attr into its individual attrs,
            # create a list of its combinations
            # i.e A|B = [A, B, A/B]
            for combo_size in range(1, len(attrs) + 1):
                for combo in itertools.combinations(attrs, combo_size):
                    # If combo isn't already a superkey, add combo to
                    # combiations list
                    if str(combo) != str(superkey):
                        combinations.append('/'.join(combo))
            # making sure the superkey isn't in the combinantions list
            combinations.remove(superkey)

            # If any subset of the superkey's attributes is a superkey itself,
            # then the largest superkey is not a candidate key
            # i.e if A|B is a superkey and A is a superkey, then A|B is not a
            # candidate key
            is_candidate_key = True
            for combo in combinations:
                if combo in superkeys:
                    is_candidate_key = False
                    break

            if is_candidate_key:
                candidate_keys[superkey] = closure

        # Just so A|B and A/B are considered the same
        for key1 in list(candidate_keys.keys()):
            cand_key1 = key1.replace('|', ',').replace('/', ',')
            for key2 in list(candidate_keys.keys())[1:]:
                cand_key2 = key2.replace('|', ',').replace('/', ',')
                if cand_key1 == cand_key2 and key1 != key2:
                    del candidate_keys[key2]

    print("Candidate Keys: ", candidate_keys)

    return candidate_keys


def check_1NF(df: pd.DataFrame):
    """
    Given a dataframe, check to see if it passes the requirments of 1NF:
    That every cell has one singluar value and that every row in the df
    is unique.
    """

    # Check to see if every cell value is a single value
    # i.e. can be a int, float, str, but not a list, array, series
    def is_single_value(x):
        return not isinstance(x, (list, tuple, set, dict, pd.Series))

    all_single_values = df.map(is_single_value).all().all()

    # Check to see if every row in the df is unique
    is_unique = not df.duplicated().any()

    if all_single_values & is_unique:
        return True
    else:
        return False


def decompose_to_2nf(df: pd.DataFrame, possible_partial_dependencies: dict) -> list:
    """
    Given a Dataframe and dict of the partial_dependencies found,
    this function divides the df into seperate dfs to satisfy 2NF:
    No partial dependencies
    """

    relations = []

    # For key and a list of its dep attrs create a subset of the df
    # starting with adding the key
    for key, dependent_attr in possible_partial_dependencies.items():
        subset = df[[key]].drop_duplicates()
        # Then add each of its deps to the subset df
        for dep in dependent_attr:
            subset[dep] = df[dep]
        # Add new df to the relations list
        relations.append(subset)

    used_dep_list = []

    # Keeping track of the dependencies already added to one subset
    for dep in possible_partial_dependencies.values():
        for _ in dep:
            used_dep_list.append(_)

    print("Used_deps: ", used_dep_list)

    # Put the remaining non-key attributes into the next df subset
    remaining_attrs = [col for col in df.columns if col not in used_dep_list]
    remaining_relation = df[remaining_attrs].drop_duplicates()
    relations.append(remaining_relation)

    # remove any duplicate rows from the dataframe
    for i, relation in enumerate(relations):
        relations[i] = relation.drop_duplicates()

    return relations


def decompose_to_3nf(original_df: pd.DataFrame, df: pd.DataFrame, FD_list: list, transitive_dependencies: dict) -> list:
    """
    Given a df, the original dfs' transitive dependencies and intermediate
    attributes causing the transivity, this function is meant to divide
    the df into seperate dfs to satify 3NF: no transitive connections
    """
    trans_dep_subset_dict = {}

    # transitive_deps includes transitive dependencies found for every combo
    # of attributes. Just want to focus on the direct attributes of the
    # dataframe
    for key, value in transitive_dependencies.items():
        if key in df.columns:
            trans_dep_subset_dict[key] = value

    print("Transitive Dict of the attributes: ", trans_dep_subset_dict)
    print("")

    relations = []

    # for the determinant and its list of deps causing the transitivity
    # if the list of dependents is equal to the list of dependencies in the
    # intermediate_attrs then the middle inter attribute is equal to the
    # key of that dict
    for key, dependent_attr in trans_dep_subset_dict.items():
        inter_attr = key
        # add the inter_attr and its dependencies to the subset df
        subset = df[[inter_attr]].drop_duplicates()
        for dep in dependent_attr:
            subset[dep] = df[dep]
        # add new df to relations list
        relations.append(subset)

    # keep track of the dependencies already added to a subset df
    used_dep_list = []

    if len(trans_dep_subset_dict) == 0:
        subset = df.copy()

        # For each determinant, add its dependencies to the subset
        for deter, depends in FD_list:
            if deter in df.columns:  # Ensure the determinant is present in the DataFrame
                for dep in depends:
                    if dep in original_df.columns:  # Add dependencies from the original dataframe
                        subset[dep] = original_df[dep]
                        used_dep_list.append(dep)
                relations.append(subset)

    else:
        # for the determinant and its list of deps causing the transitivity
        # if the list of dependents is equal to the list of dependencies in the intermediate_attrs
        # then the middle inter attribute is equal to the key of that dict
        for key, dependent_attr in trans_dep_subset_dict.items():
            inter_attr = key
            # add the inter_attr and its dependencies to the subset df
            subset = df[[inter_attr]].drop_duplicates()
            for dep in dependent_attr:
                if dep in original_df.columns:
                    subset[dep] = original_df[dep]
            # add new df to relations list
            relations.append(subset)

        for dep_list in trans_dep_subset_dict.values():
            for dep in dep_list:
                used_dep_list.append(dep)

    # Put the remaining non-key attributes into the next df subset

    remaining_df_attrs = [col for col in df.columns if col not in used_dep_list]

    # Check if remaining_attrs are in the columns of the subset; exclude them if already present
    remaining_attrs = [col for col in remaining_df_attrs if col not in subset.columns]

    # If there are any remaining attributes, create a new relation for them
    if remaining_attrs:
        remaining_relation = df[remaining_attrs].drop_duplicates()
        relations.append(remaining_relation)

    # If the relation only has one column, add its dependents to the df
    for relation in relations:
        if len(relation.columns) == 1:
            loner_column = relation.columns[0]
            for deter, depends in FD_list:
                if deter == loner_column:
                    for dep in depends:
                        if dep in original_df.columns:
                            relation[dep] = original_df[dep]

    # remove any duplicate rows from the dataframe

    for i, relation in enumerate(relations):
        relations[i] = relation.drop_duplicates()

    # Ensure the last df is not added if all its columns are already used
    final_relations = []
    used_columns = set()

    for relation in relations:
        if set(relation.columns).issubset(used_columns):
            continue  # Skip this relation if all its columns are already used
        final_relations.append(relation)
        used_columns.update(relation.columns)

    return final_relations


def connect_to_db():
    """Function to connect to MySQL Database"""
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="Buggyduggy2233!",
            database="Project1"
        )
        print("Connected to the database successfully.")
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


def close_connection(connection):
    """Function to close the database connection"""
    connection.close()
    print("Connection closed.")


def insert_data(cursor):
    """Function to insert data into a table"""
    table_name = input("Enter the table name: ")
    columns = input("Enter the columns (comma separated): ")
    values = input("Enter the values (comma separated, each value in ''): ")

    insert_query = f"INSERT INTO {table_name} ({columns}) VALUES ({values})"
    try:
        cursor.execute(insert_query)
        print(f"Data inserted successfully into {table_name}.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


def update_data(cursor):
    """Function to update data in a table"""
    table_name = input("Enter the table name: ")
    set_values = input("Enter the values to set (e.g., column1 = value1, column2 = value2): ")
    where_condition = input("Enter the WHERE condition (e.g., column = value): ")

    update_query = f"UPDATE {table_name} SET {set_values} WHERE {where_condition}"
    try:
        cursor.execute(update_query)
        print(f"Data updated successfully in {table_name}.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


def main():

    # Step 1: CSV Data Import 
    csv_path = input("Give path to csv file: ")
    df = display_data(csv_path)
    original_df = df

    # Step 2: Functional Dependency Identification
    functional_dependencies = [fd.replace(" ", "") for fd in input("Enter functional dependencies (e.g., A->B,D; C->D): ").split(';')]
    primary_keys = [key.strip() for key in input("Enter primary key(s): ").split(',')]

    relation, determinants, dependents, FD_list = database_fds(functional_dependencies)

    closure_dict = compute_closure(FD_list)

    suggest_candidate_key(relation, closure_dict)

    # Step 3: Normalization Process
    pass_1NF = check_1NF(df)

    satisfies_2nf, possible_partial_dependencies = find_partial_dependencies(primary_keys, closure_dict)

    satisfies_3nf, transitive_dependencies = find_transitive_dependencies(closure_dict, determinants, dependents, FD_list)

    print("Partial Dependencies: ", possible_partial_dependencies)
    print("")
    print("Transitive_Dependencies: ", transitive_dependencies)
    print("")
    print("Decomposed Dataframes that satisfy 3NF:")

    decomposed_dfs = []

    if pass_1NF:
        if satisfies_2nf:
            if satisfies_3nf:
                print("Dataframe is already in 3NF", df)
            else:
                new_dfs = decompose_to_3nf(df, transitive_dependencies)
                for df in new_dfs:
                    print("")
                    print("")
                    print(df)
                    decomposed_dfs.append(df)
        else:
            attr_found = set()
            new_dfs = decompose_to_2nf(df, possible_partial_dependencies)
            for df in new_dfs:
                newest_dfs = decompose_to_3nf(original_df, df, FD_list, transitive_dependencies)
                for subset in newest_dfs:

                    if len(attr_found) != len(relation):
                        print(subset)
                        decomposed_dfs.append(subset)
                        print("")
                        print("")
                        attr_found.update(subset.columns)
                        print("Attrs Found: ", attr_found)
    else:
        print("Doesn't Pass 1NF (every row unique and every cell having one value)")

    # Step 4: SQL Script Generation
    mydbase = mysql.connector.connect(host="localhost",
                                      user="root",
                                      passwd="Buggyduggy2233!",
                                      database="Project1")

    mycursor = mydbase.cursor()

    def create_table_if_not_exists(table_name, columns):
        # Dropping the table if it already exists
        drop_table_query = f"DROP TABLE IF EXISTS Project1.{table_name};"
        mycursor.execute(drop_table_query)
        print(f"Table {table_name} dropped if it existed.")

        # Creating or Recreating table
        column_definitions = ', '.join([f"`{col}` VARCHAR(255)" for col in columns])
        create_table_query = f"CREATE TABLE IF NOT EXISTS Project1.{table_name} ({column_definitions})"
        mycursor.execute(create_table_query)
        print(f"Table {table_name} checked/created.")

    n = 0
    for df in decomposed_dfs:
        n += 1
        table_title = f"Table{n}"
        print("Table_title: ", table_title)
        print("Dataframe Columns: ", df.columns)
        create_table_if_not_exists(table_title, df.columns)

        print("Number of rows to insert:", len(df))

        for row in df.itertuples(index=False):
            columns = ', '.join(df.columns)
            placeholders = ', '.join(['%s'] * len(df.columns))
            values = tuple(getattr(row, col) for col in df.columns)
            insert_statement = f"INSERT INTO Project1.{table_title} ({columns}) VALUES ({placeholders})"

            print(columns)
            print(placeholders)
            print(values)
            print(insert_statement)
            print("")

            mycursor.execute(str(insert_statement), values)

    mydbase.commit()

    mycursor.close()
    mydbase.close()


# Step 5: Database Creation and Query Interface
def interactive_menu():
    """Function to display the interactive menu and accept user input"""
    connection = connect_to_db()
    if not connection:
        return

    cursor = connection.cursor()

    while True:
        print("\nInteractive Query Interface")
        print("Operation Choices: ")
        print("Insert Data")
        print("Update Data")
        print("Exit")

        choice = input("Choose an operation: ")

        if choice == "Insert Data":
            insert_data(cursor)
        elif choice == "Update Data":
            update_data(cursor)
        elif choice == "Exit":
            print("Exiting Interface")
            break

        else:
            print("Invalid choice. Please try again.")

    connection.commit()
    close_connection(connection)


if __name__ == '__main__':
    main()
    interactive_menu()
