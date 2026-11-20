import json
import client
from people import Student, Teacher, AnketaError
from registry import Registry

def main():
    j = Registry()
    server_stats = None
    source = "сервер"
    try:
        rows = client.vse()
    except client.ServerNedostupen as exc:
        print("Сервер недоступен:", exc)
        source = "anketa.txt"
        if not j.load(source):
            print("Нет ни сервера, ни файла anketa.txt")
            return
    else:
        for i, row in enumerate(rows, 1):
            try:
                cls = {"s":Student,"t":Teacher}.get(row.get("tip"))
                if cls is None:
                    raise AnketaError("Неизвестный тип анкеты")
                extra = "gruppa" if cls is Student else "kafedra"
                j.add(cls(row["fio"],row["mail"],row["phone"],row[extra]))
            except (AnketaError, KeyError, TypeError) as exc:
                j.errors.append((row.get("nomer",i),str(row),str(exc)))
        try:
            server_stats = client.statistika()
        except client.ServerNedostupen as exc:
            print("Статистика недоступна:", exc)
    print("Источник:", source)
    accepted = []
    for p in j:
        print(p.fio,p.role(),p.mail,p.phone_mask(),p.extra(),sep=" | ")
        accepted.append({"fio":p.fio,"mail":p.mail,"role":p.role()})
        if source == "сервер":
            try:
                print("Проверка почты:",p.mail,client.proverit(p.mail))
            except client.ServerNedostupen as exc:
                print("Проверка недоступна:",exc)
    print(f"Принято: {len(j)} | Отклонено: {len(j.errors)}")
    for error in j.errors:
        print("Брак:",*error,sep=" | ")
    print("Локальные роли:",j.roles())
    print("Статистика сервера:",server_stats)
    result = {"source":source,"accepted":accepted,"errors":j.errors,
              "roles":j.roles(),"server_stats":server_stats}
    with open("otchet.json","w",encoding="utf-8") as f:
        json.dump(result,f,ensure_ascii=False,indent=2)

if __name__ == "__main__":
    main()
