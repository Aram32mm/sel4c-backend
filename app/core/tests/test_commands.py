"""
Testea los comandos de administración personalizados de Django.
"""
# para simular el comportamiento
from unittest.mock import patch

# importamos error de libreria psycopg2
from psycopg2 import OperationalError as Psycopg2OpError

# helper function de Django que llama commando
from django.core.management import call_command

# hay 2 excepciones que podria ocurrir, la de psycopg2 y esta
from django.db.utils import OperationalError
from django.test import SimpleTestCase  # para test simple


# decorador para especificar el comando que estaremos simulando
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """ Test commands """

    def test_wait_for_db_ready(self, patched_check):
        """ Test a la espera de la base de datos, si la base de datos
            está lista. """
        patched_check.return_value = True

        call_command('wait_for_db')

        patched_check.assert_called_once_with(databases=['default'])

    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """ Test a la espera de la base de datos, si la base de datos
        NO está lista.(OperationalError)    """
        # Las primeras 2 veces testeamos el error psycopg2
        # Las siguientes 3 testeamos el otro
        # Los valores no importan en realidad
        # se pueden testear las veces que se desee
        patched_check.side_effect = [Psycopg2OpError] * 2 + \
            [OperationalError] * 3 + [True]

        call_command('wait_for_db')

        self.assertEqual(patched_check.call_count, 6)
        patched_check.assert_called_with(databases=['default'])
