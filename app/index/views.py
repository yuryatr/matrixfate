
from datetime import datetime, timedelta

from aiohttp import web
import aiohttp_jinja2


class View(web.View):

    @aiohttp_jinja2.template('main.html')
    async def get(self):
        # Обработчик главной страницы
        error = None
        store = None
        params = self.request.query
        m_date = params.get('m_date', '')
        dt = _get_valid_date(m_date)
        if dt:
            if (0 < dt.year < 2100):
                arcan = Arcan(dt)
                arcan.calculation()
                store = arcan.store
            else:
                error = 'Введите дату!'

        return {'m_date': m_date, 'store': store, 'error': error}
    

def _get_valid_date(m_date: str):
    if not m_date:
        return
    try:
        # format: 0000-00-00
        dt = datetime.strptime(m_date, "%Y-%m-%d").date()
    except ValueError as e:
        return
    return dt


class Arcan(object):

    MAX = 22
    store = {
        'А': '', #  число рождения
        'Б': '', #  месяц рождения
        'В': '', #  год рождения
        'Г': '', #  = А+Б+В
        'Я': '', #  = А+Б+В+Г
        'Д': '', #  = А+Б
        'Е': '', #  = Б+В
        'Ж': '', #  = В+Г
        'З': '', #  = Г+А
        'И': '', #  = А+Я
        'К': '', #  = А+И
        'Л': '', #  = В+Я
        'М': '', #  = В+Л
        'Н': '', #  = Б+Я
        'О': '', #  = Г+Я
        'П': '', #  = Б+Н
        'Р': '', #  = Г+О
        'С': '', #  = Г+В
        'Т': '', #  = Р+М
        'У': '', #  = О+Л
        'Ф': '', #  = И+Н
        'Х': '', #  = К+П
        'Ц': '', #  = А+Б
        'year_1': '', 'year_2': '', 'year_3': '', 'year_4': '', 'year_5': '', 'year_6': '', 'year_7': '',
        'generic_program_m': '', 'generic_program_f': '',
    }

    def __init__(self, dt: datetime):
        self._dt = dt
        self._arcan_day = None
        self._arcan_month = None
        self._arcan_year = None

    @property
    def day(self):
        return self._dt.day

    @property
    def month(self):
        return self._dt.month

    @property
    def year(self):
        return self._dt.year

    # Функции суммирования чисел
    def get_sum(self, number: int) -> int:
        result_sum = 0
        if number > self.MAX:
            for digit in str(number):
                result_sum += int(digit)
            if result_sum > self.MAX:
                return self.get_sum(result_sum)
        else:
            result_sum = number
        return result_sum

    def calculation(self):
        # Первый базовый квадрат
        self.store['А'] = self.get_sum(self.day)
        self.store['Б'] = self.get_sum(self.month)
        self.store['В'] = self.get_sum(self.year)
        self.store['Г'] = self.get_sum(self.store['А'] + self.store['Б'] + self.store['В'])
        self.store['Я'] = self.get_sum(self.store['А'] + self.store['Б'] + self.store['В'] + self.store['Г'])

        # Кармический хвост
        self.store['О'] = self.get_sum(self.store['Г'] + self.store['Я'])
        self.store['Р'] = self.get_sum(self.store['Г'] + self.store['О'])

        # Арканы талантов
        self.store['Н'] = self.get_sum(self.store['Б'] + self.store['Я'])
        self.store['П'] = self.get_sum(self.store['Б'] + self.store['Н'])

        ### Линия земли ###
        # Слево
        self.store['И'] = self.get_sum(self.store['А'] + self.store['Я'])
        self.store['К'] = self.get_sum(self.store['А'] + self.store['И'])
        # Справо
        self.store['Л'] = self.get_sum(self.store['В'] + self.store['Я'])
        self.store['М'] = self.get_sum(self.store['В'] + self.store['Л'])

        # Линия благополучия
        self.store['У'] = self.get_sum(self.store['О'] + self.store['Л'])

        # Линия мужского рода
        self.store['Д'] = self.get_sum(self.store['А'] + self.store['Б'])
        self.store['Ж'] = self.get_sum(self.store['В'] + self.store['Г'])
        self.store['Ф'] = self.get_sum(self.store['И'] + self.store['Н'])
        self.store['Х'] = self.get_sum(self.store['К'] + self.store['П'])
        self.store['Ц'] = self.get_sum(self.store['А'] + self.store['Б']) # == 'Д'

        # Линия женского рода
        self.store['Е'] = self.get_sum(self.store['Б'] + self.store['В'])
        self.store['З'] = self.get_sum(self.store['А'] + self.store['Г'])
        self.store['Т'] = self.get_sum(self.store['Р'] + self.store['М'])
        self.store['С'] = self.get_sum(self.store['Г'] + self.store['В']) # == 'Ж'

        # Просчет по годам
        self.store['year_1'] = self.get_sum(self.store['А'] + self.store['Д'])
        self.store['year_2'] = self.get_sum(self.store['year_1'] + self.store['А'])
        self.store['year_3'] = self.get_sum(self.store['year_1'] + self.store['Д'])
        self.store['year_4'] = self.get_sum(self.store['year_1'] + self.store['year_2'])
        self.store['year_5'] = self.get_sum(self.store['year_1'] + self.store['year_3'])
        self.store['year_6'] = self.get_sum(self.store['year_2'] + self.store['А'])
        self.store['year_7'] = self.get_sum(self.store['year_3'] + self.store['Д'])

        # Родовая программа по мужской линии Д+Ж
        # Родовая программа по женской линии Е+З
        self.store['generic_program_m'] = self.get_sum(self.store['Д'] + self.store['Ж'])
        self.store['generic_program_f'] = self.get_sum(self.store['Е'] + self.store['З'])

