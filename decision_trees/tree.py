import questions
import sys, time

class Node(object):
    def __init__(self, parent=None, values=[], images=[], q_count=5):
        self.parent = parent
        self.values = values

        self.images       = images

        self.left_images  = [[] for i in xrange(q_count)]
        self.right_images = [[] for i in xrange(q_count)]

        self.left = None  # aboveNode
        self.right = None  # belowNode

        self.left_values = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for i in xrange(q_count)]
        self.right_values = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0] for i in xrange(q_count)]

        self.scores = []

        self.questions = [questions.Rectangle() for i in xrange(q_count)]

        # set on complete
        self.question = None
        self.question_index = None
        self.left_values_final = []
        self.right_values_final = []

        self.end = True

    def check(self, image):
        return self.getNext(self, image)

    def getNextEnd(self, node, image):
        result = node.parent.question.test(image)
        if result:
            return node.parent.left_values_final
        return node.parent.right_values_final

    def getNext(self, node, image):
        if node.end:
            return self.getNextEnd(node, image)
        if not node.question:
            return self.getNextEnd(node, image)

        result = node.question.test(image)

        if result:
            return self.getNext(node.left, image)
        else:
            return self.getNext(node.right, image)

    def score(self, q_index):
        left_side  = self.left_values[q_index]
        right_side = self.right_values[q_index]
        lsum = sum(left_side)
        rsum = sum(right_side)
        total = 0.0

        if not all([lsum, rsum]) or sum(self.values) == 0:
            return -1, 0

        for i, (left_x, right_x) in enumerate(zip(left_side, right_side)):
            prob_of_x = ((left_x * 1.0) / (lsum * 1.0)) + ((right_x * 1.0) / (rsum * 1.0))
            prob_of_input = self.values[i] / sum(self.values)

            expected_classification_gain = pow(prob_of_x - prob_of_input, 2) * self.values[i]

            total += expected_classification_gain

        return total, q_index

    def mutate(self, q_index, above, image, label):
        if above:
            self.left_images[q_index].append((label, image))
            self.left_values[q_index][label] += 1
        else:
            self.right_images[q_index].append((label, image))
            self.right_values[q_index][label] += 1

    def complete(self):
        q_cmp = lambda item: item[0]
        self.scores.sort(key=q_cmp)
        self.question_index = self.scores.pop(0)[1]

        self.question = self.questions[self.question_index] # question = questions[best_question_index]
        self.right_values_final = self.right_values[self.question_index]
        self.left_values_final = self.left_values[self.question_index]

        ## create new nodes
        if any(self.left_values_final) and any(self.right_values_final):
            self.left = Node(self, self.left_values_final, images=self.left_images[self.question_index])
            self.right = Node(self, self.right_values_final, images=self.right_images[self.question_index])
            self.end = False

    def trySerialize(self, node):
        if not node or not hasattr(node, "serialize"):
            return None
        return node.serialize()

    def serialize(self):
        if not self.question:
            return None
        return [self.question.serialize(), self.left_values_final, self.right_values_final, [self.trySerialize(self.left), self.trySerialize(self.right)]]


class TreeController(object):
    # todo serialize tree to json
    # todo run 100 tests for each level
    def __init__(self, training_files, question_count):
        self.training_files = training_files
        self.counts = {}

        for label, image in self.training_files:
            self.counts[label] = self.counts.get(label, 0) + 1


        self.root = Node(values=self.counts.values(), images=training_files, q_count=question_count)
        self.current_node = self.root

    def construct(self, depth):
        for label, image in self.training_files:
            self.counts[label] = self.counts.get(label, 0) + 1
        self.__construct(self.root, depth)

    def __construct(self, node, depth):
        if depth == 0:
            return  # break out if max depth is hit
        if not node:
            return  # node doesn't exist
        if node.images == []:
            return  # break if no images

        print "Running tests at level {0} with {1} images".format(depth, len(node.images))

        for q_index, _question in enumerate(node.questions):
            print "\t Executing test # {0}".format(q_index),
            start_time = time.time()
            for img_index, (label, image) in enumerate(node.images):
                result = _question.test(image)
                node.mutate(q_index, result, image, label)

            node.scores.append(node.score(q_index))

            print node.left_values[q_index], node.right_values[q_index], "executed in {0}".format(time.time()-start_time)

        node.complete()

        self.__construct(node.left, depth-1)
        self.__construct(node.right, depth-1)

    def serialize(self):
        return self.root.serialize()


