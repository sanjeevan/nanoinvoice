var NewInvoiceItemView = Backbone.View.extend({
  events: {
    "change select#invoice_item_type": "onTypeChange"
  },

  initialize: function() {
    this.template = JST["new_invoice_item"];
    this.parentView = this.options.parentView;
  },

  onSave: function() {
    var view = this;
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
        if (resp.InvoiceItem.total == 0) {
          view.parentView.model.trigger("change");
        }
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

  render: function() {
    var view = this;
    this.setElement( this.template({Invoice: this.model } ));
    this.$el.dialog({
      modal: true,
      width: 500,
      buttons: {
        "Save": function() {
          view.onSave();
          $(this).dialog('close');
        },
        "Cancel": function() {
          $(this).dialog('close');
        }
      }
    });

    return this;
  }
});
