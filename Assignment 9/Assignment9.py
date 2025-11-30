from typing import List, Any, Tuple
from stack_and_queue import Stack, Queue
import random, copy, math, csv


class Person:
    """Represents a person/student.

    Attributes:
        name - a string of their name
        finance_experience - the student's self-reported comfort with finance/accounting
            on a scale of 1-5, initially 0
        tech_experience - the student's self-reported comfort with tech/python
            on a scale of 1-5, initially 0
        past_teammates - a list of strings, initially empty, containing the names of folks
            they have worked with in the past
    """

    def __init__(self):
        """Initialize an instance of a person.
        """
        self.name = ""
        self.finance_experience = 0
        self.tech_experience = 0
        self.past_teammates = []

    def __str__(self):
        """Return a string representation of the person.
        """
        s = self.name + " fin " + str(self.finance_experience) + " tech " + str(self.tech_experience)
        s += " old teammates " + str(self.past_teammates)
        return s

    def get(self, category):
        """Get the peron's score on the input category.

            Args:
                category - a string representing the category that we'd like to get the score for

            Returns:
                selfs score for the input category
        """
        if category == "finance":
            return self.finance_experience
        elif category == "tech":
            return self.tech_experience

def load_csv(file_name):
    """Opens and reads the provided file. Creates and returns a list of people objects from
        the data provided in the file.

        Args:
            The path of a csv file that contains the cohort.
            Each line of the file contains data about one person in the following format:
                      name, finance score, tech score

        Returns:
            A list of people objects.
        """
    people_list = []

    with open(file_name, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip header row

        for row in reader:
            person = Person()
            person.name = row[0].strip()
            person.finance_experience = int(row[1].strip())
            person.tech_experience = int(row[2].strip())
            people_list.append(person)

    return people_list

class Pairings:
    """Represents a state (situation) in a Pairings. Some students may have been
    assigned partners while others have not. self.partners[i] will contain a person
    object representing self.people[i]'s partner. If not yet assigned, self.partners[i]
    will contain a list of the remaining partner candidates (that are not yet
    assigned as someone's partner).

    Attributes:
        num_people_assigned - initially 0, the number of people who have been assigned partners
        people - a list of people objects representing the cohort
        partners - a list of partner assignments (people). Unassigned cells contain a list of
            candidates.
        category - a string representing the category that we care about for this pairings set
            (i.e. finance or tech). Each pair will vary in skills on this category.
    """

    def __init__(self, people, cat):
        self.num_people_assigned: int = 0
        self.people: List = copy.deepcopy(people)
        self.partners: List = []
        self.category: str = cat

        # populate the candidate partners list, skipping over oneself and ones past partners
        for p in people:
            candidates = []
            for other in people:
                if other != p and other.name not in p.past_teammates:
                    candidates.append(other)
            self.partners.append(candidates)

    def __str__(self) -> str:
        s = ""
        for i in range(len(self.partners)):
            if isinstance(self.partners[i], list):
                r = self.people[i].name + " can possibly be partnered with "
                for x in self.partners[i]:
                    r += x.name
            else:
                r = self.people[i].name + " is partnered with " + self.partners[i].name + " with average " + self.category + " score of "
                r += str((self.people[i].get(self.category) + self.partners[i].get(self.category)) / 2) + "\n"
            s += r
        return s

    def get_average_score(self) -> float:
        """Get the average score of the self.people list for self.category.
        self.people[i].get("finance") will retrieve person i's finance score.
        """
        total_score = 0
        for person in self.people:
            total_score += person.get(self.category)
        return total_score / len(self.people)

    def goal_test(self) -> bool:
        """Is the number of people who have been assigned partners equal
        to the number of people.
        """
        return self.num_people_assigned == len(self.people)

    def failure_test(self) -> bool:
        """Are there any empty lists in self.partners? That is, are there
        any people who no longer have any partner candidates?
        """
        for partner_entry in self.partners:
            if isinstance(partner_entry, list) and len(partner_entry) == 0:
                return True
        return False

    def get_first_unassigned_person(self) -> int:
        """Find and return the index of the first person in the people list who does
        not yet have a partner in self.partners.
        """
        for i in range(len(self.partners)):
            if isinstance(self.partners[i], list):
                return i
        return -1

    def update(self, p1_name, p2_name):
        """Given two names (strings) as input, make them partners.
        1) put the corresponding person object in the correct place in the partner list.
            Note, you'll first have to find the relevant indices in the people list.
            For example, if p1_name corresponds to self.person[3] and p2_name is
            self.person[6], then ...
            self.partners[6] = self.people[3]
            self.partners[3] = self.people[6]
        2) add 2 to num_people_assigned
        3) loop over the partners list and remove the corresponding people objects
            from the remaining parter candidate lists. Given the example above,
            remove self.person[3] and self.person[6] from all of the lists in self.partners.
        """
        # Find indices of p1 and p2 in the people list
        p1_index = -1
        p2_index = -1
        for i in range(len(self.people)):
            if self.people[i].name == p1_name:
                p1_index = i
            if self.people[i].name == p2_name:
                p2_index = i

        # Assign them as partners
        self.partners[p1_index] = self.people[p2_index]
        self.partners[p2_index] = self.people[p1_index]

        # Add 2 to num_people_assigned
        self.num_people_assigned += 2

        # Remove these people from all remaining candidate lists
        for i in range(len(self.partners)):
            if isinstance(self.partners[i], list):
                # Remove p1 from the list if present
                self.partners[i] = [p for p in self.partners[i] if p.name != p1_name and p.name != p2_name]

def DFS(state: Pairings) -> Pairings:
    """Search for a pairings that balances skill levels in the state.category dimension.
    Here's the outline that we created in class...
    create a stack called fringe
    push the initial state into fringe
    while fringe isn't empty
        pop fringe and save the result as curr
        if curr passes the goal test
            return curr - we're done!
        else if curr is not already failing
            get the first unassigned person in curr - lets call them s
            for each possible partner t
                if their score combo is acceptable (you decide how)
                    create a deep copy of curr
                    update the deep copy making a partnership of s and t
                    push the deep copy to the fringe
    """
    # Get the average score to use as a baseline for balancing
    average_score = state.get_average_score()

    # Create a stack called fringe
    fringe = Stack()

    # Push the initial state into fringe
    fringe.push(state)

    # While fringe isn't empty
    while not fringe.is_empty():
        # Pop fringe and save the result as curr
        curr = fringe.pop()

        # If curr passes the goal test
        if curr.goal_test():
            return curr  # We're done!

        # Else if curr is not already failing
        elif not curr.failure_test():
            # Get the first unassigned person in curr
            s_index = curr.get_first_unassigned_person()
            s = curr.people[s_index]

            # For each possible partner t
            for t in curr.partners[s_index]:
                # Calculate the average score of this pairing
                pair_avg = (s.get(curr.category) + t.get(curr.category)) / 2

                # If their score combo is acceptable (within 2 points of average)
                # This balances teams by pairing high and low skilled people
                # Use a more lenient threshold to ensure solvability
                if abs(pair_avg - average_score) <= 2.0:
                    # Create a deep copy of curr
                    new_state = copy.deepcopy(curr)

                    # Update the deep copy making a partnership of s and t
                    new_state.update(s.name, t.name)

                    # Push the deep copy to the fringe
                    fringe.push(new_state)

    # If no solution found
    return None

def make_pairings(cohort_people, category):
    """Giving a list of people and a category, make a pairing that balances
    that category. After the pairing is complete, update the past_teammates
    in the cohort to reflect this pairing.
    """

    random.shuffle(cohort_people)

    a_pairing = Pairings(cohort_people[:], category)
    a_pairing = DFS(a_pairing)
    if a_pairing == None:
        print("NOT SOLVABLE!")

    #remove recent partners as possibility
    for i in range(len(cohort_people)):
        cohort_people[i].past_teammates.append(a_pairing.partners[i].name)

    return (cohort_people, a_pairing)

def generate_pairings(filename, n, f, t):
    """Load people from file called file_name. From this data, create n
    pairings, f of which are balanced in background for finance projects and t of
    which are balanced in background for tech projects.
    """
    cohort_people = load_csv(filename)

    for p in cohort_people:
        print(p)

    pairings_list = []
    #generate the finance pairings
    for i in range(f):
        cohort_people, project_pairings = make_pairings(cohort_people, "finance")
        pairings_list.append(project_pairings)

    #generate the tech pairings
    for i in range(t):
        cohort_people, project_pairings= make_pairings(cohort_people, "tech")
        pairings_list.append(project_pairings)

    #print the pairings
    for k in range(len(pairings_list)):
        print("pairings: " + str(k+1))
        print(pairings_list[k])

    #print the cohort at the end so that we can check that the "past teammates" have
    #properly been updated
    for p in cohort_people:
        print(p)

if __name__ == "__main__":
    generate_pairings("cohort.txt", 3, 2, 1)