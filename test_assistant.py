from assistant import TurkishAssistant


def test_greeting():
    bot = TurkishAssistant()
    assert "Merhaba" in bot.respond("Selam")


def test_note_save_and_list():
    bot = TurkishAssistant()
    save = bot.respond("Not al yarın spor yap")
    listed = bot.respond("notlarımı")
    assert "Not kaydedildi" in save
    assert "yarın spor yap" in listed


def test_calculation():
    bot = TurkishAssistant()
    assert bot.respond("2+3*4") == "Sonuç: 14"
