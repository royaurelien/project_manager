# -*- coding: utf-8 -*-

from email.policy import default
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)



class Project(models.Model):
    _inherit = 'project.project'

    todo_ids = fields.One2many(comodel_name='project.todo', inverse_name='project_id')
    todo_next_number = fields.Integer(default=1)
    todo_count = fields.Integer(compute='_compute_todo')

    @api.depends('todo_ids')
    def _compute_todo(self):
        for record in self:
            record.todo_count = len(record.todo_ids)

    def action_view_todo(self):
        self.ensure_one()

        action = self.env.ref("project_todo.action_view_todo").read()[0]
        action["context"] = dict(self.env.context)
        action["context"].pop("group_by", None)
        action["context"].update({
            'default_project_id': self.id,
        })
        # action["context"]["search_default_repository_id"] = self.id
        action["domain"] = [('project_id', '=', self.id)]

        _logger.warning(action["context"])

        return action