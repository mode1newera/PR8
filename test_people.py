import pytest
from people import Person, Student, Teacher, AnketaError, parse_line

@pytest.mark.parametrize("raw,expected", [
    ("иванов иван", "Иванов Иван"),
    (" ИВАНОВ   ИВАН ", "Иванов Иван"),
    ("пЕтРоВ пЁтР", "Петров Пётр"),
    ("сидорова  анна", "Сидорова Анна"),
    ("петров-водкин кузьма", "Петров-Водкин Кузьма"),
    ("ёлкин-петров пётр", "Ёлкин-Петров Пётр")])
def test_fio(raw, expected):
    assert Person.check_fio(raw) == expected

def test_single_word():
    with pytest.raises(AnketaError):
        Person.check_fio("Иванов")

@pytest.mark.parametrize("raw", ["IVAN@MAIL.RU", " Ivan@Mail.Ru "])
def test_mail(raw):
    assert Person.check_email(raw) == "ivan@mail.ru"

@pytest.mark.parametrize("raw", ["a.ru", "a@@b.ru", "a@b", "@b.ru",
                                  "iv anov@mail.ru"])
def test_bad_mail(raw):
    with pytest.raises(AnketaError):
        Person.check_email(raw)

@pytest.mark.parametrize("raw", ["89211112233", "79211112233",
                               "+7 (921) 111-22-33", "9211112233"])
def test_phone(raw):
    assert Person.check_phone(raw) == "79211112233"

@pytest.mark.parametrize("raw", ["123", "", "69211112233", "abc9211112233"])
def test_bad_phone(raw):
    with pytest.raises(AnketaError):
        Person.check_phone(raw)

@pytest.fixture
def student():
    return Student("иванов иван петрович", "a@b.ru", "89211112233", "09с41")

def test_mask(student):
    assert student.phone_mask() == "+7 (921) 111-22-33"

def test_short(student):
    assert student.short() == "Иванов И. П."

def test_roles(student):
    t = Teacher("Петров Пётр", "t@b.ru", "89211112233", "И9")
    assert student.role() == "студент"
    assert t.role() == "преподаватель"

def test_no_group():
    with pytest.raises(AnketaError):
        Student("Иванов Иван", "a@b.ru", "89211112233", " ")

@pytest.mark.parametrize("tip,cls", [("s",Student),("t",Teacher)])
def test_parse(tip, cls):
    p = parse_line(tip + ";Иванов Иван;a@b.ru;89211112233;И9")
    assert isinstance(p, cls)
    assert p.fio == "Иванов Иван"

@pytest.mark.parametrize("raw", ["", "s;a", "x;a;b;c;d"])
def test_bad_line(raw):
    with pytest.raises(AnketaError):
        parse_line(raw)
