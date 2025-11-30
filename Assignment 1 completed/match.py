def match(pattern, source):
    """Attempt to match pattern to source. % matches a sequence of zero or
        more words and _ matches any single word.

    Args:
        pattern - a list of strings. % and/or _ are utilized as placeholder
                  to match/extract words from the source
        source - a list of string. A phrase/sentence/question represented as
                 a list of words (strings).

    Returns:
        if a match is detected, returns a list of strings - a list of matched
        words (words in the source corresponding to _'s or %'s, in the
        pattern, if any).
        else if no match is detected, returns None. 

    """
    pind = 0
    sind = 0
    result = []

   # while not at the end of the pattern OR not at the end of the source
    while pind < len(pattern) or sind < len(source):
        # 1 if at the end of the pattern
        if pind >= len(pattern):
            return None
        
        # 2 if the current thing in pattern is a %
        if pattern[pind] == "%":
            # if the % is at the end of the pattern
            if pind == len(pattern) - 1:
                # grab the rest of the source, add it to result, return result
                remaining = " ".join(source[sind:])
                result.append(remaining if remaining else "")
                return result
            else:
                # move along in pattern
                pind += 1
                # create a variable to accumulate stuff in
                accumulated = []
                # while current items in pattern and source are not equal
                while (pind < len(pattern) and sind < len(source) and 
                       pattern[pind] != source[sind]):
                    # accumulate from source
                    accumulated.append(source[sind])
                    # move along in source
                    sind += 1
                # if we ran out of items in source, then no match
                if sind >= len(source):
                    return None
                # add the accumulated item into result
                result.append(" ".join(accumulated) if accumulated else "")
        
        # 3 if we reached the end of the source
        elif sind >= len(source):
            return None
        
        # 4 if the current thing in the pattern is an _
        elif pattern[pind] == "_":
            # add item from source to result
            result.append(source[sind])
            # move along in pattern and source
            pind += 1
            sind += 1
        
        # 5 if the current thing in the pattern == the current thing in the source
        elif pattern[pind] == source[sind]:
            # move along in pattern and source
            pind += 1
            sind += 1
        
        # 6 else - thus current things are unequal
        else:
            return None
    
    return result

assert match(["x", "y", "z"], ["x", "y", "z"]) == [], "test 1 failed"
assert match(["x", "z", "z"], ["x", "y", "z"]) == None, "test 2 failed"
assert match(["x", "y"], ["x", "y", "z"]) == None, "test 3 failed"
assert match(["x", "y", "z", "z"], ["x", "y", "z"]) == None, "test 4 failed"
assert match(["x", "_", "z"], ["x", "y", "z"]) == ["y"], "test 5 failed"
assert match(["x", "_", "_"], ["x", "y", "z"]) == ["y", "z"], "test 6 failed"
assert match(["%"], ["x", "y", "z"]) == ["x y z"], "test 7 failed"
assert match(["x", "%", "z"], ["x", "y", "z"]) == ["y"], "test 8 failed"
assert match(["%", "z"], ["x", "y", "z"]) == ["x y"], "test 9 failed"
assert match(["x", "%", "y"], ["x", "y", "z"]) == None, "test 10 failed"
assert match(["x", "%", "y", "z"], ["x", "y", "z"]) == [""], "test 11 failed"
assert match(["x", "y", "z", "%"], ["x", "y", "z"]) == [""], "test 12 failed"
assert match(["_", "%"], ["x", "y", "z"]) == ["x", "y z"], "test 13 failed"
assert match(["_", "_", "_", "%"], ["x", "y", "z"]) == [
        "x",
        "y",
        "z",
        "",
    ], "test 14 failed"
assert match(["x", "%", "z"], ["x", "y", "z", "z", "z"]) == None, "test 15 failed"
