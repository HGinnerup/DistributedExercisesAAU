import math
import random
import threading
import time

from emulators.Medium import Medium
from emulators.Device import Device
from emulators.MessageStub import MessageStub


class Vote(MessageStub):

    def __init__(self, sender: int, destination: int, vote: int, decided: bool):
        super().__init__(sender, destination)
        self._vote = vote
        self._decided = decided

    def vote(self):
        return self._vote

    def decided(self):
        return self._decided

    def __str__(self):
        return f'Vote: {self.source} -> {self.destination}, voted for {self._vote}, decided? {self._decided}'


class Bully(Device):

    def __init__(self, index: int, number_of_devices: int, medium: Medium):
        super().__init__(index, number_of_devices, medium)
        self._leader = None
        self._shut_up = False
        self._election = False

    def largest(self):
        return self.index() == max(self.medium().ids())

    def run(self):
        first_round=True
        while True:
            got_input=False
            if not self._shut_up and not self._election:
                self.start_election()
            new_election=False
            while True:
                ingoing=self.medium().receive()
                if ingoing is not None:
                    got_input=True
                    if ingoing.vote() < self.index(): # Other agent has lower ID
                        # This agent replies that it is larger
                        self.medium().send(Vote(self.index(), ingoing.source, self.index(), self.largest()))
                        new_election=True
                    else:
                        # Something else is confirmed larger, so this agent shuts up
                        self._shut_up=True
                        if ingoing.decided():
                            self._leader=ingoing.vote() # Someone else is confirmed leader
                            return
                else: break
                
            if not self._shut_up and not self._election and new_election:
                self.start_selection()
            if not got_input and not first_round:
                if self._election:
                    if self._shut_up:
                        self._shut_up=False
                        self.start_election()
                    else:
                        for id in self.medium().ids():
                            if id != self.index():
                                self.medium().send(Vote(self.index(), id, self.index(), True))
                        self._leader=self.index() # Self is confirmed leader
                        return
            self.medium().wait_for_next_round()
            first_round=False

    def start_election(self):
        if not self._election:
            self._election=True
            for id in self.medium().ids():
                if id > self.index():
                    self.medium().send(Vote(self.index(), id, self.index(), self.largest()))

    def print_result(self):
        print(f'Leader seen from {self._id} is {self._leader}')