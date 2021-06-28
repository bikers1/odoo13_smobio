# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HrLeaveAllocation(models.Model):
    _name = "hr.leave.allocation"
    _inherit = ["hr.leave.allocation", "tier.validation"]
    _state_from = ["draft", "confirm"]
    _state_to = ["validate1", "validate"]
