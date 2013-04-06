/*! All system models
*/

var InvoiceItemType = Backbone.Model.extend({});
var TaxRate = Backbone.Model.extend({});
var VatRegistration = Backbone.Model.extend({});

var InvoiceItem = Backbone.RelationalModel.extend({
  getQuantityString: function() {
    var q = this.get("quantity");
    var type = this.get("InvoiceItemType").name;
    
    if (type == "Hours") {
      var mins = q * 60;
      var hours = 0;
      do {
        mins = mins - 60;
        hours++;
      } while (mins >= 60);

      if (mins == 0) {
        return hours;
      } else {
        mins = Math.round(mins);
        mins = sprintf("%1$02d", mins);
        return hours + ":" + mins;
      }
    }

    return parseFloat(q) % 1 == 0 ? parseInt(q) : q;
  },
  
  shouldRenderField: function(field) {
    var noRenderFields = {
      "Comment": ["quantity", "price","tax","total"],
      "VAT": ["quantity"]
    };
    var type = this.get("InvoiceItemType").name;
    if (!noRenderFields.hasOwnProperty(type)) {
      return true;
    }
    var fields = noRenderFields[type];
    return _.include(fields, field) ? false: true;
  }
});

var Invoice = Backbone.RelationalModel.extend({
  relations: [{
    type: Backbone.HasMany,
    key: 'InvoiceItems',
    relatedModel: 'InvoiceItem',
    collectionType: 'InvoiceItemCollection',
    reverseRelation: {
      key: 'invoice',
      includeInJSON: 'id'
    }
  }]
});


/* Collections */

var InvoiceItemCollection = Backbone.Collection.extend({
  model: InvoiceItem
});

var TaxRateCollection = Backbone.Collection.extend({
  model: TaxRate
});

var InvoiceItemTypeCollection = Backbone.Collection.extend({
  model: InvoiceItemType
});
