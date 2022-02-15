from odoo import models, fields, _, api
from odoo.exceptions import ValidationError
from itertools import chain, groupby
from operator import attrgetter
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
    field_id = fields.Many2one(
        string=_('Field'),
        comodel_name='golf.field',
    )

    card_ids = fields.One2many('golf.card','tournament_id',string=_('Cards'))
    card_count = fields.Integer(compute = '_count_cards')
    active_card_count = fields.Integer(compute = '_count_cards')
    player_ids = fields.Many2many('res.partner', string='Players', domain=[("golf_player", "=", True)])

    default_product_id = fields.Many2one(
        string='Default Product',
        comodel_name='product.template',
        ondelete='restrict',
    )
    tournament_mode_id = fields.Many2one('golf.tournament_mode', string = _('Mode'))

    @api.depends('card_ids')
    def _count_cards(self):
        for rec in self:
            rec.card_count = len(rec.card_ids)
            rec.active_card_count = len([x for x in rec.card_ids if x.net_score > 0])
            rec.player_ids = rec.mapped("card_ids.player_id")
    
    def get_holes(self):
        holes = list(self.field_id.hole_ids)
        return holes

    def action_print_leaderboard(self):
        for tournament in self:
            print("PRINT LEADERBOARD",tournament)
                
    def action_open_leaderboard(self):
        for tournament in self:
            action = self.env.ref("golf.action_golf_leaderboard_act_window").read()[0]
            action["context"] = {}
            action["domain"] = ['&',("id", "in", tournament.card_ids.ids),("position",">",0)]
            return action

    
    @api.onchange("card_ids")
    def action_leaderboard(self):
        print("CALLING COMPUTE")
        self.tournament_mode_id._process_cards(self)

    