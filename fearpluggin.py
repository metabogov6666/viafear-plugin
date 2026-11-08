from typing import Any, List
import random
import time

from base_plugin import BasePlugin, HookResult, HookStrategy
from ui.settings import Header, Text

__id__ = "fearpluggin"
__name__ = "fearpluggin"
__description__ = "fearpluggin: анекдоты, мигалка, браинроты"
__author__ = "viafear"
__version__ = "2.1.0"
__icon__ = "exteraPlugins/1"
__app_version__ = ">=12.5.1"
__sdk_version__ = ">=1.4.4.3"

JOKES = [
    "Абрам приходит к раввину: «Ребе, я хочу развестись с Сарой». Раввин: «А зачем?». Абрам: «Она меня достала». Раввин: «А кто тебя не достал?».",
    "Встречаются два еврея. Один: «Как дела?». Второй: «Не жалуюсь». Первый: «А надо бы».",
    "Еврейский мальчик спрашивает отца: «Папа, а почему мы всегда экономим?». Отец: «Чтобы ты мог экономить».",
    "Рабинович звонит в справочную: «Скажите, который час?». Оператор: «Три пятнадцать». Рабинович: «А сколько минут?».",
    "Два еврея в поезде. Один: «Куда едете?». Второй: «В Варшаву». Первый: «А почему билет до Киева?». Второй: «А зачем вам знать, куда я еду?».",
    "Сара говорит Абраму: «Ты меня не любишь». Абрам: «Люблю». Сара: «А подарки?». Абрам: «Подарки — это не любовь, это расходы».",
    "Еврей на базаре: «Почём яблоки?». Продавец: «Рубль килограмм». Еврей: «А если я куплю пять килограмм?». Продавец: «Четыре рубля». Еврей: «А если десять?». Продавец: «Три рубля». Еврей: «А если я у вас всё куплю?». Продавец: «Тогда я вам доплачу».",
    "Рабинович в ресторане: «Официант, принесите мне борщ». Официант: «С мясом или без?». Рабинович: «А без мяса дешевле?». Официант: «Да». Рабинович: «Тогда без».",
    "Два еврея: «Мой сын стал врачом». «Мой — адвокатом». «А мой ещё и зарабатывает».",
    "Еврейский отец сыну: «Сынок, женись на богатой». Сын: «А если я её не люблю?». Отец: «Любовь пройдёт, деньги останутся».",
    "Абрам говорит Саре: «Я купил тебе шубу». Сара: «А где она?». Абрам: «В магазине. Я купил её для тебя, но оставил там, чтобы не испортить».",
    "Еврей на рынке: «Почём рыба?». Продавец: «Десять рублей». Еврей: «А вчера была восемь». Продавец: «Вчера была другая рыба». Еврей: «А сегодняшняя лучше?». Продавец: «Нет, просто дороже».",
    "Рабинович в отпуске: «Сара, мы экономим». Сара: «На чём?». Рабинович: «На всём, что не обязательно». Сара: «А отпуск обязательно?». Рабинович: «Нет, но мы уже заплатили».",
    "Два еврея в синагоге. Один молится: «Господи, дай мне здоровья». Второй: «А мне денег». Первый: «Ты жадный». Второй: «А ты здоровый?».",
    "Еврейский отец: «Сынок, учись, чтобы стать врачом». Сын: «А если не стану?». Отец: «Тогда стань адвокатом». Сын: «А если и там не получится?». Отец: «Тогда стань раввином — там не надо образование».",
    "Абрам: «Сара, я хочу открыть бизнес». Сара: «Какой?». Абрам: «Буду продавать воздух». Сара: «А кто купит?». Абрам: «Евреи — они и пустое купят, лишь бы дёшево».",
    "Еврей приходит в аптеку: «Дайте мне лекарство от жадности». Аптекарь: «Дорого». Еврей: «А скидка есть?».",
    "Рабинович на собеседовании: «Почему вы хотите работать у нас?». Рабинович: «Потому что вы платите». «А если мы не возьмём?». Рабинович: «Тогда я уйду к конкурентам — они платят больше».",
    "Два еврея: «Ты слышал, Фима выиграл в лотерею?». «Да, миллион». «А что он купил?». «Билет».",
    "Еврейский мальчик спрашивает учителя: «А что такое инфляция?». Учитель: «Когда хлеб стоит десять рублей». Мальчик: «А вчера?». Учитель: «Вчера хлеб стоил пять». Мальчик: «А послезавтра?». Учитель: «Двадцать». Мальчик: «А мы?». Учитель: «Мы будем есть меньше».",
    "Абрам: «Сара, я нашёл кошелёк». Сара: «Сколько там?». Абрам: «Пятьсот рублей». Сара: «А чей?». Абрам: «Не знаю». Сара: «Верни». Абрам: «А если хозяин не придёт?». Сара: «Тогда оставь себе». Абрам: «А если придёт?». Сара: «Тогда верни». Абрам: «А если он не еврей?». Сара: «Тогда точно верни — они не поймут».",
    "Еврей в ресторане: «Официант, почему порция такая маленькая?». Официант: «Это авторская кухня». Еврей: «А автор тоже голодный?».",
    "Рабинович: «Я купил акции». Друг: «Какие?». Рабинович: «Те, что растут». Друг: «А они растут?». Рабинович: «Пока нет, но купил я их по дешёвке».",
    "Два еврея обсуждают соседа: «Он теперь богатый». «Как?». «Женился на богатой». «А она?». «Она теперь не богатая».",
    "Еврейский отец сыну: «Сынок, главное в жизни — семья». Сын: «А деньги?». Отец: «Деньги — это тоже семья, только большая».",
    "Абрам: «Сара, я похудел на пять килограмм». Сара: «Как?». Абрам: «Перестал есть после шести». Сара: «А до шести?». Абрам: «До шести я ем за двоих».",
    "Еврей в магазине: «Дайте мне самый дешёвый хлеб». Продавец: «Это батон». Еврей: «А есть дешевле?». Продавец: «Буханка». Еврей: «А ещё дешевле?». Продавец: «Сухари». Еврей: «А если я их размочу?». Продавец: «Тогда это снова хлеб, но дороже».",
    "Рабинович: «Я экономлю на всём». Друг: «Даже на жене?». Рабинович: «Жена — это не расход, это инвестиция. Она экономит за меня».",
    "Два еврея: «Ты знаешь, что еврей, который не торгуется — не еврей?». «А который торгуется?». «Тоже не еврей, но хотя бы пытается».",
    "Еврейский мальчик: «Папа, а почему мы не едим свинину?». Отец: «Потому что это не кошерно». Мальчик: «А почему не кошерно?». Отец: «Потому что дорого».",
    "Абрам: «Сара, я купил тебе цветы». Сара: «Какие?». Абрам: «Искусственные — они не вянут». Сара: «А запах?». Абрам: «А зачем запах? Ты же не нюхаешь».",
    "Еврей в поезде: «Проводник, когда приедем?». Проводник: «Через час». Еврей: «А если я доплачу?». Проводник: «Через сорок минут». Еврей: «А если ещё доплачу?». Проводник: «Тогда мы приедем, когда вы скажете».",
    "Рабинович: «Я не жадный, я бережливый». Друг: «В чём разница?». Рабинович: «Жадный не даёт другим. Бережливый не даёт себе».",
    "Два еврея: «Слушай, а твой сын женился?». «Да, на еврейке». «А она красивая?». «Она богатая». «А красивая?». «Красивая — это дорого».",
    "Еврейский отец сыну: «Сынок, помни: деньги — это не главное». Сын: «А что главное?». Отец: «Чтобы деньги были».",
    "Абрам: «Сара, я подарю тебе кольцо». Сара: «С бриллиантом?». Абрам: «С надписью: \"Возвращать после развода\"».",
    "Еврей в бане: «Сколько стоит вход?». Банщик: «Сто рублей». Еврей: «А со скидкой для пенсионеров?». Банщик: «Вы пенсионер?». Еврей: «Нет, но я спрашиваю».",
    "Два еврея: «Ты куда?». «За хлебом». «А деньги?». «Дома». «А хлеб?». «Тоже дома. Я экономлю на дорогу».",
    "Еврейский отец: «Сын, женись на еврейке». Сын: «А если я полюблю русскую?». Отец: «Полюбишь — разлюбишь. А еврейка — это на всю жизнь».",
    "Рабинович: «Я купил жене подарок». Друг: «Какой?». Рабинович: «Сковородку». Друг: «А она обрадовалась?». Рабинович: «Она сказала, что я жадный. Я сказал: \"Жадный — это когда ничего не купил. А я купил\"».",
    "Еврей на рынке: «Почём этот арбуз?». Продавец: «Сто рублей». Еврей: «А вчера был восемьдесят». Продавец: «Вчера был меньше». Еврей: «А этот больше?». Продавец: «Да». Еврей: «Тогда я возьму вчерашний».",
]

BRAINROTS = [
    ("Noobini Pizzanini", "common", 40),
    ("Lirilì Larilà", "common", 40),
    ("Tim Cheese", "common", 40),
    ("Fluriflura", "common", 40),
    ("Talpa Di Fero", "common", 40),
    ("Svinina Bombardino", "common", 40),
    ("Pipi Kiwi", "common", 40),
    ("Ballerinakapuchina", "common", 40),
    ("Trippi Troppi", "rare", 25),
    ("Gangster Footera", "rare", 25),
    ("Bandito Bobritto", "rare", 25),
    ("Boneca Ambalabu", "rare", 25),
    ("Cacto Hipopotamo", "rare", 25),
    ("Ta Ta Ta Ta Sahur", "rare", 25),
    ("Tric Trac Baraboom", "rare", 25),
    ("BomBordiro Crocodilo", "rare", 25),
    ("Cappuccino Assassino", "epic", 12),
    ("Brr Brr Patapim", "epic", 12),
    ("Avocadini Antilopini", "epic", 12),
    ("Trulimero Trulicina", "epic", 12),
    ("Bambini Crostini", "epic", 12),
    ("Bananita Dolphinita", "epic", 12),
    ("Perochello Lemonchello", "epic", 12),
    ("Brri Brri Bicus Dicus Bombicus", "epic", 12),
    ("Avocadini Guffo", "epic", 12),
    ("Salamino Penguino", "epic", 12),
    ("Wombo Rollo", "epic", 12),
    ("Burbaloni Loliloli", "legendary", 6),
    ("Chimpanzini Bananini", "legendary", 6),
    ("Ballerina Cappuccina", "legendary", 6),
    ("Chef Crabracadabra", "legendary", 6),
    ("Lionel Cactuseli", "legendary", 6),
    ("Glorbo Fruttodrillo", "legendary", 6),
    ("Quivioli Ameleonni", "legendary", 6),
    ("Blueberrinni Octopusini", "legendary", 6),
    ("Pipi Potato", "legendary", 6),
    ("Strawberelli Flamingelli", "legendary", 6),
    ("Pandaccini Bananini", "legendary", 6),
    ("Sigma Boy", "legendary", 6),
    ("Frigo Camelo", "mythic", 3),
    ("Orangutini Ananassini", "mythic", 3),
    ("Rhino Toasterino", "mythic", 3),
    ("Bombardiro Crocodilo", "mythic", 3),
    ("Spioniro Golubiro", "mythic", 3),
    ("Bombombini Gusini", "mythic", 3),
    ("Zibra Zubra Zibralini", "mythic", 3),
    ("Tigrilini Watermelini", "mythic", 3),
    ("Cavallo Virtuoso", "mythic", 3),
    ("Gorillo Watermelondrillo", "mythic", 3),
    ("Leruleruleru", "mythic", 3),
    ("Tracoducotulu Delapeladustuz", "mythic", 3),
    ("Cachorrito Melonito", "mythic", 3),
    ("Carrotini Brainini", "mythic", 3),
    ("Toiletto Focaccino", "mythic", 3),
    ("Bananito Bandito", "mythic", 3),
    ("Tungtung Sahur", "mythic", 1),
]

RARITY_NAMES = {
    "common": "комонка",
    "rare": "рар",
    "epic": "эпик",
    "legendary": "легендарка",
    "mythic": "мифик",
}

_user_brainrots = {}
_steal_cooldown = {}
STEAL_CD = 5 * 60


def _uid_from_params(params):
    for attr in ("reply_to_user_id", "replyToUserId", "reply_to_peer_id", "replyToPeerId"):
        v = getattr(params, attr, None)
        if v is not None:
            try:
                return int(v)
            except Exception:
                pass
    return None


class FearplugginPlugin(BasePlugin):
    def on_plugin_load(self):
        self.add_on_send_message_hook()
        self.logger.info("fearpluggin loaded")

    def create_settings(self) -> List[Any]:
        return [
            Header(text="fearpluggin"),
            Text(text="Команды", subtext="/adot, .мигнуть, .браинроты, .спиздить", icon="msg_info"),
            Text(text="Визуал", subtext="ник + fear, подпись @viafear", icon="msg_info"),
        ]

    def on_send_message_hook(self, account: int, params: Any) -> HookResult:
        msg = getattr(params, "message", None)
        if not isinstance(msg, str):
            return HookResult()
        text = msg.strip()
        low = text.lower()

        if low == "/adot" or low.startswith("/adot "):
            params.message = random.choice(JOKES)
            return HookResult(strategy=HookStrategy.MODIFY, params=params)

        if low.startswith(".мигнуть") or low.startswith(".мигать"):
            self._run_blink(account, params)
            return HookResult(strategy=HookStrategy.CANCEL)

        if low.startswith(".браинроты") or low.startswith(".brainrots"):
            uid = _uid_from_params(params)
            key = uid if uid is not None else 0
            lst = _user_brainrots.get(key, [])
            if not lst:
                out = "У тебя нет браинротов."
            else:
                lines = ["Твои браинроты:"]
                for b in lst:
                    r = next((x[1] for x in BRAINROTS if x[0] == b), "?")
                    lines.append(f"• {b} ({RARITY_NAMES.get(r, r)})")
                out = "\n".join(lines)
            params.message = out
            return HookResult(strategy=HookStrategy.MODIFY, params=params)

        if low.startswith(".спиздить") or low.startswith(".steal"):
            now = time.time()
            uid = _uid_from_params(params)
            if uid is None:
                params.message = "Ответь на сообщение пользователя."
                return HookResult(strategy=HookStrategy.MODIFY, params=params)
            last = _steal_cooldown.get(uid, 0)
            if now - last < STEAL_CD:
                rem = int(STEAL_CD - (now - last))
                params.message = f"КД: осталось {rem} сек."
                return HookResult(strategy=HookStrategy.MODIFY, params=params)
            victim_list = _user_brainrots.get(uid, [])
            if not victim_list:
                params.message = "У него нет браинротов."
                return HookResult(strategy=HookStrategy.MODIFY, params=params)
            stolen = None
            for b in list(victim_list):
                w = next((x[2] for x in BRAINROTS if x[0] == b), 10)
                if random.random() * 100 < w:
                    stolen = b
                    break
            if stolen is None:
                stolen = random.choice(victim_list)
            victim_list.remove(stolen)
            _user_brainrots[uid] = victim_list
            me = 0
            try:
                from client_utils import get_user_id
                me = int(get_user_id())
            except Exception:
                pass
            _user_brainrots.setdefault(me, []).append(stolen)
            _steal_cooldown[uid] = now
            params.message = f"Ты успешно спиздил браинрота: {stolen}"
            return HookResult(strategy=HookStrategy.MODIFY, params=params)

        return HookResult()

    def _run_blink(self, account, params):
        chat_id = getattr(params, "peer", None) or getattr(params, "chat_id", None)
        reply_to = getattr(params, "reply_to_msg_id", None) or getattr(params, "replyToMsgId", None)
        try:
            from client_utils import send_message, edit_message
            mid = send_message(account, chat_id, "mog 1%", reply_to=reply_to)
            for i in range(10, 101, 10):
                time.sleep(0.6)
                edit_message(account, chat_id, mid, f"mog {i}%")
            time.sleep(0.4)
            edit_message(account, chat_id, mid, "ты был мигнут ты саб5")
        except Exception as e:
            self.logger.error(f"blink err: {e}")
