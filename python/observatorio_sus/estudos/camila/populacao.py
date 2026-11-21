"""DEM.1.01 e mortalidade. Transformações derivadas de CP03 com promoção condicionada."""
import argparse
from collections import Counter
from decimal import Decimal
from pathlib import Path

from observatorio_sus.io.custodia import sha256_arquivo
from . import territorio
from .lote import executar, ler, salvar
from .territorio import PAGINAS, TABELA, mapa

ANOS_POPS = {2016, 2018, 2019, 2020, 2021, 2022, 2023}
IDADES_POPS = {str(i) for i in range(81)}
IDADES = {"Menor de 1 ano":0, "01 ano":1, "80 anos e mais":80,
          **{f"{i:02d} anos":i for i in range(2,80)}}
PIN = TABELA.parents[2]/"config/estudos/fontes_taxas_camila.csv"

def integer(raw):
    v=Decimal(raw)
    if not v.is_finite() or v!=v.to_integral_value() or v<0:
        raise ValueError('Contagem populacional incompatível')
    return int(v)

def conferir(entradas, res, regions):
    records={}
    cats={}
    ag=Counter()
    for r in ler(entradas['dem']):
        y,m=int(r['co_anomes'][:4]),r['co_ibge']
        if r['co_anomes'] != f'{y}12' or y not in range(2014, 2025) or m not in regions or r['co_uf']!='32' or r['sg_granularidade']!='MN':
            raise ValueError('DEM: chave de período ou território ausente')
        label=r['ds_item_categoria']
        section=r['sg_categoria']
        if section=='Idade':
            a = IDADES.get(label)
            if a is None:
                raise ValueError(f'Rótulo de idade inválido: {label}')
            k=('IDADE',str(a))
        elif section=='PESSOA1' and label in ('Masculino','Feminino'):
            k=('SEXO','1' if label=='Masculino' else '2')
        elif section=='TC' and label=='Total':
            k=('TOTAL','TODAS')
        else:
            raise ValueError((section,label))
        key=y,m,*k
        if key in records:
            raise ValueError(f'{key}: estrato duplicado')
        v=integer(r['vl_indicador_calculado_mun'])
        records[key]=v
        cats.setdefault((y,m),set()).add(k)
        if k==('TOTAL','TODAS'):
            for t in ('ES',regions[m]):ag[y,t,'TODAS']+=v
        if k[0]=='IDADE' and 30<=int(k[1])<=69:
            a=int(k[1])
            for t in ('ES',regions[m]):
                ag[y,t,'30_69']+=v
                ag[y,t,f'{a//5*5:02d}']+=v
    expected={('TOTAL','TODAS'),('SEXO','1'),('SEXO','2'),*(('IDADE',str(i)) for i in range(81))}
    if len(cats)!=78*11 or any(c!=expected for c in cats.values()):
        raise ValueError('Cobertura DEM.1.01 incompleta')
    consistency=[]
    for y,m in sorted(cats):
        total=records[y,m,'TOTAL','TODAS']
        sumage=sum(records[y,m,'IDADE',str(i)] for i in range(81))
        sumsex=sum(records[y,m,'SEXO',str(i)] for i in (1,2))
        consistency.append((y,m,total,sumage,sumsex,total-sumage,total-sumsex))
    salvar(res/'RIPSA_DEM101_QA_TOTAIS.csv',['ano','datasus6','total','soma_idades','soma_sexos','delta_idade','delta_sexo'],consistency)
    if any(r[-2] or r[-1] for r in consistency):
        raise ValueError('DEM.1.01: divergência entre total municipal e margens de sexo ou idade')
    old=Counter()
    vistos=set()
    ibge={r['cod_municipio_ibge']:r['regiao_nome'] for r in ler(TABELA)}
    for r in ler(entradas['pop']):
        y,m,sex,age,v=int(r['ano']),r['ibge7'][:6],r['sexo'],r['idade_codigo'],integer(r['habitantes'])
        chave = (y, m, sex, age)
        if (y not in ANOS_POPS or r['ibge7'] not in ibge or ibge[r['ibge7']] != r['regiao_pdr_2024']
                or sex not in ('1', '2') or age not in IDADES_POPS or chave in vistos):
            raise ValueError(f'POPSVS: chave incompatível ou duplicada {chave}')
        vistos.add(chave)
        old[y,m,'IDADE',age]+=v
        old[y,m,'SEXO',sex]+=v
        old[y,m,'TOTAL','TODAS']+=v
    details=[(*k,v,records[k],records[k]-v) for k,v in sorted(old.items())]
    salvar(res/'COMPARACAO_POPS_RIPSA_7_ANOS.csv',['ano','datasus6','dominio','estrato','popsvs','dem101','delta_dem101_menos_popsvs'],details)
    if len(vistos)!=len(ANOS_POPS)*78*2*81 or len(details)!=45864 or any(row[-1] for row in details):
        raise ValueError('Margens POPSVS e DEM.1.01 divergentes ou incompletas')
    summary={}
    for y,m,kind,_,previous,current,delta in details:
        counts=summary.setdefault((y,kind),[0,0,0,0])
        counts[0]+=1;counts[1]+=delta==0;counts[2]+=delta;counts[3]+=abs(delta)
    salvar(res/'COMPARACAO_POPS_RIPSA_RESUMO.csv',['ano','dominio','celulas','iguais','soma_delta','soma_delta_absoluto'],
          [(*k,*v) for k,v in sorted(summary.items())])
    salvar(res/'DENOMINADOR_RIPSA_CANDIDATO.csv',['ano','territorio','faixa','habitantes','estado'],
          [(*k,v,'CANDIDATO_FONTE_ALTERNATIVA') for k,v in sorted(ag.items())])
    return ag


def calcular_taxas(entradas, out, ag, anos_cubo):
    pop={(str(y), t, f):v for (y,t,f),v in ag.items()}
    weights={r['idade_inicio'].zfill(2):float(r['peso_30_69']) for r in ler(entradas['pesos'])
             if r['peso_30_69']}
    if set(weights)!={str(a) for a in range(30,70,5)} or abs(sum(weights.values())-1)>1e-12:
        raise ValueError('Pesos quinquenais incompatíveis')
    rates=[]
    for r in ler(entradas['anual']):
        y,t=r['ano'],r['territorio']
        n=int(r['obitos'])
        d=pop[y,t,'TODAS']
        rates.append((y,t,r['grupo'],n,d,f'{n/d*100000:.6f}',r['estado_contagem'],
                      'OFICIAL_DEM101_EQUIVALENCIA_MARGINAL_7_ANOS'))
    strat={}
    for r in ler(entradas['cubo']):
        if r['grupo']=='G0' and r['idade_inicio'] in weights:
            k=r['ano'],r['territorio'],r['idade_inicio']
            strat[k]=strat.get(k,0)+int(r['obitos'])
    prem=[]
    for r in ler(entradas['prematura']):
        y,t=r['ano'],r['territorio']
        n=int(r['obitos'])
        d=pop[y,t,'30_69']
        age=[pop[y,t,x] for x in weights]
        if sum(age)!=d or min(age)<=0:
            raise ValueError(f'Soma do denominador 30–69 incompatível: {y} {t}')
        pad=r['taxa_padronizada_100mil']
        stamp='LEGADO_COM_DENOMINADOR_CONFERIDO' if pad else 'NUMERADORES_QUINQUENAIS_A_RECONSTRUIR'
        if y in anos_cubo:
            if sum(strat.get((y,t,x),0) for x in weights)!=n:
                raise ValueError('Soma do numerador 30–69 incompatível')
            pad=f'{sum(strat.get((y,t,a),0)*w/pop[y,t,a] for a,w in weights.items())*100000:.6f}'
            if r['taxa_padronizada_100mil'] and abs(float(pad)-float(r['taxa_padronizada_100mil']))>1e-6:
                raise ValueError('A taxa padronizada diverge da edição anterior')
            stamp='REPROCESSADO_BRASIL_2010'
        prem.append((y,t,n,d,f'{n/d*100000:.6f}',pad,r['estado_contagem'],stamp,
                     'OFICIAL_DEM101_EQUIVALENCIA_MARGINAL_7_ANOS'))
    esperados={(str(y),t) for y in range(2014,2025) for t in ('ES',*PAGINAS)}
    if (len(rates)!=330 or len(prem)!=55 or {r[:2] for r in prem}!=esperados or
            {r[:3] for r in rates}!={(*k,'G'+str(i)) for k in esperados for i in range(6)}):
        raise ValueError('Janela de taxas incompleta')
    salvar(out/'MORTALIDADE_BRUTA_G0_G5_2014_2024.csv',['ano','territorio','grupo','obitos','populacao','taxa_100mil',
          'estado_numerador','estado_denominador'],rates)
    salvar(out/'MORTALIDADE_PREMATURA_G0_2014_2024.csv',['ano','territorio','obitos_30_69','populacao_30_69','taxa_bruta_100mil',
          'taxa_padronizada_100mil','estado_numerador','estado_padronizacao','estado_denominador'],prem)

    return dict(brutas=len(rates), prematuras=len(prem), estados=dict(Counter(r[7] for r in prem)))


def processar(acervo, destino, dem=None):
    fontes = ler(PIN)
    entradas = {r['id']: acervo/r['membro'] for r in fontes}
    if dem:
        entradas['dem'] = dem
    entradas.update(cadastro=TABELA, contrato_fontes=PIN)

    def calcular(stage):
        ag = conferir(entradas, stage, mapa())
        for r in fontes:
            if sha256_arquivo(entradas[r['id']]) != r['sha256']:
                raise ValueError(f"Edição diferente da série conferida: {r['id']}")
        paridade = ler(entradas['paridade'])
        anos_cubo = {r['ano'] for r in paridade if r['controle']=='regiao_grupo_idade_sexo'
                     and r['diferencas']=='0' and int(r['chaves'])>0}
        if anos_cubo != {'2023','2024'}:
            raise ValueError('Cobertura do cubo intermediário CP02 divergente')
        resultado = calcular_taxas(entradas, stage, ag, anos_cubo)
        return dict(resultado, pares=858, celulas_dem=72072, margens_comuns=45864,
                    cobertura_numerador='CP02, intermediários preservados e legado por ano')
    return executar(destino, entradas, {'unidade':100000, 'arredondamento':6}, calcular,
                    [Path(territorio.__file__)])


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('acervo',type=Path)
    parser.add_argument('saida',type=Path)
    parser.add_argument('--dem',type=Path,help='Edição alternativa para testar a barreira de aceite')
    args=parser.parse_args()
    print(processar(args.acervo,args.saida,args.dem)['controles'])
