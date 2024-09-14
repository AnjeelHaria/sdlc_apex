/* @odoo-module */
import * as ogutils from "@web/webclient/actions/reports/utils";
import { getReportUrl } from "@web/webclient/actions/reports/utils";
import { download } from "@web/core/network/download";
import { session } from '@web/session';
import { useService } from '@web/core/utils/hooks';
import { jsonrpc } from "@web/core/network/rpc_service";
import { _t } from "@web/core/l10n/translation";

var company_id = session.user_companies.current_company;
var print_copies = 1;
var printer_name = null;
var printer_type = 'zpl'
var controller_url = null;
var qzVersion = 0;
var cfg = null;
var action_model = null;
var active_ids = null;
var rpc_call = null;
var all_printers = '';

    async function findVersion() {
        qz.api.getVersion().then(async function(data) {
            qzVersion = data;
        });
    }
    async function startConnection(config) {
        const comp = await rpc_call("/web/dataset/call_kw/res.company/read", {
                model: 'res.company',
                method: 'read',
                args: [[company_id], []],
                kwargs: {}
            })
        qz.security.setCertificatePromise(async function(resolve, reject) {
            if (comp.length){
                resolve(comp[0].qz_certificate);
            }
        });
        if (comp.length && comp[0].private_key != false){
                qz.security.setSignaturePromise(function(toSign) {
                    return function(resolve, reject) {
                        resolve(comp[0].private_key)
                    }
                });
            }

        if (!qz.websocket.isActive()) {
            qz.websocket.connect(config).then(async function() {
                await findVersion();
                await findPrinters();
            });
        } else {
        }
    }
    async function findPrinters() {
        qz.printers.find(printer_name).then(async function(data) {
            await setPrinter(data);
            }).catch(function(err) {console.log(">>>>>", err)});
       }

    async function setPrinter(printer) {
        var cf = getUpdatedConfig();
        cf.setPrinter(printer);
        if (typeof printer === 'object' && printer.name == undefined) {
            var shown;
            if (printer.file != undefined) {
                shown = "<em>FILE:</em> " + printer.file;
            }
            if (printer.host != undefined) {
                shown = "<em>HOST:</em> " + printer.host + ":" + printer.port;
            }
        } else {
            if (printer.name != undefined) {
                printer = printer.name;
            }

            if (printer == undefined) {
                printer = 'NONE';
            }
            if (action_model == 'stock.picking') {
                print_picking_label();
            }
            else if (action_model == 'stock.location'){
                print_location_label();
            }
            else {
                print_product_label();
            }
        }
    }
    /// QZ Config ///
    var cfg = null;

    function getUpdatedConfig() {
        if (cfg == null) {
            cfg = qz.configs.create(null);
        }

        cfg.reconfigure({
            copies: print_copies,
        });
        return cfg
    }
    function print_product_label() {
        rpc_call("/zebra" + controller_url)
            .then(function(res_data) {
                var config = getUpdatedConfig();
                res_data.data.forEach(function(product) {
                    if (printer_type == 'zpl'){
                        var printData =
                            [
                                '^XA',
                                '^CF0,40',
                                '^FO20,25^FD'+product.name+'^FS',
                                '^BY2,20,50',
                                '^FO20,75^BC^FD'+product.barcode+'^FS',
                                '^XZ',
                            ];
                    }
                    else{
                        var printData =
                            [
                                '\nN\n',
                                'q609\n',
                                'Q203,26\n',
                                'D7\n',
                                'A190,10,0,3,1,1,N,"'+product.name+'"\n',
                                'B190,60,0,1,1,2,60,B,"'+product.barcode+'"\n',
                                '\nP1,1\n'
                            ];
                    }
                    qz.print(config, printData).catch(function(e) {});
                });
            }).then(function() {
                location.reload();
            });
    }
    function print_picking_label() {
        rpc_call("/zebra" + controller_url)
            .then(function(res_data) {
                var config = getUpdatedConfig();
                res_data.data.forEach(function(picking) {
                    if (printer_type == 'zpl'){
                        var printData =
                            [
                                '^XA',
                                '^CF0,40',
                                '^BY2,20,50',
                                '^FO20,25^BC^FD'+picking.label+'^FS',
                                '^XZ',
                            ];
                    }
                    else{
                        var printData =
                            [
                                '\nN\n',
                                'q609\n',
                                'Q203,26\n',
                                'B190,10,0,1,1,2,60,B,"'+picking.label+'"\n',
                                '\nP1,1\n'
                            ];
                    }
                    qz.print(config, printData).catch(function(e) {});
                });
            }).then(function() {
                location.reload();
            });
    }
    function print_location_label() {
        rpc_call("/zebra" + controller_url)
            .then(function(res_data) {
                var config = getUpdatedConfig();
                res_data.data.forEach(function(stlocation) {
                    if (printer_type == 'zpl'){
                        var printData =
                            [
                                '^XA',
                                '^CF0,130',
                                '^FO100,120^FD'+stlocation.name+'^FS',
                                '^BY2,20,120',
                                '^FO250,250^BC^FD'+stlocation.barcode+'^FS',
                                '^XZ',
                            ];
                    }
                    else{
                        var printData =
                            [
                               '\nN\n',
                                'q609\n',
                                'Q203,26\n',
                                'D7\n',
                                'A190,10,0,3,1,1,N,"'+stlocation.name+'"\n',
                                'B190,60,0,1,1,2,60,B,"'+stlocation.barcode+'"\n',
                                '\nP1,1\n'
                            ];
                    }
                    console.log(">>>",printData)
                    qz.print(config, printData).catch(function(e) {});
                });
            }).then(function() {
                location.reload();
            });
    }
function getWKHTMLTOPDF_MESSAGES(status) {
    const link = '<br><br><a href="http://wkhtmltopdf.org/" target="_blank">wkhtmltopdf.org</a>'; // FIXME missing markup
    const _status = {
        broken:
            _t(
                "Your installation of Wkhtmltopdf seems to be broken. The report will be shown in html."
            ) + link,
        install:
            _t("Unable to find Wkhtmltopdf on this system. The report will be shown in html.") +
            link,
        upgrade:
            _t(
                "You should upgrade your version of Wkhtmltopdf to at least 0.12.0 in order to get a correct display of headers and footers as well as support for table-breaking between pages."
            ) + link,
        workers: _t(
            "You need to start Odoo with at least two workers to print a pdf version of the reports."
        ),
    };
    return _status[status];
}
ogutils.downloadReport =  async function(rpc, action, type, userContext) {
    let message;
    rpc_call = rpc;
    const comp = await rpc_call("/web/dataset/call_kw/res.company/read", {
        model: 'res.company',
        method: 'read',
        args: [[company_id], []],
        kwargs: {}
    })
    if (comp.length){
        const printers = await rpc_call("/web/dataset/call_kw/label.printer/read", {
                model: 'label.printer',
                method: 'read',
                args: [comp[0].printer_ids, []],
                kwargs: {}
            });
        if (printers.length){
            all_printers = '<select name="select_printer" id="select_printer">'
            printers.forEach(function(pr) {
                all_printers += `<option value="${pr.name}">${pr.name}</option>`
            })
            all_printers += '</select>'
        }
    }
    if (type === "pdf") {
        // Cache the wkhtml status on the function. In prod this means is only
        // checked once, but we can reset it between tests to test multiple statuses.
        var txt_t;
        var person = null;
        var is_zebra_print = false
        $("#myModalpopup").remove();
        var model_popup = 
            '<div class="modal fade" id="myModalpopup" role="dialog" style="display: none;" aria-hidden="true">'+
            '<div class="modal-dialog modal-sm">'+
                '<div class="modal-content">'+
                    '<div class="modal-header">'+
                      '<h4 class="modal-title">No Of Copies</h4>'+
                      '<button type="button" class="close" data-bs-dismiss="modal">&times;</button>'+
                    '</div>'+
                    '<div class="modal-body">'+
                        all_printers+
                      '<input type="number" name="copies_count" value="1">'+
                    '</div>'+
                    '<div class="modal-footer">'+
                      '<button type="button" class="btn btn-default" data-bs-dismiss="modal">Close</button>'+
                      '<button type="button" class="btn btn-default pull-right copies_text_in" data-bs-dismiss="modal">OK</button>'+
                    '</div>'+
                  '</div>'+
                '</div>'+
              '</div>'+
            '</div>'
            $('body').append(model_popup);
        if (action.report_name !== undefined){
            if (action.report_name === 'label_zebra_printer.report_zebra_shipmentlabel' || action.report_name === 'stock.report_location_barcode') {
                is_zebra_print = true;
                action_model = action.context.active_model
                action.context.active_ids = action.context.active_ids
                controller_url = getReportUrl(action, type);
            } 
        }
        if (is_zebra_print == true) {
            $("#myModalpopup").modal('show');
            $('#myModalpopup').on('click', '.copies_text_in', async function() {
                    var input_val = $("input[name='copies_count']").val()
                    printer_name = $("#select_printer :selected").text();
                    person = input_val;
                    if (person == null || person == "") {
                        txt_t = "Cancelled copies";
                        return false;
                    }
                    else {
                            if(parseInt(person)){
                                print_copies = person;
                                return await startConnection();
                            }
                            else{
                                return false;
                            }
                        }
                });
            return { success: true};
        }
        else{
            ogutils.downloadReport.wkhtmltopdfStatusProm ||= rpc("/report/check_wkhtmltopdf");
            const status = await ogutils.downloadReport.wkhtmltopdfStatusProm;
            message = getWKHTMLTOPDF_MESSAGES(status);
            if (!["upgrade", "ok"].includes(status)) {
                return { success: false, message };
            }
            const url = getReportUrl(action, type);
            await download({
                url: "/report/download",
                data: {
                    data: JSON.stringify([url, action.report_type]),
                    context: JSON.stringify(userContext),
                },
            });
            return { success: true, message };
        }
    }
    else{
        if (action.context.active_model === 'product.template'|| action.context.active_model === 'product.product')
            {
                controller_url = `/report/pdf/${action.report_name}/${action.context.active_ids}/`;
                action_model = action.context.active_model;
                var txt_t;
                var person = null;
                var is_zebra_print = false
                $("#myModalpopup").remove();
                var model_popup = 
                    '<div class="modal fade" id="myModalpopup" role="dialog" style="display: none;" aria-hidden="true">'+
                    '<div class="modal-dialog modal-sm">'+
                        '<div class="modal-content">'+
                            '<div class="modal-header">'+
                              '<h4 class="modal-title">No Of Copies</h4>'+
                              '<button type="button" class="close" data-bs-dismiss="modal">&times;</button>'+
                            '</div>'+
                            '<div class="modal-body">'+
                            all_printers+
                              '<input type="number" name="copies_count" value="1">'+
                            '</div>'+
                            '<div class="modal-footer">'+
                              '<button type="button" class="btn btn-default" data-bs-dismiss="modal">Close</button>'+
                              '<button type="button" class="btn btn-default pull-right copies_text_in" data-bs-dismiss="modal">OK</button>'+
                            '</div>'+
                          '</div>'+
                        '</div>'+
                      '</div>'+
                    '</div>'
                    $('body').append(model_popup);

                $("#myModalpopup").modal('show');
                $('#myModalpopup').on('click', '.copies_text_in', async function() {
                        var input_val = $("input[name='copies_count']").val()
                        printer_name = $("#select_printer :selected").text();
                        person = input_val;
                        if (person == null || person == "") {
                            txt_t = "Cancelled copies";
                            return false;
                        }
                        else {
                                if(parseInt(person)){
                                    print_copies = person;
                                    return await startConnection();
                                }
                                else{
                                    return false;
                                }
                            }
                    });
                return { success: true};
            }
            else{
                const url = getReportUrl(action, type);
                await download({
                    url: "/report/download",
                    data: {
                        data: JSON.stringify([url, action.report_type]),
                        context: JSON.stringify(userContext),
                    },
                });
                return { success: true, message };
            }
    }
};
export * from "@web/webclient/actions/reports/utils";