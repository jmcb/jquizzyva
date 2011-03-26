var _tabify_orig = $.ui.tabs.prototype._tabify;
$.extend($.ui.tabs.prototype, {
  _tabify: function(init) {
    _tabify_orig.apply(this, arguments);

    var self = this, o = this.options;
    if (o.closable) {
      this.$lis = $('li:has(a[href])', this.element);
      function closeTab(el) { self.remove(self.$lis.index(el.parentNode)); };
      this.$lis.not(".no_close").each(function(){
        $(o.closeTemplate.replace(/#\{text\}/g, o.closeText)).appendTo(this)
        .addClass(o.closeAnchorClass)
        .click(function() {closeTab(this);})
      });
    }
  }
});
