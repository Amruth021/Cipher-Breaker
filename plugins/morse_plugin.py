from plugins import Plugin

MORSE = {
    ".-":"A","-...":"B","-.-.":"C","-..":"D",".":"E","..-.":"F","--.":"G","....":"H","..":"I",
    ".---":"J","-.-":"K",".-..":"L","--":"M","-.":"N","---":"O",".--.":"P","--.-":"Q",".-.":"R",
    "...":"S","-":"T","..-":"U","...-":"V",".--":"W","-..-":"X","-.--":"Y","--..":"Z",
    "-----":"0",".----":"1","..---":"2","...--":"3","....-":"4",".....":"5","-....":"6",
    "--...":"7","---..":"8","----.":"9"
}

class MorsePlugin(Plugin):
    name = "Morse"

    def accepts(self, text: str) -> bool:
        return all(c in ".- /" for c in text)

    def transform(self, text: str) -> list[str]:
        words = text.split(" / ")
        decoded_words = []
        for word in words:
            decoded_letters = [MORSE.get(symbol, "?") for symbol in word.split()]
            decoded_words.append("".join(decoded_letters))
        return [" ".join(decoded_words)]

