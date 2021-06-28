odoo.define("hr_dep_chart_overview", function (require) {
    "use strict";

    var core = require("web.core");
    var HrOrgChartOverview = require("hr_org_chart_overview");

    var HrDepChartOverview = HrOrgChartOverview.extend({

        willStart: function () {
            this._super.apply(this, arguments)
            var self = this;
            var def = this._rpc({
                model: "hr.department",
                method: "get_organization_department_data",
            }).then(function (res) {
                // console.log(res)
                self.orgChartData = res;
                return;
            });

            return Promise.all([def]);
        },

        start: function () {
            var parent_result = this._super.apply(this, arguments);
            this.oc.exportFilename = "MyDepartmentChart";
            return parent_result;
        },
    });

    core.action_registry.add("hr_dep_chart_overview", HrDepChartOverview);

    return HrDepChartOverview;
});