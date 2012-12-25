/*! DraftInvoiceView */

var DraftInvoiceView = Backbone.View.extend({
  el: "#manage",

  events: {
    "click .delete": "onDeleteClick",
    "click #add_invoice_item": "onAddInvoiceItem",
    "click .edit": "onEditItemClick"
  },

  initialize: function() { 
    this.addItemView = new NewInvoiceItemView({ model: this.model, parentView: this });
    
    this.model.on("change", this.render, this);
    this.model.on("change", this.updateTotals, this);

    //this.model.on("update:InvoiceItems", this.render);
    //this.model.on("update:InvoiceItems", this.render);
  },

  onEditItemClick: function(evt) {
    evt.preventDefault();
    var id = $(evt.currentTarget).data("id");
    console.log(id);
    
    var view = new EditInvoiceItemView({ 
      parentView: this,
      model: this.model.get("InvoiceItems").get(id) 
    });

    view.render();
  },

  onAddInvoiceItem: function(evt) {
    evt.preventDefault();
    this.addItemView.render(); 
  },

  onDeleteClick: function(evt) {
    var el = $(evt.currentTarget);
    var id = el.data("id");
    var view = this;

    evt.preventDefault();

    $.ajax({
      url: el.attr("href"),
      type: "DELETE",
      data: { "id": id },
      success: function(json) {
        view.model.set(json.Invoice);
      }
    });
  },
  
  updateTotals: function() {
    var subTotal = numberFormat(this.model.get("sub_total"), 2);
    var salesTax = numberFormat(this.model.get("tax"), 2);
    var total = numberFormat(this.model.get("total"), 2); 

    this.$el.find("#net_total_amount").html(subTotal)
    this.$el.find("#sales_tax_amount").html(salesTax);
    this.$el.find("#total_amount").html(total);
  },

  render: function() {
    var view = this;
    var itemsHtml = "";
    console.log('rendering');
    
    this.model.get("InvoiceItems").each(function(item) {
      itemsHtml += JST["invoice_item"]({ InvoiceItem: item, Invoice: view.model }); 
    });
    
    this.$el.find("#invoice_items").html(itemsHtml);
  }
});
