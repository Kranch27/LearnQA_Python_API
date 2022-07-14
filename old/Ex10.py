class TestEx10:

    def test_ex10(self):
        phrase = input("Введите фразу короче 15 символов: ")
        assert len(phrase) < 15, "Фраза должна быть короче 15 символов"
