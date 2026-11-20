import pytest
from registry import Registry
from people import Student

@pytest.fixture
def journal(tmp_path):
    p = tmp_path / "anketa.txt"
    p.write_text(
        "s;Иванов Иван;i@b.ru;89211112233;09с41\n"
        "t;Петров Пётр;p@b.ru;89211112233;И9\n"
        "s;Антонов Антон;a@b.ru;89211112233;09с41\n"
        "брак\n\nunknown;a;b;c;d\n", encoding="utf-8")
    j = Registry()
    assert j.load(p)
    return j

def test_empty():
    assert len(Registry()) == 0

def test_count(journal):
    assert len(journal) == 3

def test_errors(journal):
    assert len(journal.errors) == 3

def test_error_numbers(journal):
    assert [e[0] for e in journal.errors] == [4,5,6]

def test_missing(tmp_path):
    assert Registry().load(tmp_path / "absent") is False

def test_roles(journal):
    assert journal.roles() == {"студент":2,"преподаватель":1}

def test_groups(journal):
    assert journal.groups() == {"09с41":2}

def test_iteration(journal):
    assert len(list(journal)) == 3

def test_sort(journal):
    assert [p.fio for p in journal.sorted_people()] == [
        "Антонов Антон", "Иванов Иван", "Петров Пётр"]

def test_save_ok(journal, tmp_path):
    p = tmp_path / "ok"
    journal.save_ok(p)
    assert len(p.read_text(encoding="utf-8").splitlines()) == 3

def test_save_errors(journal, tmp_path):
    p = tmp_path / "errors"
    journal.save_errors(p)
    assert "Неизвестный тип" in p.read_text(encoding="utf-8")

def test_yo_sort():
    j = Registry()
    for fio in ["Яковлев Иван", "Ёлкин Иван", "Абрамов Иван"]:
        j.add(Student(fio, fio.split()[0] + "@b.ru", "89211112233", "09с41"))
    assert [p.fio.split()[0] for p in j.sorted_people()] == [
        "Абрамов", "Ёлкин", "Яковлев"]

def test_control():
    j = Registry()
    assert j.load("anketa.txt")
    assert (len(j),len(j.errors)) == (4,6)
