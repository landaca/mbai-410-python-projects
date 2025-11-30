import csv

def load_csv(file_name):
    """Opens and reads the provided file. Creates a dictionary that maps name to a
        list of ranking and value. For example, the "population" dictionary would look like...
        {'China': ['1', '1,397,897,720'],
        'India': ['2', '1,339,330,514'],
        'United States': ['3', '334,998,398'],
        'Indonesia': ['4', '275,122,131'],
        ...}
        Notice that all items in values/lists (e.g. ['1', '1,397,897,720']) are strings.

        Args:
            The path of a csv file that contains some world factbook country comparison data.
            The file must be one that includes the following fields: name, ranking, and value. 

        Returns:
            A dictionary mapping 'name' to a list containing rank and value - both as strings. 
        """
    #write your code here
    result = {}

    with open(file_name, mode='r', newline='') as file:
        csv_dict_reader = csv.DictReader(file)
        for row in csv_dict_reader:
            name = row["name"]
        
            ranking = row["ranking"]
            value = row["value"]
            result[name.lower()] = [ranking, value]
    return result

features = {}
features["area"] = load_csv("world_factbook/geography/area.csv")
features["population"] = load_csv("world_factbook/people_and_society/population.csv")
features["median age"] = load_csv("world_factbook/people_and_society/median_age.csv")
features["life expectancy"] = load_csv("world_factbook/people_and_society/life_expectancy_at_birth.csv")
features["gdp"] = load_csv("world_factbook/economy/real_gdp_purchasing_power_parity.csv")
features["birth rate"] = load_csv("world_factbook/people_and_society/birth_rate.csv")
features["death rate"] = load_csv("world_factbook/people_and_society/death_rate.csv")

assert features["population"]["united states"][0] == "3", "US population rank test"
assert features["life expectancy"]["chile"][1] == "79.57", "Chile life expectancy value test"
assert features["area"]["south africa"][1] == "1,219,090", "South Africa area value test"
assert len(features["median age"]) == 226, "Median Age dictionary size test"
assert features["gdp"]["china"][0] == "1", "China gdp rank test"
assert features["birth rate"]["niger"][0] == "1", "Niger birth rate rank test"
assert features["death rate"]["lithuania"][0] == "15.05", "Lithuania death rate rank test"