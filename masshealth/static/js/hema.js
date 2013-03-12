jQuery.fn.exists = function () {
    try {
        return 0 != jQuery(this).length ? !0 : !1
    } catch (a) {}
};
var userAgent = navigator.userAgent.toLowerCase();

function browserDetection() {
    jQuery.browser.chrome = /chrome/.test(navigator.userAgent.toLowerCase());
    jQuery.browser.msie && (jQuery("body").addClass("IE"), jQuery("body").addClass("IE" + jQuery.browser.version.substring(0, 1)));
    if (jQuery.browser.chrome) jQuery("body").addClass("Chrome"), userAgent = userAgent.substring(userAgent.indexOf("chrome/") + 7), userAgent = userAgent.substring(0, 1), jQuery("body").addClass("Chrome" + userAgent), jQuery.browser.safari = !1;
    jQuery.browser.safari && (jQuery("body").addClass("Safari"),
    userAgent = userAgent.substring(userAgent.indexOf("version/") + 8), userAgent = userAgent.substring(0, 1), jQuery("body").addClass("Safari" + userAgent));
    jQuery.browser.mozilla && (-1 != navigator.userAgent.toLowerCase().indexOf("firefox") ? (jQuery("body").addClass("Firefox"), userAgent = userAgent.substring(userAgent.indexOf("firefox/") + 8), userAgent = userAgent.substring(0, 1), jQuery("body").addClass("Firefox" + userAgent)) : jQuery("body").addClass("Mozilla"))
}
jQuery.noConflict();
jQuery(browserDetection);
jQuery(document).ready(function (a) {
    function d(b) {
        a(".nav_prev", ".home_featured_maps_rotator_wrap").bind("click", function () {
            b.prev();
            return !1
        });
        a(".nav_next", ".home_featured_maps_rotator_wrap").bind("click", function () {
            b.next();
            return !1
        })
    }
    a("body").addClass("j_on");
    a(".clear_value").focus(function () {
        a(this).val() == a(this).attr("title") && (a(this).val(""), a(this).removeClass("clear_value_off"))
    }).blur(function () {
        "" == a(this).val() && (a(this).val(a(this).attr("title")), a(this).addClass("clear_value_off"))
    });
    a(".formcell").length && (a(".formcell").click(function () {
        a(".form_selected").removeClass("form_selected");
        a(this).addClass("form_selected")
    }), a(".formcell *").blur(function () {
        a(".form_selected").removeClass("form_selected")
    }), a(".formcell *").focus(function () {
        a(this).parents(".formcell:first").addClass("form_selected")
    }));
    a("div.formcell .error").length && a("div.formcell .error:visible").each(function () {
        a(this).parents(".formcell:first").addClass("form_err")
    });
    a("ul.utility_nav_items").length && a("ul.utility_nav_items li.utility_nav_item").hover(function () {
        a(this).toggleClass("active")
    }).find("div.dropdown_nav a:last").addClass("last");
    a("div.primary_nav").length && a("li.pri_nav").hover(function () {
        a(this).toggleClass("active")
    });
    a("div.home_slider").length && (a("div.home_slide").before('<div class="home_slide_nav">').cycle({
        fx: "scrollHorz",
        cleartypeNoBg: !0,
        timeout: 15E3,
        pauseOnPagerHover: !0,
        pause: 1,
        startingSlide: 0,
        speed: "slow",
        pager: ".home_slide_nav",
        pagerAnchorBuilder: function (b) {
            return '<a href="#">' + a(".home_slide_box:nth-child(" + (b + 1) + ") .home_slide_box_nav_title:first").html() + "</a>"
        }
    }), 1 >= a("div.home_slide_box").length && a("div.home_slide_nav_links").hide());
    a("div.page_tabs").length && a(".page_tabs").tabs();
    1 < a("div.home_weave_rotator").children(".data_vis").length && a("div.home_weave_rotator").cycle({
        fx: "scrollHorz",
        cleartypeNoBg: !0,
        timeout: 0,
        pauseOnPagerHover: !0,
        pause: 1,
        startingSlide: 0,
        speed: "slow",
        next: ".home_weave_rotator_header .nav_next",
        prev: ".home_weave_rotator_header .nav_prev"
    });
    a("ul.home_featured_maps_rotator").length && a("ul#FeaturedMapsRotator").jcarousel({
        scroll: 1,
        visible: 3,
        wrap: "circular",
        initCallback: d,
        buttonNextHTML: null,
        buttonPrevHTML: null
    });
    a("div.vis_properties_form").length && a(".data_vis_header .expand_link").toggle(function () {
        a(this).html("Edit Properties [-]");
        a(".vis_properties_form:first").show()
    }, function () {
        a(this).html("Edit Properties [+]");
        a(".vis_properties_form").hide()
    });
    a("div.related_vis").length && a(".related_vis_header .expand_link").toggle(function () {
        a(this).html("Collapse [-]").parents(".related_vis:first").find(".related_vis_content:first").show()
    }, function () {
        a(this).html("Expand [+]").parents(".related_vis:first").find(".related_vis_content:first").hide()
    });
    a("div.results_filter_listing").length && a(".results_filter_listing_header .expand_link").toggle(function () {
        a(this).html("Collapse [-]").parents(".results_filter_listing:first").addClass("expanded").find(".results_filter_listing_content:first").show()
    }, function () {
        a(this).html("Expand [+]").parents(".results_filter_listing:first").removeClass("expanded").find(".results_filter_listing_content:first").hide()
    });
    a("div.faq_wrap").length && a(".faq_header .expand_link").toggle(function () {
        a(this).html("Expand [+]").parents(".faq_wrap:first").removeClass("expanded").find(".faq_content:first").hide()
    },

    function () {
        a(this).html("Collapse [-]").parents(".faq_wrap:first").addClass("expanded").find(".faq_content:first").show()
    });
    a("div.column_callouts").length && a("div.column_callouts").each(function () {
        var b = a("div.column_callouts_items", this),
            c = b.find("div.column_callouts_item");
        c.filter(":last").addClass("last");
        b.width();
        b = c.length;
        2 == b ? c.css("width", "405").find(".column_callouts_img img").css("max-width", "300px").end().filter(":not(.last)").css("marginRight", "130px") : 3 == b ? c.css("width", "270").find(".column_callouts_img img").css("max-width",
            "270px").end().filter(":not(.last)").css("marginRight", "65px") : 4 == b && c.css("width", "200").find(".column_callouts_img img").css("max-width", "200px").end().filter(":not(.last)").css("marginRight", "45px")
    });
    a("table.grid_table").length && a("table.grid_table").each(function () {
        a(this).find("tr:has(td):odd").addClass("odd")
    });
    a("div.view_related", ".sector_subnav").hover(function () {
        a(this).toggleClass("active")
    });
    0 < a("div#FeaturedDataVisualizationsRotator").length && 1 < a("div#FeaturedDataVisualizationsRotator").children().length &&
        a("div#FeaturedDataVisualizationsRotator").cycle({
        activePagerClass: "active",
        fx: "scrollHorz",
        pager: "div#FeaturedDataVisualizationsPager",
        pause: 1,
        speed: 700,
        timeout: 6E3,
        after: function (b, c) {
            a(".feat_data_rotator_controls .label").html(a(c).index() + 1 + " of " + a("div#FeaturedDataVisualizationsRotator").children().length + ": ")
        },
        pagerAnchorBuilder: function (a) {
            return "$('div#FeaturedDataVisualizationsPager').append('<a href='javascript:;'>" + a + "</a>')"
        }
    })
});