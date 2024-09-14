/** @odoo-module **/
import { isBarcodeScannerSupported, scanBarcode} from "@web/webclient/barcode/barcode_scanner";
import { bus } from "@bus/services/bus_service";
import { ConfirmationDialog } from "@web/core/confirmation_dialog/confirmation_dialog";
import { registry } from "@web/core/registry";
import { useService,useBus } from "@web/core/utils/hooks";
import { EventBus } from "@odoo/owl";

const { Component, onMounted, onWillUnmount, onWillStart, useState, onWillDestroy} = owl;

export class MainMenu extends Component {
    setup() {
    super.setup();
        const user = useService('user');
        const bus = new EventBus();
        this.actionService = useService("action");
        this.dialogService = useService('dialog');
        this.notificationService = useService("notification");
        this.rpc = useService('rpc');
        this.orm = useService('orm');
        const barcode = useService("barcode");
        useBus(barcode.bus, "barcode_scanned", (ev) => this.onBarcodeScanned(ev.detail.barcode));

        onMounted(() => {
            bus.trigger('barcode_scanned', this, this.onBarcodeScanned);
        });
        onWillUnmount(() => {
            bus.trigger('barcode_scanned', this, this.onBarcodeScanned);
        });

        onWillDestroy(() => {
            bus.trigger('barcode_scanned', this, this.onBarcodeScanned);
        });
    }
    async onBarcodeScanned(barcode) {
        this.open_delivery_order_scanned (barcode)
        }
     async show_picking_order(){
             this.actionService.doAction('eg_stock_barcode.stock_picking_type_kanban_view_action');
        }
     async back_to_main_menu()
     {
     this.actionService.doAction('mail.action_discuss');
     }
     async open_barcode_prompt(){
        var self = this;
        swal({
          title: "Add barcode manually",
          text: "Enter Barcode for open location,picking type or picking order!",
          type: "input",
          showCancelButton: true,
          closeOnConfirm: false,
          animation: "slide-from-top",
          inputPlaceholder: "Enter Barcode"
        },
        (barcode)=>{
              if (barcode === false) return false;
              if (barcode === "") {
                swal.showInputError("Enter Barcode");
                return false
              }
              this.open_delivery_order_scanned(barcode);
        }
        )
     }

     async open_delivery_order_scanned (barcode){
            var self = this;
            // if check when barcode scan not main page and scan stock piking barcode page when not run main page scan
            if (barcode){
                this.rpc('/stock_details/open_picking_barcode', {
                  barcode: barcode,
                })
                .then(function(result) {
                    if (result){
                    // for Location found
                        if (result.location_id){
                        swal({title:"Location Found",text:"Location found given barcode" , type:"success",timer:2000});
                            return self.actionService.doAction(result.action);


                        }
                        // for picking type (operation picking type) found
                        else if (result.stock_operation_type_id){
                        swal({title:"Stock Picking Found",text:"stock Picking found given barcode" , type:"success",timer:2000});
                             return self.actionService.doAction(result.action);


                        }
                        // for picking order found
                        else if (result.context){
                        swal({title:"Picking Order Found",text:"Picking Order found given barcode" , type:"success",timer:2000});
                             return self.actionService.doAction(result);
                        }
                        // error when not location, picking type and picking order found
                        else{
                            swal("Not Found!", "Record not found for given barcode : "+result.barcode, "error");
                        }
                    }
                });
           }
           else{
             this.actionService.doAction('eg_stock_barcode.action_barcode_scan_main_menu');
           }
        }
}
MainMenu.template = 'eg_stock_barcode.StockBarcodeScanWidget';
MainMenu.components = { scanBarcode };

registry.category('actions').add('stock_barcode_main_menu', MainMenu);