
/*
 * Derive from the base class.
 */
DialogueEditor = function() {
	CommonEditor.call(this);

    // start node's keu
    this.start_point_key = "__START__";

    // this dialogue's key
    this.dialogue_key = "";

    // this dialogue's sentences
    this.sentences = {};

    // js_plumb's instance
    this.jsplumb = null;

    // nodes that have been created
    this.created = {};

    // node's grid
    this.x_step = 350;
    this.y_step = 150;
}

DialogueEditor.prototype = prototype(CommonEditor.prototype);
DialogueEditor.prototype.constructor = DialogueEditor;


DialogueEditor.prototype.bindEvents = function() {
    CommonEditor.prototype.bindEvents.call(this);

    $("#add-sentence").on("click", this.addSentence);
    $("#sentence-table").on("click", ".edit-row", this.onEditSentence);
    $("#sentence-table").on("click", ".delete-row", this.onDeleteSentence);
}

DialogueEditor.prototype.onImageLoad = function() {
    parent.controller.setFrameSize();
}

DialogueEditor.prototype.onEditSentence = function(e) {
    var record_id = $(this).attr("data-record-id");
    if (record_id) {
        var editor = "sentence";
        var table = "dialogue_sentences";
        var args = {
            dialogue: controller.dialogue_key,
        }
        window.parent.controller.editRecord(editor, table, record_id, args);
    }
}

DialogueEditor.prototype.onDeleteSentence = function(e) {
    var record_id = $(this).attr("data-record-id");
    window.parent.controller.confirm("",
                                     "Delete this sentence?",
                                     controller.confirmDeleteSentence,
                                     {record: record_id});
}

DialogueEditor.prototype.confirmDeleteSentence = function(e) {
    window.parent.controller.hide_waiting();

    var table = controller.table_name;
    var record_id = e.data.record;
    service.deleteRecord(table, record, this.deleteSentenceSuccess);
}

DialogueEditor.prototype.deleteSentenceSuccess = function(data) {
    var record_id = data.record;
    $("#sentence-table").bootstrapTable("remove", {
        field: "id",
        values: [record_id],
    });
}

DialogueEditor.prototype.queryFormSuccess = function(data) {
    for (var i = 0; i < data.length; i++) {
        if (data[i].name == "key") {
            var value = data[i].value;
            if (value) {
                controller.dialogue_key = value;
            }
            else {
                controller.dialogue_key = "";
            }
            break;
        }
    }

    CommonEditor.prototype.queryFormSuccess.call(this, data);
}

DialogueEditor.prototype.queryAreasSuccess = function(data) {
    controller.areas = data;
    controller.setFields();
    service.queryDialogueSentences(controller.dialogue_key, controller.querySentenceTableSuccess, controller.querySentenceTableFailed);
}

DialogueEditor.prototype.querySentenceTableSuccess = function(data) {
    // Add root.
    var start = {
        key: controller.start_point_key,
        content: "START",
        root: false,
        next: [],
    };
    controller.sentences = {};
    controller.sentences[start.key] = start;

    // Add the first level sentences.
    for (var i = 0; i < data.length; i++) {
        controller.sentences[data[i].key] = data[i];
        if (data[i].root) {
            controller.sentences[controller.start_point_key].next.push(data[i].key);
        }
    }

    controller.reload();
    window.parent.controller.setFrameSize();
}

DialogueEditor.prototype.querySentencesTableFailed = function(code, message, data) {
    window.parent.controller.notify("ERROR", code + ": " + message);
}

DialogueEditor.prototype.addSentence = function(e) {
    if (!controller.dialogue_key) {
        window.parent.controller.notify("You should save this dialogue first.");
        return;
    }

    var editor = "sentence"
    var table = "dialogue_sentences";
    var record = "";
    var args = {
        dialogue: controller.dialogue_key,
    }
    window.parent.controller.editRecord(editor, table, record, args);
}

DialogueEditor.prototype.onJsPlumbReady = function() {
    // setup some defaults for jsPlumb.
    var instance = controller.jsplumb = jsPlumb.getInstance({
        Endpoint: ["Dot", {radius: 2}],
        Connector:"StateMachine",
        HoverPaintStyle: {stroke: "#1e8151", strokeWidth: 2 },
        ConnectionOverlays: [
            [ "Arrow", {
                location: 1,
                visible:true,
                width:11,
                length:11,
                id:"ARROW"
            } ],
            [ "Label", { label: "NEXT", id: "label", cssClass: "aLabel" }]
        ],
        Container: "canvas"
    });

    instance.registerConnectionType("basic", { anchors:["Bottom", "Top"], connector:"Flowchart" });

    window.jsp = instance;

    var canvas = document.getElementById("canvas");

    // bind a click listener to each connection; the connection is deleted. you could of course
    // just do this: instance.bind("click", instance.deleteConnection), but I wanted to make it clear what was
    // happening.
    instance.bind("click", function (c) {
        instance.deleteConnection(c);
    });

    // bind a connection listener. note that the parameter passed to this function contains more than
    // just the new connection - see the documentation for a full list of what is included in 'info'.
    // this listener sets the connection's internal
    // id as the label overlay's text.
    instance.bind("connection", function (info) {
        //info.connection.getOverlay("label").setLabel(info.connection.id);
        info.connection.getOverlay("label").hide();
    });

    // bind a double click listener to "canvas"; add new node when this occurs.
    jsPlumb.on(canvas, "dblclick", function(e) {
        newNode(e.offsetX, e.offsetY);
    });
}

// reload the flowchart
DialogueEditor.prototype.reload = function() {
    this.jsplumb.empty("canvas");

    var x = 100;
    var y = 20;

    // reset created nodes
    this.created = {};

    // create the tree from root
    this.createTree(x, y, this.start_point_key);

    // connect nodes after all nodes have been created because node's position may change in creating.
    for (var key in this.sentences) {
        var children = this.sentences[key].next;
        for (var i = 0; i < children.length; i++) {
            this.jsplumb.connect({ source: key, target: children[i], type:"basic" });
        }
    }
}

// Create a tree.
DialogueEditor.prototype.createTree = function(x, y, root) {
    var node = this.newNode(x, y, root, this.sentences[root].content);

    var x_pos = x;
    var y_pos = y + this.y_step;
    var children = this.sentences[root].next;
    for (var i = 0; i < children.length; i++) {
        if (!(children[i] in this.created)) {
            // This node has not been created.
            if (i > 0) {
                x_pos += this.x_step;
            }
            // get child tree's x position
            x_pos = this.createTree(x_pos, y_pos, children[i]);
        }
    }

    // reset root node's position according to children's positions
    node.style.left = (x + x_pos) / 2 + "px";

    this.jsplumb.getContainer().appendChild(node);
    this.initNode(node);

    return x_pos;
}

// add a new node
DialogueEditor.prototype.newNode = function(x, y, key, content) {

	var template = $(".sentence-node.template");
	var item = template.clone().removeClass("template");
	item.attr("id", key);
	item.find(".content").text(content);
	item.css({"left": x + "px", "top": y + "px"});

	item.on("dblclick", this.onClickNode);

    return item[0];
}

//
// initialise element as connection targets and source.
//
DialogueEditor.prototype.initNode = function(el) {

    // initialise draggable elements.
    this.jsplumb.draggable(el);

    this.jsplumb.makeSource(el, {
        filter: ".add-connection",
        anchors:["Bottom", "Top"],
        connectorStyle: { stroke: "#5c96bc", strokeWidth: 2, outlineStroke: "transparent", outlineWidth: 4 },
        connectionType:"basic",
        maxConnections: -1,
        extract:{
            "action":"the-action"
        },
    });

    this.jsplumb.makeTarget(el, {
        dropOptions: { hoverClass: "dragHover" },
        anchors:["Bottom", "Top"],
        allowLoopback: false,
    });
}


//
DialogueEditor.prototype.onClickNode = function(e) {
    if ($(this).attr("id") == controller.start_point_key) {
        return;
    }

    var content = $(this).find(".content").text();
    content = prompt("Please input the sentence.", content);
    if (content == null) {
        return;
    }

    $(this).find(".content").text(content);
}