DIGITOS = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def valor_do_digito(digito):
    return DIGITOS.index(digito)


def digito_do_valor(valor):
    return DIGITOS[valor]


def base_valida(base):
    return 2 <= base <= len(DIGITOS)


def digito_valido(digito, base):
    return digito in DIGITOS and valor_do_digito(digito) < base


def numero_valido(numero, base):
    if numero == "":
        return False

    for digito in numero:
        if not digito_valido(digito, base):
            return False

    return True


def valores_dos_digitos(numero):
    valores = []

    for digito in numero:
        valores.append(valor_do_digito(digito))

    return valores


def comparar_numeros(numero1, numero2):
    numero1 = numero1.lstrip("0") or "0"
    numero2 = numero2.lstrip("0") or "0"

    if len(numero1) > len(numero2):
        return 1

    if len(numero1) < len(numero2):
        return -1

    for i in range(len(numero1)):
        valor1 = valor_do_digito(numero1[i])
        valor2 = valor_do_digito(numero2[i])

        if valor1 > valor2:
            return 1

        if valor1 < valor2:
            return -1

    return 0


def somar(numero1, numero2, base):
    resultado = []
    vai_um = 0

    i = len(numero1) - 1
    j = len(numero2) - 1

    while i >= 0 or j >= 0 or vai_um > 0:
        if i >= 0:
            valor1 = valor_do_digito(numero1[i])
        else:
            valor1 = 0

        if j >= 0:
            valor2 = valor_do_digito(numero2[j])
        else:
            valor2 = 0

        soma = valor1 + valor2 + vai_um

        if soma >= base:
            soma -= base
            vai_um = 1
        else:
            vai_um = 0

        resultado.append(digito_do_valor(soma))

        i -= 1
        j -= 1

    resultado.reverse()

    return "".join(resultado)


def subtrair(numero1, numero2, base):
    if comparar_numeros(numero1, numero2) < 0:
        return "0"

    resultado = []
    emprestimo = 0

    i = len(numero1) - 1
    j = len(numero2) - 1

    while i >= 0:
        valor1 = valor_do_digito(numero1[i]) - emprestimo

        if j >= 0:
            valor2 = valor_do_digito(numero2[j])
        else:
            valor2 = 0

        if valor1 < valor2:
            valor1 += base
            emprestimo = 1
        else:
            emprestimo = 0

        diferenca = valor1 - valor2

        resultado.append(digito_do_valor(diferenca))

        i -= 1
        j -= 1

    resultado.reverse()

    return "".join(resultado).lstrip("0") or "0"


def multiplicar_por_digito(numero, digito, base):
    resultado = []
    vai_um = 0

    valor_digito = valor_do_digito(digito)

    i = len(numero) - 1

    while i >= 0:
        valor = valor_do_digito(numero[i])

        produto = valor * valor_digito + vai_um

        resto = produto % base
        vai_um = produto // base

        resultado.append(digito_do_valor(resto))

        i -= 1

    while vai_um > 0:
        resultado.append(digito_do_valor(vai_um % base))
        vai_um = vai_um // base

    resultado.reverse()

    return "".join(resultado).lstrip("0") or "0"


def multiplicar(numero1, numero2, base):
    resultado = "0"
    deslocamento = 0

    i = len(numero2) - 1

    while i >= 0:
        parcial = multiplicar_por_digito(
            numero1,
            numero2[i],
            base
        )

        if parcial != "0":
            parcial += "0" * deslocamento

        resultado = somar(
            resultado,
            parcial,
            base
        )

        deslocamento += 1
        i -= 1

    return resultado


def dividir_direta(numero, divisor, base):
    quociente = []
    resto = "0"

    if divisor == "0":
        return None, None

    for digito in numero:
        if resto == "0":
            resto = digito
        else:
            resto += digito

        resto = resto.lstrip("0") or "0"

        digito_quociente = "0"

        while comparar_numeros(resto, divisor) >= 0:
            resto = subtrair(
                resto,
                divisor,
                base
            )

            valor = valor_do_digito(digito_quociente)
            valor += 1

            digito_quociente = digito_do_valor(valor)

        quociente.append(digito_quociente)

    resultado_quociente = "".join(quociente).lstrip("0") or "0"

    return resultado_quociente, resto


def converter_base_destino_para_origem(base_destino, base_origem):
    resultado = "0"

    for _ in range(base_destino):
        resultado = somar(
            resultado,
            "1",
            base_origem
        )

    return resultado


def converter_resto_para_destino(resto, base_origem, base_destino):
    candidato = "0"

    for valor in range(base_destino):
        if candidato == resto:
            return digito_do_valor(valor)

        candidato = somar(
            candidato,
            "1",
            base_origem
        )

    return "?"


def converter_inteiro_para_base_direto(
    numero,
    base_origem,
    base_destino
):
    if not base_valida(base_origem):
        return "Base de origem invalida"

    if not base_valida(base_destino):
        return "Base de destino invalida"

    if not numero_valido(numero, base_origem):
        return "Numero invalido"

    numero = numero.lstrip("0") or "0"

    if numero == "0":
        return "0"

    divisor = converter_base_destino_para_origem(
        base_destino,
        base_origem
    )

    atual = numero
    restos = []

    while atual != "0":
        quociente, resto = dividir_direta(
            atual,
            divisor,
            base_origem
        )

        restos.append(resto)
        atual = quociente

    restos.reverse()

    resultado = ""

    for resto in restos:
        resultado += converter_resto_para_destino(
            resto,
            base_origem,
            base_destino
        )

    return resultado


def converter_fracao(
    numerador,
    denominador,
    base_origem,
    base_destino,
    limite=20
):
    if not base_valida(base_origem):
        return "Base de origem invalida"

    if not base_valida(base_destino):
        return "Base de destino invalida"

    if not numero_valido(numerador, base_origem):
        return "Numerador invalido"

    if not numero_valido(denominador, base_origem):
        return "Denominador invalido"

    if denominador == "0":
        return "Divisao por zero"

    resto = numerador
    digitos = []
    restos = []

    base_na_origem = converter_base_destino_para_origem(
        base_destino,
        base_origem
    )

    for _ in range(limite):
        if resto == "0":
            break

        if resto in restos:
            indice = restos.index(resto)

            return (
                "".join(digitos[:indice])
                + "("
                + "".join(digitos[indice:])
                + ")"
            )

        restos.append(resto)

        resto_multiplicado = multiplicar(
            resto,
            base_na_origem,
            base_origem
        )

        parte_inteira, novo_resto = dividir_direta(
            resto_multiplicado,
            denominador,
            base_origem
        )

        digito = converter_resto_para_destino(
            parte_inteira,
            base_origem,
            base_destino
        )

        digitos.append(digito)
        resto = novo_resto

    if resto in restos:
        indice = restos.index(resto)

        return (
            "".join(digitos[:indice])
            + "("
            + "".join(digitos[indice:])
            + ")"
        )

    return "".join(digitos)


def normalizar(numero, base):
    numero = numero.lstrip("0")

    if numero == "":
        return "0", 0

    expoente = len(numero)
    mantissa = "0." + numero

    return mantissa, expoente


def truncar_mantissa(mantissa, precisao):
    parte = mantissa[2:]
    parte = parte[:precisao]

    return "0." + parte


def arredondar_mantissa(mantissa, precisao, base):
    parte = mantissa[2:]

    if len(parte) <= precisao:
        return mantissa

    mantida = parte[:precisao]
    proximo = valor_do_digito(parte[precisao])

    if proximo >= (base / 2):
        valores = valores_dos_digitos(mantida)

        i = len(valores) - 1

        while i >= 0:
            valores[i] += 1

            if valores[i] < base:
                break

            valores[i] = 0
            i -= 1

        if i < 0:
            mantida = "1" + ("0" * precisao)
        else:
            mantida = "".join(
                digito_do_valor(valor)
                for valor in valores
            )

    return "0." + mantida[:precisao]


def ponto_flutuante(
    numero,
    base,
    precisao,
    metodo="arredondamento"
):
    mantissa, expoente = normalizar(
        numero,
        base
    )

    if metodo == "truncamento":
        mantissa = truncar_mantissa(
            mantissa,
            precisao
        )
    else:
        mantissa = arredondar_mantissa(
            mantissa,
            precisao,
            base
        )

    return mantissa, expoente


def erro_absoluto(valor_exato, valor_aproximado):
    return abs(
        valor_exato - valor_aproximado
    )


def erro_relativo(valor_exato, valor_aproximado):
    if valor_exato == 0:
        return 0

    return erro_absoluto(
        valor_exato,
        valor_aproximado
    ) / abs(valor_exato)


def alinhar_expoentes(
    mantissa1,
    expoente1,
    mantissa2,
    expoente2
):
    if expoente1 == expoente2:
        return (
            mantissa1,
            expoente1,
            mantissa2,
            expoente2
        )

    if expoente1 > expoente2:
        diferenca = expoente1 - expoente2

        mantissa2 = (
            "0."
            + ("0" * diferenca)
            + mantissa2[2:]
        )

        return (
            mantissa1,
            expoente1,
            mantissa2,
            expoente1
        )

    diferenca = expoente2 - expoente1

    mantissa1 = (
        "0."
        + ("0" * diferenca)
        + mantissa1[2:]
    )

    return (
        mantissa1,
        expoente2,
        mantissa2,
        expoente2
    )


def somar_mantissas(
    mantissa1,
    mantissa2,
    base
):
    numero1 = mantissa1[2:]
    numero2 = mantissa2[2:]

    tamanho = max(
        len(numero1),
        len(numero2)
    )

    numero1 = numero1.ljust(tamanho, "0")
    numero2 = numero2.ljust(tamanho, "0")

    resultado = somar(
        numero1,
        numero2,
        base
    )

    return "0." + resultado


def somar_ponto_flutuante(
    mantissa1,
    expoente1,
    mantissa2,
    expoente2,
    base,
    precisao
):
    (
        mantissa1,
        expoente,
        mantissa2,
        expoente
    ) = alinhar_expoentes(
        mantissa1,
        expoente1,
        mantissa2,
        expoente2
    )

    resultado = somar_mantissas(
        mantissa1,
        mantissa2,
        base
    )

    resultado = resultado[2:]

    mantissa_resultado, novo_expoente = normalizar(
        resultado,
        base
    )

    mantissa_resultado = arredondar_mantissa(
        mantissa_resultado,
        precisao,
        base
    )

    return mantissa_resultado, novo_expoente


def subtrair_mantissas(
    mantissa1,
    mantissa2,
    base
):
    numero1 = mantissa1[2:]
    numero2 = mantissa2[2:]

    tamanho = max(
        len(numero1),
        len(numero2)
    )

    numero1 = numero1.ljust(tamanho, "0")
    numero2 = numero2.ljust(tamanho, "0")

    if comparar_numeros(
        numero1,
        numero2
    ) >= 0:
        resultado = subtrair(
            numero1,
            numero2,
            base
        )

        sinal = 1

    else:
        resultado = subtrair(
            numero2,
            numero1,
            base
        )

        sinal = -1

    return "0." + resultado, sinal


def subtrair_ponto_flutuante(
    mantissa1,
    expoente1,
    mantissa2,
    expoente2,
    base,
    precisao
):
    (
        mantissa1,
        expoente,
        mantissa2,
        expoente
    ) = alinhar_expoentes(
        mantissa1,
        expoente1,
        mantissa2,
        expoente2
    )

    resultado, sinal = subtrair_mantissas(
        mantissa1,
        mantissa2,
        base
    )

    resultado = resultado[2:]

    mantissa_resultado, novo_expoente = normalizar(
        resultado,
        base
    )

    mantissa_resultado = arredondar_mantissa(
        mantissa_resultado,
        precisao,
        base
    )

    return (
        sinal,
        mantissa_resultado,
        novo_expoente
    )


def multiplicar_ponto_flutuante(
    mantissa1,
    expoente1,
    mantissa2,
    expoente2,
    base,
    precisao
):
    numero1 = mantissa1[2:]
    numero2 = mantissa2[2:]

    resultado = multiplicar(
        numero1,
        numero2,
        base
    )

    novo_expoente = expoente1 + expoente2

    resultado = resultado.lstrip("0")

    if resultado == "":
        resultado = "0"

    mantissa_resultado, ajuste = normalizar(
        resultado,
        base
    )

    novo_expoente = novo_expoente + ajuste - 1

    mantissa_resultado = arredondar_mantissa(
        mantissa_resultado,
        precisao,
        base
    )

    return (
        mantissa_resultado,
        novo_expoente
    )


def dividir_fracao_direta(
    numero,
    divisor,
    base,
    limite=20
):
    digitos = []
    resto = numero
    restos = []

    base_na_origem = converter_base_destino_para_origem(
        base,
        base
    )

    for _ in range(limite):
        if resto == "0":
            break

        if resto in restos:
            break

        restos.append(resto)

        resto_multiplicado = multiplicar(
            resto,
            base_na_origem,
            base
        )

        parte_inteira, novo_resto = dividir_direta(
            resto_multiplicado,
            divisor,
            base
        )

        digitos.append(parte_inteira)
        resto = novo_resto

    return "".join(digitos)


def dividir_ponto_flutuante(
    mantissa1,
    expoente1,
    mantissa2,
    expoente2,
    base,
    precisao
):
    numero1 = mantissa1[2:]
    numero2 = mantissa2[2:]

    parte_inteira, resto = dividir_direta(
        numero1,
        numero2,
        base
    )

    if resto == "0":
        resultado = parte_inteira

    else:
        parte_fracionaria = dividir_fracao_direta(
            resto,
            numero2,
            base,
            precisao
        )

        resultado = (
            parte_inteira
            + parte_fracionaria
        )

    resultado = resultado.lstrip("0")

    if resultado == "":
        resultado = "0"

    mantissa_resultado, ajuste = normalizar(
        resultado,
        base
    )

    novo_expoente = (
        expoente1
        - expoente2
        + ajuste
    )

    mantissa_resultado = arredondar_mantissa(
        mantissa_resultado,
        precisao,
        base
    )

    return (
        mantissa_resultado,
        novo_expoente
    )


def converter_valor(
    numero,
    base_origem,
    base_destino
):
    if "." in numero:
        parte_inteira, parte_fracionaria = numero.split(".", 1)
    else:
        parte_inteira = numero
        parte_fracionaria = ""

    resultado_inteiro = converter_inteiro_para_base_direto(
        parte_inteira or "0",
        base_origem,
        base_destino
    )

    if parte_fracionaria == "":
        return resultado_inteiro

    denominador = "1"

    for _ in parte_fracionaria:
        denominador = somar(
            denominador,
            "0",
            base_origem
        )

    base_origem_representada = converter_base_destino_para_origem(
        base_origem,
        base_origem
    )

    denominador = "1"

    for _ in range(len(parte_fracionaria)):
        denominador = multiplicar(
            denominador,
            base_origem_representada,
            base_origem
        )

    fracao = converter_fracao(
        parte_fracionaria,
        denominador,
        base_origem,
        base_destino
    )

    if fracao == "":
        return resultado_inteiro

    return resultado_inteiro + "." + fracao


if __name__ == "__main__":
    print(converter_inteiro_para_base_direto("101", 2, 10))
    print(converter_inteiro_para_base_direto("1111", 2, 16))
    print(converter_inteiro_para_base_direto("F", 16, 2))

    print(somar("1021", "112", 3))
    print(somar("123", "234", 5))
    print(somar("1A", "2B", 16))

    print(subtrair("1210", "112", 3))
    print(subtrair("412", "123", 5))
    print(subtrair("45", "1A", 16))

    print(multiplicar("102", "12", 3))
    print(multiplicar("23", "14", 5))
    print(multiplicar("1A", "2", 16))

    print(dividir_direta("110", "10", 2))
    print(dividir_direta("144", "12", 5))
    print(dividir_direta("3C", "4", 16))

    print(dividir_direta("1011", "10", 2))
    print(dividir_direta("123", "4", 5))
    print(dividir_direta("2A", "4", 16))

    print(converter_fracao("7", "10", 10, 3))
    print(converter_fracao("1", "3", 10, 2))