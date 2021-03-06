
if (typeof(require) != "undefined") {
    require("../css/new_char.css");

    require("../controllers/base_controller.js");
}

/*
 * Derive from the base class.
 */
MudderyNewChar = function(el) {
	BasePopupController.call(this, el);
}

MudderyNewChar.prototype = prototype(BasePopupController.prototype);
MudderyNewChar.prototype.constructor = MudderyNewChar;

/*
 * Reset the view's language.
 */
MudderyNewChar.prototype.resetLanguage = function() {
	this.select("#new_char_view_header").text($$.trans("Set Character"));
	this.select("#new_char_view_name").text($$.trans("Name"));
	this.select("#new_char_button_create").text($$.trans("Create"));
	this.select("#new_char_name").attr("placeholder", $$.trans("name"));
}

/*
 * Bind events.
 */
MudderyNewChar.prototype.bindEvents = function() {
    this.onClick("#new_char_close_box", this.onClose);
    this.onClick("#new_char_button_create", this.onCreate);
}

/*
 * Event when clicks the close button.
 */
MudderyNewChar.prototype.onClose = function(element) {
	$$.main.doClosePopupBox();
}

/*
 * Event when clicks the create button.
 */
MudderyNewChar.prototype.onCreate = function(element) {
	var char_name = this.select("#new_char_name").val();
	$$.commands.createCharacter(char_name);
	this.select("#new_char_name").val("");
}
