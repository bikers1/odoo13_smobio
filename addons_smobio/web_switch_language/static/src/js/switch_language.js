odoo.define('web_switch_language.SwitchLanguageMenu', function(require) {
"use strict";

var config = require('web.config');
var session = require('web.session');
var core = require('web.core');
var framework = require('web.framework');
var SystrayMenu = require('web.SystrayMenu');
var Widget = require('web.Widget');

var _t = core._t;

var SwitchLanguageMenu = Widget.extend({
    template: 'SwitchLanguageMenu',
    events: {
        'click .dropdown-item[data-menu]': '_onMenuClick',
    },

    init: function () {
        this._super.apply(this, arguments);
        this.isMobile = config.device.isMobile;
        this._onMenuClick = _.debounce(this._onMenuClick, 1500, true);
    },

    willStart: function () {
        var self = this;
        var _super = this._super();
        return this._rpc({
                model: 'res.lang',
                method: 'search_read',
                fields: ['name', 'code'],
            }).then(function(langs) {
                if (langs.length > 1) {
                    return _super;
                } else {
                    return $.Deferred().reject();
                }
            });
    },

    start: function () {
        var self = this;
        var languageList = '';
        var def = this._rpc({
                model: 'res.lang',
                method: 'search_read',
                fields: ['name', 'code'],
            })
            .then(function(langs) {
                _.each(langs, function(lang) {
                    var langCode = lang['code']
                    var langName = lang['name'].split('/').pop().trim()
                    if (langCode === session.user_context.lang) {
                        self.$('.oe_topbar_name').text(langName);
                    } else {
                        languageList += '<a role="menuitem" href="#" class="dropdown-item o_change_lang" data-menu="lang" data-lang="' +
                                        langCode + '">' + langName + '</a>';
                    }
                });
                self.$('.dropdown-menu').html(languageList);
            });
        return $.when(def, this._super.apply(this, arguments));
    },

    _onMenuClick: function (ev) {
        var self = this;
        ev.preventDefault();
        var langCode = $(ev.currentTarget).data('lang');
        this._rpc({
            model: 'res.users',
            method: 'write',
            args: [[session.uid], {'lang': langCode}],
        })
        .then(function(result) {
            if (result) {
                framework.blockUI();
                self.do_action({
                    type: 'ir.actions.client',
                    tag: 'reload_context',
                    params: {}
                });
            }
            else {
                alert(_t("Updated language failed!"));
            }
        });
    },
});

SystrayMenu.Items.push(SwitchLanguageMenu);
return SwitchLanguageMenu;

});
