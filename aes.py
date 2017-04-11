import PyV8
import urllib2

def enc_data(secret,key,iv):
	ctx = PyV8.JSContext()
	ctx.enter()

	aes_js = urllib2.urlopen('http://no1.kt.com/js/aes.js')
	ctx.eval(aes_js.read())

	# str.format(func_str,"1e0c8aaa6c2b21f39e53e5040246f3be","4d37dc89ab9e7214e26b795f4bcd8890")
	
	func_str1 = 'function enc_data(secret){var key = CryptoJS.enc.Hex.parse("'
	func_str2 = '");var iv =  CryptoJS.enc.Hex.parse("'
	func_str3 = '");var encrypted = CryptoJS.AES.encrypt(secret, key, {iv:iv});encrypted = encrypted.ciphertext.toString(CryptoJS.enc.Base64);return encodeURIComponent(encrypted);}'
	func_str4 = 'var ret = enc_data("'
	func_str5 = '")'

	script = func_str1 + key + func_str2 + iv + func_str3 + func_str4 + secret + func_str5

	ctx.eval(script)

	return ctx.locals['ret']
