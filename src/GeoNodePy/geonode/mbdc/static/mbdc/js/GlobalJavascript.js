//==========================================================================================
// Verndale.com - GlobalJavascript.js
//==========================================================================================
/* In this file:
	[jQuery Extensions] - all custom jQuery.extend functions
	[Global Variables] - any variables needed globally
	[JavaScript and jQuery Plugins] - all plugins written in javascript or jQuery
	[Javascript Functions] - all none jQuery functions
	[jQuery functions on load] - all modules / controls of the site
*/


//==========================================================================================
// BEGIN: JavaScript and jQuery Plugins
// END: JavaScript and jQuery Plugins

//==========================================================================================
// BEGIN: Extend jQuery
jQuery.fn.exists = function() {
	try {
		return jQuery(this).length != 0 ? true : false ;
	} catch (err) {
		// do nothing
	}
};
// END: Extend jQuery

//==========================================================================================
// BEGIN: Global Variables
// Set user agent
var userAgent = navigator.userAgent.toLowerCase();
// End: Global Variables

//==========================================================================================
// BEGIN: Functions
// -------------------------------------------------------------------------
// Begin "Browser detection"
function browserDetection() {
	jQuery.browser.chrome = /chrome/.test(navigator.userAgent.toLowerCase()); 
	if(jQuery.browser.msie) { // Is this a version of IE?
		jQuery("body").addClass("IE");        
		jQuery("body").addClass("IE" + jQuery.browser.version.substring(0,1));
	}
	if(jQuery.browser.chrome) { // Is this a version of Chrome?
		jQuery("body").addClass("Chrome");
		userAgent = userAgent.substring(userAgent.indexOf("chrome/") +7);
		userAgent = userAgent.substring(0,1);
		jQuery("body").addClass("Chrome" + userAgent);  
		jQuery.browser.safari = false; // If it is chrome then jQuery thinks it's safari so we have to tell it it isn't
	}
	if(jQuery.browser.safari) { // Is this a version of Safari?
		jQuery("body").addClass("Safari");        
		userAgent = userAgent.substring(userAgent.indexOf("version/") +8);
		userAgent = userAgent.substring(0,1);
		jQuery("body").addClass("Safari" + userAgent);
	}
	if(jQuery.browser.mozilla) { // Is this a version of Mozilla?
		if(navigator.userAgent.toLowerCase().indexOf("firefox") != -1) { //Is it Firefox?
			jQuery("body").addClass('Firefox');
			userAgent = userAgent.substring(userAgent.indexOf("firefox/") +8);
			userAgent = userAgent.substring(0,1);
			jQuery("body").addClass("Firefox" + userAgent);
		} else { // If not then it must be another Mozilla
			jQuery("body").addClass("Mozilla");
		}
	}
}
// End "Browser detection"
// END: Functions

//==========================================================================================
// BEGIN: jQuery functions on load
jQuery.noConflict();
jQuery(browserDetection);
jQuery(document).ready(function($) {
	// --------------------------------------------------------------------------------------
	// BEGIN: clear_value
	// If JavaScript is enabled this adds "j_on" to body tag.
	$("body").addClass("j_on");
	// END: clear_value
	

	// ------------------------------------------------------------------------------
	// BEGIN: Default Input Value
	// On load - remove clear_value_off class if text box is pre-loaded with non-default value
	$(".clear_value").focus(function() {
		if ($(this).val() == $(this).attr("title")) {
			$(this).val("");
			$(this).removeClass("clear_value_off");
		}
	}).blur(function() {
		if ($(this).val() == "") {
			$(this).val($(this).attr("title"));
			$(this).addClass("clear_value_off");
		}
	});
	// END: Default Input Value
	
	
	// --------------------------------------------------------------------------------------
	// BEGIN: form highlights
	if ( $('.formcell').length ) {
		$(".formcell").click( function() {
			$(".form_selected").removeClass("form_selected");
			$(this).addClass("form_selected");
		});
		// When user tab's through fields
		$(".formcell *").blur(function(){
			$(".form_selected").removeClass("form_selected");
		});
		$(".formcell *").focus(function(){
			$(this).parents(".formcell:first").addClass("form_selected");
		});
	}
	// END: form highlights
	
	
	// --------------------------------------------------------------------------------------
	// BEGIN: form error
	if ( $('div.formcell .error').length ) {
		$('div.formcell .error:visible').each(function(){
			$(this).parents('.formcell:first').addClass('form_err');
		});
	}
	// END: form error

	//utility_nav
	if ( $('ul.utility_nav_items').length ) {
		$('ul.utility_nav_items li.utility_nav_item').hover(function(){$(this).toggleClass('active');}).find('div.dropdown_nav a:last').addClass('last');
		
	}
	
	//primary_nav
	if ( $('div.primary_nav').length ) {
		$('li.pri_nav').hover(function(){$(this).toggleClass('active');})
	}
	
	//home_slide
	if ( $('div.home_slider').length ) {
		$('div.home_slide').before('<div class="home_slide_nav">').cycle({
			fx: 'scrollHorz', //http://malsup.com/jquery/cycle/begin.html
			cleartypeNoBg: true,
			timeout:15000,
			pauseOnPagerHover: true,
			pause: 1,
			startingSlide: 0,
			speed: 'slow', 
			pager: '.home_slide_nav', 
			pagerAnchorBuilder: function(idx, slide) { 
				var navTitle = $(".home_slide_box:nth-child("+ (idx+1) +") .home_slide_box_nav_title:first").html();
				return '<a href="#">'+navTitle+'</a>'; 
			}
		});
		if ($('div.home_slide_box').length <= 1 ){$('div.home_slide_nav_links').hide();}
	}
	
	//page_tabs
	if ( $('div.page_tabs').length ) {
		$( ".page_tabs" ).tabs();
	}
	
	//data_vis_tabs
	if ( $('div.data_vis_tabs').length ) {
		$( ".data_vis_tabs" ).each(function(){$(this).tabs();})
	}
	
	//home_weave_rotator
	if($('div.home_weave_rotator').children('.data_vis').length > 1) {
		$('div.home_weave_rotator').cycle({
			fx: 'scrollHorz', //http://malsup.com/jquery/cycle/begin.html
			cleartypeNoBg: true,
			timeout:0,
			pauseOnPagerHover: true,
			pause: 1,
			startingSlide: 0,
			speed: 'slow', 
			next: '.home_weave_rotator_header .nav_next',
			prev: '.home_weave_rotator_header .nav_prev'
		});
	}
	
	//home_maps_rotator
	if($('ul.home_featured_maps_rotator').length) {
		$('ul#FeaturedMapsRotator').jcarousel({
			scroll: 1,
			visible: 3,
			wrap: "circular",
			initCallback: mycarousel_initCallback,
			buttonNextHTML: null,
			buttonPrevHTML: null	
		});
	}
	
	function mycarousel_initCallback(carousel) {
		$('.nav_prev','.home_featured_maps_rotator_wrap').bind('click', function() {
			carousel.prev();
			return false;
		});
		$('.nav_next','.home_featured_maps_rotator_wrap').bind('click', function() {
			carousel.next();
			return false;
		});
	}
	
	
	//related_vis
	if ( $('div.related_vis').length ) {
		$( ".related_vis_header .expand_link" ).toggle(function(){
			$(this).html('Collapse [-]').parents('.related_vis:first').find('.related_vis_content:first').show();
		},function(){
			$(this).html('Expand [+]').parents('.related_vis:first').find('.related_vis_content:first').hide();
		});
	}
	
	
	//results_filter_listing
	if ( $('div.results_filter_listing').length ) {
		$( ".results_filter_listing_header .expand_link" ).toggle(function(){
			$(this).html('Collapse [-]').parents('.results_filter_listing:first').addClass('expanded').find('.results_filter_listing_content:first').show();
		},function(){
			$(this).html('Expand [+]').parents('.results_filter_listing:first').removeClass('expanded').find('.results_filter_listing_content:first').hide();
		});
	}
	
	
	//faq_wrap
	if ( $('div.faq_wrap').length ) {
		$( ".faq_header .expand_link" ).toggle(function(){
			$(this).html('Expand [+]').parents('.faq_wrap:first').removeClass('expanded').find('.faq_content:first').hide();
		},function(){
			$(this).html('Collapse [-]').parents('.faq_wrap:first').addClass('expanded').find('.faq_content:first').show();
		});
	}
	
	////////////////////////////////////////////////////////////////////////////////////
	
	//partners_slider
	if ( $('div.partners_slider').length ) {
		$('div.partners_slider_items').cycle({
			fx: 'fade', //http://malsup.com/jquery/cycle/begin.html
			cleartypeNoBg: true,
			pauseOnPagerHover: true,
			pause: 1,
			startingSlide: 0,
			//random: 1,
			speed: 'slow', 
			next: '.partners_slider_nav .next', 
			prev: '.partners_slider_nav .prev'
		}).cycle('pause');
		if ($('div.partners_slider_item').length <= 1 ){$('div.partners_slider_nav').hide();}
	}
	//partners_slider
	if ( $('div.hub_slider').length ) {
		$('div.hub_slider_items').cycle({
			fx: 'fade', //http://malsup.com/jquery/cycle/begin.html
			cleartypeNoBg: true,
			pauseOnPagerHover: true,
			pause: 1,
			startingSlide: 0,
			speed: 'slow', 
			next: '.hub_slider_nav .next', 
			prev: '.hub_slider_nav .prev' 
		}).cycle('pause');
		if ($('div.hub_slider_item').length <= 1 ){$('div.hub_slider_nav').hide();}
	}
	
	//column_callouts
	if($('div.column_callouts').length){
		$('div.column_callouts').each(function(){
			var item_container = $('div.column_callouts_items', this);
			var all_items = item_container.find('div.column_callouts_item');
			all_items.filter(":last").addClass('last');
			//count and resize to count
			var items_width = item_container.width(); //container width
			var item_num = all_items.length;
			//2 items (container = 940px, item = 405px, margin between = 130px )
			/*var item_spacer = 130; //seperation number in px
			var item_s = Math.round((item_spacer / item_num)-1)+'px'; //final seperation number in px
			var item_w = ((items_width - item_spacer)/item_num); //final item width in px
			
			all_items.css('width',item_w).find('.column_callouts_img img').css('max-width','300px').end().filter(':not(.last)').css('marginRight',item_s);*/
			if (item_num == 2){
				all_items.css('width','405').find('.column_callouts_img img').css('max-width','300px').end().filter(':not(.last)').css('marginRight','130px');
			} else if (item_num == 3) {
				all_items.css('width','270').find('.column_callouts_img img').css('max-width','270px').end().filter(':not(.last)').css('marginRight','65px');
			} else if (item_num == 4) {
				all_items.css('width','200').find('.column_callouts_img img').css('max-width','200px').end().filter(':not(.last)').css('marginRight','45px');
			}
		});
	}
	
	//.grid_table tr.odd
	if($('table.grid_table').length){
		$('table.grid_table').each(function(){$(this).find('tr:has(td):odd').addClass('odd')});
	}
	
	//topic_indicator_list
	if($('div.topic_indicator_list').length){
		$('.topic_indicator_list_item_header').toggle(function(){
			$(this).parents('div.topic_indicator_list_item').addClass('active').find('.topic_indicator_list_item_header:first .link').html('- collapse');
		},function(){
			$(this).parents('div.topic_indicator_list_item').removeClass('active').find('.topic_indicator_list_item_header:first .link').html('+ collapse');
		})
	}
	
	/* Apply active class to dropdown in subnav */
	$('div.view_related','.sector_subnav').hover(function() {
		$(this).toggleClass('active');
	});
	
	/* Goal Detail Dropdown Menu */
	if ( $('div.goal_dropdown').length ) {
		$('div.goal_menu').hoverIntent(function(){
			$(this).parent('div.goal_dropdown').addClass('active');
			
			$(this).parent('div.goal_dropdown').find('div.goal_drop_nav_tabs:not(.constructed)').addClass('constructed').tabs({event: "mouseover", show:function(event, ui) {
				var ind = ui.index;
				
				var tabHeight = $(ui.tab).height();
				var tabOffTop = $(ui.tab).offset().top;
				
				var panelHeight = $(ui.panel).height();
				var pannelOffTop = $(ui.panel).offset().top;
				
				if((tabOffTop + tabHeight) > (pannelOffTop+panelHeight)) {
					$(ui.panel).height( panelHeight+((tabOffTop + tabHeight)-(pannelOffTop+panelHeight)) );
				}
			}}).find('ul.goal_drop_nav_tabs_nav li:last').has('a').addClass('last_link');
			//$('.goal_drop_nav_tabs_nav li').
			
		}, function(){$(this).parent('div.goal_dropdown').removeClass('active');})
	}
	
	/* Sector Detail Rotator */
	if($('div#FeaturedDataVisualizationsRotator').length > 0) {
		// if it exists
		if($('div#FeaturedDataVisualizationsRotator').children().length > 1) {
			// if it has more than 1 slide
			$('div#FeaturedDataVisualizationsRotator').cycle({
				activePagerClass: 'active',
				fx: 'scrollHorz',
				pager: 'div#FeaturedDataVisualizationsPager',
				pause: 1,
				speed: 700,
				timeout: 6000,
				after: function (currSlide, nextSlide, options, forwardFlag) {
					$('.feat_data_rotator_controls .label').html($(nextSlide).index()+1 + " of " + $('div#FeaturedDataVisualizationsRotator').children().length+": ");
				},
				pagerAnchorBuilder: function(index, slide) {
					return "$('div#FeaturedDataVisualizationsPager').append('<a href='javascript:;'>" + index + "</a>')";
				}
			});
		}
	}
	
	//indicator_detail_intro toggle content
	if ( $('div.indicator_detail_desc').length ) {
		$('div.indicator_detail_desc').each(function(){
			var this_item = $(this);
			var desc_height = this_item.height();
			var content_height = this_item.find('.indicator_detail_cont').height();
			if (content_height > desc_height){
				add_links = true;
				this_item.after('<a href="javascript:;" class="link_more">+ View More</a>');
			}
		})
		$('div.indicator_detail_intro .link_more').toggle(function(){
			$(this).html('- View Less').addClass('active');
			$('div.indicator_detail_intro .link_more:not(.active)').click();
			var this_desc = $(this).siblings('.indicator_detail_desc:first');
			var this_cont = this_desc.find('.indicator_detail_cont');
			$(this).data('this_desc_h',this_desc.height());
			this_desc.animate({height:this_cont.height()},750);
		},function(){
			$(this).html('+ View More').removeClass('active');
			$('div.indicator_detail_intro .link_more.active').click();
			var this_desc = $(this).siblings('.indicator_detail_desc:first');
			var this_desc_h = $(this).data('this_desc_h');
			this_desc.animate({height:this_desc_h},750);
		})
	}
	
	//goal_listing
	if ($("div.goal_listing").length){
		//toggle item
		$("div.goal_listing_item_link a").toggle(function() { 
			$(this).addClass('active').parents(".goal_listing_item:first").find(".goal_listing_item_table:first").slideToggle();
			$(this).html('- Collapse Goal');
		},function(){
			$(this).removeClass('active').parents(".goal_listing_item:first").find(".goal_listing_item_table:first").slideToggle();
			$(this).html('+ Expand Goal');
		});
		//toggle all
		$("div.goal_listing_header_link a").toggle(function(){
			$(this).html('- Collapse All');
			$(".goal_listing_item_link a:not(.active)").click();
		},function(){
			$(this).html('+ Expand All');
			$(".goal_listing_item_link a.active").click();
		});
	}

	
	//modal_window
	//opening modal function so all items can use it
	function modalOpen(modalID){
		//close any open modals from body data
		$($('body').data('modal_id')).dialog('close');
		//add data to body on which modal is open
		$('body').data('modal_id',modalID);
		//open new modal
		$(modalID).dialog('open');
	}
	//function to pull from URL ID to open modal
	function queryStFind(stringID) {
		loc_query = window.location.search.substring(1);
		query_ar = loc_query.split("&");
		for (i=0;i<query_ar.length;i++) {
			query_item = query_ar[i].split("=");
			if (query_item[0] == stringID) {
				return query_item[1];
			}
		}
	}
	$('.modal_window_cont').jScrollPane();
	//setup function for EACH modal on page
	if ( $('.modal_window').length ) {
		$(".modal_window").each(function(){
			$(this).dialog({
				bgiframe:true,
				width:875, 
				modal: true,
				autoOpen: false,
				closeText: 'Close',
				dialogClass: 'modal_body',
				draggable: true,
				open: function(type, data) {
					$(this).parent().appendTo("form");
					var this_modal = $(this);
					this_modal.find('.modal_window_cont').jScrollPane();
					this_modal.find('.modal_window_embed_textarea textarea').click(function(){$(this).select();});
					this_modal.find('a.embed').click(function(){
						$(this).toggleClass('on');
						this_modal.find('.modal_window_embed').toggle();
					});
					this_modal.find('.modal_window_embed_link a').click(function(){
						this_modal.find('a.embed').click();
					});
				}
			})
		});
		
		//get ID and open from url query [Data-Visualization]
		var modalUrlID = queryStFind('Data-Visualization');
		if (modalUrlID != null){modalOpen('#'+modalUrlID);}
		
		//media_link modal open
		$(".media_link a").click(
			function(event){
				event.preventDefault();
				var modal_id = $(this).attr('href');
				modalOpen(modal_id);
			}
		);		
	}
	
	
});
// BEGIN: jQuery functions on load