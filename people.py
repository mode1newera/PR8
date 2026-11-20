import re

class AnketaError(ValueError):
    pass

class Person:
    def __init__(self, fio, mail, phone):
        self.fio = self.check_fio(fio)
        self.mail = self.check_email(mail)
        self.phone = self.check_phone(phone)

    @staticmethod
    def check_fio(value):
        words = value.split()
        if len(words) < 2:
            raise AnketaError("В ФИО нужно хотя бы два слова")
        if any(not re.fullmatch(r"[^\W\d_]+(?:-[^\W\d_]+)*", w)
               for w in words):
            raise AnketaError("В ФИО допустимы буквы и дефис")
        return " ".join(w.title() for w in words)

    @staticmethod
    def check_email(value):
        value = value.strip().lower()
        if not re.fullmatch(r"[^\s@;]+@[^\s@;.]+(?:\.[^\s@;.]+)+", value):
            raise AnketaError("Неверная почта")
        return value

    @staticmethod
    def check_phone(value):
        if re.search(r"[^0-9+() \-]", value):
            raise AnketaError("Недопустимые символы телефона")
        digits = re.sub(r"\D", "", value)
        if len(digits) == 10:
            digits = "7" + digits
        if len(digits) == 11 and digits[0] == "8":
            digits = "7" + digits[1:]
        if len(digits) != 11 or digits[0] != "7":
            raise AnketaError("Нужен российский телефон из 10 или 11 цифр")
        return digits

    def phone_mask(self):
        p = self.phone
        return f"+7 ({p[1:4]}) {p[4:7]}-{p[7:9]}-{p[9:]}"

    def short(self):
        surname, *names = self.fio.split()
        return surname + " " + " ".join(n[0] + "." for n in names)

    def role(self):
        return "человек"

    def extra(self):
        return ""

    def __eq__(self, other):
        if not isinstance(other, Person):
            return NotImplemented
        return self.mail == other.mail

    def __hash__(self):
        return hash(self.mail)

class Student(Person):
    def __init__(self, fio, mail, phone, group):
        super().__init__(fio, mail, phone)
        self.group = "".join(group.split()).lower()
        if not self.group:
            raise AnketaError("Не указана группа")

    def role(self):
        return "студент"

    def extra(self):
        return self.group

class Teacher(Person):
    def __init__(self, fio, mail, phone, kafedra):
        super().__init__(fio, mail, phone)
        self.kafedra = " ".join(kafedra.split())
        if not self.kafedra:
            raise AnketaError("Не указана кафедра")

    def role(self):
        return "преподаватель"

    def extra(self):
        return self.kafedra

def parse_line(line):
    parts = line.strip().split(";")
    if len(parts) != 5:
        raise AnketaError("Ожидается пять полей через точку с запятой")
    tip, *fields = parts
    cls = {"s": Student, "t": Teacher}.get(tip)
    if cls is None:
        raise AnketaError("Неизвестный тип анкеты")
    return cls(*fields)
