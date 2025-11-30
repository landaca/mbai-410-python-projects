# Netid: bsz6907 (Pablo Landa Catan) and Raz Kurteran
from match import match
from data import features
import string

##########Action Functions###############################
    
def country_by_rank(matches):     # matches look like this: ['1', 'population']
    """Takes a list of matches as input - specifically one that holds a rank
        and a feature, like 'population.' Finds the country with that rank 
        using tha feature and returns it in a list.

        Args: matches - a list of strings resulting from a call to match. It
        holds a rank and a feature. 

        Returns: a list of one string - the rank of the country for the
        specified feature. If the country or feature is not found, returns an
        empty list. 
    """
    try:
        data = features[matches[1]]
        country = ""
        for key in data:
            if data[key][0] == matches[0]:
                country = key
        if country == "":
            return []            # return empty list when no country at that rank
        return [country]
    except:
        return []

def rank_by_country(matches): # ["united states", "area"]
    """Takes a list of matches as input - specifically one that holds a country
        and a feature, like 'population.' Finds the rank for that country
        using tha feature and returns it in a list.

        Args: matches - a list of strings resulting from a call to match. It
        holds a country and a feature. 

        Returns: a list of one string - the rank of the country for the
        specified feature. If the country or feature is not found, returns an
        empty list. 
    """
    try:
        searched_country = matches[0]
        current_feature = matches[1]

        data = features[current_feature]
        country = data[searched_country]
        rank = country[0]

        return [rank]
    except:
        return []
    

def list_countries(unused):
    """Takes an input that is unused (empty list resulting from a call to match).
        Constructs a list of countries by looking at the keys from one of the
        dictionaries. You can use *any* of the dictionaries for this. I know
        this is not an accurate response as some countries are listed under
        some features but not under others. 

        Args: unused - an empty list resulting from a call to match.

        Returns: a list of countries. 
    """

    result = []
    data = features["population"]

    for country in data:
        result.append(country)

    return result

def list_patterns(unused):
    """Takes an input that is unused (empty list resulting from a call to match).
        Constructs a list of the patterns from the pa_list and returns it.

        Args: unused - an empty list resulting from a call to match.

        Returns: a list of the known patterns. 
    """

    #  get the list of paterns and return the left side of it

    result = []
    for pattern in pa_list:
        result.append(pattern[0])

    return result
        

def bye_action(unused):
    """This action function gets called when the user writes 'bye'.
        It raises KeyboardInterrupt in order to break out of the query loop.

        Args: unused - an empty list resulting from a call to match.
    """
    raise KeyboardInterrupt

def population_of_country(matches):
    """Returns the population value for the given country, else []."""
    try:
        searched_country = matches[0]
        current_feature = "population"

        data = features[current_feature]
        country_info = data[searched_country]
        population_value = country_info[1]

        return [str(population_value)]
    except:
        return []

def median_age_of_country(matches): 
    """Returns the median age value for the given country, else []."""
    try:
        searched_country = matches[0]
        data = features["median age"]
        median_age_value = data[searched_country][1]
        return [str(median_age_value)]
    except:
        return []   

def birth_rate_of_country(matches):
    try:
        country = matches[0]
        data = features["birth rate"]
        if country in data:
            return [str(data[country][1])]
        if country.lower() in data:
            return [str(data[country.lower()][1])]
        return []
    except:
        return []

##########Pattern, Action list###############################



pa_list = [(str.split("which country is ranked number _ for %"), country_by_rank),
           (str.split("what is % ranked for %"), rank_by_country),
           (str.split("which countries do you know about"), list_countries),
           (str.split("what kinds of questions do you understand"), list_patterns),
           (str.split("what is the population of _"), population_of_country),
           (str.split("what is the median age of _"), median_age_of_country),
           (str.split("what is the birth rate of _"), birth_rate_of_country),
           (str.split("birth rate of _"), birth_rate_of_country),
           (["bye"], bye_action)]


def search_pa_list(src):
    """Takes source, finds matching pattern and calls corresponding action. If it finds
    a match but has no answers it returns ["No answers"]. If it finds no match it
    returns ["I don't understand"].

    Args:
        source - a phrase represented as a list of words (strings)

    Returns:
        a list of answers. Will be ["I don't understand"] if it finds no matches and
        ["No answers"] if it finds a match but no answers
    """
    result = ["I don't understand"]

    for pattern in pa_list:
        pattern_string = pattern[0]
        pattern_function = pattern[1]

        match_res = match(pattern_string, src)
        if match_res or pattern_string == src:
            result = pattern_function(match_res)

            if len(result) == 0:
                return ["No answers"]

            return result

    return result


def query_loop():
    """Query_lop asks the user for input, then "cleans" that input
        by converting all characters to lowercase, removing any training
        punctuation (e.g. ?). After then converting the input to a list
        of strings, we pass the list off to search_pa_list to get answers,
        then display the answers to the user.
        Use a try/except structure to catch Ctrl-C or Ctrl-D characters
        and exit gracefully. You'll need to except KeyboardInterrupt and
        EOFError.
    """

    try:
        while True:
            user_input = input("What do you want?")
            print(search_pa_list(user_input.lower().rstrip(string.punctuation).split()))
    except KeyboardInterrupt:
        return
    except EOFError:
        return

if __name__ == "__main__":
    assert country_by_rank(["2", "population"]) == ["india"], "country_by_rank test"
    assert rank_by_country(["united states", "area"]) == ["4"], "rank_by_country test"
    assert search_pa_list(["hi", "there"]) ==["I don't understand"], "search_pa_list test 1"
    assert search_pa_list(["which", "country", "is", "ranked", "number", "2", "for",
                                                   "median", "age"]) == ["japan"], "search_pa_list test 2"
    assert search_pa_list(["what", "is", "XYZ", "ranked", "for", "population"]) == ["No answers"], "search_pa_list test 3"
    assert search_pa_list(["what","is","the","population","of","japan"]) != ["No answers"], "population_of_country returns a value"
    assert search_pa_list(["what","is","the","median","age","of","japan"]) != ["No answers"], "median_age_of_country returns a value"
    assert search_pa_list(["what","is","the","birth","rate","of","japan"]) != ["No answers"], "birth_rate_of_country returns a value"

    #uncomment the line below to interact with your chatbot
    query_loop()

    # CHATBOT TRANSCRIPT
    # What do you want?what is the population of japan
    # ['124,687,293']
    # What do you want?what is the median age of china
    # ['38.4']
    # What do you want?what is the birth rate of india
    # ['17.53']
    # What do you want?what is the birth rate of fakecountry
    # ['No answers']
    # What do you want?which country is ranked number 1 for population
    # ['china']
    # What do you want?what is united states ranked for area
    # ['4']
    # What do you want?which countries do you know about
    # ['china', 'india', 'united states', 'indonesia', 'pakistan', 'nigeria', 'brazil', 'bangladesh', ...]
    # What do you want?what kinds of questions do you understand
    # [['which', 'country', 'is', 'ranked', 'number', '_', 'for', '%'], ['what', 'is', '%', 'ranked', 'for', '%'],
    #  ['which', 'countries', 'do', 'you', 'know', 'about'], ['what', 'kinds', 'of', 'questions', 'do', 'you', 'understand'],
    #  ['what', 'is', 'the', 'population', 'of', '_'], ['what', 'is', 'the', 'median', 'age', 'of', '_'],
    #  ['what', 'is', 'the', 'birth', 'rate', 'of', '_'], ['birth', 'rate', 'of', '_'], ['bye']]
    # What do you want?hey there
    # ["I don't understand"]
    # What do you want?bye
    # pablolandacatan@Pablos-MacBook-Pro-9 Assignment 3 % 