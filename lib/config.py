import os
import sys
from typing import List, Tuple
import yaml

class _Configuration:
    name: str
    highscores: List[Tuple[str, int]]
    location: str

    def __init__(self, name, highscores, location=""):
        self.name = name
        self.highscores = highscores
        self.location = location

    def register_highscore(self, name, new_score):
        for i, score in enumerate(self.highscores):
            if score[1] < new_score:
                self.highscores.insert(i, (name, new_score))
                break
        else:
            self.highscores.append((name, new_score))
        if len(self.highscores) > 10:
            self.highscores = self.highscores[:10]

    def is_highest_score(self, score):
        if not self.highscores:
            return True
        return self.highscores[0][1] <= score

    def is_highscore(self, score):
        if not self.highscores:
            return True
        return self.highscores[-1][1] < score or len(self.highscores) < 10

    @property
    def highest_score(self):
        if not self.highscores:
            return None
        return self.highscores[0]

    def to_dict(self):
        return {'name': self.name, 'highscores': self.highscores}

    def __iter__(self):
        yield from self.to_dict().items()

    @classmethod
    def load_from(cls, location):
        with open(location, 'r') as file:
            data = yaml.load(file.read())
        return cls(location=location, **data)

    def save(self, location=""):
        if not (location or self.location):
            raise ValueError("No location provided nor load location stored for configuration file to save in")

        with open(location or self.location, 'w') as file:
            file.write(yaml.dump(self.to_dict()))

try:
    Configuration = _Configuration.load_from('rsc/data.yaml')
except:
    Configuration = _Configuration(None, [], location='rsc/data.yaml')