# -*- coding: utf-8 -*-
from odoo import api, fields, models


class HrLeave(models.Model):
    _name = "hr.leave"
    _inherit = ["hr.leave", "tier.validation"]
    _state_from = ["draft", "confirm"]
    _state_to = ["validate1", "validate"]
