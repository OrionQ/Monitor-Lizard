from split_settings.tools import optional, include

include(
    'components/base.py',
    optional('components/email.py'),
)