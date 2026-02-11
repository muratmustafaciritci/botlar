from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
import re
from typing import Callable


@dataclass
class TurkishAssistant:
    """Türkçe konuşan basit bir sanal asistan.

    Bu sürüm internet gerektirmeden temel görevleri yerine getirir:
    - Selamlama
    - Saat / tarih söyleme
    - Hesaplama
    - Motivasyon mesajı
    - Not alma
    """

    notes: list[str] = field(default_factory=list)

    def respond(self, message: str) -> str:
        cleaned = self._normalize(message)

        if self._asks_note_save(cleaned):
            return self._handle_note_save(message)

        routes: list[tuple[Callable[[str], bool], Callable[[str], str]]] = [
            (self._is_greeting, self._handle_greeting),
            (self._asks_time, self._handle_time),
            (self._asks_date, self._handle_date),
            (self._asks_note_list, self._handle_note_list),
            (self._is_calculation, self._handle_calculation),
            (self._asks_motivation, self._handle_motivation),
        ]

        for matcher, handler in routes:
            if matcher(cleaned):
                return handler(cleaned)

        return (
            "Bunu anlayamadım ama yardımcı olmak isterim. "
            "Şunları deneyebilirsin: 'Saat kaç?', 'Not al ...', '2+2'."
        )

    def _normalize(self, text: str) -> str:
        lowered = text.strip().lower()
        lowered = lowered.replace("ı", "i")
        return re.sub(r"\s+", " ", lowered)

    def _is_greeting(self, text: str) -> bool:
        return any(word in text for word in ("merhaba", "selam", "gunaydin", "iyi aksamlar"))

    def _handle_greeting(self, _: str) -> str:
        return "Merhaba! Ben Türkçe sanal asistanın. Sana nasıl yardımcı olabilirim?"

    def _asks_time(self, text: str) -> bool:
        return "saat" in text and ("kac" in text or "nedir" in text)

    def _handle_time(self, _: str) -> str:
        return f"Şu an saat {datetime.now().strftime('%H:%M')}."

    def _asks_date(self, text: str) -> bool:
        return "tarih" in text or "bugun gunlerden ne" in text

    def _handle_date(self, _: str) -> str:
        return f"Bugünün tarihi {datetime.now().strftime('%d.%m.%Y')}."

    def _asks_note_save(self, text: str) -> bool:
        return text.startswith("not al")

    def _handle_note_save(self, text: str) -> str:
        note = re.sub(r"^\s*not al\s*", "", text, flags=re.IGNORECASE).strip(" :")
        if not note:
            return "Not içeriği boş görünüyor. Örnek: 'Not al yarın 10:00 toplantı'."
        self.notes.append(note)
        return f"Not kaydedildi: '{note}'"

    def _asks_note_list(self, text: str) -> bool:
        return any(p in text for p in ("notlarim", "notlarımı", "notlari listele", "notlari goster"))

    def _handle_note_list(self, _: str) -> str:
        if not self.notes:
            return "Henüz kayıtlı notun yok."
        numbered = "\n".join(f"{idx}. {note}" for idx, note in enumerate(self.notes, start=1))
        return f"Kayıtlı notların:\n{numbered}"

    def _is_calculation(self, text: str) -> bool:
        return bool(re.fullmatch(r"[0-9\s+\-*/().]+", text))

    def _handle_calculation(self, text: str) -> str:
        try:
            result = eval(text, {"__builtins__": {}}, {})
            return f"Sonuç: {result}"
        except Exception:
            return "Bu işlemi hesaplayamadım. Lütfen geçerli bir matematik ifadesi gir."

    def _asks_motivation(self, text: str) -> bool:
        return any(p in text for p in ("motivasyon", "moral", "beni motive et"))

    def _handle_motivation(self, _: str) -> str:
        return "Harika gidiyorsun! Küçük adımların toplamı büyük başarılar getirir."


if __name__ == "__main__":
    assistant = TurkishAssistant()
    print("Türkçe Asistan hazır. Çıkmak için 'çıkış' yaz.")
    while True:
        user_input = input("Sen: ")
        if user_input.strip().lower() in {"çıkış", "cikis", "quit", "exit"}:
            print("Asistan: Görüşmek üzere!")
            break
        print("Asistan:", assistant.respond(user_input))
