from queue import Queue
import threading
class GlobalQueue:
    def __init__(self):
        self.global_queue = Queue()
        self.queues = []

    def put(self,item):
        self.global_queue.put(item)

        for queue in self.queues:
            queue.put(item)

    def get_new_queue(self):
        queue = PrivateQueue(self)

        for item in self.to_array():
            queue.put(item)

        self.queues.append(queue)

        return queue

    def remove_queue(self,queue):
        self.queues.remove(queue)

    def to_array(self):
        return list(self.global_queue.queue)

    def clear(self):
        self.global_queue.queue.clear()

        for queue in self.queues:
            queue.queue.clear()
class PrivateQueue(Queue):
    def __init__(self,global_queue):
        Queue.__init__(self)
        self.global_queue = global_queue

    def delete_queue(self):
        self.global_queue.remove_queue(self)