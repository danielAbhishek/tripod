from company.models import (
    Event, Package, PackageLinkProduct, Product
)


products = {
    'photo frame': {
        'product_name': 'photo frame',
        'unit_price': 1000,
        'unit_measure_type': Product.MEASURE_TYPES[0][0],
        'product_type': Product.PRODUCT_TYPES[0][0],
        'description': 'testing 123',
        'display': False,
        'is_active': True
    },
    'short video': {
        'product_name': 'short video',
        'unit_price': 5000,
        'unit_measure_type': Product.MEASURE_TYPES[1][0],
        'product_type': Product.PRODUCT_TYPES[1][0],
        'description': 'testing 123',
        'display': False,
        'is_active': True
    },
    'photo album': {
        'product_name': 'photo album',
        'unit_price': 20000,
        'unit_measure_type': Product.MEASURE_TYPES[0][0],
        'product_type': Product.PRODUCT_TYPES[0][0],
        'description': 'testing 123',
        'display': False,
        'is_active': True
    }
}


events = {
    'wedding': {'event_name': 'Wedding', 'description': 'testing'},
    'birthday': {'event_name': 'Birthday', 'description': 'new data'}
}

packages = {
    'wedding april': {
        'package_name': 'wedding April',
        'description': 'testing description',
        # 'event': self.event,
        'is_active': True,
    },
    'pre-shoot': {
        'package_name': 'Pre-shoot',
        'description': 'testing description updated',
        # 'event': self.event,
        'is_active': False,
    }
}

product_units = {
    'photo frame': 3,
    'short video': 4,
    'photo album': 1,
}
