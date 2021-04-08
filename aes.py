#!/usr/bin/env python
# -*- coding: utf-8 -*-
import execjs
import urllib2

def enc_data(secret,key,iv):
    aes_js = urllib2.urlopen('http://no1.kt.com/js/aes.js')
    script = 'function _enc_data(secret, key, iv)' \
            '{' \
            '    var key = CryptoJS.enc.Hex.parse(key);' \
            '    var iv =  CryptoJS.enc.Hex.parse(iv);' \
            '    var encrypted = CryptoJS.AES.encrypt(secret, key, {iv:iv}); ' \
            '    encrypted = encrypted.ciphertext.toString(CryptoJS.enc.Base64);' \
            '    return encrypted;' \
            '}' 
    ctx= execjs.compile(aes_js.read() + script)
    return ctx.call("_enc_data", secret, key, iv)
#res = enc_data("1111", "699c7cf18b281775f4543e23b6c55a1a", "5bd010e26f0231a6c5ef94053a7db32f")
#print(res)
