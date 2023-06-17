import re

class Lexem:
		def __init__(self, code, token):
			self.code = code
			self.token = token
		def __repr__(self):
			return f"('{self.code}', '{self.token}')"

class Lexer:
	def __init__(self, token_type, token_type_error, token_type_divide = []):
		self.token_type = token_type
		self.token_type_error = token_type_error
		self.token_type_divide = token_type_divide

	def getLexems(self, text):
		lexems = []
		error = False

		token_regex = '|'.join('(?P<%s>%s)' % it for it in self.token_type)

		for it in re.finditer(token_regex, text):
			code = it.lastgroup
			token = it.group(code)

			flag = True
			for i in self.token_type_error:
				if flag and code == i[0] and len(lexems) != 0:
					for j in i[1]:
						if flag and j == lexems[-1].code:
							flag = False
							error = True
			flag = True
			for i in self.token_type_divide:
				if flag and code == i[0] and len(lexems) != 0:
					for j in i[1]:
						if flag and j == lexems[-1].code:
							divide_token_regex = '|'.join('(?P<%s>%s)' % its for its in i[2])

							for its in re.finditer(divide_token_regex, token):
								code = its.lastgroup
								token = its.group(code)

								lexem = Lexem(code, token)
								lexems.append(lexem)
							flag = False
			if flag:
				lexem = Lexem(code, token)
				lexems.append(lexem)
		if error:
			return []
		else:
			return lexems

token_type = [
	('ID', r'[\_a-zA-Z][\_a-zA-Z\d]*'),
	('NUM', r'[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?'),
	('LBR', r'[\(\[]'),
	('RBR', r'[\)\]]'),
	('OPER', r'[\+\-\*\/]'),
	('EOF', r'$')
	]
# что вызывает ошибку
# условие ошибки, если слева ...
# сообщение
token_type_error = [
	('ID', ('NUM', ''), "Error identifier")
	]
# что нужно разбить
# условие разбиения, если слева ...
# правила разбиения
token_type_divide = [
	('NUM', ('ID', 'NUM', 'RBR', ''), (('NUM', r'(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?'), ('OPER', r'[\+\-]')))
	]

lexer = Lexer(token_type, token_type_error, token_type_divide)

def testing(index, lexem, result):
	if (result == lexer.getLexems(lexem).__repr__()):
		if (lexer.getLexems(lexem).__repr__() == "[]"):
			print("Test:", index, "- OK.  : [Error] -", lexem)
		else:
			print("Test:", index, "- OK.  :", lexer.getLexems(lexem))
	else:
		print("Test:", index, "- NOT. :", lexer.getLexems(lexem))

testing(1, "", "[('EOF', '')]")
testing(2, "abc", "[('ID', 'abc'), ('EOF', '')]")
testing(3, "ab123", "[('ID', 'ab123'), ('EOF', '')]")
testing(4, "_123", "[('ID', '_123'), ('EOF', '')]")
testing(5, "1ab", "[]")
testing(6, "123", "[('NUM', '123'), ('EOF', '')]")
testing(7, "12e-1", "[('NUM', '12e-1'), ('EOF', '')]")
testing(8, "1.25E+7", "[('NUM', '1.25E+7'), ('EOF', '')]")
testing(9, "0.1", "[('NUM', '0.1'), ('EOF', '')]")
testing(10, "1E+10", "[('NUM', '1E+10'), ('EOF', '')]")
testing(11, "()", "[('LBR', '('), ('RBR', ')'), ('EOF', '')]")
testing(12, "[]", "[('LBR', '['), ('RBR', ']'), ('EOF', '')]")
testing(13, "[)", "[('LBR', '['), ('RBR', ')'), ('EOF', '')]")
testing(14, "(a+b)", "[('LBR', '('), ('ID', 'a'), ('OPER', '+'), ('ID', 'b'), ('RBR', ')'), ('EOF', '')]")
testing(15, "(a+1)", "[('LBR', '('), ('ID', 'a'), ('OPER', '+'), ('NUM', '1'), ('RBR', ')'), ('EOF', '')]")
testing(16, "(a-1)", "[('LBR', '('), ('ID', 'a'), ('OPER', '-'), ('NUM', '1'), ('RBR', ')'), ('EOF', '')]")
testing(17, "(a*1)", "[('LBR', '('), ('ID', 'a'), ('OPER', '*'), ('NUM', '1'), ('RBR', ')'), ('EOF', '')]")
testing(18, "(a/1)", "[('LBR', '('), ('ID', 'a'), ('OPER', '/'), ('NUM', '1'), ('RBR', ')'), ('EOF', '')]")
testing(19, "(a+b)*(c+d)", "[('LBR', '('), ('ID', 'a'), ('OPER', '+'), ('ID', 'b'), ('RBR', ')'), ('OPER', '*'), ('LBR', '('), ('ID', 'c'), ('OPER', '+'), ('ID', 'd'), ('RBR', ')'), ('EOF', '')]")
testing(20, "-3", "[('NUM', '-3'), ('EOF', '')]")

testing(21, "ab16a-17+-9.3+84*a/(1+45.34)", "[('ID', 'ab16a'), ('OPER', '-'), ('NUM', '17'), ('OPER', '+'), ('NUM', '-9.3'), ('OPER', '+'), ('NUM', '84'), ('OPER', '*'), ('ID', 'a'), ('OPER', '/'), ('LBR', '('), ('NUM', '1'), ('OPER', '+'), ('NUM', '45.34'), ('RBR', ')'), ('EOF', '')]")
testing(22, "16ab-17+-9.3+84E+16go", "[]")
testing(23, "a+b*c/(goto--16.01E-17*e)*f+g-16.01E-18", "[('ID', 'a'), ('OPER', '+'), ('ID', 'b'), ('OPER', '*'), ('ID', 'c'), ('OPER', '/'), ('LBR', '('), ('ID', 'goto'), ('OPER', '-'), ('NUM', '-16.01E-17'), ('OPER', '*'), ('ID', 'e'), ('RBR', ')'), ('OPER', '*'), ('ID', 'f'), ('OPER', '+'), ('ID', 'g'), ('OPER', '-'), ('NUM', '16.01E-18'), ('EOF', '')]")
testing(24, "a+b*c/(goto+E-16.13E+17*e)*f+g-16as01E-18", "[]")
testing(25, "116168126417117.04004040646416E+21103436", "[('NUM', '116168126417117.04004040646416E+21103436'), ('EOF', '')]")

input()