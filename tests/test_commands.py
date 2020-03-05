from latex.utils import Commands


def test_buffer():
    c = Commands()
    assert c.get_buffer() == ''
    hola = 'hola'
    c.set_buffer(hola)
    assert c.get_buffer() == hola
