from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

student = {
    'type': 'object',
    'properties': {
        'firstname': {
            'type': 'string'
        },
        'lastname': {
            'type': 'string'
        },
        'email': {
            'type': 'string',
            'format': 'email',
        },
        'password': {
            'type': 'string'
        }
    }
}


def validate_student(data):
    try:
        validate(data, student)
        return {'msg': 'success'}
    except SchemaError as e:
        return {'msg': 'error', 'error': e.message}
    except ValidationError as e:
        return {'msg': 'error', 'error': e.message}

