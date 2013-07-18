import random, sys
import utils
import pprint


class Rectangle(object):
    def __init__(self, x=None, y=None, w=None, h=None, t=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.t = t
        if not any([x,y,w,h,t]):
            self.x, self.y, self.w, self.h, self.t = self.randomize()

    def randomize(self):
        x, y = random.randint(1,27), random.randint(1,27)
        w = random.randint(1, 28-x)
        h = random.randint(1, 28-y)
        t = random.randint(0, w*h)
        return (x,y,w,h,t)

    def test(self, image):
        count = 0
        for x in xrange(self.x, self.w + self.x):
            for y in xrange(self.y, self.h + self.y):
                pixel = image[x+y*28]
                if pixel != 0:
                    count +=1
        return count > self.t

    def serialize(self):
        return ",".join(map(str, [self.x, self.y, self.w, self.h, self.t]))


error = """
Traceback (most recent call last):
  File "main.py", line 49, in <module>
    main()
  File "main.py", line 39, in main
    node = controller.root.check(test_files[1][0])
  File "/home/iso/pyNeuralNet/decision_trees/tree.py", line 31, in check
    return self.getNext(self, image)
  File "/home/iso/pyNeuralNet/decision_trees/tree.py", line 37, in getNext
    result = node.question.test(image)
  File "/home/iso/pyNeuralNet/decision_trees/questions.py", line 27, in test
    pixel = image[x+y*28]
TypeError: 'int' object has no attribute '__getitem__'
"""