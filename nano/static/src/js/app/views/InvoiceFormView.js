var InvoiceFormView = Backbone.View.extend({
  
  format: "DD/MM/YYYY",

  events: {
    "change #invoice_payment_term_id": "onPaymentTermsChange"
  },
  
  initialize: function() { 
    this.dueDate = this.$el.find("#invoice_due_date");
    this.dateIssued = this.$el.find("#invoice_date_issued");

    this.parentLi = this.dueDate.parent("li:first");

    var k4 = new Kalendae.Input("invoice_due_date", {
			months: 2,
      format: this.format
		});

    var k5 = new Kalendae.Input("invoice_date_issued", {
			months: 2,
      format: this.format
		});


  },

  onPaymentTermsChange: function(evt) {
    var select = $(evt.currentTarget);
    var days = parseInt(select.val());

    if (days != -1) {
      var dateIssued = this.dateIssued.val();
      var k = Kalendae.moment(dateIssued, this.format).add('days', days);
      this.dueDate.val(k.format(this.format));
    }
  },
  
});
