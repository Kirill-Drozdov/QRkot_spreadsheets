from copy import deepcopy
from datetime import datetime
from typing import Dict, Union, List

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.core.constants import (
    FORMAT,
    TABLE_VALUES,
    SPREADSHEET_BODY,
    ROW_COUNT,
    PERMISSIONS_BODY,
    PROPERTIES_TITLE
)


async def spreadsheets_create(
        wrapper_services: Aiogoogle,
        spreadsheet_body: Dict[
            str,
            Union[
                Dict[str, str],
                List[
        Dict[
            str,
            Dict[str, Union[str, int]]
        ]
                ]
            ]
        ] = deepcopy(SPREADSHEET_BODY)
) -> str:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body['properties']['title'] = PROPERTIES_TITLE.format(now_date_time)
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheetid: str,
        wrapper_services: Aiogoogle
) -> None:
    PERMISSIONS_BODY['emailAddress'] = settings.email
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheetid,
            json=PERMISSIONS_BODY,
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
    rows_total = len(TABLE_VALUES)
    if rows_total > ROW_COUNT:
        raise OverflowError('В таблице превышен лимит строк!')

    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{rows_total}C3',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
