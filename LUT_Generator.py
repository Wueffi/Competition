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


############# Custom strategy ###############

class LUT_Generator:
    def __init__(self):
        self.guess_LUT = {}
        self.left_right_LUT = {}
        self.guess_LUT2 = {}
        self.solution = None
        self.feedbacks = []
        self.feedbacks2 = []

        self.luts: tuple[
                       dict[tuple[int, ...], tuple[int, int]],
                       dict[tuple[int, ...], tuple[int, ...]],
                       dict[tuple[int, ...], tuple[int, ...]]
                   ] | None = None
        return

    def guess(self, guess):
        feedbacks = tuple(self.feedbacks)
        if feedbacks not in self.guess_LUT:
            self.guess_LUT[feedbacks] = guess
        feedback = sum(1 for g, s in zip(guess, self.solution) if g == s)
        self.feedbacks.insert(0, feedback)
        return feedback

    def guess_half(self, guess, mappings, first_half: bool, certain=False):
        """first_half: True if it's the first half of the stage 2 guess and False if it's the second half
        certain: True if the guess is certain to be correct and False if it's not certain.
        "certain" guesses must be guessed anyway in the second half of the stage 2
        """
        feedbacks = tuple(self.feedbacks2)

        if feedbacks not in self.guess_LUT2:
            self.guess_LUT2[feedbacks] = guess, certain

        check_against = self.solution[:4] if first_half else self.solution[4:]
        feedback = sum(1 for g, s in zip([mappings[i] for i in guess], check_against) if g == s)
        self.feedbacks2.insert(0, feedback)
        return feedback

    def finish_stage1(self, left, right):
        self.stage1_len = len(self.feedbacks)
        self.left_right_LUT[tuple(self.feedbacks)] = tuple(left + right)
        return

    def finish_stage2(self, half):
        if tuple(self.feedbacks2) not in self.guess_LUT2 and self.feedbacks2[0] != 4:   # no point in guessing after a 4
            self.guess_LUT2[tuple(self.feedbacks2)] = half, True
        self.feedbacks2 = []
        return

    def generate_LUT(self) -> tuple[dict[tuple[int, ...], tuple[int, int]], dict[tuple[int, ...], tuple[int, ...]], dict[tuple[int, ...], tuple[int, ...]]]:
        """Returns:
        1. LUT for guesses of stage 1
        2. LUT for left-right mapping
        3. LUT for guesses of stage 2
        """
        if self.luts is not None:
            return self.luts

        self.reset_LUT()

        # run every game
        for sol in generate_possible_sequences(tuple(i for i in range(1, 8+1))):
            self.new_game(sol)
            custom_strategy(self)

        new_dict = {}
        for key, val in self.guess_LUT.items():
            new_key = list(key)
            while len(new_key) < 5:
                new_key.append(3)

            new_dict[tuple(new_key)] = (val[0], val[4])

        new_dict2 = {}
        for key, val in self.left_right_LUT.items():
            new_key = list(key)
            while len(new_key) < 5:
                new_key.append(3)

            new_dict2[tuple(new_key)] = val

        new_dict3 = {}
        for key, val in self.guess_LUT2.items():
            new_key = list(key)
            while len(new_key) < 4:
                new_key.append(5)

            new_dict3[tuple(new_key)] = val[0] + (int(val[1]),)

        return new_dict, new_dict2, new_dict3

    def print_LUTs(self):
        self.generate_LUT() # making sure they are generated

        print("Stage1 LUT:")
        d = self.guess_LUT | self.left_right_LUT
        print_tree(build_decision_tree(d, 3))
        print("\nStage2 LUT:")
        print_tree(build_decision_tree(self.guess_LUT2, 5))
        return

    def reset_LUT(self):
        self.guess_LUT = {}
        self.left_right_LUT = {}
        self.guess_LUT2 = {}
        self.luts = None
        return

    def new_game(self, solution):
        self.solution = solution
        self.feedbacks = []
        self.feedbacks2 = []
        return


def custom_strategy(lut_gen: LUT_Generator):
    left, right = stage1(lut_gen)
    lut_gen.finish_stage1(left, right)

    half1 = stage2(lut_gen, left)
    lut_gen.finish_stage2(half1)

    half2 = stage2(lut_gen, right, final=True)
    #lut_gen.finish_stage2(half2)
    return half1 + half2

def stage1(lut_gen: LUT_Generator):
    left = []
    right = []
    first3guesses(lut_gen, left, right)
    if len(left) == 0:  # all feedbacks are 1 -> 12 34 56 78
        guess = (1, 1, 1, 1, 3, 3, 3, 3)
        feedback = lut_gen.guess(guess)

        if feedback == 0:
            left += [3, 4]
            right += [1, 2]
        elif feedback == 2:
            left += [1, 2]
            right += [3, 4]
        else:
            guess = (1, 1, 1, 1, 5, 5, 5, 5)
            feedback = lut_gen.guess(guess)
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
        feedback = lut_gen.guess(guess)
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
        feedback = lut_gen.guess(guess)
        if feedback == 0:
            left += [3, 4]
            right += [1, 2]
        elif feedback == 2:
            left += [1, 2]
            right += [3, 4]
        else:
            assert False

        guess = (7, 7, 7, 7, 8, 8, 8, 8)
        feedback = lut_gen.guess(guess)
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
        feedback = lut_gen.guess(guess)
        if feedback == 0:
            left += [8]
            right += [7]
        elif feedback == 2:
            left += [7]
            right += [8]
        else:
            assert False

        guess = (1, 1, 1, 1, 5, 5, 5, 5)
        feedback = lut_gen.guess(guess)
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
        feedback = lut_gen.guess(guess)
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
        feedback = lut_gen.guess(guess)
        if feedback == 0:
            left += [8]
            right += [7]
        elif feedback == 2:
            left += [7]
            right += [8]
        else:
            assert False

        guess = (3, 3, 3, 3, 5, 5, 5, 5)
        feedback = lut_gen.guess(guess)
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
        feedback = lut_gen.guess(guess)
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
        feedback = lut_gen.guess(guess)
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
        feedback = lut_gen.guess(guess)
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

def first3guesses(lut_gen, left, right):
    for i in range(0, 3, 1):
        guess = tuple(1 +2*i + j // 4 for j in range(0, 8))
        feedback = lut_gen.guess(guess)

        if feedback == 0:
            left.append(guess[4])
            right.append(guess[0])
        elif feedback == 2:
            left.append(guess[0])
            right.append(guess[4])

def stage2(lut_gen: LUT_Generator, parts, final=False):
    a, b, c, d = (0, 1, 2, 3)

    guess = (a, a, b, b)
    feedback = lut_gen.guess_half(guess, parts, not final)
    if feedback == 0:
        guess = (d, b, a, d)
        feedback = lut_gen.guess_half(guess, parts, not final)
        if feedback == 0:
            guess = (b, c, d, a)
            feedback = lut_gen.guess_half(guess, parts, not final)
            if feedback != 4:
                guess = (b, d, c, a)
                if final:
                    feedback = lut_gen.guess_half(guess, parts, not final, True)
                    assert feedback == 4
            return guess
        elif feedback == 1:
            guess = (c, b, d, a)
            feedback = lut_gen.guess_half(guess, parts, not final)
            if feedback != 4:
                guess = (b, d, a, c)
                if final:
                    feedback = lut_gen.guess_half(guess, parts, not final, True)
                    assert feedback == 4
            return guess
        elif feedback == 2:
            guess = (d, b, c, a)
            feedback = lut_gen.guess_half(guess, parts, not final)
            if feedback != 4:
                guess = (b, c, a, d)
                if final:
                    feedback = lut_gen.guess_half(guess, parts, not final, True)
                    assert feedback == 4
            return guess
        elif feedback == 3:
            guess = (d, b, a, c)
            feedback = lut_gen.guess_half(guess, parts, not final)
            if feedback != 4:
                guess = (c, b, a, d)
                if final:
                    feedback = lut_gen.guess_half(guess, parts, not final, True)
                    assert feedback == 4
            return guess
        else:
            assert False
    elif feedback == 1:
        guess = (b, a, a, c)
        feedback = lut_gen.guess_half(guess, parts, not final)
        if feedback == 0:
            guess = (c, d, b, a)
            feedback = lut_gen.guess_half(guess, parts, not final)
            if feedback == 0:
                guess = (a, b, c, d)
                if final:
                    feedback = lut_gen.guess_half(guess, parts, not final, True)
                    assert feedback == 4
            elif feedback == 2:
                guess = (d, c, b, a)
                if final:
                    feedback = lut_gen.guess_half(guess, parts, not final, True)
                    assert feedback == 4
            else:
                assert feedback == 4
            return guess
        elif feedback == 1:
            guess = (c, d, a, b)
            feedback = lut_gen.guess_half(guess, parts, not final)
            if feedback == 0:
                guess = (a, b, d, c)
                if final:
                    feedback = lut_gen.guess_half(guess, parts, not final, True)
                    assert feedback == 4
            elif feedback == 2:
                guess = (d, c, a, b)
                if final:
                    feedback = lut_gen.guess_half(guess, parts, not final, True)
                    assert feedback == 4
            else:
                assert feedback == 4
            return guess
        elif feedback == 2:
            guess = (b, a, c, d)
            if final:
                feedback = lut_gen.guess_half(guess, parts, not final)
                assert feedback == 4
            return guess
        elif feedback == 3:
            guess = (b, a, d, c)
            if final:
                feedback = lut_gen.guess_half(guess, parts, not final)
                assert feedback == 4
            return guess
        else:
            assert False
    elif feedback == 2:
        guess = (a, d, d, b)
        feedback = lut_gen.guess_half(guess, parts, not final)
        if feedback == 0:
            guess = (d, a, b, c)
            feedback = lut_gen.guess_half(guess, parts, not final)
            if feedback != 4:
                guess = (c, a, b, d)
                if final:
                    feedback = lut_gen.guess_half(guess, parts, not final, True)
                    assert feedback == 4
            return guess
        elif feedback == 1:
            guess = (d, a, c, b)
            feedback = lut_gen.guess_half(guess, parts, not final)
            if feedback != 4:
                guess = (a, c, b, d)
                if final:
                    feedback = lut_gen.guess_half(guess, parts, not final, True)
                    assert feedback == 4
            return guess
        elif feedback == 2:
            guess = (a, d, b, c)
            feedback = lut_gen.guess_half(guess, parts, not final)
            if feedback != 4:
                guess = (c, a, d, b)
                if final:
                    feedback = lut_gen.guess_half(guess, parts, not final, True)
                    assert feedback == 4
            return guess
        elif feedback == 3:
            guess = (a, c, d, b)
            feedback = lut_gen.guess_half(guess, parts, not final)
            if feedback != 4:
                guess = (a, d, c, b)
                if final:
                    feedback = lut_gen.guess_half(guess, parts, not final, True)
                    assert feedback == 4
            return guess
        else:
            assert False
    else:
        assert False


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


def build_decision_tree(guess_LUT, empty_element):
    root = TreeNode(guess_LUT[tuple(empty_element for _ in next(iter(guess_LUT.keys())))], None)
    for key, val in guess_LUT.items():
        node = root
        for feedback in reversed(key):
            if feedback is empty_element:
                continue
            if feedback not in node.children:
                #node.children[feedback] = TreeNode(val if len(val) != 2 else val[0]+(f"|{val[1]}",), feedback)
                node.children[feedback] = TreeNode(val, feedback)
            node = node.children[feedback]

    return root


########## Games using LUT #########
"""
def guess_w_LUT1(solution):
    if tuple(feedbacks) in guess_LUT:
        guess = guess_LUT[tuple(feedbacks)]
        feedback = get_feedback(solution, guess)
        feedbacks[_feedback_counter - 1] = feedback
        return feedback
    return None

def guess_w_LUT2(solution, parts, first_half=False):
    if tuple(feedbacks2) in guess_LUT2:
        guess, final = guess_LUT2[tuple(feedbacks2)]
        actual_guess = tuple(parts[i] for i in guess)
        if final and first_half:
            return None
        feedback = get_feedback(solution, actual_guess)
        feedbacks2[_feedback_counter - feedback_offset - 1] = feedback
        return feedback
    return None

def verify_all_solutions():
    seqs = generate_possible_sequences(tuple(i for i in range(1, 8+1)))
    tries = 0
    for sol in seqs:
        g = custom_strategy(None)
        if g != sol:
            print(f"Solution: {sol}, Guess: {g}")
        tries += _feedback_counter
    print(f"Average number of tries: {tries / len(seqs)}")
    return
"""