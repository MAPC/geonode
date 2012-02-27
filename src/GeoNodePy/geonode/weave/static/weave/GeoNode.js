/*
 * Extending the GeoNode client prototype
 */

// Helper for rendering visualization embed functionality. 
// 'visUrl' should be set on instantiation
Ext.namespace("GeoNode");
GeoNode.VisualizationEmbedCode = Ext.extend(Ext.util.Observable, {
    embedText: "Embed Visualization",
    embedElement: "embed_code",
    constructor: function(config) {
        Ext.apply(this, config);
    },
    renderButton: function() {
		var showEmbedWin = this.showEmbedWin;
		var embedVisualizationButton = new Ext.Button({
			renderTo: this.embedElement,
			text: this.embedText,
			visUrl: this.visUrl,
			handler: function() {
				showEmbedWin(this.visUrl);
			}
		});
	},
	renderLink: function() {	
		var el = Ext.get(this.embedElement);
		el.update(this.embedText);
		var visUrl = this.visUrl
		var showEmbedWin = this.showEmbedWin;
		el.on('click', function() {
			showEmbedWin(visUrl);
		});
	},
	showEmbedWin: function(visUrl) {
		var embedCode = "<iframe width='500' height='350' frameborder='0' scrolling='no' marginheight='0' marginwidth='0' src='" + visUrl + "embed'></iframe><br /><small><a href='" + visUrl + "'>View Larger Visualization</a></small>";
		var embedCodeWin = new Ext.Window({
			title: "Copy the code below to embed your Visualization",
			width: 340,
			height: 160,
			x: Ext.get(document.body).getWidth()/2 - 170,
			y: 140,
			layout: "fit",
			border: false,
			closable: true,
			items: [{
				xtype: "form",
				id: "embedCodeForm",
				bodyStyle:"padding:10px",
				hideLabels: true,
				items: [{
					xtype: "textarea",
					id: "embedcode",
					height: 110,
					width: 306,
					value: embedCode
				}]
			}]
		}).show();
	}
});

// based on GeoNode.MapSearchTable, 'doLayout' method has been modified
Ext.namespace("GeoNode");
GeoNode.VisualizationSearchTable = Ext.extend(Ext.util.Observable, {
    autoExpandColumn: 'title',
    titleHeaderText: 'Title',
    contactHeaderText: "Contact",
    lastModifiedHeaderText: "Last Modified",
    mapAbstractLabelText: "Abstract",
    mapLinkLabelText: "View or edit this Visualization",
    previousText: 'Prev',
    nextText: 'Next',
    ofText: 'of',
    noResultsText: 'Your search did not match any items.',
    searchLabelText: 'Search Maps',
    searchButtonText: 'Search',
    showingText: 'Showing',
    loadingText: 'Loading',
    permalinkText: 'permalink',
    constructor: function(config) {
        this.addEvents('load');
        Ext.apply(this, config);
        this.initFromQuery();
        this.loadData();
    },
    loadData: function() {
        this.searchStore = new Ext.data.JsonStore({
            url: this.searchURL,
            root: 'rows',
            idProperty: 'name',
            remoteSort: true,
            totalProperty: 'total',
            fields: [{
                name: 'id',
                mapping: 'id'
            },
            {
                name: 'title',
                type: 'string'
            },
            {
                name: 'abstract',
                type: 'string'
            },
            {
                name: 'detail',
                type: 'string'
            },
            {
                name: 'owner',
                type: 'string'
            },
            {
                name: 'owner_detail',
                type: 'string'
            },
            {
                name: 'last_modified',
                type: 'string'
            }]
        });
        this.searchStore.on('load',
        function() {
            this.updateControls();
            this.fireEvent('load', this);
        },
        this);
        this.doLayout();
        this.doSearch();
    },
    initFromQuery: function() {
        if (!this.searchParams) {
            this.searchParams = {};
        }
        if (!this.searchParams.start) {
            this.searchParams.start = 0;
        }
        if (!this.searchParams.limit) {
            this.searchParams.limit = 25;
        }
        if (this.constraints) {
            for (var i = 0; i < this.constraints.length; i++) {
                this.constraints[i].initFromQuery(this, this.searchParams);
            }
        }
    },
    doSearch: function() {
        this.searchParams.start = 0;
        if (this.constraints) {
            for (var i = 0; i < this.constraints.length; i++) {
                this.constraints[i].applyConstraint(this.searchParams);
            }
        }
        this._search(this.searchParams);
    },
    _search: function(params) {
        this.disableControls();
        this.searchStore.load({
            params: params
        });
        this.updatePermalink(params);
    },
    loadNextBatch: function() {
        this.searchParams.start += this.searchParams.limit;
        this._search(this.searchParams);
    },
    loadPrevBatch: function() {
        this.searchParams.start -= this.searchParams.limit;
        if (this.searchParams.start < 0) {
            this.searchParams.start = 0;
        }
        this._search(this.searchParams);
    },
    disableControls: function() {
        this.nextButton.setDisabled(true);
        this.prevButton.setDisabled(true);
        this.pagerLabel.setText(this.loadingText);
    },
    updateControls: function() {
        var total = this.searchStore.getTotalCount();
        if (this.searchParams.start > 0) {
            this.prevButton.setDisabled(false);
        }
        else {
            this.prevButton.setDisabled(true);
        }
        if (this.searchParams.start + this.searchParams.limit < total) {
            this.nextButton.setDisabled(false);
        }
        else {
            this.nextButton.setDisabled(true);
        }
        var minItem = this.searchParams.start + 1;
        var maxItem = minItem + this.searchParams.limit - 1;
        if (maxItem > total) {
            maxItem = total;
        }
        this.pagerLabel.setText(this.showingText + ' ' + minItem + '-' + maxItem + ' ' + this.ofText + ' ' +
        total);
    },
    updatePermalink: function() {
        if (this.permalink) {
            this.permalink.href = Ext.urlAppend(this.permalinkURL, Ext.urlEncode(this.searchParams));
        }
    },
    updateQuery: function() {
        this.searchParams.q = this.queryInput.getValue();
        this.doSearch();
    },
    hookupSearchButtons: function(el) {
        var root = Ext.get(el);
        var buttons = root.query('.search-button');
        for (var i = 0; i < buttons.length; i++) {
            var text = buttons[i].innerHTML || this.searchButtonText;
            Ext.get(buttons[i]).update('');
            var searchButton = new Ext.Button({
                text: text,
                renderTo: buttons[i]
            });
            searchButton.on('click', this.doSearch, this);
        }
    },
    doLayout: function() {
        var widgetHTML = '<div class="search-results">' + '<div class="search-input"></div>' + '<div class="search-table"></div>' + '<div class="search-controls"></div>' + '</div>';
        var el = Ext.get(this.renderTo);
        el.update(widgetHTML);
        var input_el = el.query('.search-input')[0];
        var table_el = el.query('.search-table')[0];
        var controls_el = el.query('.search-controls')[0];
        var tpl = new Ext.Template('<p><b>' + this.mapAbstractLabelText + ':</b> {abstract}</p>' + '<p><a href="/visualizations/{id}">' + this.mapLinkLabelText + '</a></p>');
        var expander = new Ext.grid.RowExpander({
            tpl: tpl
        });
        expander.on("expand",
        function(expander, record, body, idx) {
            Ext.select("a", Ext.get(body)).on("click",
            function(evt) {
                evt.stopPropagation();
            });
        });
        tableCfg = {
            store: this.searchStore,
            plugins: [expander],
            autoExpandColumn: 'title',
            viewConfig: {
                autoFill: true,
                forceFit: true,
                emptyText: this.noResultsText,
                listeners: {
                    refresh: function(view) {
                        Ext.select("a", Ext.get(view.mainBody)).on("click",
                        function(evt) {
                            evt.stopPropagation();
                        });
                    },
                    rowsinserted: function(view, start, end) {
                        for (var i = start; i < end; i++) {
                            Ext.select("a", Ext.get(view.getRow(i))).on("click",
                            function(evt) {
                                evt.stopPropagation();
                            });
                        }
                    },
                    rowupdated: function(view, idx, record) {
                        Ext.select("a", Ext.get(view.getRow(idx))).on("click",
                        function(evt) {
                            evt.stopPropagation();
                        });
                    }
                }
            },
            autoHeight: true,
            renderTo: table_el
        };
        tableCfg.listeners = {
            "rowdblclick": function(grid, rowIndex, evt) {
                var rec = grid.store.getAt(rowIndex);
                if (rec != null) {
                    location.href = rec.get('detail');
                }
            },
            "rowclick": function(grid, rowIndex, evt) {
                expander.toggleRow(rowIndex);
            },
            "beforerender": function(grid) {
                grid.on('render',
                function() {
                    grid.getView().mainBody.un('mousedown', expander.onMouseDown, expander);
                })
            }
        };
        var columns = [expander, {
            header: this.titleHeaderText,
            dataIndex: 'title',
            id: 'title',
            renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                var detail = record.get('detail');
                if (detail) {
                    return '<a href="' + detail + '">' + value + '</a>';
                }
                else {
                    return value;
                }
            }
        },
        {
            header: this.contactHeaderText,
            dataIndex: 'owner',
            id: 'owner',
            renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                var detail = record.get('owner_detail');
                if (detail) {
                    return '<a href="' + detail + '">' + value + '</a>';
                }
                else {
                    return value;
                }
            }
        },
        {
            header: this.lastModifiedHeaderText,
            dataIndex: 'last_modified',
            id: 'last_modified',
            renderer: function(value, metaData, record, rowIndex, colIndex, store) {
                dt = Date.parseDate(value, 'c');
                return dt.format("F j, Y");
            }
        }];
        var colModel = new Ext.grid.ColumnModel({
            defaults: {
                menuDisabled: true,
                sortable: true
            },
            columns: columns
        });
        tableCfg.colModel = colModel;
        this.table = new Ext.grid.GridPanel(tableCfg);
        this.queryInput = new Ext.form.TextField({
            fieldLabel: this.searchLabelText,
            name: 'search',
            allowBlank: true,
            width: 350
        });
        this.queryInput.on('specialkey',
        function(field, e) {
            if (e.getKey() == e.ENTER) {
                this.updateQuery();
            }
        },
        this);
        var searchButton = new Ext.Button({
            text: this.searchButtonText
        });
        searchButton.on('click', this.updateQuery, this)
        var searchForm = new Ext.Panel({
            frame: false,
            border: false,
            layout: new Ext.layout.HBoxLayout({
                defaultMargins: {
                    top: 10,
                    bottom: 10,
                    left: 0,
                    right: 10
                }
            }),
            items: [this.queryInput, searchButton]
        });
        searchForm.render(input_el);
        this.prevButton = new Ext.Button({
            text: this.previousText
        });
        this.prevButton.on('click', this.loadPrevBatch, this);
        this.nextButton = new Ext.Button({
            text: this.nextText
        });
        this.nextButton.on('click', this.loadNextBatch, this);
        this.pagerLabel = new Ext.form.Label({
            text: ""
        });
        var controls = new Ext.Panel({
            frame: false,
            border: false,
            layout: new Ext.layout.HBoxLayout({
                defaultMargins: {
                    top: 10,
                    bottom: 10,
                    left: 0,
                    right: 10
                }
            }),
            items: [this.prevButton, this.nextButton, this.pagerLabel]
        });
        controls.render(controls_el);
        this.permalink = Ext.query('a.permalink')[0];
        this.disableControls();
        if (this.searchParams.q) {
            this.queryInput.setValue(this.searchParams.q);
        }
        this.updatePermalink();
    }
});