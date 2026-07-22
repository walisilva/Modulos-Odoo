/** @odoo-module **/

import { patch } from "@web/core/utils/patch";
import { crmKanbanView } from "@crm/views/crm_kanban/crm_kanban_view";
import { onWillUnmount, useState } from "@odoo/owl";

const AUTO_REFRESH_INTERVAL_MS = 30000;

patch(crmKanbanView.Controller.prototype, {
    setup() {
        super.setup();
        this.fpAutoRefreshState = useState({ enabled: false });
        this.fpAutoRefreshTimer = null;
        onWillUnmount(() => this.fpStopAutoRefresh());
    },

    fpOnToggleAutoRefresh(ev) {
        this.fpAutoRefreshState.enabled = ev.target.checked;
        if (this.fpAutoRefreshState.enabled) {
            this.fpStartAutoRefresh();
        } else {
            this.fpStopAutoRefresh();
        }
    },

    fpStartAutoRefresh() {
        this.fpStopAutoRefresh();
        this.fpAutoRefreshTimer = setInterval(() => {
            this.model.load();
        }, AUTO_REFRESH_INTERVAL_MS);
    },

    fpStopAutoRefresh() {
        if (this.fpAutoRefreshTimer) {
            clearInterval(this.fpAutoRefreshTimer);
            this.fpAutoRefreshTimer = null;
        }
    },
});
