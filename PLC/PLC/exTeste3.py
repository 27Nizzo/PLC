import re
codigoSecreto = "4T4UG5H281E60X45L4MQ1T9P25A089M66L1E801D"
mensagem = re.findall(f'[13579](.)[2468]', codigoSecreto)
print("".join(mensagem))

