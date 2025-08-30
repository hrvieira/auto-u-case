from backend.utils_text import preprocess_text

def test_preprocess_basic():
    txt = "Olá! Meu e-mail é teste@ex.com. Acesse http://exemplo.com"
    out = preprocess_text(txt)
    assert isinstance(out, str)
    assert "http" not in out
    assert "@" not in out
