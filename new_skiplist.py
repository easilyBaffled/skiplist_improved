from random import uniform
class SkipNode:
    """
    A simple node, containing the value and a tower
    """
    def __init__(self, node_key=None, node_value=None, tower_height=0):
        """
        Initialize node
        @param tower_height: tower height
        @type tower_height: int
        @param node_key: key of the node
        @param node_value: value in the node
        """
        self.tower = [None]*tower_height
        self.height = tower_height
        self.skip_index = [1] + [0] * self.height
        self.node_key = node_key
        self.node_value = node_value
        self.use_frequency = 0

    def __str__(self):
        output = str(self.node_key) + ", " + str(self.node_value) + "\t"
        for level in range(self.height):
            output += "-"
        return output

    def tower_str(self):
        """
        Prints the tower of the node
        :return:
        """
        output = ""
        for elem in self.tower:
            output += str(elem) + ", "
        return output

    def __len__(self):
        """
        Returns the height of the tower
        """
        return self.height

EXISTING_KEY = 0


class SkipList:
    def __init__(self, max_height=16, probability= 0.5):
        """
        Initializes a new Skiplist, starting with
        a head and tail sentinel with negative and positive infinity as keys and values
        :param max_height: The heighest a tower can be
        :param probability: The probability of a new tower height
        """
        self.max_height = max_height
        self.head = SkipNode(float("-inf"), float("-inf"), self.max_height)

        self.tail = SkipNode(float("inf"), float("inf"), self.max_height)
        for index in range(self.max_height):
            self.head.tower[index] = self.tail
        self.count = 0
        self.number_of_elements = 0
        self.probability = probability

    def __str__(self):
        output = str(self.head) + "\n"
        current_node = self.head
        for index in range(self.number_of_elements):
            current_node = current_node.tower[0]
            output += str(current_node) + "\n"
        output += str(self.tail) + "\n"
        return output

    def random_height(self):
        """
        Returns a random height that is less than the max height.
        There is also a random bound that is related to the number of values in the list
        """
        height = 1
        while height < self.max_height and uniform(0.0, self.probability + 0.1) < self.probability:
            height += 1
        return height

    def generate_look_back_tower(self, key):
        """
        Creates a tower, marking the path to get to a node
        @param key: the key of the node you are looking for
        """
        look_back_tower = [None] * (self.max_height + 1)
        current_node = self.head
        for index in reversed(range(self.count)):
            while current_node is not None and current_node.tower[index ].node_key < key:
                current_node = current_node.tower[index]
            look_back_tower[index] = current_node
        return look_back_tower

    def search(self, key):
        """
        Finds the key in the list, and returns the node that holds the key
        @param key: key you are searching for
        """
        look_back_tower = self.generate_look_back_tower(key)
        node = look_back_tower[0]
        possible_key = node.tower[0].node_key
        if key == possible_key:
            return node.tower[0]

    def search_with_frequency(self, key):
        """
        Finds the key in the list, and returns the node that holds the key
        @param key: key you are searching for
        """
        look_back_tower = self.generate_look_back_tower(key)
        node = look_back_tower[0]
        found_node = node.tower[0]
        possible_key = found_node.node_key
        if key == possible_key:
            if found_node.use_frequency > 5:
                found_node.use_frequency = 0
                self.increase_node_tower(found_node)
            else:
                found_node.use_frequency += 1
            return found_node

    def increase_node_tower(self, node):
        height = node.height
        if height + 1 < self.max_height:
            key = node.node_key
            current_node = self.head
            while current_node is not None and (current_node.height >= height + 1 and current_node.tower[height+1].node_key < key):
                current_node = current_node.tower[height+1]
            node.height += 1
            current_node.tower[height + 1] = node
            node.tower.append(current_node.tower[height + 1])
            if self.count < height + 1:
                self.count = height + 1

    def insert(self, key, value=None):
        """
        If the given key is not found, it will insert a new key into the list
        If a the key is found then it will replace the value
        @param key: The key you are looking for
        @param value: The value you plan to put into the node
        """
        node = self.head
        look_back_tower = self.generate_look_back_tower(key)
        node = look_back_tower[0]
        if node:
            possible_key = node.tower[0].node_key
            if key == possible_key:
                node.tower[0].node_value = value
                return EXISTING_KEY
        new_height = self.random_height()
        if new_height > self.count:
            for index in range(self.count, new_height):
                look_back_tower[index] = self.head
            self.count = new_height
        new_node = SkipNode(key, value, new_height)
        for index in range(new_height):
            new_node.tower[index] = look_back_tower[index].tower[index]
            look_back_tower[index].tower[index] = new_node
        self.number_of_elements += 1
        return new_node

    def delete(self, key,):
        """
        Searches for the given key in the list, if it is found then it removes the key
        This will readjust the count if necessary
        @param key: The key you are looking for to delete
        """
        node = self.head
        look_back_tower = self.generate_look_back_tower(key)
        node = look_back_tower[0]
        if node:
            node = node.tower[0]
            possible_key = node.node_key
            if key == possible_key:
                for index in range(self.count):
                    if look_back_tower[index].tower[index] == node:
                        look_back_tower[index].tower[index] = node.tower[index]
                while self.count > 0 and self.head.tower[self.count-1].node_key == float("inf"):
                    self.count -= 1
                self.number_of_elements -= 1


from profile import run
from random import randint


def test_skip_list_insert(number_of_elements=100):
    skip_list = SkipList(16)
    for index in range(number_of_elements):
        skip_list.insert(index, index)
    return skip_list


def test_skip_list_search():
    key_val = randint(1, number_of_elements)
    skip_list.search(474907)


def test_skip_list_search_with_frequency():
    key_val = randint(1, number_of_elements)
    skip_list.search_with_frequency(474907)



number_of_elements = 100000
skip_list = test_skip_list_insert(number_of_elements)
"""
ncalls
how many times the function is called
tottime
time spent on the function, excluding time spent on calling other functions
percall
tottime divided by ncalls
cumtime
time spent on the fucntion, incuding calls to other functions
percall
cumtime divided by tottime
"""
'''
for i in range(10):
    run('test_skip_list_search(); print')
    print "======================================"
print
print
print
'''
for i in range(20):
    run('test_skip_list_search_with_frequency(); print')
    print "++++++++++++++++++++++++++++++++++++++"
