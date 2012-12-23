var NewInvoiceItemView = Backbone.View.extend({
  events: {
    "click button#save": "onSave",
    "click a.cancel": "onCancel",
    "change select#invoice_item_type": "onTypeChange"
  },

  initialize: function() { 
    this.template = AppTemplates["new_invoice_item.html"];
    this.parentView = this.options.parentView;
  },

  onSave: function(evt) {
    var view = this;
    evt.preventDefault();
    $.ajax(this.$el.find("form").attr("action"), {
      data: this.$el.find("form").serialize(),
      type: "POST",
      success: function(resp) {
        view.parentView.model.get("InvoiceItems").push(resp.InvoiceItem);
        view.parentView.model.set({
          "total": resp.Invoice.total,
          "tax": resp.Invoice.tax,
          "sub_total": resp.Invoice.sub_total
        });
        // If item price is 0, attributes won't be changed, so manually
        // trigger event
        view.parentView.model.trigger("change");
        $.facebox.close();
      }
    });
  },

  // When type is changed
  onTypeChange: function(evt) {
    var name = $("#invoice_item_type option:selected").text();
    
    if (name == "Hours") {
      this.$el.find("#hours-help").show();  
    } else {
      this.$el.find("#hours-help").hide();
    }

    if (name == "Comment") {
      this.$el.find("#tax-row").hide();
      this.$el.find("#price-row").hide();
      this.$el.find("#quantity").attr("disabled", true);
    } else {
      this.$el.find("#tax-row").show();
      this.$el.find("#price-row").show();
      this.$el.find("#quantity").attr("disabled", false);
    }
  },

  onSaveAndContinue: function(evt) {
  },

  onCancel: function(evt) {
    evt.preventDefault();
    $.facebox.close();
  },

  render: function() {
    this.setElement( _.template( this.template, {Invoice: this.model } ));
    $.facebox(this.$el); 

    return this;
  }
});
