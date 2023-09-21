def validate_cpf(cpf):
    """
    Valida um CPF brasileiro.

    Args:
        cpf (str): O CPF a ser validado.

    Returns:
        bool: True se o CPF for válido, False caso contrário.
    """
    # Remove caracteres não numéricos do CPF
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifica se o CPF possui 11 dígitos
    if len(cpf) != 11:
        return False

    # Calcula o primeiro dígito verificador
    soma = 0
    peso = 10
    for i in range(9):
        soma += int(cpf[i]) * peso
        peso -= 1
    resto = soma % 11
    digito1 = 0 if resto < 2 else 11 - resto

    # Calcula o segundo dígito verificador
    soma = 0
    peso = 11
    for i in range(10):
        soma += int(cpf[i]) * peso
        peso -= 1
    resto = soma % 11
    digito2 = 0 if resto < 2 else 11 - resto

    # Verifica se os dígitos verificadores são válidos
    return int(cpf[9]) == digito1 and int(cpf[10]) == digito2
