// DEFINES JAVASCRIPT FOR NATURAL LANGUAGE FORM - WORK IN PROGRESS AS OF 9/6/15
// NOT CURRENTLY DISPLAYED IN FRONT-END

function NLForm( el ) {
	// the form element
	this.el = el;
	// the overlay
	this.overlay = this.el.querySelector( '.nl-overlay' );
	// array with all the possible custom fields
	this.fields = [];
	// counter for each custom field
	this.fldOpen = -1;
	this._init();
}

// Replace all the select and input elements in the form

NLForm.prototype = {
	_init : function() {
		var self = this;
		Array.prototype.slice.call( this.el.querySelectorAll( 'select' ) ).forEach( function( el, i ) {
			self.fldOpen++;
			self.fields.push( new NLField( self, el, 'dropdown', self.fldOpen ) );
		} );
		Array.prototype.slice.call( this.el.querySelectorAll( 'input' ) ).forEach( function( el, i ) {
			self.fldOpen++;
			self.fields.push( new NLField( self, el, 'input', self.fldOpen ) );
		} );
	},
}

function NLField( form, el, type, idx ) {
	this.form = form;
	// the original HTML element
	this.elOriginal = el;
	this.pos = idx;
	this.type = type;
	this._create();
	this._initEvents();
}
NLField.prototype = {
	_create : function() {
		if( this.type === 'dropdown' ) {
			this._createDropDown();
		}
		else if( this.type === 'input' ) {
			this._createInput();
		}
	},
}


// The structure will be different depending on if its an input or select field

NLField.prototype = {
	_createDropDown : function() {
		var self = this;
		this.fld = document.createElement( 'div' );
		this.fld.className = 'nl-field nl-dd';
		this.toggle = document.createElement( 'a' );
		this.toggle.innerHTML = this.elOriginal.options[ this.elOriginal.selectedIndex ].innerHTML;
		this.toggle.className = 'nl-field-toggle';
		this.optionsList = document.createElement( 'ul' );
		var ihtml = '';
		Array.prototype.slice.call( this.elOriginal.querySelectorAll( 'option' ) ).forEach( function( el, i ) {
			ihtml += self.elOriginal.selectedIndex === i ? '' + el.innerHTML + '' : '' + el.innerHTML + '';
			// selected index value
			if( self.elOriginal.selectedIndex === i ) {
				self.selectedIdx = i;
			}
		} );
		this.optionsList.innerHTML = ihtml;
		this.fld.appendChild( this.toggle );
		this.fld.appendChild( this.optionsList );
		this.elOriginal.parentNode.insertBefore( this.fld, this.elOriginal );
		this.elOriginal.style.display = 'none';
	},
	_createInput : function() {
		var self = this;
		this.fld = document.createElement( 'div' );
		this.fld.className = 'nl-field nl-ti-text';
		this.toggle = document.createElement( 'a' );
		this.toggle.innerHTML = this.elOriginal.placeholder;
		this.toggle.className = 'nl-field-toggle';
		this.optionsList = document.createElement( 'ul' );
		this.getinput = document.createElement( 'input' );
		this.getinput.setAttribute( 'type', 'text' );
		this.getinput.placeholder = this.elOriginal.placeholder;
		this.getinputWrapper = document.createElement( 'li' );
		this.getinputWrapper.className = 'nl-ti-input';
		this.inputsubmit = document.createElement( 'button' );
		this.inputsubmit.className = 'nl-field-go';
		this.inputsubmit.innerHTML = 'Go';
		this.getinputWrapper.appendChild( this.getinput );
		this.getinputWrapper.appendChild( this.inputsubmit );
		this.example = document.createElement( 'li' );
		this.example.className = 'nl-ti-example';
		this.example.innerHTML = this.elOriginal.getAttribute( 'data-subline' );
		this.optionsList.appendChild( this.getinputWrapper );
		this.optionsList.appendChild( this.example );
		this.fld.appendChild( this.toggle );
		this.fld.appendChild( this.optionsList );
		this.elOriginal.parentNode.insertBefore( this.fld, this.elOriginal );
		this.elOriginal.style.display = 'none';
	},
}

// Bind custom events

NLField.prototype = {
	_initEvents : function() {
		var self = this;
		this.toggle.addEventListener( 'click', function( ev ) { ev.preventDefault(); ev.stopPropagation(); self._open(); } );
		this.toggle.addEventListener( 'touchstart', function( ev ) { ev.preventDefault(); ev.stopPropagation(); self._open(); } );

		if( this.type === 'dropdown' ) {
			var opts = Array.prototype.slice.call( this.optionsList.querySelectorAll( 'li' ) );
			opts.forEach( function( el, i ) {
				el.addEventListener( 'click', function( ev ) { ev.preventDefault(); self.close( el, opts.indexOf( el ) ); } );
				el.addEventListener( 'touchstart', function( ev ) { ev.preventDefault(); self.close( el, opts.indexOf( el ) ); } );
			} );
		}
		else if( this.type === 'input' ) {
			this.getinput.addEventListener( 'keydown', function( ev ) {
				if ( ev.keyCode == 13 ) {
					self.close();
				}
			} );
			this.inputsubmit.addEventListener( 'click', function( ev ) { ev.preventDefault(); self.close(); } );
			this.inputsubmit.addEventListener( 'touchstart', function( ev ) { ev.preventDefault(); self.close(); } );
		}

	},
	_open : function() {
		if( this.open ) {
			return false;
		}
		this.open = true;
		this.form.fldOpen = this.pos;
		var self = this;
		this.fld.className += ' nl-field-open';
	},
	close : function( opt, idx ) {
		if( !this.open ) {
			return false;
		}
		this.open = false;
		this.form.fldOpen = -1;
		this.fld.className = this.fld.className.replace(/\b nl-field-open\b/,'');

		if( this.type === 'dropdown' ) {
			if( opt ) {
				// remove class nl-dd-checked from previous option
				var selectedopt = this.optionsList.children[ this.selectedIdx ];
				selectedopt.className = '';

				opt.className = 'nl-dd-checked';
				this.toggle.innerHTML = opt.innerHTML;

				// update selected index value
				this.selectedIdx = idx;
				// update original select element´s value
				this.elOriginal.value = this.elOriginal.children[ this.selectedIdx ].value;
			}
		}
		else if( this.type === 'input' ) {
			this.getinput.blur();
			this.toggle.innerHTML = this.getinput.value.trim() !== '' ? this.getinput.value : this.getinput.placeholder;
			this.elOriginal.value = this.getinput.value;
		}
	}
}
