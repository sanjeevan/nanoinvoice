window.JST = window.JST || {};
window.JST['invoice_item'] = _.template('<tr class="item " id="invoice-item-<%= InvoiceItem.get(\'id\') %>">\n  <td class="item_l quantity_td">\n    <% if (InvoiceItem.shouldRenderField("quantity")) { %>\n      <%= InvoiceItem.getQuantityString() %> \n    <% } %>\n    <%= InvoiceItem.get("InvoiceItemType").name  %>\n  </td>\n  <td class="item_l description_td">\n    <%= InvoiceItem.get("description") %>\n  </td>\n\n  <td class="item_r price_td"> \n    <% if (InvoiceItem.shouldRenderField("price")) { %>\n      <%= numberFormat(InvoiceItem.get("price"), 2) %>\n    <% } %>\n  </td>\n  \n  <td class="item_r taxrate_td">\n    <% if (InvoiceItem.shouldRenderField(\'tax\')) { %>\n      <%= numberFormat(InvoiceItem.get(\'tax\'), 2) %>\n    <% } %>\n  </td>\n\n  <td class="item_r subtotal_td">\n    <% if (Invoice.get("status") == "draft") { %>\n    <div class="item-controls">\n      <a data-id="<%= InvoiceItem.get("id") %>" href="#" class="btn btn-default btn-xs edit" title="Edit invoice item">Edit</a>\n      <a data-id="<%= InvoiceItem.get("id") %>" href="/invoice_item/delete/<%= InvoiceItem.get(\'id\') %>" class="delete">\n        <img src="/static/img/delete.png" />\n      </a>\n    </div>\n    <% } %>\n    <% if (InvoiceItem.shouldRenderField("total")) { %>\n      <%= numberFormat(InvoiceItem.get("total"), 2) %>\n    <% } %>\n  </td>\n</tr>\n\n');
window.JST['invoice_footer'] = _.template('\n<% if (Invoice.get("tax") > 0) { %>\n  <tr id="net_total_tr">\n    <td colspan="2">&nbsp;</td>\n    <td colspan="2" class="item_r">Net Total</td>\n    <td class="item_r" id="net_total_amount">{{ invoice.sub_total|format_currency }}</td>\n  </tr>\n\n  <tr id="vat_tr">\n    <td colspan="2">&nbsp;</td>\n    <td colspan="2" class="item_r">TAX</td>\n    <td class="item_r" id="sales_tax_amount">{{ invoice.tax|format_currency }}</td>\n  </tr>\n<% } %>\n\n<tr id="total_tr">\n  <td colspan="2" class="inv_btn">\n    <% if (Invoice.get("status") == "draft") { %>\n        <a href="#" class="btn btn-primary btn-sm" id="add_invoice_item" title="Add Invoice Item">\n      <span>Add Invoice Item</span>\n    </a> &nbsp; \n    <a href="#" class="btn btn-default btn-sm" id="reorder_invoice_items">\n      <span>Reorder</span>\n    </a>\n    <% } %>\n  </td>\n\n  <% var col_span = 1 %>\n  <% if (Invoice.get("tax") > 0) { %>\n    <% col_span = 2 %>\n  <% } %>\n  <td colspan="<%= col_span %>" class="total" id="total_currency"><span class="currency"><%= Invoice.get("currency_code") %> </span>Total</td>\n  <td class="total" id="total_amount"><%= numberFormat(Invoice.get("total"), 2) %></td>\n</tr>\n');
window.JST['edit_invoice_item'] = _.template('<div id="edit-invoice-item" title="Edit line item">\n  <div class="content">\n    <form accept-charset="utf-8" method="post" action="/invoice_item/update/<%= InvoiceItem.get(\'id\') %>" class="inline big">\n      <div class="fields">\n        <div class="field">\n          <label>Qty</label>\n\n          <input size="2" id="quantity" type="text" name="quantity" value="<%= InvoiceItem.getQuantityString() %>">\n\n          <select id="invoice_item_type" name="type_id">\n            <% App.invoiceItemTypes.each(function(t) { %>\n              <% if (t.get("id") == InvoiceItem.get("type_id")) { %>\n                <option selected="selected" value="<%= t.get("id") %>"><%= t.get("name") %></option>\n              <% } else { %>\n                <option value="<%= t.get("id") %>"><%= t.get("name") %></option>\n              <% } %>\n            <% }) %>\n          </select>\n\n          <div id="hours-help" class="help" style="display: none">\n            (e.g. One and a half hours can be entered as either 1:30 or 1.5)\n          </div>\n        </div>\n\n        <div class="field">\n          <label>Details</label>\n          <textarea id="details" class="wide" name="description"><%= InvoiceItem.get("description") %></textarea>\n        </div>\n\n        <div class="field" id="price-row">\n          <label>Unit Price (£)</label>\n          <input id="price" type="text" name="price" value="<%= InvoiceItem.get("price") %>" />\n        </div>\n\n        <% if (App.taxRates.length > 0) { %>\n          <div class="field" id="tax-row">\n            <label>Tax</label>\n            <select name="tax_rate_id">\n              <% App.taxRates.each(function(t){ %>\n                <% if (InvoiceItem.get("tax_rate_id") == t.get("id")) { %>\n                <option selected="selected" value="<%= t.get("id") %>"><%= t.get("name") %> (<%= t.get("rate") %>%)</option>\n                <% } else { %>\n                <option value="<%= t.get("id") %>"><%= t.get("name") %> (<%= t.get("rate") %>%)</option>\n                <% } %>\n              <% }) %>\n            </select>\n          </div>\n        <% } else { %>\n          <input type="hidden" name="tax_rate_id" value="-1"/>\n        <% } %>\n      </div>\n    </form>\n  </div>\n</div>\n');
window.JST['new_invoice_item'] = _.template('<div id="new-invoice-item">\n  <div class="header"><h2>Add Invoice Item</h2></div>\n  <div class="content">\n    <form accept-charset="utf-8" method="post" action="/invoice_item/create" class="inline">\n    <input type="hidden" name="invoice_id" value="<%= Invoice.get("id") %>" />\n    <div class="fields">\n      <div class="field">\n        <label>Qty</label>\n\n        <input size="2" id="quantity" type="text" name="quantity" value="1">\n\n        <select id="invoice_item_type" name="type_id">\n          <% App.invoiceItemTypes.each(function(t) { %>\n            <% if (t.get("name") == App.defaults.itemType) { %>\n              <option selected="selected" value="<%= t.get("id") %>"><%= t.get("name") %></option>\n            <% } else { %>\n              <option value="<%= t.get("id") %>"><%= t.get("name") %></option>\n            <% } %>\n          <% }) %>\n        </select>\n\n        <div id="hours-help" class="help" style="display: none">\n          (e.g. One and a half hours can be entered as either 1:30 or 1.5)\n        </div>\n      </div>\n\n      <div class="field">\n        <label>Details</label>\n        <textarea id="details" class="wide" name="description"></textarea>\n      </div>\n\n      <div class="field" id="price-row">\n        <label>Unit Price (£)</label>\n        <input id="price" type="text" name="price" value="0.0" />\n      </div>\n\n      <% if (App.taxRates.length > 0) { %>\n      <div class="field" id="tax-row">\n        <label>Tax</label>\n        <select name="tax_rate_id">\n          <% App.taxRates.each(function(t){ %>\n            <% if (t.get("id") == App.defaults.taxRateId) { %>\n              <option selected="selected" value="<%= t.get("id") %>"><%= t.get("name") %> (<%= t.get("rate") %>%)</option>\n            <% } else { %>\n              <option value="<%= t.get("id") %>"><%= t.get("name") %> (<%= t.get("rate") %>%)</option>\n            <% } %>\n          <% }) %>\n        </select>\n      </div>\n      <% } else { %>\n        <input type="hidden" name="tax_rate_id" value="-1" />\n      <% } %>\n    </div>\n  </form>\n  </div>\n</div>\n');
