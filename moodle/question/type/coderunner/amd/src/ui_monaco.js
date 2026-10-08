// This file is part of Moodle - http://moodle.org/
//
// Moodle is free software: you can redistribute it and/or modify
// it under the terms of the GNU General Public License as published by
// the Free Software Foundation, either version 3 of the License, or
// (at your option) any later version.
//
// Moodle is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with Moodle.  If not, see <http://www.gnu.org/licenses/>.

/**
 * JavaScript to interface to the Monaco editor (the VS Code editor).
 *
 * Monaco brings its own AMD loader, which clashes with Moodle's RequireJS,
 * so the editor runs inside a same-origin iframe (monaco/editor.html) and
 * this module drives it directly via the iframe's window object.
 * It implements the same UI plugin interface as ui_ace.
 *
 * @module qtype_coderunner/ui_monaco
 * @copyright  2026
 * @license    http://www.gnu.org/copyleft/gpl.html GNU GPL v3 or later
 */

define(['jquery', 'core/config'], function($, config) {
    const GLOBAL_THEME_KEY = 'qtype_coderunner.monaco.theme';
    const PAGE_URL = config.wwwroot + '/question/type/coderunner/monaco/editor.html';

    // Map CodeRunner language names to Monaco language ids.
    const LANG_MAP = {
        'python2': 'python', 'python3': 'python', 'python': 'python', 'pypy3': 'python',
        'c': 'cpp', 'cpp': 'cpp', 'c++': 'cpp', 'java': 'java', 'php': 'php',
        'nodejs': 'javascript', 'javascript': 'javascript', 'pascal': 'pascal',
        'sql': 'sql', 'csharp': 'csharp', 'octave': 'plaintext', 'matlab': 'plaintext'
    };

    /**
     * Constructor for the Monaco interface object.
     * @param {string} textareaId The ID of the HTML textarea element to be wrapped.
     * @param {int} w The width in pixels of the textarea.
     * @param {int} h The height in pixels of the textarea.
     * @param {object} params The UI parameter object.
     */
    function MonacoWrapper(textareaId, w, h, params) {
        const t = this;
        this.textarea = $(document.getElementById(textareaId));
        this.textareaId = textareaId;
        this.params = params;
        this.editor = null;
        this.monaco = null;
        this.contentsChanged = false;
        this.pendingLang = params.lang;
        this.focusRequested = this.textarea[0] === document.activeElement;
        this.fail = false;

        this.frame = $('<iframe></iframe>');
        this.frame.attr({
            title: 'Code editor - Enter your code here.',
            src: PAGE_URL
        });
        this.frame.css({
            border: '1px solid #555',
            width: '100%',
            height: h,
            display: 'block',
            background: '#1e1e1e'
        });
        this.frame.on('load', function() {
            t.initEditor();
        });
    }

    MonacoWrapper.prototype.extractFromJsonMaybe = function(code) {
        // If the given code looks like JSON from the Scratchpad UI,
        // extract and return the answer_code attribute.
        try {
            const jsonObj = JSON.parse(code);
            code = jsonObj.answer_code[0];
        } catch (err) {
            // Not JSON, just use the code as is.
        }
        return code;
    };

    MonacoWrapper.prototype.initEditor = function() {
        const t = this;
        const win = this.frame[0].contentWindow;
        if (!win || !win.monacoPageReady) {
            this.showFallback();
            return;
        }
        const params = this.params;
        let code = this.textarea.val();
        if (params.import_from_scratchpad === undefined || params.import_from_scratchpad) {
            code = this.extractFromJsonMaybe(code);
        }
        const userTheme = this.safeStorage(GLOBAL_THEME_KEY);
        const fontSize = parseInt(params.font_size, 10) || 16;
        const live = params.live_autocompletion === undefined ? false : !!params.live_autocompletion;

        win.initMonaco({
            value: code,
            language: this.langId(this.pendingLang),
            theme: userTheme || params.theme || 'vs-dark',
            readOnly: !!this.textarea.prop('readonly'),
            automaticLayout: true,
            fontSize: fontSize,
            fontFamily: "'Fira Code', 'Cascadia Code', Consolas, 'DejaVu Sans Mono', monospace",
            tabSize: 4,
            insertSpaces: true,
            detectIndentation: false,
            minimap: {enabled: params.minimap === undefined ? true : !!params.minimap},
            scrollBeyondLastLine: false,
            bracketPairColorization: {enabled: true},
            guides: {indentation: true, bracketPairs: true},
            autoClosingBrackets: 'never',
            autoClosingQuotes: 'never',
            autoClosingOvertype: 'never',
            autoClosingDelete: 'never',
            autoSurround: 'never',
            autoIndent: 'full',
            formatOnPaste: false,
            formatOnType: false,
            quickSuggestions: live,
            suggestOnTriggerCharacters: live,
            wordBasedSuggestions: live ? 'currentDocument' : 'off',
            acceptSuggestionOnEnter: live ? 'on' : 'off',
            tabCompletion: 'off',
            snippetSuggestions: live ? 'inline' : 'none',
            parameterHints: {enabled: live},
            inlineSuggest: {enabled: live},
            hover: {enabled: live},
            lightbulb: {enabled: 'off'},
            codeLens: false,
            renderWhitespace: 'selection',
            smoothScrolling: true,
            cursorSmoothCaretAnimation: 'on',
            lineNumbers: 'on',
            wordWrap: 'off',
            ariaLabel: 'Code editor - Enter your code here.'
        }, function(editor, monaco) {
            t.editor = editor;
            t.monaco = monaco;
            editor.onDidChangeModelContent(function() {
                t.textarea.val(editor.getValue());
                t.contentsChanged = true;
            });
            editor.onDidBlurEditorText(function() {
                if (t.contentsChanged) {
                    t.textarea.trigger('change');
                }
            });
            if (t.focusRequested) {
                editor.focus();
                const model = editor.getModel();
                editor.setPosition(model.getPositionAt(model.getValueLength()));
            }
        });
    };

    MonacoWrapper.prototype.showFallback = function() {
        // Editor page could not be loaded: fall back to the plain textarea.
        this.fail = true;
        this.frame.remove();
        this.textarea[0].style.display = '';
    };

    MonacoWrapper.prototype.safeStorage = function(key) {
        try {
            return window.localStorage.getItem(key);
        } catch (err) {
            return null;
        }
    };

    MonacoWrapper.prototype.langId = function(language) {
        if (typeof language !== 'string') {
            return 'plaintext';
        }
        const key = language.toLowerCase();
        return LANG_MAP[key] || LANG_MAP[key.replace(/\d+$/, '')] || 'plaintext';
    };

    MonacoWrapper.prototype.setLanguage = function(language) {
        this.pendingLang = language;
        if (this.editor) {
            this.monaco.editor.setModelLanguage(this.editor.getModel(), this.langId(language));
        }
    };

    MonacoWrapper.prototype.getElement = function() {
        return this.frame;
    };

    MonacoWrapper.prototype.failed = function() {
        return this.fail;
    };

    MonacoWrapper.prototype.failMessage = function() {
        return 'ace_ui_notready';
    };

    MonacoWrapper.prototype.sync = function() {
        // Data is always synced to the textarea on change. Here we just make
        // sure that nothing was missed.
        if (this.editor) {
            this.textarea.val(this.editor.getValue());
        }
    };

    MonacoWrapper.prototype.syncIntervalSecs = function() {
        return 2;
    };

    MonacoWrapper.prototype.resize = function(w, h) {
        this.frame.outerHeight(h);
        if (this.editor) {
            this.editor.layout();
        }
    };

    MonacoWrapper.prototype.allowFullScreen = function() {
        return true;
    };

    MonacoWrapper.prototype.hasFocus = function() {
        return this.editor ? this.editor.hasTextFocus() : false;
    };

    MonacoWrapper.prototype.destroy = function() {
        if (this.editor) {
            const focused = this.editor.hasTextFocus();
            this.textarea.val(this.editor.getValue()); // Copy data back.
            this.editor.dispose();
            this.editor = null;
            this.frame.remove();
            if (focused) {
                this.textarea.focus();
                this.textarea[0].selectionStart = this.textarea[0].value.length;
            }
        } else {
            this.frame.remove();
        }
    };

    return {
        Constructor: MonacoWrapper
    };
});
