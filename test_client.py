import pytest
import requests
import client

class Reply:
    def __init__(self, code, data):
        self.status_code,self.data,self.text = code,data,str(data)
    def json(self):
        return self.data
    def raise_for_status(self):
        if self.status_code >= 400:
            raise requests.HTTPError(str(self.status_code))

@pytest.mark.parametrize("exc",[requests.ConnectionError,requests.Timeout])
def test_network(monkeypatch,exc):
    def fail(*args,**kwargs):
        assert kwargs["timeout"] == 3
        raise exc("Проверка недоступности")
    monkeypatch.setattr(requests,"request",fail)
    with pytest.raises(client.ServerNedostupen):
        client.vse()

def test_500(monkeypatch):
    monkeypatch.setattr(requests,"request",lambda *a,**k:Reply(500,{}))
    with pytest.raises(client.ServerNedostupen):
        client.statistika()

def test_missing(monkeypatch):
    monkeypatch.setattr(requests,"request",lambda *a,**k:Reply(404,{}))
    assert client.odna(99) is None

@pytest.mark.parametrize("code,value",[(200,True),(400,False)])
def test_check(monkeypatch,code,value):
    monkeypatch.setattr(requests,"request",
                        lambda *a,**k:Reply(code,{"prinyato":value}))
    assert client.proverit("a@b.ru") is value
