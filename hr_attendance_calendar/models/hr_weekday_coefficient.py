# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2018 Compassion CH (http://www.compassion.ch)
#    @author: Stephane Eicher <seicher@compassion.ch>
#
#    The licence is in the file __manifest__.py
#
##############################################################################

from odoo import models, fields, api


class HrWeekdayCoefficient(models.Model):
    _name = "hr.weekday.coefficient"

    ##########################################################################
    #                                 FIELDS                                 #
    ##########################################################################
    name = fields.Char(compute='_compute_name')
    day_of_week = fields.Selection([
        ('0', 'Monday'),
        ('1', 'Tuesday'),
        ('2', 'Wednesday'),
        ('3', 'Thursday'),
        ('4', 'Friday'),
        ('5', 'Saturday'),
        ('6', 'Sunday'),
        ('7', 'Default')], 'Day of Week', required=True, index=True,
        default='0')
    category_ids = fields.Many2many('hr.employee.category',
                                    string='Employee tag')
    coefficient = fields.Float(
        help='Multiply the worked hours by the coefficient')

    ##########################################################################
    #                             FIELDS METHODS                             #
    ##########################################################################
    @api.multi
    @api.depends('coefficient')
    def _compute_name(self):
        for rd in self:
            rd.name = rd.coefficient
