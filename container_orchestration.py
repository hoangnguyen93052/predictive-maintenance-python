import os
import subprocess
import json
import time
from typing import Dict, List

class Container:
    def __init__(self, name: str, image: str):
        self.name = name
        self.image = image
        self.status = "stopped"
    
    def start(self):
        if self.status == "running":
            print(f"Container {self.name} is already running")
            return
        print(f"Starting container {self.name} using image {self.image}")
        subprocess.run(["docker", "run", "-d", "--name", self.name, self.image])
        self.status = "running"

    def stop(self):
        if self.status == "stopped":
            print(f"Container {self.name} is already stopped")
            return
        print(f"Stopping container {self.name}")
        subprocess.run(["docker", "stop", self.name])
        self.status = "stopped"

    def remove(self):
        print(f"Removing container {self.name}")
        subprocess.run(["docker", "rm", self.name])

    def get_status(self) -> str:
        return self.status

class Orchestrator:
    def __init__(self):
        self.containers: Dict[str, Container] = {}

    def create_container(self, name: str, image: str):
        if name in self.containers:
            print(f"Container {name} already exists.")
            return
        container = Container(name, image)
        self.containers[name] = container
        print(f"Created container {name} with image {image}")

    def start_container(self, name: str):
        if name not in self.containers:
            print(f"Container {name} does not exist.")
            return
        self.containers[name].start()

    def stop_container(self, name: str):
        if name not in self.containers:
            print(f"Container {name} does not exist.")
            return
        self.containers[name].stop()

    def remove_container(self, name: str):
        if name not in self.containers:
            print(f"Container {name} does not exist.")
            return
        self.containers[name].remove()
        del self.containers[name]

    def list_containers(self):
        if not self.containers:
            print("No containers found.")
            return
        for name, container in self.containers.items():
            print(f"Container {name}: Status = {container.get_status()}")

class DockerStats:
    @staticmethod
    def get_containers_stats() -> List[Dict]:
        result = subprocess.run(["docker", "ps", "--format", "{{json .}}"], capture_output=True, text=True)
        stats = [json.loads(line) for line in result.stdout.splitlines()]
        return stats

class Application:
    def __init__(self):
        self.orchestrator = Orchestrator()

    def run(self):
        while True:
            print("\nContainer Orchestration Management")
            print("1. Create container")
            print("2. Start container")
            print("3. Stop container")
            print("4. Remove container")
            print("5. List containers")
            print("6. Get Docker stats")
            print("7. Exit")

            choice = input("Select an option: ")

            if choice == "1":
                name = input("Enter container name: ")
                image = input("Enter image name: ")
                self.orchestrator.create_container(name, image)
            elif choice == "2":
                name = input("Enter container name to start: ")
                self.orchestrator.start_container(name)
            elif choice == "3":
                name = input("Enter container name to stop: ")
                self.orchestrator.stop_container(name)
            elif choice == "4":
                name = input("Enter container name to remove: ")
                self.orchestrator.remove_container(name)
            elif choice == "5":
                self.orchestrator.list_containers()
            elif choice == "6":
                stats = DockerStats.get_containers_stats()
                print("Docker Containers Stats:")
                for stat in stats:
                    print(stat)
            elif choice == "7":
                print("Exiting...")
                break
            else:
                print("Invalid option. Please select again.")
            time.sleep(1)

if __name__ == "__main__":
    app = Application()
    app.run()