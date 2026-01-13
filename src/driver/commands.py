from dataclasses import dataclass


@dataclass
class Command:
    name: str
    code: str
    description: str

    def add_to_list(self, commands):
        commands.append(self)
        return self
