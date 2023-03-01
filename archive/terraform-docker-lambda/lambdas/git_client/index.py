import logging
import os
import git

TMP_DIR = "/tmp"
REPO_DIR = 'aws-config-rules'
REPO_URL = f'https://github.com/andreivmaksimov/{REPO_DIR}'
CLONE_PATH = os.path.join(TMP_DIR, REPO_DIR)

LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)


def clone(branch='master'):
    repo = git.Repo.clone_from(REPO_URL, CLONE_PATH, branch=branch)

    with repo.config_writer() as git_config:
        git_config.set_value('user', 'email', 'no-reply@hands-on.cloud')
        git_config.set_value('user', 'name', 'Git Lambda')


def handler(event, context):
    LOGGER.info('Event: %s', event)

    LOGGER.info('Cloning repo: %s', REPO_URL)
    clone()
