#!/usr/bin/env python
# coding: utf-8

import web

render = web.template.render('templates/', cache=False)

web.config.debug = True

replaceList = []

config = web.storage(
    email='qichangxing@gmail.com',
    site_name = 'simple-todo',
    site_desc = '',
    static = '/static',
)

web.template.Template.globals['config'] = config
web.template.Template.globals['render'] = render
web.template.Template.globals['replaceList'] = replaceList