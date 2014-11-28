from django.core import management

import kronos

# search index update
@kronos.register('10 * * * *')
def remove_expired():
    management.call_command('update_index', verbosity=0, interactive=False)
