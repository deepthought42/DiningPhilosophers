import threading
import time

class Philosopher(threading.Thread):
    def __init__(self, name, left_fork, right_fork):
        threading.Thread.__init__(self)
        self.name = name
        self.left_fork = left_fork
        self.right_fork = right_fork

    def run(self):
        while True:
            print(f"{self.name} is thinking.")
            time.sleep(1)
            print(f"{self.name} is hungry.")
            self.dine()

    def dine(self):
        fork1, fork2 = self.left_fork, self.right_fork

        while True:
            fork1.acquire()  # Try to pick up left fork
            acquired = fork2.acquire(False)  # Try to pick up right fork
            if acquired:
                break  # If successful, break the loop and start eating
            fork1.release()  # Otherwise, release left fork and retry
            time.sleep(0.5)  # Pause briefly before retrying

        print(f"{self.name} is eating.")
        time.sleep(2)  # Simulate eating
        fork1.release()
        fork2.release()
        print(f"{self.name} finished eating.")

# Create locks for forks
forks = [threading.Lock() for _ in range(5)]

# Create philosophers
philosophers = [
    Philosopher(f"Philosopher {i + 1}", forks[i % 5], forks[(i + 1) % 5])
    for i in range(5)
]

# Start the philosopher threads
for philosopher in philosophers:
    philosopher.start()