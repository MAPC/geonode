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
	
	//vis properties form
	if ( $('div.vis_properties_form').length ) {
		$( ".data_vis_header .expand_link" ).toggle(function(){
			$(this).html('Edit Properties [-]')
			$('.vis_properties_form:first').show();
		},function(){
			$(this).html('Edit Properties [+]')
			$('.vis_properties_form').hide();
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

	
	/* Apply active class to dropdown in subnav */
	$('div.view_related','.sector_subnav').hover(function() {
		$(this).toggleClass('active');
	});
	
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

});
// BEGIN: jQuery functions on load