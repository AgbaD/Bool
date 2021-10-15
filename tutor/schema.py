from jsonschema import validate
from jsonschema.exceptions import ValidationError, SchemaError

TutorModel = {
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
        }
    }
}


def validate_tutor(data):
    try:
        validate(data, TutorModel)
        return {'msg': 'success'}
    except SchemaError as e:
        return {'msg': 'error', 'error': e.message}
    except ValidationError as e:
        return {'msg': 'error', 'error': e.message}

