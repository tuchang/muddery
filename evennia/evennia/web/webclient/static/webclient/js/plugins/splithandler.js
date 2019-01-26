/*
 *
 * Plugin to use split.js to create a basic windowed ui
 *
 */
let splithandler_plugin = (function () {

    var num_splits = 0;
    var split_panes = {};
    var backout_list = new Array;

    var known_types = new Array();

    // Exported Functions

    //
    // function to assign "Text types to catch" to a pane
    var set_pane_types = function (splitpane, types) {
        split_panes[splitpane]['types'] = types;
    }

    //
    // Add buttons to the Evennia webcilent toolbar
    function addToolbarButtons () {
        var toolbar = $('#toolbar');
        toolbar.append( $('<button id="splitbutton" type="button">&#x21f9;</button>') );
        toolbar.append( $('<button id="panebutton" type="button">&#x2699;</button>') );
        toolbar.append( $('<button id="undobutton" type="button">&#x21B6;</button>') );
        $('#undobutton').hide();
    }

    function addSplitDialog () {
        plugins['popups'].createDialog('splitdialog', 'Split Dialog', '');
    }

    function addPaneDialog () {
        plugins['popups'].createDialog('panedialog', 'Pane Dialog', '');
    }

    //
    // Handle resizing the InputField after a client resize event so that the splits dont get too big.
    function resizeInputField () {
        var wrapper = $("#inputform")
        var input = $("#inputcontrol")
        var prompt = $("#prompt")

        input.height( wrapper.height() - (input.offset().top - wrapper.offset().top) );
    }

    //
    // Handle resizing of client
    function doWindowResize() {
        var resizable = $("[data-update-append]");
        var parents = resizable.closest(".split");

        resizeInputField();

        parents.animate({
            scrollTop: parents.prop("scrollHeight")
        }, 0);
    }

    //
    // create a new UI split
    var dynamic_split = function (splitpane, direction, pane_name1, pane_name2, update_method1, update_method2, sizes) {
        // find the sub-div of the pane we are being asked to split
        splitpanesub = splitpane + '-sub';

        // create the new div stack to replace the sub-div with.
        var first_div  = $( '<div id="'+pane_name1+'" class="split split-'+direction+'" />' )
        var first_sub  = $( '<div id="'+pane_name1+'-sub" class="split-sub" />' )
        var second_div = $( '<div id="'+pane_name2+'" class="split split-'+direction+'" />' )
        var second_sub = $( '<div id="'+pane_name2+'-sub" class="split-sub" />' )

        // check to see if this sub-pane contains anything
        contents = $('#'+splitpanesub).contents();
        if( contents ) {
            // it does, so move it to the first new div-sub (TODO -- selectable between first/second?)
            contents.appendTo(first_sub);
        }
        first_div.append( first_sub );
        second_div.append( second_sub );

        // update the split_panes array to remove this pane name, but store it for the backout stack
        var backout_settings = split_panes[splitpane];
        delete( split_panes[splitpane] );

        // now vaporize the current split_N-sub placeholder and create two new panes.
        $('#'+splitpane).append(first_div);
        $('#'+splitpane).append(second_div);
        $('#'+splitpane+'-sub').remove();

        // And split
        Split(['#'+pane_name1,'#'+pane_name2], {
            direction: direction,
            sizes: sizes,
            gutterSize: 4,
            minSize: [50,50],
        });

        // store our new split sub-divs for future splits/uses by the main UI.
        split_panes[pane_name1] = { 'types': [], 'update_method': update_method1 };
        split_panes[pane_name2] = { 'types': [], 'update_method': update_method2 };

        // add our new split to the backout stack
        backout_list.push( {'pane1': pane_name1, 'pane2': pane_name2, 'undo': backout_settings} );

        $('#undobutton').show();
    }

    //
    // Reverse the last UI split
    var undo_split = function () {
        // pop off the last split pair
        var back = backout_list.pop();
        if( !back ) {
            return;
        }

        if( backout_list.length === 0 ) {
            $('#undobutton').hide();
        }

        // Collect all the divs/subs in play
        var pane1 = back['pane1'];
        var pane2 = back['pane2'];
        var pane1_sub = $('#'+pane1+'-sub');
        var pane2_sub = $('#'+pane2+'-sub');
        var pane1_parent = $('#'+pane1).parent();
        var pane2_parent = $('#'+pane2).parent();

        if( pane1_parent.attr('id') != pane2_parent.attr('id') ) {
            // sanity check failed...somebody did something weird...bail out
            console.log( pane1 );
            console.log( pane2 );
            console.log( pane1_parent );
            console.log( pane2_parent );
            return;
        }

        // create a new sub-pane in the panes parent
        var parent_sub = $( '<div id="'+pane1_parent.attr('id')+'-sub" class="split-sub" />' )

        // check to see if the special #messagewindow is in either of our sub-panes.
        var msgwindow = pane1_sub.find('#messagewindow')
        if( !msgwindow ) {
            //didn't find it in pane 1, try pane 2
            msgwindow = pane2_sub.find('#messagewindow')
        }
        if( msgwindow ) {
            // It is, so collect all contents into it instead of our parent_sub div
            // then move it to parent sub div, this allows future #messagewindow divs to flow properly
            msgwindow.append( pane1_sub.contents() );
            msgwindow.append( pane2_sub.contents() );
            parent_sub.append( msgwindow );
        } else {
            //didn't find it, so move the contents of the two panes' sub-panes into the new sub-pane
            parent_sub.append( pane1_sub.contents() );
            parent_sub.append( pane2_sub.contents() );
        }

        // clear the parent
        pane1_parent.empty();

        // add the new sub-pane back to the parent div
        pane1_parent.append(parent_sub);

        // pull the sub-div's from split_panes
        delete split_panes[pane1];
        delete split_panes[pane2];

        // add our parent pane back into the split_panes list for future splitting
        split_panes[pane1_parent.attr('id')] = back['undo'];
    }

    //
    // UI elements
    //

    //
    // Draw "Split Controls" Dialog
    var onSplitDialog = function () {
        var dialog = $("#splitdialogcontent");
        dialog.empty();

        dialog.append("<h3>Split?</h3>");
        dialog.append('<input type="radio" name="direction" value="vertical" checked> top/bottom<br />');
        dialog.append('<input type="radio" name="direction" value="horizontal"> side-by-side<br />');

        dialog.append("<h3>Split Which Pane?</h3>");
        for ( var pane in split_panes ) {
            dialog.append('<input type="radio" name="pane" value="'+ pane +'">'+ pane +'<br />');
        }

        dialog.append("<h3>New Pane Names</h3>");
        dialog.append('<input type="text" name="new_pane1" value="" />');
        dialog.append('<input type="text" name="new_pane2" value="" />');

        dialog.append("<h3>New First Pane Flow</h3>");
        dialog.append('<input type="radio" name="flow1" value="append" checked>append<br />');
        dialog.append('<input type="radio" name="flow1" value="replace">replace<br />');

        dialog.append("<h3>New Second Pane Flow</h3>");
        dialog.append('<input type="radio" name="flow2" value="append" checked>append<br />');
        dialog.append('<input type="radio" name="flow2" value="replace">replace<br />');

        dialog.append('<div id="splitclose" class="button">Split It</div>');

        $("#splitclose").bind("click", onSplitDialogClose);

        plugins['popups'].togglePopup("#splitdialog");
    }

    //
    // Close "Split Controls" Dialog
    var onSplitDialogClose = function () {
        var pane      = $("input[name=pane]:checked").attr("value");
        var direction = $("input[name=direction]:checked").attr("value");
        var new_pane1 = $("input[name=new_pane1]").val();
        var new_pane2 = $("input[name=new_pane2]").val();
        var flow1     = $("input[name=flow1]:checked").attr("value");
        var flow2     = $("input[name=flow2]:checked").attr("value");

        if( new_pane1 == "" ) {
            new_pane1 = 'pane_'+num_splits;
            num_splits++;
        }

        if( new_pane2 == "" ) {
            new_pane2 = 'pane_'+num_splits;
            num_splits++;
        }

        if( document.getElementById(new_pane1) ) {
            alert('An element: "' + new_pane1 + '" already exists');
            return;
        }

        if( document.getElementById(new_pane2) ) {
            alert('An element: "' + new_pane2 + '" already exists');
            return;
        }

        dynamic_split( pane, direction, new_pane1, new_pane2, flow1, flow2, [50,50] );

        plugins['popups'].closePopup("#splitdialog");
    }

    //
    // Draw "Pane Controls" dialog
    var onPaneControlDialog = function () {
        var dialog = $("#splitdialogcontent");
        dialog.empty();

        dialog.append("<h3>Set Which Pane?</h3>");
        for ( var pane in split_panes ) {
            dialog.append('<input type="radio" name="pane" value="'+ pane +'">'+ pane +'<br />');
        }

        dialog.append("<h3>Which content types?</h3>");
        for ( var type in known_types ) {
            dialog.append('<input type="checkbox" value="'+ known_types[type] +'">'+ known_types[type] +'<br />');
        }

        dialog.append('<div id="paneclose" class="button">Make It So</div>');

        $("#paneclose").bind("click", onPaneControlDialogClose);

        plugins['popups'].togglePopup("#splitdialog");
    }

    //
    // Close "Pane Controls" dialog
    var onPaneControlDialogClose = function () {
        var pane = $("input[name=pane]:checked").attr("value");

        var types = new Array; 
        $('#splitdialogcontent input[type=checkbox]:checked').each(function() {
            types.push( $(this).attr('value') );
        });

        set_pane_types( pane, types );

        plugins['popups'].closePopup("#splitdialog");
    }

    //
    // plugin functions
    //

    //
    // Accept plugin onText events
    var onText = function (args, kwargs) {
        if ( kwargs && 'type' in kwargs ) {
            var msgtype = kwargs['type'];
            if ( ! known_types.includes(msgtype) ) {
                // this is a new output type that can be mapped to panes
                console.log('detected new output type: ' + msgtype)
                known_types.push(msgtype);
            }

            for ( var key in split_panes) {
                var pane = split_panes[key];

                // is this message type mapped to this pane?
                if ( (pane['types'].length > 0) && pane['types'].includes(msgtype) ) {
                    // yes, so append/replace this pane's inner div with this message
                    var text_div = $('#'+key+'-sub');
                    if ( pane['update_method'] == 'replace' ) {
                        text_div.html(args[0])
                    } else {
                        text_div.append(args[0]);
                        var scrollHeight = text_div.parent().prop("scrollHeight");
                        text_div.parent().animate({ scrollTop: scrollHeight }, 0);
                    }
                    return true;
                }
            }
        }
        return false;
    }

    //
    // Required plugin "init" function
    var init = function(settings) {
        known_types.push('help');

        Split(['#main','#input'], {
            direction: 'vertical',
            sizes: [90,10],
            gutterSize: 4,
            minSize: [50,50],
        });

        split_panes['main']  = { 'types': [], 'update_method': 'append' };

        // Create our UI
        addToolbarButtons();
        addSplitDialog();
        addPaneDialog();

        // Register our utility button events
        $("#splitbutton").bind("click", onSplitDialog);
        $("#panebutton").bind("click", onPaneControlDialog);
        $("#undobutton").bind("click", undo_split);

        // Event when client window changes
        $(window).bind("resize", doWindowResize);

        $("[data-role-input]").bind("resize", doWindowResize)
                              .bind("paste", resizeInputField)
                              .bind("cut", resizeInputField);

        // Event when any key is pressed
        $(document).keyup(resizeInputField);

        console.log("Splithandler Plugin Initialized.");
    }

    return {
        init: init,
        onText: onText,
        dynamic_split: dynamic_split,
        undo_split: undo_split,
        set_pane_types: set_pane_types,
    }
})()
plugin_handler.add('splithandler', splithandler_plugin);
