import itertools
from PrettyPrint import PrettyPrintTree

print_tree = PrettyPrintTree(
    lambda x: x.get_subtrees(),
    lambda x: x.get_guess(),
    lambda x: x.get_feedback(),
    orientation=PrettyPrintTree.Vertical
)


def generate_possible_sequences(options, length=-1):
    return set(itertools.permutations(options, len(options) if length == -1 else length))


_feedback_counter = 0
def get_feedback(guess, solution):
    global _feedback_counter
    _feedback_counter += 1
    return sum(1 for g, s in zip(guess, solution) if g == s)


############# Custom strategy ###############

# globals
INVALID = 3
feedbacks = [None] * 5

guess_LUT = {}
left_right_LUT = {}

INVALID2 = 5
feedbacks2 = [None] * 4
guess_LUT2 = {}
half_LUT = {}
feedback_offset = 0


def custom_strategy(solution):
    global _feedback_counter, feedback_offset, feedbacks, feedbacks2
    _feedback_counter = 0
    feedback_offset = _feedback_counter
    feedbacks = [None] * 5

    left, right = stage1(solution)
    left_right_LUT[tuple(feedbacks)] = tuple(left + right)

    feedbacks2 = [None] * 4
    feedback_offset = _feedback_counter
    half_LUT[tuple(feedbacks2)] = stage2(solution[:4], left)

    feedbacks2 = [None] * 4
    feedback_offset = _feedback_counter
    half_LUT[tuple(feedbacks2)] = stage2(solution[4:], right, final=True)
    return

def stage1(solution):
    left = []
    right = []
    first3guesses(solution, left, right)
    if len(left) == 0:  # all feedbacks are 1 -> 12 34 56 78
        guess = (1, 1, 1, 1, 3, 3, 3, 3)
        feedback = guess_(solution, guess)

        if feedback == 0:
            left += [3, 4]
            right += [1, 2]
        elif feedback == 2:
            left += [1, 2]
            right += [3, 4]
        else:
            guess = (1, 1, 1, 1, 5, 5, 5, 5)
            feedback = guess_(solution, guess)
            if feedback == 0:
                left += [5, 6, 7, 8]
                right += [1, 2, 3, 4]
                return left, right
            elif feedback == 2:
                left += [1, 2, 3, 4]
                right += [5, 6, 7, 8]
                return left, right
            else:
                assert False

        guess = (5, 5, 5, 5, 7, 7, 7, 7)
        feedback = guess_(solution, guess)
        if feedback == 0:
            left += [7, 8]
            right += [5, 6]
        elif feedback == 2:
            left += [5, 6]
            right += [7, 8]
        else:
            assert False
        assert len(left) == len(right) == 4
        return left, right

    elif len(left) == 1 and left[0] in (5, 6):  # 12? 34? 5|6 7|8?
        guess = (1, 1, 1, 1, 3, 3, 3, 3)
        feedback = guess_(solution, guess)
        if feedback == 0:
            left += [3, 4]
            right += [1, 2]
        elif feedback == 2:
            left += [1, 2]
            right += [3, 4]
        else:
            assert False

        guess = (7, 7, 7, 7, 8, 8, 8, 8)
        feedback = guess_(solution, guess)
        if feedback == 0:
            left += [8]
            right += [7]
        elif feedback == 2:
            left += [7]
            right += [8]
        else:
            assert False

        return left, right

    elif len(left) == 1 and left[0] in (3, 4):  # 12|56? 3|4 7|8?
        guess = (7, 7, 7, 7, 8, 8, 8, 8)
        feedback = guess_(solution, guess)
        if feedback == 0:
            left += [8]
            right += [7]
        elif feedback == 2:
            left += [7]
            right += [8]
        else:
            assert False

        guess = (1, 1, 1, 1, 5, 5, 5, 5)
        feedback = guess_(solution, guess)
        if feedback == 0:
            left += [5, 6]
            right += [1, 2]
        elif feedback == 2:
            left += [1, 2]
            right += [5, 6]
        else:
            assert False

        return left, right

    elif len(left) == 2 and left[0] in (3, 4) and left[1] in (5, 6):
        guess = (1, 1, 1, 1, 7, 7, 7, 7)
        feedback = guess_(solution, guess)
        if feedback == 0:
            left += [7, 8]
            right += [1, 2]
        elif feedback == 2:
            left += [1, 2]
            right += [7, 8]
        else:
            assert False

        return left, right

    elif len(left) == 1 and left[0] in (1, 2):  # 1|2 34 56 7|8?
        guess = (7, 7, 7, 7, 8, 8, 8, 8)
        feedback = guess_(solution, guess)
        if feedback == 0:
            left += [8]
            right += [7]
        elif feedback == 2:
            left += [7]
            right += [8]
        else:
            assert False

        guess = (3, 3, 3, 3, 5, 5, 5, 5)
        feedback = guess_(solution, guess)
        if feedback == 0:
            left += [5, 6]
            right += [3, 4]
        elif feedback == 2:
            left += [3, 4]
            right += [5, 6]
        else:
            assert False

        return left, right

    elif len(left) == 2 and left[0] in (1, 2) and left[1] in (5, 6):
        guess = (3, 3, 3, 3, 7, 7, 7, 7)
        feedback = guess_(solution, guess)
        if feedback == 0:
            left += [7, 8]
            right += [3, 4]
        elif feedback == 2:
            left += [3, 4]
            right += [7, 8]
        else:
            assert False

        return left, right

    elif len(left) == 2 and left[0] in (1, 2) and left[1] in (3, 4):
        guess = (5, 5, 5, 5, 7, 7, 7, 7)
        feedback = guess_(solution, guess)
        if feedback == 0:
            left += [7, 8]
            right += [5, 6]
        elif feedback == 2:
            left += [5, 6]
            right += [7, 8]
        else:
            assert False

        return left, right

    elif len(left) == 3:
        guess = (7, 7, 7, 7, 8, 8, 8, 8)
        feedback = guess_(solution, guess)
        if feedback == 0:
            left += [8]
            right += [7]
        elif feedback == 2:
            left += [7]
            right += [8]
        else:
            assert False
        return left, right

    else:
        assert False

def first3guesses(solution, left, right):
    for i in range(0, 3, 1):
        guess = tuple(1 +2*i + j // 4 for j in range(0, 8))
        feedback = guess_(solution, guess)

        if feedback == 0:
            left.append(guess[4])
            right.append(guess[0])
        elif feedback == 2:
            left.append(guess[0])
            right.append(guess[4])

def guess_(solution, guess):
    if tuple(feedbacks) not in guess_LUT:
        guess_LUT[tuple(feedbacks)] = guess
    feedback = get_feedback(guess, solution)
    feedbacks[_feedback_counter-1] = feedback
    return feedback

def stage2(solution, parts, final=False):
    a, b, c, d = (0, 1, 2, 3)

    guess = (a, a, b, b)
    feedback = guess_2(solution, guess, parts)
    if feedback == 0:
        guess = (d, b, a, d)
        feedback = guess_2(solution, guess, parts)
        if feedback == 0:
            guess = (b, c, d, a)
            feedback = guess_2(solution, guess, parts)
            if feedback != 4:
                guess = (b, d, c, a)
                if final:
                    feedback = guess_2(solution, guess, parts)
                    assert feedback == 4
            return guess
        elif feedback == 1:
            guess = (c, b, d, a)
            feedback = guess_2(solution, guess, parts)
            if feedback != 4:
                guess = (b, d, a, c)
                if final:
                    feedback = guess_2(solution, guess, parts)
                    assert feedback == 4
            return guess
        elif feedback == 2:
            guess = (d, b, c, a)
            feedback = guess_2(solution, guess, parts)
            if feedback != 4:
                guess = (b, c, a, d)
                if final:
                    feedback = guess_2(solution, guess, parts)
                    assert feedback == 4
            return guess
        elif feedback == 3:
            guess = (d, b, a, c)
            feedback = guess_2(solution, guess, parts)
            if feedback != 4:
                guess = (c, b, a, d)
                if final:
                    feedback = guess_2(solution, guess, parts)
                    assert feedback == 4
            return guess
        else:
            assert False
    elif feedback == 1:
        guess = (b, a, a, c)
        feedback = guess_2(solution, guess, parts)
        if feedback == 0:
            guess = (c, d, b, a)
            feedback = guess_2(solution, guess, parts)
            if feedback == 0:
                guess = (a, b, c, d)
                if final:
                    feedback = guess_2(solution, guess, parts)
                    assert feedback == 4
            elif feedback == 2:
                guess = (d, c, b, a)
                if final:
                    feedback = guess_2(solution, guess, parts)
                    assert feedback == 4
            else:
                assert feedback == 4
            return guess
        elif feedback == 1:
            guess = (c, d, a, b)
            feedback = guess_2(solution, guess, parts)
            if feedback == 0:
                guess = (a, b, d, c)
                if final:
                    feedback = guess_2(solution, guess, parts)
                    assert feedback == 4
            elif feedback == 2:
                guess = (d, c, a, b)
                if final:
                    feedback = guess_2(solution, guess, parts)
                    assert feedback == 4
            else:
                assert feedback == 4
            return guess
        elif feedback == 2:
            guess = (b, a, c, d)
            if final:
                feedback = guess_2(solution, guess, parts)
                assert feedback == 4
            return guess
        elif feedback == 3:
            guess = (b, a, d, c)
            if final:
                feedback = guess_2(solution, guess, parts)
                assert feedback == 4
            return guess
        else:
            assert False
    elif feedback == 2:
        guess = (a, d, d, b)
        feedback = guess_2(solution, guess, parts)
        if feedback == 0:
            guess = (d, a, b, c)
            feedback = guess_2(solution, guess, parts)
            if feedback != 4:
                guess = (c, a, b, d)
                if final:
                    feedback = guess_2(solution, guess, parts)
                    assert feedback == 4
            return guess
        elif feedback == 1:
            guess = (d, a, c, b)
            feedback = guess_2(solution, guess, parts)
            if feedback != 4:
                guess = (a, c, b, d)
                if final:
                    feedback = guess_2(solution, guess, parts)
                    assert feedback == 4
            return guess
        elif feedback == 2:
            guess = (a, d, b, c)
            feedback = guess_2(solution, guess, parts)
            if feedback != 4:
                guess = (c, a, d, b)
                if final:
                    feedback = guess_2(solution, guess, parts)
                    assert feedback == 4
            return guess
        elif feedback == 3:
            guess = (a, c, d, b)
            feedback = guess_2(solution, guess, parts)
            if feedback != 4:
                guess = (a, d, c, b)
                if final:
                    feedback = guess_2(solution, guess, parts)
                    assert feedback == 4
            return guess
        else:
            assert False
    else:
        assert False

def guess_2(solution, guess, parts, last_feedback=False):
    if tuple(feedbacks2) not in guess_LUT2:
        guess_LUT2[tuple(feedbacks2)] = guess, last_feedback
    feedback = get_feedback(tuple(parts[i] for i in guess), solution)
    feedbacks2[_feedback_counter-feedback_offset-1] = feedback #+ (4 if last_feedback and feedback < 4 else 0)
    return feedback


########## Decision tree from LUT #########

class TreeNode:
    def __init__(self, guess, feedback):
        self.guess = guess
        self.feedback = feedback
        self.children = {}

    def get_subtrees(self):
        return self.children.values()

    def get_guess(self):
        return "".join(str(x) for x in self.guess)

    def get_feedback(self):
        return "" if self.feedback is None else str(self.feedback)



def build_decision_tree():
    root = TreeNode(guess_LUT[tuple(None for _ in range(5))], None)
    for key, val in guess_LUT.items():
        node = root
        for i, feedback in enumerate(key):
            if feedback is None:
                break
            if feedback not in node.children:
                node.children[feedback] = TreeNode(val, feedback)
            node = node.children[feedback]

    return root


########## Games using LUT #########

def verify_all_solutions():
    global _feedback_counter
    seqs = generate_possible_sequences((1, 2, 3, 4, 5, 6, 7, 8))
    tries = 0
    for sol in seqs:
        _feedback_counter = 0
        g = custom_strategy(sol)    # TODO
        if g != sol:
            print(f"Solution: {sol}, Guess: {g}")
        tries += _feedback_counter
    print(f"Average number of tries: {tries / len(seqs)}")
    return