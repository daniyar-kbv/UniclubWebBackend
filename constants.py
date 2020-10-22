R = 6373.0

DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
DATE_FORMAT = '%Y-%m-%d'

TIME_BEFORE_LUNCH = 'BEFORE_LUNCH'
TIME_AFTER_LUNCH = 'AFTER_LUNCH'
TIME_ALL_DAY = 'ALL_DAY'

TIMES = [
    TIME_BEFORE_LUNCH,
    TIME_AFTER_LUNCH,
    TIME_ALL_DAY
]

MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6

WEEKDAYS = (
    (MONDAY, 'Понедельник'),
    (TUESDAY, 'Вторник'),
    (WEDNESDAY, 'Среда'),
    (THURSDAY, 'Четверг'),
    (FRIDAY, 'Пятница'),
    (SATURDAY, 'Суббота'),
    (SUNDAY, 'Воскресенье'),
)

LESSON_ATTENDED = 0
LESSON_NOT_ATTENDED = 1
LESSON_CANCELED = 2

LESSON_STATUSES = (
    (LESSON_ATTENDED, 'Ребенок присутствовал'),
    (LESSON_NOT_ATTENDED, 'Ребенок отсутствовал'),
    (LESSON_CANCELED, 'Отменили занятие'),
)