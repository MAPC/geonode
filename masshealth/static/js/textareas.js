tinyMCE.init({

  // General options
  mode: "exact",
  elements: "id_profile, id_program_desc, id_abstract, id_text, id_content, id_description",
  theme: "advanced",
  // funky cross-dependencies makes deactivating single plugins a minefield
  plugins: "autolink,lists,spellchecker,pagebreak,style,layer,table,save,advhr,advimage,advlink,emotions,iespell,inlinepopups,insertdatetime,preview,media,searchreplace,print,contextmenu,paste,directionality,fullscreen,noneditable,visualchars,nonbreaking,xhtmlxtras,template",

  // Theme options
  theme_advanced_buttons1: "formatselect,separator,preview,separator,bold,italic,underline,strikethrough,separator,bullist,numlist,outdent,indent,separator,undo,redo,separator,link,unlink,anchor,separator,image,media,separator,removeformat,cleanup,pastetext,pasteword,separator,code",
  // theme_advanced_buttons1: "save,newdocument,|,bold,italic,underline,strikethrough,|,justifyleft,justifycenter,justifyright,justifyfull,|,styleselect,formatselect,fontselect,fontsizeselect",
  // theme_advanced_buttons2: "cut,copy,paste,pastetext,pasteword,|,search,replace,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,help,code,|,insertdate,inserttime,preview,|,forecolor,backcolor",
  // theme_advanced_buttons3: "tablecontrols,|,hr,removeformat,visualaid,|,sub,sup,|,charmap,emotions,iespell,media,advhr,|,print,|,ltr,rtl,|,fullscreen",
  // theme_advanced_buttons4: "insertlayer,moveforward,movebackward,absolute,|,styleprops,spellchecker,|,cite,abbr,acronym,del,ins,attribs,|,visualchars,nonbreaking,template,blockquote,pagebreak,|,insertfile,insertimage",
  theme_advanced_blockformats : "p,h3,h4,blockquote",
  theme_advanced_toolbar_location: "top",
  theme_advanced_toolbar_align: "left",
  theme_advanced_statusbar_location: "bottom",
  theme_advanced_resizing: true,
  height: "280",

  // Content CSS (slimmer than main.css)
  content_css: "/static/css/custom.css",

  file_browser_callback: "CustomFileBrowser"
  
});

function CustomFileBrowser(field_name, url, type, win) {

  var cmsURL = '/admin/filebrowser/browse/?pop=2';
  cmsURL = cmsURL + '&type=' + type;

  tinyMCE.activeEditor.windowManager.open({
    file: cmsURL,
    width: 980, // Your dimensions may differ - toy around with them!
    height: 500,
    resizable: 'yes',
    scrollbars: 'yes',
    inline: 'no', // This parameter only has an effect if you use the inlinepopups plugin!
    close_previous: 'no'
  }, {
    window: win,
    input: field_name,
    editor_id: tinyMCE.selectedInstance.editorId
  });
  return false;
}