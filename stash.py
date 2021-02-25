# Britsa Inc. All Rights Reserved (c) 2021
# service-stash PyPI package

from firebase_admin import credentials, firestore, initialize_app
import logging
import ast

from rest_framework.response import Response
import os
import logging
from dotenv import load_dotenv
logger = logging.getLogger(__name__)


logger = logging.getLogger(__name__)

LOGGER_PREFIX: str = 'Brittsa (service-stash): '


def connect_firestore_with_key(collection_name: str, firestore_key: str or dict):
    try:
        logger.debug(
            f"{LOGGER_PREFIX}Establishing connection to Firebase's Firestore")
        cred = credentials.Certificate(ast.literal_eval(firestore_key))
        initialize_app(cred)
    except ValueError:
        logger.info(f"{LOGGER_PREFIX}Firebase's firestore app is initialized already")
    finally:
        database = firestore.client()
        logger.info(f"{LOGGER_PREFIX}Firebase's firestore app is successfully connected")
        document_reference = database.collection(collection_name)
        return document_reference


class App_Exception(Exception):
    def _init_(self, app_response_code: AppResponseCodes, message: str or None = None, validation_error: bool = False) -> None:
        super(App_Exception, self)._init_(app_response_code.error_message())

        if not message:
            message = ''
        else:
            message = f' [msg= {message}]'

        self.__app_response_statement: str = f'{app_response_code.error_message()}{message} ({app_response_code.error_code()})'
        logger.error(f'Exception raised on {self.__app_response_statement}')

        if validation_error:
            self.__http_code: HTTPResponseCodes = HTTPResponseCodes.INVALID_INPUT_PARAMETERS
        else:
            self.__http_code: HTTPResponseCodes = HTTPResponseCodes.INTERNAL_SERVER_ERROR

    def response(self) -> Response:
        logger.error(f'{self._http_code.status_code()} {self.http_code.status_message()} error response out for {self._app_response_statement})')
        error_response_object: dict = {
            'error_description': self.__http_code.status_message(),
        }
        return Response(error_response_object, status=self.__http_code.status_code())


def get_env(key: str) -> str or App_Exception:
    response_value: str or None = os.environ.get(key)
    if response_value:
        response_value = str(response_value)
        return response_value
    else:
        logger.warning('Application loading .env file')
        load_dotenv()
        logger.info('.env loaded successfully.')
        response_value = os.environ.get(key)
        if response_value:
            response_value = str(response_value)
            return response_value
    raise App_Exception(AppResponseCodes.ENVIRONMENT_NOT_FOUND, message=key, validation_error=False)    




