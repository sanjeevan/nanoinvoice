window.JST = window.JST || {};
window.JST['invoice_item'] = _.template('<tr class="item " id="invoice-item-<%= InvoiceItem.get("id") %>">\n  <td class="item_l quantity_td">\n    <% if (InvoiceItem.shouldRenderField("quantity")) { %>\n      <%= InvoiceItem.getQuantityString() %> \n    <% } %>\n    <%= InvoiceItem.get("InvoiceItemType").name  %>\n  </td>\n\n  <td class="item_l description_td">\n    <%= InvoiceItem.get("description") %>\n  </td>\n\n  <td class="item_r price_td"> \n    <% if (InvoiceItem.shouldRenderField("price")) { %>\n      <%= numberFormat(InvoiceItem.get("price"), 2) %>\n    <% } %>\n  </td>\n  \n  <% if (User.vatRegistration.get("status") == "registered") { %>\n  <td class="item_r taxrate_td">\n    <% if (InvoiceItem.shouldRenderField("tax")) { %>\n      <%= numberFormat(InvoiceItem.get("TaxRate").rate, 0) %>%\n    <% } %>\n  </td>\n  <% } %>\n\n  <td class="item_r subtotal_td">\n    <% if (Invoice.get("status") == "draft") { %>\n    <div class="item-controls">\n      <a data-id="<%= InvoiceItem.get("id") %>" href="#" class="btn-small edit" title="Edit invoice item">Edit</a>\n      <a data-id="<%= InvoiceItem.get("id") %>" href="/invoice_item/delete" class="delete">\n        <img src="/images/delete.png" />\n      </a>\n    </div>\n    <% } %>\n    <% if (InvoiceItem.shouldRenderField("total")) { %>\n      <%= numberFormat(InvoiceItem.get("total"), 2) %>\n    <% } %>\n  </td>\n</tr>\n\n');
window.JST['edit_invoice_item'] = _.template('<div id="edit-invoice-item">\n  <div class="header"><h2>Edit</h2></div>\n  <div class="content">\n    <form accept-charset="utf-8" method="post" action="/invoice_item/update/<%= InvoiceItem.get(\'id\') %>" class="inline big">\n      <div class="fields">\n        <div class="field">\n          <label>Qty</label>\n          \n          <input size="2" id="quantity" type="text" name="quantity" value="<%= InvoiceItem.getQuantityString() %>">\n\n          <select id="invoice_item_type" name="type_id">\n            <% App.invoiceItemTypes.each(function(t) { %>\n              <% if (t.get("id") == InvoiceItem.get("type_id")) { %>\n                <option selected="selected" value="<%= t.get("id") %>"><%= t.get("name") %></option>\n              <% } else { %> \n                <option value="<%= t.get("id") %>"><%= t.get("name") %></option>\n              <% } %>\n            <% }) %>\n          </select>\n          \n          <div id="hours-help" class="help" style="display: none">\n            (e.g. One and a half hours can be entered as either 1:30 or 1.5)\n          </div>\n        </div>\n        \n        <div class="field">\n          <label>Details</label>\n          <textarea id="details" class="wide" name="description"><%= InvoiceItem.get("description") %></textarea>\n        </div>\n\n        <div class="field" id="price-row">\n          <label>Unit Price (£)</label>\n          <input id="price" type="text" name="price" value="<%= InvoiceItem.get("price") %>" />\n        </div>\n        \n        <% if (App.taxRates.length > 0) { %>\n          <div class="field" id="tax-row">\n            <label>Tax</label>\n            <select name="tax_rate_id">\n              <% App.taxRates.each(function(t){ %>\n                <% if (InvoiceItem.get("tax_rate_id") == t.get("id")) { %>\n                <option selected="selected" value="<%= t.get("id") %>"><%= t.get("name") %> (<%= t.get("rate") %>%)</option>\n                <% } else { %>\n                <option value="<%= t.get("id") %>"><%= t.get("name") %> (<%= t.get("rate") %>%)</option>\n                <% } %>\n              <% }) %> \n            </select>\n          </div>\n        <% } else { %>\n          <input type="hidden" name="tax_rate_id" value="-1"/>\n        <% } %>\n\n        <div class="field actions">\n          <button id="save" class="button normal">Update</button> &nbsp; \n          <a href="#" class="cancel">Cancel</a>\n        </div>\n      </div>\n    </form>\n  </div>\n</div>\n');
window.JST['new_invoice_item'] = _.template('<div id="new-invoice-item">\n  <div class="header"><h2>Add Invoice Item</h2></div>\n  <div class="content">\n    <form accept-charset="utf-8" method="post" action="/invoice_item/create" class="inline">\n    <input type="hidden" name="invoice_id" value="<%= Invoice.get("id") %>" />\n    <div class="fields">\n      <div class="field">\n        <label>Qty</label>\n        \n        <input size="2" id="quantity" type="text" name="quantity" value="1">\n\n        <select id="invoice_item_type" name="type_id">\n          <% App.invoiceItemTypes.each(function(t) { %>\n            <% if (t.get("name") == App.defaults.itemType) { %> \n              <option selected="selected" value="<%= t.get("id") %>"><%= t.get("name") %></option>\n            <% } else { %>\n              <option value="<%= t.get("id") %>"><%= t.get("name") %></option>\n            <% } %>\n          <% }) %>\n        </select>\n\n        <div id="hours-help" class="help" style="display: none">\n          (e.g. One and a half hours can be entered as either 1:30 or 1.5)\n        </div>\n      </div>\n      \n      <div class="field">\n        <label>Details</label>\n        <textarea id="details" class="wide" name="description"></textarea>\n      </div>\n\n      <div class="field" id="price-row">\n        <label>Unit Price (£)</label>\n        <input id="price" type="text" name="price" />\n      </div>\n      \n      <% if (App.taxRates.length > 0) { %>\n      <div class="field" id="tax-row">\n        <label>Tax</label>\n        <select name="tax_rate_id">\n          <% App.taxRates.each(function(t){ %>\n            <% if (t.get("id") == App.defaults.taxRateId) { %> \n              <option selected="selected" value="<%= t.get("id") %>"><%= t.get("name") %> (<%= t.get("rate") %>%)</option>\n            <% } else { %>\n              <option value="<%= t.get("id") %>"><%= t.get("name") %> (<%= t.get("rate") %>%)</option>\n            <% } %>\n          <% }) %> \n        </select>\n      </div>\n      <% } else { %>\n        <input type="hidden" name="tax_rate_id" value="-1" />\n      <% } %>\n\n      <div class="field actions">\n        <button id="save" class="button normal">Create</button> \n        <a href="#" class="cancel">Cancel</a>\n      </div>\n    </div>\n  </form>\n  </div>\n</div>\n');
