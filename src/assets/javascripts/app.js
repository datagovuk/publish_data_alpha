!(function () {
  'use strict';

  // Utilities

  // hide something, show something
  var hs = function(stuffToHideSelector, stuffToShowSelector) {
    if (stuffToHideSelector) $(stuffToHideSelector).attr('aria-hidden', 'true').hide();
    if (stuffToShowSelector) $(stuffToShowSelector).attr('aria-hidden', 'false').show();
  };


  // Components

  var tableShowHide = {
    selector: '.table-show-hide ',

    init: function(params) {
      var that = this;
      $.each($(this.selector), function(index, showHide) {
        var rows = $(showHide).find('table tr');
        rows.each(function() {
          if ($(this).index() >= params.rowLimit) {
            $(this).hide();
          }
        });
        if (rows.length > params.rowLimit) {
          $(showHide).find('a.toggle')
            .on('click', params, that.callback)
            .show();
        }
      });
    },

    callback: function(event) {
      var a = $(this);
      var rows = $(this).parents('section').first().find('tr');
      a.toggleClass('expanded');
      if (a.hasClass('expanded')) {
        a.text('Close');
        rows.show();
      } else {
        a.text('Show all');
        rows.each(function(i) {
          if ($(this).index() >= event.data.rowLimit) $(this).hide();
        });
      }
    }
  };

  var typeAhead = {
    options: {
      hint: true,
      highlight: true,
      minLength: 3,
      classNames: {
        input: 'form-control tt-input',
        hint: 'form-control tt-hint'
      }
    },

    sourceOptions: {
      name: 'states',
      source: new Bloodhound({
        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),
        queryTokenizer: Bloodhound.tokenizers.whitespace,
        remote: {
          url: '/api/locations?q=%QUERY',
          wildcard: '%QUERY'
        }
      })
    },

    // what to do when the first 'Add another area' button is clicked
    add1: function() { hs('#add1', '#location2, #add2, #del1, #del2') },

    // what to do when the second 'Add another area' button is clicked
    add2: function() { hs('#add2', '#location3, #add2, #del2, #del3') },

    // what to do when the first 'Remove' button is clicked
    del1: function() {
      // we've remove the first location, copy the 2 others down
      $('#id_location1').val($('#id_location2').val());
      $('#id_location2').val($('#id_location3').val());

      // second location field disappears if not third present
      if (!$('#location3').is(':visible')) {
        hs('#location2, #add2', '#add1');
      } else {
        hs('', '#add2');
      }
      if (!$('#location2').is(':visible')) {
        hs('#del1');
      }
      hs('#location3');
      $('#location3').val('');
    },

    // second Remove button is clicked
    del2: function() {
      $('#id_location2').val($('#id_location3').val());
      $('#id_location3').val('');
      if (!$('#location3').is(':visible')) {
        hs('#location2, #add2, #del1, #del2', '#add1');
      } else {
        hs('', '#add2');
      }
      hs('#location3');
    },

    del3: function() {
      $('#id_location3').val('');
      hs('#location3', '#add2');
    },

    init: function(params) {
      if ($('#id_location2').val()) {
        hs('#add1', '#location2, #add2, #del2');
      } else {
        hs('', '#add1');
      }

      if ($('#id_location3').val()) {
        hs('#add2', '#location3, #del3');
      }

      $('#add1').on('click', this.add1);
      $('#add2').on('click', this.add2);
      $('#del1').on('click', this.del1);
      $('#del2').on('click', this.del2);
      $('#del3').on('click', this.del3);

      $(params.selector).typeahead(this.options, this.sourceOptions);
    },
  };

  var dashboardStats = {

    fetchStats: function() {
      $.get(this.endpoint + 'stats/?orgs=' + this.orgs.join())
        .done($.proxy(this.makeStatsMarkup, this))
        .fail(function(xhr, text, error) {
          console.log('fail: ', text, error);
        })
    },

    statText: function(stat) {
      switch(stat.statistic) {
        // TODO: make it easier to translate the text
        case 'view': return 'Views: ' + stat.total;
        case 'download': return 'Downloads: ' + stat.total;
        case 'search': return 'Searched: ' + stat.total;
        default: return '';
      }
    },

    makeStatsMarkup: function(data) {
      var $tbody = this.$statsSection.find('table tbody');
      var $rowTemplate = $('#row-template');
      $.each(data, function(index, datum) {
        var $newRow = $rowTemplate.clone().removeAttr('id style');
        var statText = dashboardStats.statText(datum);
        if (datum.dataset_title && statText) {
          $newRow
            .find('.stats-title')
            .text(datum.dataset_title);
          $newRow
            .find('.stats-downloads')
            .text(statText);
          $tbody.append($newRow);
        }
      });
      this.$statsSection.removeClass('js-hidden');
    },

    init: function(selector) {
      this.$statsSection = $(selector);
      if (this.$statsSection) {
        this.endpoint = $('#api-endpoint').text();
        this.orgs = JSON.parse($('#orgs').text());
        if (this.endpoint.length && this.orgs.length) {
          this.fetchStats();
        }
      }
    }
  };



  $(document).ready(function() {
    tableShowHide.init({ rowLimit: 3});
    typeAhead.init({ selector: '.location-input' });
    dashboardStats.init('#dashboard-stats');
  });

})();
