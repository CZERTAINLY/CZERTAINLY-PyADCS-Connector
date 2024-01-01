from django.http import JsonResponse

import logging

from PyADCSConnector.exceptions.winrm_execution_exception import WinRMExecutionException

logger = logging.getLogger(__name__)


class ExceptionHandlerMiddleware:
    """Handle uncaught exceptions instead of raising a 500.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    @staticmethod
    def process_exception(request, exception):
        """
        Handle uncaught exceptions.
        """
        if isinstance(exception, WinRMExecutionException):
            logger.info("WinRMExecutionException occurred: " + str(exception))
            logger.exception(exception)
            return JsonResponse({'message': str(exception)}, status=400)
        if isinstance(exception, Exception):
            logger.info("Exception occurred: " + str(exception))
            logger.exception(exception)
            # Or you could return json for your frontend app
            return JsonResponse({'message': str(exception)}, status=500)

        return None  # Middlewares should return None when not applied
