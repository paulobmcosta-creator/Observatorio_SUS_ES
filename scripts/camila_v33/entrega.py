"""Monta em temporário, valida e sela a entrega v3.3 em armazenamento local."""
import os
import tempfile
import platform
from comum import *
from documentar import documentar
from visuais import executar
from conferir_edicao import conferir

def hashes(pasta):
    return {p.relative_to(pasta).as_posix():sha(p) for p in sorted(pasta.rglob('*')) if p.is_file()}

def main():
    a=Acervo()
    final=a.e
    if final.exists(): raise FileExistsError('Edição já existente. Use outro --destino para reprodução.')
    cp=a.w/'checkpoint-B'
    rec=json.loads((cp/'recibo.json').read_text(encoding='utf8'))
    for nome,h in rec['arquivos'].items():
        assert sha(cp/nome)==h
    anterior=hashes(a.b)
    assert len(anterior)==295
    with tempfile.TemporaryDirectory(prefix='edicao-',dir=a.w) as tmp:
        a.e=Path(tmp)/'v33'
        a.r=a.e/'08_REPRODUTIBILIDADE'
        a.tab=a.e/'02_TABELAS'
        shutil.copytree(a.b,a.e)
        recibos=a.r/'recibos'
        recibos.mkdir()
        for n in ['recibo.json','controles.json']:
            (a.e/n).rename(recibos/('base_v321_'+n))
        # A lista de hashes dos visuais v3.2.1 refere-se à edição anterior.
        (a.r/'validacao_visuais.csv').rename(recibos/'visuais_v321.csv')
        for sigla in ['A','B']:
            shutil.copyfile(a.w/('checkpoint-'+sigla)/'recibo.json',recibos/('checkpoint-'+sigla+'.json'))
        testes=a.r/'testes'
        testes.mkdir()
        shutil.copyfile(cp/'contraprovas.csv',testes/'contraprovas_quantitativas.csv')
        for p in ['testes-python.log','testes-python-validado.log']:
            shutil.copyfile(a.w/p,testes/p)
        for codigo in Path(__file__).parent.glob('*.py'):
            dest=a.r/'scripts_v33'/codigo.name
            dest.parent.mkdir(exist_ok=True)
            shutil.copyfile(codigo,dest)
        src=a.p/'mandato-v3.2/fontes/municipios-es.geojson'
        json_out(recibos/'ambiente_v33.json',{'python':platform.python_version(),'pandas':pd.__version__,'numpy':np.__version__,'malha_municipal_sha256':sha(src),'pdr_sha256':sha(REPO/'metadata/territorio/pdr_es_2024_tcc_v1.csv'),'edicao_base_sha256':sha(a.f/(a.b.name+'.zip')),'manuscrito_v4_sha256':sha(a.doc),'agregados_sih':3564,'dependencia_cartografia':'Shapely 2.1.2','tolerancia_absoluta':1e-7})
        figs=executar(a)
        inv=documentar(a,figs)
        testes_fig=conferir(a,figs,inv)
        gravar(testes_fig,testes/'matriz_e_visuais.csv')
        imagens=[]
        for r in inv[inv.tipo.isin(['Gráfico','Mapa'])].itertuples():
            svg=a.e/r.figura
            imagens.append((r.id,sha(a.e/r.tabela),sha(svg),sha(svg.with_suffix('.png'))))
        gravar(pd.DataFrame(imagens,columns=['id','sha256_csv','sha256_svg','sha256_png']),a.r/'validacao_visuais.csv')
        nota(a.r/'indice_scripts.md','''# Reprodução dos checkpoints

Use o checkout da branch do TCC e o ambiente Python analítico com pandas, NumPy, DuckDB, Matplotlib, Pillow e Shapely 2.1.2. Acrescente a pasta python do checkout ao PYTHONPATH. As cópias de scripts_v33 correspondem a scripts/camila_v33 do checkout. Execute os módulos usando o Python desse ambiente, passando dois argumentos posicionais, raiz da custódia SIM e pasta privada dos documentos. A opção --destino seleciona outra raiz de trabalho vazia para todos os módulos. Use a mesma raiz em todos os comandos.

1. diagnostico.py compara os produtos com os ZIPs selados, lê o manuscrito e produz o checkpoint A.
2. hospital.py, oferta.py e mortalidade.py produzem os agregados novos do checkpoint B. hospital.py lê os CSVs analíticos certificados de cada partição.
3. integracao.py completa SIH, fluxos e matriz larga/longa. validar.py roda a contraprova das tabelas finais e sela o checkpoint B.
4. Para reproduzir a suíte, use o ambiente de testes homologado venv-testes-v32, com seu Scripts no início do PATH e PYTHONUTF8=1. Os logs da execução inicial com ambiente incompleto e da verificação conclusiva são evidências externas copiadas para a pasta testes. Para uma nova reprodução da entrega, reutilize esses logs documentais no diretório de trabalho como testes-python.log e testes-python-validado.log.
5. entrega.py usa documentar.py, visuais.py e conferir_edicao.py. Monta a edição em diretório temporário e promove o resultado após conferir os produtos. empacotar.py relê cada arquivo do ZIP acadêmico e do ZIP restrito de auditoria.

A tabela comparacao_v321_v33.csv compara os produtos substantivos presentes antes do próprio confronto. O manifesto completo verifica todos os bytes da edição exceto o próprio manifesto. Os hashes dos ZIPs são externos. As entradas privadas e os controles completos dos checkpoints acompanham o ZIP de auditoria.''')
        old=anterior
        new=hashes(a.e)
        dif=pd.DataFrame([(n,old.get(n,''),new.get(n,''),'preservado' if old.get(n)==new.get(n) else ('acrescentado' if n not in old else ('realocado' if n not in new else 'atualizado'))) for n in sorted(set(old)|set(new))],columns=['arquivo','sha256_v321','sha256_v33','situacao'])
        quant=[n for n in old if n.startswith(('01_BASES_E_INDICADORES/','02_TABELAS/'))]
        assert all(old[n]==new[n] for n in quant) and len(quant)==28
        gravar(dif,a.r/'comparacao_v321_v33.csv')
        json_out(a.e/'recibo.json',{'edicao':'v3.3','tabelas_analiticas_base_preservadas':len(quant),'matriz_ano_territorio':77,'controles_quantitativos':rec['testes'],'comparacoes_checkpoint_B':rec['comparacoes'],'testes_matriz_visuais':testes_fig.to_dict('records'),'sha256_checkpoint_B':sha(cp/'recibo.json'),'sha256_base_original':sha(a.f/(a.b.name+'.zip')),'figuras_acrescentadas':9,'mapas_regionais_revistas':['M02']})
        gravar(pd.DataFrame(hashes(a.e).items(),columns=['caminho','sha256']),a.r/'manifesto_sha256.csv')
        assert hashes(a.b)==anterior
        a.e.rename(final)
    print(final)
if __name__=='__main__':main()
