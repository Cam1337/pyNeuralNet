#!/usr/bin/env python
import sys, pprint, time
import mnist
from decision_trees import questions
from decision_trees import tree

def main_dep():
    mnist_files = mnist.MNIST("files/")
    mnist_files.load_training()

    test_files = zip(mnist_files.train_labels, mnist_files.train_images)

    while True: # 10 different things
        above = [0,0,0,0,0,0,0,0,0,0]
        below = [0,0,0,0,0,0,0,0,0,0]
        q = questions.Rectangle()
        for label, image in test_files:
            above_t = q.test(image)
            if above_t:
                above[label] += 1
            else:
                below[label] += 1
        #print "[{0} above | {1} below] with x:{2} y:{3} w:{4} h:{5} t:{6}".format(below, above, q.x, q.y, q.w, q.h, q.t)
        gains = []
        for a, b in zip(above, below):
            total = (a + b) * 1.0
            gains.append("{:.2f}".format(abs((a/total) - (b/total))))
        gains = map(float, gains)
        print gains


def processResult(result, mnist_cls, label, image, serial):
    print mnist_cls.display(image)
    print "The image is a {0}".format(label)
    print "Best guess for the image is : {0} with a {1} assurance.".format(result.index(max(result)), max(result) / (1.0 * sum(result)))
    print "These are the other percentages:"
    s_results = list(enumerate(result))
    s_results.sort(key=lambda i: i[1], reverse=True)
    print s_results
    for i,r in s_results:
        guess = r / (1.0 * sum(result))
        print "\t{0} -> {1}".format(i, guess)
    fname = "tree_{0}.txt".format(time.time())
    open(fname, "w").write(pprint.pformat(serial))
    print "Wrote tree to file {0}".format(fname)



def main():
    mnist_files = mnist.MNIST("files/")

    mnist_files.load_training()
    mnist_files.load_testing()

    train_files = zip(mnist_files.train_labels, mnist_files.train_images)
    test_files  = zip(mnist_files.test_labels, mnist_files.test_images)

    controller = tree.TreeController(train_files, question_count=500);
    controller.construct(10)

    print controller.serialize()

    result = controller.root.check(test_files[0][1])

    processResult(result, mnist_files, test_files[0][0], test_files[0][1], controller.serialize())


if __name__ == "__main__":
    main()