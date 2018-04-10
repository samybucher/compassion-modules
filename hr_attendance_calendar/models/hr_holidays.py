# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2018 Compassion CH (http://www.compassion.ch)
#    @author: Stephane Eicher <seicher@compassion.ch>
#
#    The licence is in the file __manifest__.py
#
##############################################################################
import logging

from odoo import models, fields, api

_logger = logging.getLogger(__name__)


class HrHolidays(models.Model):
    _inherit = 'hr.holidays'

    ##########################################################################
    #                                 FIELDS                                 #
    ##########################################################################
    hr_att_day_ids = fields.Many2many('hr.attendance.day',
                                      string='Attendance day related')

    ##########################################################################
    #                               ORM METHODS                              #
    ##########################################################################
    @api.model
    def create(self, vals):
        rd = super(HrHolidays, self).create(vals)
        rd.find_attendance_day()
        return rd

    @api.multi
    def write(self, vals):
        super(HrHolidays, self).write(vals)
        if 'date_from' in vals or 'date_to' in vals:
            self.find_attendance_day()
            self.hr_att_day_ids.recompute_due_hours()
        return True

    ##########################################################################
    #                             PUBLIC METHODS                             #
    ##########################################################################
    @api.multi
    def find_attendance_day(self):
        for rd in self:
            rd.hr_att_day_ids = self.env['hr.attendance.day'].search([
                ('employee_id', '=', rd.employee_id.id),
                ('date', '>=', rd.date_from),
                ('date', '<=', rd.date_to)
            ])

    @api.model
    def compute_work_day(self, str_date):
        """
        Compute if the leave duration for the day is full/half work day.

        :param str_date: date to compute (string)
        :return: daily leave duration (in days)
        :rtype: float [1,0.5]
        """

        start = fields.Datetime.context_timestamp(self.employee_id,
                                                  fields.Datetime.from_string(
                                                      self.date_from))

        end = fields.Datetime.context_timestamp(self.employee_id,
                                                fields.Datetime.from_string(
                                                    self.date_to))

        date = fields.Date.from_string(str_date)
        date = start.replace(year=date.year, month=date.month, day=date.day,
                             hour=12, minute=0, second=0)

        if start.date() == date.date():
            if start < date:
                return 1
            else:
                return 0.5
        elif end.date() == date.date():
            if end > date:
                return 1
            else:
                return 0.5
        elif start.date() < date.date() < end.date():
            return 1
        else:
            _logger.error(
                "This attendance day doesn't correspond to this leave"
            )
            return 0