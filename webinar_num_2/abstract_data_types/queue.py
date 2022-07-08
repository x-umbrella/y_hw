from typing import Optional, Any, List


class Queue:
    """ Abstract Data Type Queue """

    def __init__(self):
        self.items: List[Any] = []

    def enqueue(self, item: Any) -> None:
        """
        The runtime is O(n) or linear time, change index positions
        :param item: Any
        :return: None
        """
        self.items.insert(0, item)

    def dequeue(self) -> Optional[Any]:
        if self.items:
            return self.items.pop()

    def peek(self) -> Optional[Any]:
        if self.items:
            return self.items[-1]

    def size(self) -> int:
        return len(self.items)

    def is_empty(self) -> bool:
        return self.items == []

my_queue = Queue()

my_queue.enqueue("Alex")
my_queue.enqueue("Oleg")
my_queue.enqueue("Elena")

print(my_queue.size())
print(my_queue.is_empty())
print(my_queue.dequeue())
print(my_queue.size())
print(my_queue.is_empty())
print(my_queue.dequeue())
print(my_queue.size())
print(my_queue.is_empty())
print(my_queue.dequeue())
print(my_queue.size())
print(my_queue.is_empty())
