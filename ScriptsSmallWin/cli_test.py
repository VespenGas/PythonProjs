#pip install pytest
# $ pytest this_file_name.py
import hello

def test_main(capsys):
    hello.main(['value'])
    out, err = capsys.readouterr()
    assert out #== whatever out should be
    assert err == ''
def test_none_input(capsys):
    assert hello.main(['value'])
    out, err = capsys.readouterr()
    assert out == ''
    assert err == 'This message is from main, where'
    #the error is given as print with argument 'file = sys.stderr'
    