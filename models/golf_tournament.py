from odoo import models, fields, _, api
from odoo.exceptions import ValidationError
from itertools import chain

class GolfTournament(models.Model):
    _name = 'golf.tournament'
    _description = 'a golf tournament'

    name = fields.Char(
        string='Name',
        required=True,
        default=lambda self: _('New'),
        copy=False
    )

    date = fields.Date(string=_('Date'))

    field_ids = fields.Many2many(
        string=_('Fields'),
        comodel_name='golf.field',
    )

    card_ids = fields.One2many('golf.card','tournament_id',string=_('Cards'))
    card_count = fields.Integer(compute = '_count_cards')

    default_product_id = fields.Many2one(
        string='Default Product',
        comodel_name='product.template',
        ondelete='restrict',
    )
    
    def _count_cards(self):
        for rec in self:
            rec.card_count = len([x for x in rec.card_ids if x.net_score > 0])
    
    def get_holes(self):
        holes = []
        for field in self.field_ids:
            holes += list(field.hole_ids)
        print("holes",holes)
        return holes
        
    def action_open_leaderboard(self):
        for tournament in self:
            action = self.env.ref("golf.action_golf_leaderboard_act_window").read()[0]
            action["context"] = {}
            action["domain"] = ['&',("id", "in", tournament.card_ids.ids),("net_score",">",0)]
            return action
    
    