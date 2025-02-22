from itertools import groupby
from operator import attrgetter
from odoo import models, fields, _, api


class GolfTournamentMode(models.Model):
    _inherit = "golf.tournament_mode"

    def _process_cards_strokes(self,tournament):
        cards = list(x for x in tournament.card_ids if x.net_score > 0)
        get_score = attrgetter('net_score')
        res = [list(v) for l,v in groupby(sorted(cards,key = get_score), get_score)]        
        self._set_positions(res)
        
    def _process_cards(self,tournament):
        if self.code == 'STROKES':
            # process cards
            self._process_cards_strokes(tournament)
            return None
        return super()._process_cards(tournament)

        
