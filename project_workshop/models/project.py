# -*- coding: utf-8 -*-

from email.policy import default
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)



class Project(models.Model):
    _inherit = 'project.project'

    allow_workshop = fields.Boolean(default=False)
    workshop_name = fields.Char(default=_('Workshop'))
    partner_spoc_id = fields.Many2one(comodel_name="res.partner", string="SPOC")
