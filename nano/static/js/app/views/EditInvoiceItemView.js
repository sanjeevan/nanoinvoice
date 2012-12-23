var EditInvoiceItemView = Backbone.View.extend({
  events: {
    "click button#save": "onSave",
    "click a.cancel": "onCancel",
    "change select#invoice_item_type": "onTypeChange"
  },

  initialize: function() { 
    this.template = AppTemplates["edit_invoice_item.html"];
    this.parentView = this.options.parentView;
  },

  onSave: function(evt) {
    var view = this;
    evt.preventDefault();
    $.ajax(this.$el.find("form").attr("action"), {
      data: this.$el.find("form").serialize(),
      type: "POST",
      success: function(resp) {
        view.parentView.model.set(resp.Invoice);
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
    this.setElement( _.template( this.template, { InvoiceItem: this.model } ));
    $.facebox(this.$el);
    // Call this after popup has been rendered to page, otherwise it doesn't
    // work the first time the popup appears, but works on subsequent opens.
    this.onTypeChange();
    
    return this;
  }
});
