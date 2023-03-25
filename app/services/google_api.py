from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import FORMAT, TABLE_VALUES, SPREADSHEET_BODY


async def spreadsheets_create(
        wrapper_services: Aiogoogle,
        spreadsheet_body=SPREADSHEET_BODY
) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body['properties']['title'].format(now_date_time)
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    print(f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}')  # TODO Убрать отладочный принт.
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {'type': 'user',
                        'role': 'writer',
                        'emailAddress': settings.email}
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=permissions_body,
            fields="id"
        ))


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    TABLE_VALUES[0][1] = now_date_time
    for res in projects:
        completion_rate = res.close_date - res.create_date
        new_row = [str(res.name), str(completion_rate), str(res.description)]
        TABLE_VALUES.append(new_row)

    update_body = {
        'majorDimension': 'ROWS',
        'values': TABLE_VALUES
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range='A1:E30',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
