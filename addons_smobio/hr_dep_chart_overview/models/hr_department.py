# Copyright 2020 ForgeFlow S.L. (https://www.forgeflow.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, models

dep_chart_classes = {
    0: "level-0",
    1: "level-1",
    2: "level-2",
    3: "level-3",
    4: "level-4",
}

class HrDepartment(models.Model):
    _inherit = "hr.department"

    def _get_department_domain(self, parent_id):
        company = self.env.company
        domain = [("company_id", "=", company.id)]
        if not parent_id:
            domain.extend([
                ("parent_id", "=", False),
                ("child_ids", "!=", False)
            ])
        else:
            domain.append(("parent_id", "=", parent_id))
        return domain

    def _get_department_data(self, level=0):
        return {
            "id": self.manager_id.id,
            "name": self.name,
            "title": self.manager_id.job_id.name,
            "className": dep_chart_classes[level],
            "image": self.env["ir.attachment"].sudo().search([
                ("res_model", "=", "hr.employee"),
                ("res_id", "=", self.manager_id.id),
                ("res_field", "=", "image_512"),
            ], limit=1,).datas,
        }

    @api.model
    def _get_children_data(self, child_ids, level):
        children = []
        for department in child_ids:
            data = department._get_department_data(level)
            department_child_ids = self.search(
                self._get_department_domain(department.id))
            if department_child_ids:
                data.update(
                    {
                        "children": self._get_children_data(
                            department_child_ids, (level + 1) % 5
                        )
                    }
                )
            children.append(data)
        return children

    @api.model
    def get_organization_department_data(self):
        domain = self._get_department_domain(False)
        top_department = self.search(domain, limit=1)
        data = top_department._get_department_data()
        top_department_child_ids = self.search(
            self._get_department_domain(top_department.id))
        if top_department_child_ids:
            data.update({
                "children": self._get_children_data(top_department_child_ids, 1)
            })
        return data
