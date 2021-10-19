from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

StudentModel = {
    'type': 'object',
    'properties': {
        "firstname": {
            'type': 'string'
        },
        "lastname": {
            'type': 'string'
        },
        'email': {
            'type': 'string',
            'format': 'email'
        },
        'phone': {
            'type': 'string'
        },
        'headline': {
            'type': 'string'
        }
    },
    'required': ['firstname', 'lastname', 'email', 'phone', 'headline'],
    'additionalProperties': False
}


def validate_student(data):
    try:
        validate(data, StudentModel)
        return {'msg': 'success'}
    except SchemaError as e:
        return {'msg': 'error', 'error': e.message}
    except ValidationError as e:
        return {'msg': 'error', 'error': e.message}
