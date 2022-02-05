# -*- coding: utf-8 -*-

from email.policy import default
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)



class ProjectTask(models.Model):
    _inherit = 'project.task'

    todo_ids = fields.One2many(comodel_name='project.todo', inverse_name='task_id')
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
            'default_task_id': self.id,
            'default_project_id': self.project_id.id,
        })
        # action["context"]["search_default_repository_id"] = self.id
        action["domain"] = [('id', 'in', self.todo_ids.ids)]

        _logger.warning(action["context"])

        # action = {
        #     'name': _("Update %s", self.definition_id.name),
        #     'id': self.id,
        #     'type': 'ir.actions.act_window',
        #     'views': [[False, 'form']],
        #     'target': 'new',
        #     'context': {'default_goal_id': self.id, 'default_current': self.current},
        #     'res_model': 'gamification.goal.wizard'
        # }

        return action