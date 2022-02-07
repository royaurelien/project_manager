# -*- coding: utf-8 -*-

from email.policy import default
from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError
import logging

_logger = logging.getLogger(__name__)



class ProjectTask(models.Model):
    _inherit = 'project.task'

    @api.model
    def _default_attendees(self):
        partners = self.env.user.partner_id

        return partners

    def get_companies(self):
        # partners = self.env.user.partner_id
        # company_ids = self.attendee_ids.mapped('company_id').partner_id

        partner_ids = self.attendee_ids.filtered(lambda rec: rec.company_type == 'company')
        others = self.attendee_ids - partner_ids
        partner_ids |= others.filtered(lambda rec: rec.parent_id).mapped('parent_id')
        partner_ids |= self.attendee_ids.mapped('company_id.partner_id')

        _logger.error(self.attendee_ids)

        companies = [(rec.id, rec.name) for rec in partner_ids]
        _logger.warning(companies)

        return companies

    partner_spoc_id = fields.Many2one(related='project_id.partner_spoc_id', readonly=True)
    allow_workshop = fields.Boolean(related='project_id.allow_workshop')
    is_workshop = fields.Boolean(default=False)
    is_workshop_locked = fields.Boolean(default=False)
    workshop_version = fields.Char()
    workshop_subject = fields.Char()
    workshop_location = fields.Char()
    workshop_url = fields.Char()
    workshop_date = fields.Datetime()
    workshop_content = fields.Html()
    workshop_note = fields.Text()
    attendee_ids = fields.Many2many(
        'res.partner', 'project_task_attendee_res_partner_rel',
        string='Attendees', default=_default_attendees)

    @api.onchange('workshop_subject', 'is_workshop')
    def _onchange_workshop(self):
        if self.is_workshop and self.workshop_subject:
            self.name = "{}: {}".format(self.project_id.workshop_name, self.workshop_subject)


    def action_toggle_workshop_lock(self):
        self.ensure_one()
        self.is_workshop_locked = not self.is_workshop_locked

        return True


    def action_workshop_report_send(self):
        ''' Opens a wizard to compose an email, with relevant mail template loaded by default '''
        self.ensure_one()

        if not self.is_workshop_locked:
            raise ValidationError("You must lock workshop before send it.")

        template_id = self.env['ir.model.data'].xmlid_to_res_id('project_workshop.email_template_workshop', raise_if_not_found=False)
        lang = self.env.context.get('lang')
        template = self.env['mail.template'].browse(template_id)
        if template.lang:
            lang = template._render_lang(self.ids)[self.id]
        ctx = {
            'default_model': 'project.task',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            # 'mark_so_as_sent': True,
            # 'custom_layout': "mail.mail_notification_paynow",
            'force_email': True,
            # 'model_description': self.with_context(lang=lang).type_name,
        }
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': ctx,
        }