import re, random

def get_user_inputs(template):
    placeholders = re.findall(r'\{(.*?)\}', template)
    inputs = {}
    for placeholder in placeholders:
        if placeholder not in inputs:
            user_input = input(f"Enter a {placeholder.replace('_', ' ')}: ")
            inputs[placeholder] = user_input
    return inputs

def play_madlibs():
    stories = [
        """
        One day, a {adjective} {noun} decided to {verb} at the {place}. 
        Suddenly, a {animal} wearing a {clothing_item} appeared and started to {action}.
        Everyone was {emotion} by the sight of the {animal} {action}.
        """,
        """
        In the land of {fantasy_place}, a {adjective1} {creature} loved to {verb1} every morning.
        Its best friend, a {adjective2} {another_creature}, always joined in to {verb2}.
        Together, they {plural_noun} and {verb3} until the sun set.
        """,
        """
        Last Halloween, {person_name} dressed up as a {adjective} {noun}.
        While trick-or-treating, they found a {color} {object} that could {magical_action}.
        Excited, {person_name} decided to {verb_past_tense} with it all night.
        """,
        """
        During the {season}, a group of {plural_noun} went on an adventure to find the {adjective} {artifact}.
        Along the way, they encountered a {adjective2} {animal} that helped them {verb}.
        In the end, they {verb_past_tense} the {artifact} and celebrated with a {celebration}.
        """,
        """
        At the {event}, a {adjective} {profession} was tasked with {verb_ing}.
        To accomplish this, they used a {tool} and a {object}.
        The crowd was {emotion} as the {profession} {verb_past_tense} successfully.
        """,
        """
        In a {adjective} {time_period}, a {noun} discovered a {magical_item} that could {ability}.
        They decided to {verb} it, leading to {unexpected_result}.
        This changed their life forever, making them {new_status}.
        """,
        """
        Every morning, a {adjective} {animal} would {verb} by the {location}.
        One day, it met a {adjective2} {another_animal} who loved to {verb2}.
        Together, they {verb3} and {verb4}, becoming the best of friends.
        """,
        """
        On {holiday}, {person_name} baked a {adjective} {food_item} that could {magical_power}.
        When they {verb_past_tense} it, everyone in town started to {reaction}.
        It was the most {superlative} {holiday} ever!
        """,
        """
        In the {adjective} forest, a {creature} was searching for a {rare_item}.
        It used its {body_part} to {action}, navigating through the {environment}.
        Finally, it found the {rare_item} and felt {emotion}.
        """,
        """
        A {adjective} {vehicle} raced down the {place}, driven by a {profession}.
        Suddenly, it had to {action} to avoid a {obstacle}.
        The driver {verb_past_tense} skillfully, winning the {competition}.
        """
    ]
    print("Welcome to Mad Libs!\n")
    story = random.choice(stories)
    user_inputs = get_user_inputs(story)
    completed_story = story.format(**user_inputs)
    print("\nHere's your Mad Libs story:\n")
    print(completed_story)

if __name__ == "__main__":
    play_madlibs()
