def calcular_extra(salario_hora, horas_normais, horas_50, horas_100):
    salario_base = salario_hora * horas_normais
    adicional_50 = salario_hora * 1.5 * horas_50
    adicional_100 = salario_hora * 2 * horas_100
    total_bruto = salario_base + adicional_50 + adicional_100
    return salario_base, adicional_50, adicional_100, total_bruto


def calcular_inss(base):
    faixas = [
        (1412.00, 0.075),
        (2666.68, 0.09),
        (4000.03, 0.12),
        (7786.02, 0.14),
    ]
    inss = 0
    teto = 908.85
    for teto_faixa, aliquota in faixas:
        if base > teto_faixa:
            inss += (teto_faixa - (faixas[faixas.index((teto_faixa, aliquota)) - 1][0] if faixas.index((teto_faixa, aliquota)) > 0 else 0)) * aliquota
        else:
            break

    salario_contribuicao = base
    inss = 0
    faixa_anterior = 0
    for teto_faixa, aliquota in faixas:
        if salario_contribuicao > teto_faixa:
            inss += (teto_faixa - faixa_anterior) * aliquota
        else:
            inss += (salario_contribuicao - faixa_anterior) * aliquota
            break
        faixa_anterior = teto_faixa
    return min(inss, teto)


def calcular_irrf(base, dependentes=0):
    deducao_dependente = 189.59
    base_irrf = base - dependentes * deducao_dependente
    faixas = [
        (2259.20, 0, 0),
        (2826.65, 0.075, 158.40),
        (3751.05, 0.15, 370.40),
        (4664.68, 0.225, 651.73),
        (float("inf"), 0.275, 884.96),
    ]
    for teto, aliquota, deducao in faixas:
        if base_irrf <= teto:
            irrf = base_irrf * aliquota - deducao
            return max(irrf, 0)
    return 0


def exibir_cabecalho():
    print("=" * 50)
    print("          CALCULADORA DE HORAS EXTRAS")
    print("=" * 50)


def obter_float(mensagem):
    while True:
        try:
            return float(input(mensagem).replace(",", "."))
        except ValueError:
            print("  Valor invalido. Digite um numero.")


def obter_int(mensagem):
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("  Valor invalido. Digite um numero inteiro.")


def main():
    exibir_cabecalho()

    salario_hora = obter_float("Salario por hora (R$): ")
    horas_normais = obter_float("Horas normais trabalhadas: ")
    horas_50 = obter_float("Horas extras 50%: ")
    horas_100 = obter_float("Horas extras 100%: ")
    dependentes = obter_int("Numero de dependentes: ")

    salario_base, adicional_50, adicional_100, total_bruto = calcular_extra(
        salario_hora, horas_normais, horas_50, horas_100
    )

    inss = calcular_inss(total_bruto)
    irrf = calcular_irrf(total_bruto - inss, dependentes)
    total_liquido = total_bruto - inss - irrf

    print()
    print("-" * 50)
    print(f"Salario base           R$ {salario_base:>9.2f}")
    print(f"Adicional 50%          R$ {adicional_50:>9.2f}")
    print(f"Adicional 100%         R$ {adicional_100:>9.2f}")
    print("-" * 50)
    print(f"Total Bruto            R$ {total_bruto:>9.2f}")
    print(f"INSS                   R$ {inss:>9.2f}")
    print(f"IRRF                   R$ {irrf:>9.2f}")
    print("=" * 50)
    print(f"Total Liquido          R$ {total_liquido:>9.2f}")
    print("=" * 50)


if __name__ == "__main__":
    main()
