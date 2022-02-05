# -*- coding: utf-8 -*-

from email.policy import default
from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)


class ProjectTodoType(models.Model):
    _name = 'project.todo.type'
    _description = "Project ToDo Type"

    active = fields.Boolean(default=True)
    name = fields.Char(required=True)
    code = fields.Char(required=True)


class ProjectTodo(models.Model):
    _name = 'project.todo'
    _description = "Project ToDo"

    name = fields.Char(compute='_compute_name')
    description = fields.Text()
    sequence = fields.Integer(required=True, default=1, index=True)
    is_done = fields.Boolean(default=False)
    project_id = fields.Many2one(comodel_name='project.project', required=True)
    task_id = fields.Many2one(comodel_name='project.task', required=True)
    type_id = fields.Many2one(comodel_name='project.todo.type', required=True)
    partner_id = fields.Many2one(comodel_name='res.partner', required=True)
    date_deadline = fields.Date()

    @api.depends('type_id', 'sequence')
    def _compute_name(self):
        for record in self:
            record.name = "{o.type_id.code}{o.sequence}".format(o=record) if record.type_id else ""

    @api.model
    def create(self, vals):
        project = self.env['project.project'].browse(vals.get('project_id'))
        vals.update({'sequence': project.todo_next_number})
        res = super(ProjectTodo, self).create(vals)

        project.todo_next_number += 1

        return res


