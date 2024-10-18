from poop_db import coordMatrix
from typing import List, Tuple, Callable, Any
import math

def match(pattern: List[str], source: List[str]) -> List[str]:
    """Attempt to match pattern to source

    % matches a sequence of zero or more words and _ matches any single word

    Args:
        pattern - a pattern using to % and/or _ to extract words from the source
        source - a phrase represented as a list of words (strings)

    Returns:
        None if the pattern and source do not "match" ELSE A list of matched words
        (words in the source corresponding to _'s or %'s, in the pattern, if any)
    """
    sind = 0  # current index we are looking at in the source list
    pind = 0  # current index we are looking at in the pattern list
    result: List[str] = []  # to store the substitutions that we will return if matched

    # keep checking as long as we haven't hit the end of both pattern and source while
    # pind is still a valid index OR sind is still a valid index (valid index means that
    # the index is != to the length of the list)
    while pind != len(pattern) or sind != len(source):
        # 1) check to see if we are at the end of the pattern (from the while condition
        # we know since we already checked to see if you were at the end of the pattern
        # and the source, then you know that if this is True, then the pattern has
        # ended, but the source has not) if we reached the end of the pattern but not
        # source then no match
        if pind == len(pattern):
            return None

        # 2) check to see if the current thing in the pattern is a %
        elif pattern[pind] == "%":
            # at end of pattern grab the rest of the source
            if pind == (len(pattern) - 1):
                return result + [" ".join(source[sind:])]
            else:
                accum = ""
                pind += 1
                while pattern[pind] != source[sind]:
                    accum += " " + source[sind]
                    sind += 1

                    # abort in case we've run out of source with more pattern left
                    if sind >= len(source):
                        return None

                result.append(accum.strip())

        # 3) if we reached the end of the source but not pattern then no match
        elif sind == len(source):
            return None

        # 4) check to see if the current thing in the pattern is an _
        elif pattern[pind] == "_":
            # neither has ended: add a singleton
            result += [source[sind].strip()]
            pind += 1
            sind += 1

        # 5) check to see if the current thing in the pattern is the same as the current
        # thing in the source
        elif pattern[pind] == source[sind]:
            # neither has ended and the words match, continue checking
            pind += 1
            sind += 1

        # 6) this will happen if none of the other conditions are met
        else:
            # neither has ended and the words do not match, no match
            return None

    return result

def coordDistance(lon1, lat1, lon2, lat2):
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lon1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lon2)

    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    a = (math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2)
    c = 2 * math.asin(math.sqrt(a))

    radius_miles = 3956 #r of earth in miles

    distance = radius_miles * c
    return distance

def inChicago(userlon, userlat): 
    if coordDistance(userlon,userlat,41.8781,-87.6298) <= 12.5:
        return True
    else:
        return False
    
def poopByRadius(userlon, userlat, radius) -> int:
    if inChicago(userlon,userlat) == True: 
        count = 0
        for plon,plat in coordMatrix:
            if coordDistance(userlon,userlat,plon,plat) <= radius:
                count += 1
        print(count)
        return count
    else:
        return "Your location is not in Chicago."

def amIStandingOnPoop(userlon, userlat):
    if inChicago(userlon,userlat) == True: 
        for plon,plat in coordMatrix:
            if coordDistance(userlon,userlat,plon,plat) <= 0.0006:
                return True
            else: 
                return False
    else:
        return "Your location is not in Chicago."

def bye_action(dummy: List[str]) -> None:
    raise KeyboardInterrupt

pa_list: List[Tuple[List[str], Callable[[List[str]], List[Any]]]] = [
    (str.split("How many poops are with a radius of _ miles"), poopByRadius),
    (str.split("Am I standing on poop if I'm at %"), amIStandingOnPoop),
    (["bye"], bye_action),
]


def search_pa_list(src: List[str]) -> List[str]:
    """Takes source, finds matching pattern and calls corresponding action. If it finds
    a match but has no answers it returns ["No answers"]. If it finds no match it
    returns ["I don't understand"].

    Args:
        source - a phrase represented as a list of words (strings)

    Returns:
        a list of answers. Will be ["I don't understand"] if it finds no matches and
        ["No answers"] if it finds a match but no answers
    """
    for pat, act in pa_list:
        val = match(pat,src)
        if val != None:
            result = act(val)
            if not result:
                return ["No answers"]
            return result
    else:
            return ["I don't understand"]


def query_loop() -> None:
    """The simple query loop. The try/except structure is to catch Ctrl-C or Ctrl-D
    characters and exit gracefully.
    """
    print("Welcome to the movie database!\n")
    while True:
        try:
            print()
            query = input("Your query? ").replace("?", "").lower().split()
            answers = search_pa_list(query)
            for ans in answers:
                print(ans)

        except (KeyboardInterrupt, EOFError):
            break

    print("\nBye!\n")




if __name__ == "__main__":
    assert isinstance(poopByRadius([41.983, -87.6598, 0.095]), int), "poopByRadius not returning an int"
    assert sorted(poopByRadius([41.983, -87.6598,0.095])) == sorted(
        [0]
    ), "failed poopByRadius test"
    assert isinstance(poopByRadius)

    assert isinstance(amIStandingOnPoop([41.983, -87.6598]), bool), "amIStandingOnPoop not returning a list"
    assert sorted(amIStandingOnPoop([41.983, -87.6598])) == sorted(
        [False]
    ), "failed amIStandingOnPoop"

    assert isinstance(poopByRadius([41.965304, -87.665429, 0.095]), int), "poopByRadius not returning an int"
    assert sorted(poopByRadius([41.965304, -87.665429,0.095])) == sorted(
        [1]
    ), "failed poopByRadius test1"
    assert isinstance(poopByRadius)

    assert isinstance(amIStandingOnPoop([41.776862402207, -87.72028639493]), bool), "amIStandingOnPoop not returning a list"
    assert sorted(amIStandingOnPoop([41.776862402207, -87.72028639493])) == sorted(
        [True]
    ), "failed amIStandingOnPoop1"

    assert isinstance(poopByRadius([0, 0, 1]), str), "poopByRadius not returning an int"
    assert sorted(poopByRadius([0, 0, 1])) == sorted(
        ["Your location is not in Chicago."]
    ), "failed poopByRadius test1"
    assert isinstance(poopByRadius)
    
    print("All tests passed!")

    