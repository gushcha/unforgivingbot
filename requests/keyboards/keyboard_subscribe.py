from constants.callback_actions import CALLBACK_ACTION_SUBSCRIBE


def keyboard_subscribe(dispute_id: str) -> dict:
    return [
        [
            {
                'text': 'Subscribe',
                'callback_data': f'{CALLBACK_ACTION_SUBSCRIBE} {dispute_id}'
            },
        ],
    ]
