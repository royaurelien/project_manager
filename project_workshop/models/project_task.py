# -*- coding: utf-8 -*-

from email.policy import default
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)



class Project(models.Model):
    _inherit = 'project.project'

    allow_workshop = fields.Boolean(default=False)
    # todo_ids = fields.One2many(comodel_name='project.todo', inverse_name='project_id')
    # todo_next_number = fields.Integer(default=1)

class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.model
    def _default_partners(self):
        partners = self.env.user.partner_id
        return partners

    def _get_companies(self):
        # partners = self.env.user.partner_id
        company_ids = self.attendee_ids.mapped('company_name')
        _logger.error(self.attendee_ids)

        companies = [(rec.id, rec.name) for rec in company_ids]
        _logger.warning(companies)

        return companies

    allow_workshop = fields.Boolean(related='project_id.allow_workshop')
    is_workshop = fields.Boolean(default=False)

    attendee_ids = fields.Many2many(
        'res.partner', 'project_task_attendee_res_partner_rel',
        string='Attendees', default=_default_partners)

    @api.onchange('workshop_subject', 'is_workshop')
    def _onchange_workshop(self):
        if self.is_workshop and self.workshop_subject:
            self.name = "Workshop: {}".format(self.workshop_subject)

    workshop_subject = fields.Char()
    workshop_location = fields.Char()
    workshop_url = fields.Char()
    workshop_date = fields.Datetime()
    workshop_content = fields.Html()
    workshop_note = fields.Text()

