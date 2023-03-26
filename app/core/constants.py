FORMAT = "%Y/%m/%d %H:%M:%S"

TABLE_VALUES = [
    ['Отчет от', 'now_date_time'],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]

ROW_COUNT = 100
COLUMN_COUNT = 11
SHEET_ID = 0
PROPERTIES_TITLE = 'Отчет от {}'
SHEETS_TITLE = 'Лист1'

SPREADSHEET_BODY = dict(
    properties=dict(
        title=...,
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=SHEET_ID,
        title=SHEETS_TITLE,
        gridProperties=dict(
            rowCount=ROW_COUNT,
            columnCount=COLUMN_COUNT,
        )
    ))]
)

PERMISSIONS_BODY = dict(
    type='user',
    role='writer',
    emailAddress=...,
)
