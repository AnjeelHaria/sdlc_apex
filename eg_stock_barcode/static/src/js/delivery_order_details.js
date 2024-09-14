/** @odoo-module **/

import { bus } from "@bus/services/bus_service";
import { Component,useState, onWillUpdateProps, onWillStart } from "@odoo/owl";
import { isBarcodeScannerSupported, scanBarcode} from "@web/webclient/barcode/barcode_scanner";
import { useBus, useService } from "@web/core/utils/hooks";
import { registry } from "@web/core/registry";
import { renderToString } from "@web/core/utils/render"
import { _t } from "@web/core/l10n/translation";



export class StockPickingDetails extends Component {

     setup() {
        super.setup();
        this.actionService = useService("action");
        this.dialog = useService("dialog");
        this.notification = useService("notification");
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        this.state = useState({
            hierarchy: {},
            picking_dict:{},
            });

        const { default_event_id, active_model, active_id } = this.props.action.context;
        this.picking_id = active_id || (active_model === "stock.picking" && active_id);
        this.isMultiEvent = !this.picking_id;

        const barcode = useService("barcode");
        useBus(barcode.bus, "barcode_scanned", (ev) => this.onBarcodeScanned(ev.detail.barcode));

        onWillStart(async () => await this.fetchHierarchy(this.picking_id));
        onWillUpdateProps(async (nextProps) => {
            await this.fetchHierarchy(this.picking_id);
        });
    }
    async fetchHierarchy(picking_id) {

       this.state.hierarchy = await this.orm.call("stock.picking", "barcode_stock_picking_data_get", [], {
            picking_id: this.picking_id,
        });
    }
    async back_to_main_menu(event)
    {
    this.actionService.doAction('eg_stock_barcode.stock_picking_action_kanban_for_stock_barcode');
    }
   // when Barcode Scan when call this Method and add new product or add a Done Quantity
   async onBarcodeScanned (product_barcode){
        var self = this;
        const result = await this.orm.call("stock.picking", "add_new_order_line", [], {

        picking_id: this.picking_id,
        product_barcode : product_barcode
    });

      if (result.order){
                swal({title:"Success!", text:"Product Added Successfully!", type:"success",timer:2000});
                var $all_rows = $('.stock-move-line-row');
                self.picking_dict = result;
                var youContextData = {};
                var new_product_orderline_qweb = window.$(
                    renderToString('BarcodeStockMoveLine', {
                    'picking_id': result,
                    'updated_line_id': result.updated_line_id,
                })
                );
                $all_rows.replaceWith(new_product_orderline_qweb);
                 $('html').animate({
                    scrollTop: parseInt($("#blink").offset().top)
                 }, 1000);
        }
        else{ swal({title:"Not Found!", text:result.message, type:"error",timer:2000});}

        }

   /* Validate a Picking Order if check a not done state show a python wizard (like backorder) and after show a updated data */
        async validate_picking_order(){
            var self = this;
            const result = await this.orm.call("stock.picking", "validate_picking_order", [], {
                picking_id: this.picking_id,
            });
            if (result.name){
                this.actionService.doAction(result,{

                    onClose: async () => { const result = await this.orm.call("stock.picking", "open_picking_order", [], {
                            picking_id: this.picking_id,
                        });
             var $page_content_wrapper = $('.stock_body_footer');
                            self.picking_dict = result;
                            var stock_barcode_qweb = window.$(
                        renderToString('StockBodyFooter', {
                        'picking_id': result,
                        'updated_line_id': result.updated_line_id,
                    })
                    );
                    $page_content_wrapper.replaceWith(stock_barcode_qweb);
                   },
                });
            }
            else{
                var $page_content_wrapper = $('.stock_body_footer');
                self.picking_dict = result;
                var stock_barcode_qweb = window.$(
                        renderToString('StockBodyFooter', {
                        'picking_id': result,
                        'updated_line_id': result.updated_line_id,
                    })
                    );
                $page_content_wrapper.replaceWith(stock_barcode_qweb);
            }
       }


        // open prompt when enter Barcode Manually
       async open_barcode_prompt(){
            var self = this;
            swal({
              title: "Add Product Barcode!",
              text: "Enter Product Barcode for add new Product",
              type: "input",
              showCancelButton: true,
              closeOnConfirm: false,
              animation: "slide-from-top",
              inputPlaceholder: "Enter Product Barcode"
            },
            (inputValue)=>{
                  if (inputValue === false) return false;
                  if (inputValue === "") {
                    swal.showInputError("Please enter product Barcode");
                    return false
                  }
                  var order_barcode = self.order_barcode;
                  self.onBarcodeScanned(inputValue,self.picking_id);
            }
            )
        }
       // pencil button click when visible a done quantity and lot input and invisible done quantity and lot (given value)
       async change_product_quantity_prompt(event){
            if($(event.target).parents('.stock-move-line-row').hasClass('edited-mode')){
//                alert('Update Edited line!'); // when one line edited when another line not update and show alert
                alert(_t('Update Edited line!'));
            }
            else{
                var use_create_lot = $(event.target).attr('use-create-lot'); // picking type lot create or not
                var isCreateLots = (use_create_lot === 'true');
                 $(".lot-dynamic-selection").selectize({
                    create: isCreateLots,
                 });
                $(event.target).parent().hide();
                $(event.target).parents('tr').find('.update_quantity-lot').show(); // check button visible
                $(event.target).parents('tr').find('.done_quantity_text').hide(); // hide done quantity
                $(event.target).parents('tr').find('.new-updated-done_quantity').css("display","inline-block"); // done quantity input visible
                $(event.target).parents('tr').find('.lot-assign-input-text').hide(); // lot hide
                $(event.target).parents('tr').find('.lot-assign-input').css("display","inline-block"); // lot selection visible

            }
        }
    // when done quantity and lot updated when update a line
        async update_stock_move_line(event){
            var self = this;
            var order_barcode = self.order_barcode;
            var line_id =$(event.target).parents('tr').find('#update-line-quantity-lot').attr('data-line-id');
            var new_updated_done_quantity = $(event.target).parents('tr').find('.new-updated-done_quantity').val();
            var lot_number = $(event.target).parents('tr').find('.lot-enter-input').val();
            if (lot_number){
                lot_number = lot_number;
            }
            else{
                lot_number = false;
            }
            $(event.target).parents('tr').find('.lot-assign-input-text').show();
            $(event.target).parents('.stock-move-line-row').removeClass('edited-mode');
                   const result = await this.orm.call("stock.picking", "edit_done_qty", [parseInt(line_id),parseFloat(new_updated_done_quantity),lot_number], {

            });
            if (result.order){
                var $all_rows = $('.stock-move-line-row');
                self.picking_dict = result;
                var new_product_orderline_qweb = window.$(
                    renderToString('BarcodeStockMoveLine', {
                    'picking_id': result,
                    'updated_line_id': result.updated_line_id,
                })
                );

                $all_rows.replaceWith(new_product_orderline_qweb);
                 $('html').animate({
                    scrollTop: parseInt($("#blink").offset().top)
                 }, 1000);
                swal({title:"Success!", text:"Update Successfully!", type:"success",timer:2000});
            }
            else{
               alert( _t(result.message));
                }
        }

        // Todo mark as a order (python action_confirm method call)
          async action_confirm (event){
                    var self = this;
                     const result = await this.orm.call("stock.picking", "mark_as_todo_order", [self.picking_id], {
                });
                if (result.context){
                    var $page_content_wrapper = $('.stock_body_footer');
                    self.picking_dict = result;
                    var stock_barcode_qweb = window.$(
                        renderToString('StockBodyFooter', {
                        'picking_id': result,
                        'updated_line_id': false,
                    })
                    );
                    $page_content_wrapper.replaceWith(stock_barcode_qweb);
                }
                else{
                    alert(_t(result.message));
                    }
                }

      // When +1 Button Click when add 1 Quantiy in Selected Orderline
        async plus_one_done_qty (event){
            var self = this;
            var line_id =$(event.target).attr('data-line-id')? $(event.target).attr('data-line-id'):$(event.target).closest('.no_border_input').attr('data-line-id');
            this.rpc("/stock_details/plus_one", {line_id: line_id})
            .then(function(result) {
                $(event.target).parents('tr').find('.done_quantity_text').text(result);
                var high_lighted_line =  $(event.target).parents('.stock-move-line-row').find('.blink');
                if (high_lighted_line){
                    high_lighted_line.removeClass('blink');
                }
                $(event.target).parents('tr').addClass('blink');
            });
        }

       // When -1 Button Click when decrease 1 quantity
        async decrease_one_done_qty(event){
            var self = this;
            var line_id =$(event.target).attr('data-line-id')? $(event.target).attr('data-line-id'):$(event.target).closest('.no_border_input').attr('data-line-id');
            this.rpc("/stock_details/decrease_one",{line_id: line_id})
            .then(function(result) {
                $(event.target).parents('tr').find('.done_quantity_text').text(result);
                var high_lighted_line =  $(event.target).parents('.stock-move-line-row').find('.blink');
                if (high_lighted_line){
                    high_lighted_line.removeClass('blink');
                }
                $(event.target).parents('tr').addClass('blink');

            });
        }
    }
StockPickingDetails.template = 'eg_stock_barcode.StockPickingDetails';
StockPickingDetails.components = { scanBarcode };

registry.category('actions').add('stock_picking_details_client_action', StockPickingDetails);