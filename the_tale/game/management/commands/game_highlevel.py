# coding: utf-8
import sys
import traceback

from django.core.management.base import BaseCommand
from django.utils.log import getLogger

from dext.utils import pid

from game.workers.environment import workers_environment

logger = getLogger('the-tale.workers.game_highlevel')

class Command(BaseCommand):

    help = 'run game logic'

    requires_model_validation = False

    @pid.protector('game_highlevel')
    def handle(self, *args, **options):

        try:
            workers_environment.highlevel.run()
        except KeyboardInterrupt:
            pass
        except Exception:
            traceback.print_exc()
            logger.error('Game worker exception: game_highlevel',
                         exc_info=sys.exc_info(),
                         extra={} )

        workers_environment.deinitialize()
