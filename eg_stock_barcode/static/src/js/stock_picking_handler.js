/* @odoo-module */
import { KanbanRecord } from "@web/views/kanban/kanban_record";

export class StockBarcodeKanbanRecord extends KanbanRecord {
 async _openRecord() {
        var self = this;
        if (this.modelName === 'stock.picking') {
            this.$('button').first().click();
        } else {
            this._super.apply(this, arguments);
        }
    }
}

