from collections import Counter
from people import AnketaError, Student, parse_line

class Registry:
    def __init__(self):
        self.people = []
        self.errors = []

    def __len__(self):
        return len(self.people)

    def __iter__(self):
        return iter(self.people)

    def add(self, person):
        self.people.append(person)

    def load(self, filename):
        try:
            with open(filename, encoding="utf-8") as f:
                lines = f.read().splitlines()
        except OSError:
            return False
        self.people.clear()
        self.errors.clear()
        for number, line in enumerate(lines, 1):
            try:
                self.add(parse_line(line))
            except AnketaError as exc:
                self.errors.append((number, line, str(exc)))
        return True

    def roles(self):
        return dict(Counter(p.role() for p in self))

    def groups(self):
        return dict(Counter(p.group for p in self if isinstance(p, Student)))

    def sorted_people(self):
        return sorted(self, key=lambda p: p.fio.lower().replace("ё", "е"))

    def save_ok(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            for p in self:
                f.write(f"{p.fio};{p.mail};{p.phone};{p.extra()}\n")

    def save_errors(self, filename):
        with open(filename, "w", encoding="utf-8") as f:
            for number, line, reason in self.errors:
                f.write(f"{number}: {line} | {reason}\n")
