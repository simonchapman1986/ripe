config = {
    'registrations-raw': {
        'location': '',
        'request_paths_format': [
            'client_id',
            'report_name',
            'group',
            'interval',
            'territory',
            'platform',
            'start_date',
            'end_date'
        ],
        'request_paths': [
            '{}/registrations-raw/all/total/all/all/{}/{}/',
        ],
        'headers': [
                {'repnbr': 0, 'dbfield': 'client_name', 'csvfield': 'Client ID'},
                {'repnbr': 0, 'dbfield': 'date', 'csvfield': 'Date'},
                {'repnbr': 0, 'dbfield': 'external_user_id', 'csvfield': 'User ID'},
                {'repnbr': 0, 'dbfield': 'first_name', 'csvfield': 'First Name'},
                {'repnbr': 0, 'dbfield': 'last_name', 'csvfield': 'Last Name'},
        ]
    },
    'content': {
        'location': {
            'server': 'reports.sd-ngp.net',
            'port': 22,
            'path': '/home/default/reports/dev'
        },
        'headers': [
            {'repnbr': 0, 'dbfield': 'client_name', 'csvfield': 'Client ID'},
            {'repnbr': 0, 'dbfield': 'item_provider_name', 'csvfield': 'Content Provider'},
            {'repnbr': 0, 'dbfield': 'territory_code', 'csvfield': 'Territory'},
            {'repnbr': 0, 'dbfield': 'asset_id', 'csvfield': 'Asset ID'},
            {'repnbr': 0, 'dbfield': 'item_provider_id', 'csvfield': 'Vendor ID'},
            {'repnbr': 0, 'dbfield': 'item_id', 'csvfield': 'Item ID'},
            {'repnbr': 0, 'dbfield': 'item_title', 'csvfield': 'Title of Item'},
            {'repnbr': 0, 'dbfield': 'asset_type', 'csvfield': 'Asset Type'},
            {'repnbr': 0, 'dbfield': 'data_role', 'csvfield': 'Data Role'},
            {'repnbr': 0, 'dbfield': 'spec_name', 'csvfield': 'Spec'},
            {'repnbr': 0, 'dbfield': 'delivery_date', 'csvfield': 'Delivery Date'},
            {'repnbr': 0, 'dbfield': 'date', 'csvfield': 'Event Date'},
            {'repnbr': 0, 'dbfield': 'definition', 'csvfield': 'Definition'},
            {'repnbr': 0, 'dbfield': 'languages_iso_code', 'csvfield': 'Languages'},
            {'repnbr': 0, 'dbfield': 'file_size', 'csvfield': 'File Size'},
            {'repnbr': 0, 'dbfield': 'duration', 'csvfield': 'Duration'},
            {'repnbr': 0, 'dbfield': 'used_asset_ids', 'csvfield': 'Used Asset IDs'},
            {'repnbr': 0, 'dbfield': 'processing_state', 'csvfield': 'Processing State'},
        ],
        'request_paths_format': [
            'client_id',
            'report_name',
            'group',
            'interval',
            'start_date',
            'end_date'
        ],
        'request_paths': [
            '{}/content/all/weekly/{}/{}'
        ],
    },
    'license': {
        'request_paths': [
            '{}/license/all/weekly/{}/{}'
        ],
        'headers': [
            {'repnbr': 0, 'dbfield': 'client_name', 'csvfield': 'Client ID'},
            {'repnbr': 0, 'dbfield': 'date', 'csvfield': 'Date'},
            {'repnbr': 0, 'dbfield': 'external_user_id', 'csvfield': 'User ID'},
            {'repnbr': 0, 'dbfield': 'device_id', 'csvfield': 'Device ID'},
            {'repnbr': 0, 'dbfield': '', 'csvfield': 'First Name'},
            {'repnbr': 0, 'dbfield': '', 'csvfield': 'Last Name'},
            {'repnbr': 0, 'dbfield': 'item_title', 'csvfield': 'Item Title'},
            {'repnbr': 0, 'dbfield': 'item_id', 'csvfield': 'Item ID'},
            {'repnbr': 0, 'dbfield': 'drm_type', 'csvfield': 'License Type'},
            {'repnbr': 0, 'dbfield': '', 'csvfield': 'Delivery Type'},
            {'repnbr': 0, 'dbfield': 'territory_code', 'csvfield': 'Territory'},
            {'repnbr': 0, 'dbfield': '', 'csvfield': 'Content Type'},
            {'repnbr': 0, 'dbfield': '', 'csvfield': 'Definition'},
            {'repnbr': 0, 'dbfield': '', 'csvfield': 'Purchase Type'},
            {'repnbr': 0, 'dbfield': '', 'csvfield': 'Studio'},
            {'repnbr': 0, 'dbfield': 'platform_name', 'csvfield': 'Platform'},
        ],
        'request_paths_format': [
            'client_id',
            'report_name',
            'group',
            'interval',
            'start_date',
            'end_date'
        ]

    },
    'transaction': {
        'request_paths': [
            '{}/transaction/all/weekly/{}/{}'
        ],
        'headers': [
            {'repnbr': 0, 'dbfield': 'client_name', 'csvfield': 'Client ID'},
            {'repnbr': 0, 'dbfield': 'date', 'csvfield': 'Date'},
            {'repnbr': 0, 'dbfield': 'external_user_id', 'csvfield': 'User ID'},
            {'repnbr': 0, 'dbfield': 'first_name', 'csvfield': 'First Name'},
            {'repnbr': 0, 'dbfield': 'last_name', 'csvfield': 'Last Name'},
            {'repnbr': 0, 'dbfield': 'total_price_day', 'csvfield': 'Price'},
            {'repnbr': 0, 'dbfield': 'currency_code', 'csvfield': 'Currency'},
            {'repnbr': 0, 'dbfield': 'territory_code', 'csvfield': 'Territory'},
            {'repnbr': 0, 'dbfield': 'last_4_digits', 'csvfield': 'Card Suffix'},
            {'repnbr': 0, 'dbfield': 'content_type', 'csvfield': 'Content Type'},
            {'repnbr': 0, 'dbfield': '', 'csvfield': 'Purchase Type'},
            {'repnbr': 0, 'dbfield': '', 'csvfield': 'Studio'},
            {'repnbr': 0, 'dbfield': 'item_title', 'csvfield': 'Item Title'},
            {'repnbr': 0, 'dbfield': 'platform_name', 'csvfield': 'Platform'},
            {'repnbr': 0, 'dbfield': 'platform_os', 'csvfield': 'Platform OS'},
            {'repnbr': 0, 'dbfield': 'platform_version', 'csvfield': 'Platform Version'},
            {'repnbr': 0, 'dbfield': 'retail_model', 'csvfield': 'Retail Model'},
        ],
        'request_paths_format': [
            'client_id',
            'report_name',
            'group',
            'interval',
            'start_date',
            'end_date'
        ]

    },
    'subscription_revenue': {
        'request_paths': [
            '{}/subscription_revenue/all/weekly/{}/{}'
        ],
        'headers': [
            {'repnbr': 0, 'dbfield': 'client_name', 'csvfield': 'Client ID'},
            {'repnbr': 0, 'dbfield': 'date', 'csvfield': 'Date'},
            {'repnbr': 0, 'dbfield': '', 'csvfield': 'User ID'},
            {'repnbr': 0, 'dbfield': '', 'csvfield': 'First Name'},
            {'repnbr': 0, 'dbfield': '', 'csvfield': 'Last Name'},
            {'repnbr': 0, 'dbfield': 'price', 'csvfield': 'Price'},
            {'repnbr': 0, 'dbfield': '', 'csvfield': 'Currency'},
            {'repnbr': 0, 'dbfield': 'territory_code', 'csvfield': 'Territory'},
            {'repnbr': 0, 'dbfield': '', 'csvfield': 'Card Suffix'},
            {'repnbr': 0, 'dbfield': 'subscription_status', 'csvfield': 'Subscription Status'},
            {'repnbr': 0, 'dbfield': '', 'csvfield': 'Subscription Package'},
            {'repnbr': 0, 'dbfield': 'name', 'csvfield': 'Subscription Platform'},
        ],
        'request_paths_format': [
            'client_id',
            'report_name',
            'group',
            'interval',
            'start_date',
            'end_date'
        ]

    }

}



