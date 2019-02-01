
/*
 * Derive from the base class.
 */
MapEditor = function() {
	CommonEditor.call(this);

    this.room_index = 0;
    this.path_index = 0;
    this.current_room_id = "";
    this.current_x = 0;
    this.current_y = 0;

    // All rooms and paths.
    this.rooms = {};
    this.paths = {};
    this.room_paths = {};
}

MapEditor.prototype.init = function() {
    this.area_key = utils.getQueryString("area");

    $("#exit-button").removeClass("hidden");
    $("#save-record").removeClass("hidden");
    if (this.obj_key) {
        $("#delete-record").removeClass("hidden");
    }

    $("#form-name").text(this.area_key);

    this.onImageLoad();
    this.bindEvents();
    this.refresh();
}

MapEditor.prototype.bindEvents = function() {
    CommonEditor.prototype.bindEvents.call(this);

    $("#map-image").on("load", this.onImageLoad);

    // drag and drop to place new elements.
    $("#element-selector>.new-element").draggable ({
        helper: "clone",
        scope: "plant",
        containment: "#container"
    });
    $("#container").droppable({
        accept: ".new-element",
        scope: "plant",
        drop: controller.onDropRoom
    });

    // Click on a room to select it.
    $("#container").on("click", ".element-room", this.onClickRoom);

    // Click the background to unselect all rooms.
    $("#container").on("click", this.onClickContainer);

    // Drag from a selected room.
    $("#container").on("mousedown", ".element-selected", this.onMouseDownRoom);
}

MapEditor.prototype.onImageLoad = function() {
    var width = $("#map-image").width();
    var height = $("#map-image").height();

    $("#container").width(width);
    $("#container").height(height);

    $("#map-svg").width(width);
    $("#map-svg").height(height);

    $("#image-width").val(width);
    $("#image-height").val(height);
}

MapEditor.prototype.onSave = function() {
    // Upload images before submit the form.
    var upload_images = false;
    controller.file_fields = [];

    var image_fields = $(".image-input-control");
    for (var i = 0; i < image_fields.length; i++) {
        var file_obj = image_fields[i].files[0];
        if (file_obj && file_obj.size > 0) {
            upload_images = true;
            var image_type = $(image_fields[i]).data("image_type");
            var name = $(image_fields[i]).data("field_name");
            controller.file_fields.push(name);
            service.uploadImage(file_obj, name, image_type, controller.uploadSuccess(name), controller.uploadFailed);
        }
    }

    if (!upload_images) {
        controller.saveFields(controller.saveFormSuccess, controller.saveFormFailed);
    }
}

MapEditor.prototype.confirmDelete = function(e) {
    window.parent.controller.hideWaiting();

    service.deleteObject(controller.base_typeclass,
                         controller.obj_key,
                         controller.deleteSuccess);
}

MapEditor.prototype.onUpload = function(e) {
    var record_id = $(this).attr("data-record-id");
    if (record_id) {
        var editor = "event";
        var table = "event_data";
        var args = {
            trigger: controller.obj_key,
        }
        window.parent.controller.editRecord(editor, table, record_id, args);
    }
}

MapEditor.prototype.onDeleteEvent = function(e) {
    var record_id = $(this).attr("data-record-id");
    window.parent.controller.confirm("",
                                     "Delete this record?",
                                     controller.confirmDeleteEvent,
                                     {record: record_id});
}

MapEditor.prototype.confirmDeleteEvent = function(e) {
    window.parent.controller.hideWaiting();

    var table = controller.table_name;
    var record_id = e.data.record;
    service.deleteRecord(table, record, this.deleteEventSuccess);
}

MapEditor.prototype.deleteEventSuccess = function(data) {
    var record_id = data.record;
    $("#event-table").bootstrapTable("remove", {
        field: "id",
        values: [record_id],
    });
}

/*
 * Drag and drop a new room.
 */
MapEditor.prototype.onDropRoom = function(event, ui) {
    controller.room_index++;
    var room_id = "room-" + controller.room_index;

    var x = ui.offset.left - $(this).offset().left;
    var y = ui.offset.top - $(this).offset().top;
    controller.createRoom(room_id, x, y);
    controller.saveRoom(room_id);
}

/*
 * Create a new element.
 */
MapEditor.prototype.createRoom = function(room_id, x, y) {
    $("<div>")
        .attr("id", room_id)
        .addClass("element-room")
        .css({"left": x, "top": y, "position": "absolute"})
        .draggable ({
            scope: "plant",
            cancel: ".element-selected",
            containment: "#container",
            drag: controller.onDragRoom
        })
        .appendTo($("#container"));
}

/*
 * Drag a room.
 */
MapEditor.prototype.onDragRoom = function(event, ui) {
    var room_id = $(this).attr("id");
    var position = $(this).position();
    var width = $(this).outerWidth();
    var height = $(this).outerHeight();
    var x = position.left + width / 2;
    var y = position.top + height / 2;

    // Move linked paths.
    for (var path_id in controller.rooms[room_id].paths) {
        var path_info = controller.paths[path_id];
        var x1 = path_info.source_x;
        var y1 = path_info.source_y;
        var x2 = path_info.target_x;
        var y2 = path_info.target_y;

        if (room_id == path_info.source) {
            x1 = x;
            y1 = y;

            controller.paths[path_id]["source_x"] = x;
            controller.paths[path_id]["source_y"] = y;
        }
        else if (room_id == path_info.target) {
            x2 = x;
            y2 = y;

            controller.paths[path_id]["target_x"] = x;
            controller.paths[path_id]["target_y"] = y;
        }

        // Move path.
        var path = document.getElementById(path_id);
        path.setAttribute("d", "M " + x1 + " " + y1 + " L " + x2 + " " + y2);
    }
}

/*
 * Click to select a room.
 */
MapEditor.prototype.onClickRoom = function(event) {
    if ($(this).hasClass("new-element")) {
        return;
    }
    controller.current_room_id = $(this).attr("id");
    $(".element-room").removeClass("element-selected");
    $(this).addClass("element-selected");
    event.stopPropagation();
}

/*
 * Click the background to unselect all room.
 */
MapEditor.prototype.onClickContainer = function(event) {
    $(".element-room").removeClass("element-selected");
}

/*
 * Drag from a selected room
 */
MapEditor.prototype.onMouseDownRoom = function(event) {
    var position = $(this).position();
    var width = $(this).outerWidth();
    var height = $(this).outerHeight();
    var x = position.left + width / 2;
    var y = position.top + height / 2;
    controller.current_x = x;
    controller.current_y = y;

    // Drag a line.
    var svg = document.getElementById("map-svg");
    var namespace = "http://www.w3.org/2000/svg";
    var path = document.createElementNS(namespace, "path");
    path.setAttribute("id", "map-path");
    path.setAttribute("d", "M " + x + " " + y + " L " + x + " " + y);
    path.setAttribute("stroke", "#555");
    svg.appendChild(path);

    // Add mouse events.
    $("#container").on("mousemove", controller.onMouseMove);
    $("#container").on("mouseup", controller.onContainerMouseUp);
    $(".element-room").on("mouseup", controller.onRoomMouseUp);
}

/*
 * On drag.
 */
MapEditor.prototype.onMouseMove = function(event) {
    var x1 = controller.current_x;
    var y1 = controller.current_y;
    var x2 = event.clientX - $(this).offset().left;
    var y2 = event.clientY - $(this).offset().top;

    var path = document.getElementById("map-path");
    path.setAttribute("d", "M " + x1 + " " + y1 + " L " + x2 + " " + y2);
}


/*
 * On drag finished.
 */
MapEditor.prototype.onRoomMouseUp = function(event) {
    event.stopPropagation();

    // Remove events.
    $("#container").off("mousemove", controller.onMouseMove);
    $("#container").off("mouseup", controller.onContainerMouseUp);
    $(".element-room").off("mouseup", controller.onRoomMouseUp);

    var path = document.getElementById("map-path");
    if (!path) {
        return;
    }

    var current_room = $(controller.current_room_id);
    if (!current_room) {
        path.parentNode.removeChild(path);
        return;
    }

    // Link to the target room.
    var x1 = controller.current_x;
    var y1 = controller.current_y;

    var position = $(this).position();
    var width = $(this).outerWidth();
    var height = $(this).outerHeight();
    var x2 = position.left + width / 2;
    var y2 = position.top + height / 2;
    path.setAttribute("d", "M " + x1 + " " + y1 + " L " + x2 + " " + y2);

    // Rename the path.
    controller.path_index++;
    var path_id = "path-" + controller.path_index;
    path.setAttribute("id", path_id);

    // Save this path.
    var source_id = controller.current_room_id;
    var target_id = $(this).attr("id");
    controller.savePath(path_id, source_id, x1, y1, target_id, x2, y2);
}

/*
 * On drag finished.
 */
MapEditor.prototype.onContainerMouseUp = function(event) {
    // Remove events.
    $("#container").off("mousemove", controller.onMouseMove);
    $("#container").off("mouseup", controller.onContainerMouseUp);
    $(".element-room").off("mouseup", controller.onRoomMouseUp);

    // Remove the path.
    var path = document.getElementById("map-path");
    path.parentNode.removeChild(path);
}

/*
 * Save a room
 */
MapEditor.prototype.saveRoom = function(room_id) {
    this.rooms[room_id] = {
        paths: {}
    }
}

/*
 * Save a path
 */
MapEditor.prototype.savePath = function(path_id, source_id, source_x, source_y, target_id, target_x, target_y) {
    this.paths[path_id] = {
        source: source_id,
        source_x: source_x,
        source_y: source_y,
        target: target_id,
        target_x: target_x,
        target_y: target_y
    }

    this.rooms[source_id].paths[path_id] = "";
    this.rooms[target_id].paths[path_id] = "";
}


MapEditor.prototype.refresh = function() {
    service.queryMap(this.area_key,
                     this.queryMapSuccess,
                     this.queryMapFailed);
}

MapEditor.prototype.uploadSuccess = function(field_name) {
    var callback = function(data) {
        // Show images when upload images success.
        for (var i = 0; i < controller.file_fields.length; i++) {
            if (controller.file_fields[i] == field_name) {
                controller.file_fields.splice(i, 1);
                var field = $("#control-" + field_name);
                field.find(".editor-control").val(data.resource);
                field.find("img")
                    .attr("src", CONFIG.resource_url + data.resource)
                    .on("load", controller.onImageLoad);
                break;
            }
        }

        // Submit the form.
        if (controller.file_fields.length == 0) {
            controller.saveFields(controller.saveFormSuccess, controller.saveFormFailed);
        }
    }

    return callback;
}

MapEditor.prototype.uploadFailed = function(code, message, data) {
    window.parent.controller.notify("ERROR", code + ": " + message);
}

MapEditor.prototype.queryMapSuccess = function(data) {
    controller.table_fields = data;
    controller.obj_typeclass = "";
    controller.obj_key = "";

    // get object's typeclass
    for (var t = 0; t < data.length && !controller.obj_typeclass; t++) {
        var fields = data[t].fields;
        for (var f = 0; f < fields.length; f++) {
            if (fields[f].name == "typeclass") {
                var value = fields[f].value;
                if (value) {
                    controller.obj_typeclass = value;
                }
                break;
            }
        }
    }

    // get object's key
    for (var t = 0; t < data.length && !controller.obj_key; t++) {
        var fields = data[t].fields;
        for (var f = 0; f < fields.length; f++) {
            if (fields[f].name == "key") {
                var value = fields[f].value;
                if (value) {
                    controller.obj_key = value;
                }
                break;
            }
        }
    }

    // If has area fields.
    var query_areas = false;
    for (var t = 0; t < data.length && !query_areas; t++) {
        for (var f = 0; f < data[t].fields.length; f++) {
            if (data[t].fields[f].type == "Location") {
                query_areas = true;
                break;
            }
        }
    }
}

MapEditor.prototype.queryAreaFailed = function(code, message, data) {
    window.parent.controller.notify("ERROR", code + ": " + message);
}