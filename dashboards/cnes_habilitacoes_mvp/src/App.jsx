import { useEffect, useMemo, useState } from "react";
import {
  ALL,
  MAP_METRICS,
  deriveViewModel,
  metricValue,
  metricBand,
  mapViewBox,
  validateDataContract,
  exportRecordsCsv,
} from "./metrics.js";

const formatInteger = new Intl.NumberFormat("pt-BR");
const formatPercent = new Intl.NumberFormat("pt-BR", {
  minimumFractionDigits: 1,
  maximumFractionDigits: 1,
});
const formatDate = new Intl.DateTimeFormat("pt-BR", { timeZone: "UTC" });

function formatMetric(value, metric) {
  if (value === null || value === undefined) return "—";
  if (metric === "validationRate") return `${formatPercent.format(value)}%`;
  return formatInteger.format(value);
}

const MAP_COLORS = ["#e7ebed", "#d3ebe5", "#92c9c3", "#4e9ca2", "#0b666b"];

function mapLegend(metric) {
  return metric === "validationRate"
    ? ["Sem registros", "< 25%", "25%–49,9%", "50%–74,9%", "≥ 75%"]
    : ["Sem registros", "1–2", "3–5", "6–10", "≥ 11"];
}

function KpiCard({ value, label, accent }) {
  return (
    <article className={`kpi ${accent ? "kpi-accent" : ""}`}>
      <span className="kpi-rule" aria-hidden="true" />
      <strong>{value}</strong>
      <span>{label}</span>
    </article>
  );
}

function Filter({ id, label, value, onChange, children }) {
  return (
    <label className="filter" htmlFor={id}>
      <span>{label}</span>
      <select id={id} value={value} onChange={(event) => onChange(event.target.value)}>
        {children}
      </select>
    </label>
  );
}

function MapPanel({ municipalities, metric, selectedMunicipality, onSelectMunicipality }) {
  const [hovered, setHovered] = useState(null);
  const [fullExtent, setFullExtent] = useState(false);
  const viewBox = useMemo(() => mapViewBox(municipalities, fullExtent), [municipalities, fullExtent]);
  const focus = hovered ?? (selectedMunicipality === ALL ? null : selectedMunicipality);
  const focusMunicipality = municipalities.find((municipality) => municipality.codigo === focus);
  const focusValue = focusMunicipality ? metricValue(focusMunicipality, metric) : null;

  return (
    <section className="panel map-panel" aria-labelledby="map-title">
      <div className="panel-heading">
        <div>
          <p className="eyebrow">Distribuição territorial</p>
          <h2 id="map-title">{MAP_METRICS[metric].label} por município</h2>
        </div>
        <button type="button" className="reset-button" aria-pressed={fullExtent} onClick={() => setFullExtent((v) => !v)}>{fullExtent ? "Ampliar área continental" : "Ver extensão completa"}</button>
      </div>
      <div className="map-layout">
        <svg className="state-map" viewBox={viewBox} role="img" aria-label={`Mapa municipal do Espírito Santo: ${MAP_METRICS[metric].label}`}>
          {municipalities.map((municipality) => {
            const value = metricValue(municipality, metric);
            const selected = selectedMunicipality === municipality.codigo;
            return (
              <path
                key={municipality.codigo}
                d={municipality.path}
                fill={MAP_COLORS[metricBand(value, metric)]}
                fillRule="evenodd"
                className={selected ? "map-shape map-shape-selected" : "map-shape"}
                tabIndex="0"
                aria-label={`${municipality.nome}: ${formatMetric(value, metric)} ${MAP_METRICS[metric].short}`}
                onMouseEnter={() => setHovered(municipality.codigo)}
                onMouseLeave={() => setHovered(null)}
                onFocus={() => setHovered(municipality.codigo)}
                onBlur={() => setHovered(null)}
                onClick={() => onSelectMunicipality(selected ? ALL : municipality.codigo)}
                onKeyDown={(event) => {
                  if (event.key === "Enter" || event.key === " ") {
                    event.preventDefault();
                    onSelectMunicipality(selected ? ALL : municipality.codigo);
                  }
                }}
              >
                <title>{`${municipality.nome}: ${formatMetric(value, metric)} ${MAP_METRICS[metric].short}`}</title>
              </path>
            );
          })}
        </svg>
        <div className="map-aside">
          <div className="map-legend" aria-label="Legenda do mapa">
            {mapLegend(metric).map((label, index) => (
              <div key={label}>
                <span style={{ background: MAP_COLORS[index] }} aria-hidden="true" />
                <small>{label}</small>
              </div>
            ))}
          </div>
          <div className="map-detail" aria-live="polite">
            {focusMunicipality ? (
              <>
                <p>{focusMunicipality.nome}</p>
                <strong>{formatMetric(focusValue, metric)}</strong>
                <span>{MAP_METRICS[metric].short}</span>
                <dl>
                  <div><dt>Validados</dt><dd>{formatInteger.format(focusMunicipality.validatedRecords)}</dd></div>
                  <div><dt>Revisar</dt><dd>{formatInteger.format(focusMunicipality.reviewRecords)}</dd></div>
                </dl>
              </>
            ) : (
              <>
                <p>Explore o mapa</p>
                <strong>{municipalities.length}</strong>
                <span>municípios do ES</span>
                <small>Passe o cursor ou selecione um município.</small>
              </>
            )}
          </div>
        </div>
      </div>
      <p className="panel-note">{fullExtent ? "Extensão completa, incluindo ilhas afastadas." : "Área continental em destaque; extensão completa disponível."} O enquadramento não altera contagens. Cinza significa “sem registros no subconjunto filtrado”; não significa zero de oferta assistencial.</p>
    </section>
  );
}

function LinesPanel({ stats }) {
  const max = Math.max(1, ...stats.map((item) => item.selectedRecords));
  return (
    <section className="panel lines-panel" aria-labelledby="lines-title">
      <div className="panel-heading">
        <div><p className="eyebrow">Comparação temática</p><h2 id="lines-title">Registros por linha de cuidado</h2></div>
        <div className="mini-legend"><span><i className="dot valid" />Validado</span><span><i className="dot review" />Revisar</span></div>
      </div>
      <div className="bar-chart">
        {stats.map((item) => (
          <div className="bar-row" key={item.name}>
            <span className="bar-label" title={item.name}>{item.name}</span>
            <div className="bar-track" aria-label={`${item.name}: ${item.validatedRecords} validados e ${item.reviewRecords} a revisar`}>
              <span className="bar-segment bar-valid" style={{ width: `${(100 * item.validatedRecords) / max}%` }}>{item.validatedRecords > 8 ? item.validatedRecords : ""}</span>
              <span className="bar-segment bar-review" style={{ width: `${(100 * item.reviewRecords) / max}%` }}>{item.reviewRecords > 8 ? item.reviewRecords : ""}</span>
            </div>
            <strong>{item.selectedRecords}</strong>
          </div>
        ))}
      </div>
      <p className="panel-note">Contagem de chaves de registro; não representa volume de procedimentos.</p>
    </section>
  );
}

function RegionsPanel({ stats }) {
  const max = Math.max(1, ...stats.map((item) => item.selectedRecords));
  return (
    <section className="panel region-panel" aria-labelledby="region-title">
      <div className="panel-heading">
        <div><p className="eyebrow">Comparação territorial</p><h2 id="region-title">Regiões geográficas intermediárias</h2></div>
        <span className="source-tag">IBGE</span>
      </div>
      <div className="region-grid">
        {stats.map((item) => (
          <article key={item.name}>
            <div className="region-name">{item.name}</div>
            <strong>{formatInteger.format(item.selectedRecords)}</strong>
            <span>registros</span>
            <div className="region-track"><span style={{ width: `${(100 * item.selectedRecords) / max}%` }} /></div>
            <small>{formatInteger.format(item.distinctEstablishments)} estabelecimentos • {item.validationRate === null ? "—" : `${formatPercent.format(item.validationRate)}%`} validados</small>
          </article>
        ))}
      </div>
      <p className="panel-note">Recorte geográfico do IBGE; não corresponde às regiões de saúde do Espírito Santo.</p>
    </section>
  );
}

function RankingPanel({ ranking }) {
  return (
    <section className="panel ranking-panel" aria-labelledby="ranking-title">
      <div className="panel-heading"><div><p className="eyebrow">Leitura municipal</p><h2 id="ranking-title">Municípios com maiores contagens</h2></div></div>
      <div className="table-scroll">
        <table>
          <thead><tr><th>Município</th><th>Registros</th><th>Estab.</th><th>% validado</th></tr></thead>
          <tbody>
            {ranking.map((item) => (
              <tr key={item.codigo}>
                <td>{item.nome}</td>
                <td>{formatInteger.format(item.selectedRecords)}</td>
                <td>{formatInteger.format(item.distinctEstablishments)}</td>
                <td>{item.validationRate === null ? "—" : `${formatPercent.format(item.validationRate)}%`}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      <p className="panel-note">Ordenação por registros, sem ajuste por população, necessidade ou porte da rede.</p>
    </section>
  );
}

export default function App() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [status, setStatus] = useState(ALL);
  const [line, setLine] = useState(ALL);
  const [region, setRegion] = useState(ALL);
  const [municipality, setMunicipality] = useState(ALL);
  const [metric, setMetric] = useState("selectedRecords");

  useEffect(() => {
    let active = true;
    fetch("./data/mvp-data.json")
      .then((response) => {
        if (!response.ok) throw new Error("A base local do painel ainda não está disponível neste ambiente.");
        return response.json();
      })
      .then((payload) => active && setData(validateDataContract(payload)))
      .catch((reason) => active && setError(reason.message));
    return () => { active = false; };
  }, []);

  const filters = useMemo(() => ({ status, line, region, municipality }), [status, line, region, municipality]);
  const view = useMemo(() => (data ? deriveViewModel(data, filters) : null), [data, filters]);
  const municipalityOptions = useMemo(
    () => data?.municipios.filter((item) => region === ALL || item.regiaoIntermediaria === region) ?? [],
    [data, region],
  );

  function changeRegion(value) {
    setRegion(value);
    if (value !== ALL) {
      const selected = data?.municipios.find((item) => item.codigo === municipality);
      if (selected && selected.regiaoIntermediaria !== value) setMunicipality(ALL);
    }
  }

  function clearFilters() {
    setStatus(ALL);
    setLine(ALL);
    setRegion(ALL);
    setMunicipality(ALL);
    setMetric("selectedRecords");
  }

  function exportFiltered() {
    const url = URL.createObjectURL(new Blob([exportRecordsCsv(view.selected)], { type: "text/csv;charset=utf-8" }));
    const link = document.createElement("a");
    link.href = url;
    link.download = `cnes_habilitacoes_filtrado_${data.metadata.competencia}.csv`;
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 0);
  }

  if (error) return <main className="load-state"><h1>Falha ao carregar o MVP</h1><p>{error}</p></main>;
  if (!data || !view) return <main className="load-state"><p>Carregando base validada…</p></main>;
  const summary = view.global;

  return (
    <>
      <header className="app-header">
        <div className="header-inner">
          <div><span className="brand-mark" aria-hidden="true">OS</span><div><p>Observatório SUS-ES</p><h1>Habilitações estratégicas CNES</h1></div></div>
          <div className="header-meta"><span>Oferta cadastrada</span><strong>competência {data.metadata.competenciaRotulo}</strong></div>
        </div>
      </header>

      <main className="dashboard">
        <section className="intro-row">
          <div><p className="eyebrow">Candidata V2 • não homologada</p><h2>Registros estratégicos do CNES por território</h2><p>Um único subconjunto filtrado alimenta cartões, comparações, mapa e tabela.</p></div>
          <div className="panel-actions"><button type="button" className="reset-button" onClick={exportFiltered}>Exportar CSV filtrado</button><button type="button" className="reset-button" onClick={clearFilters}>Limpar filtros</button></div>
        </section>

        <aside className="baseline-status">
          <strong>Base exibida:</strong> {formatInteger.format(data.resumoCanonico.selectedRecords)} chaves linha a linha do pacote fornecido. A reconciliação com agregados alternativos permanece pendente de dataset versionado.
        </aside>

        <section className="filters" aria-label="Filtros do painel">
          <Filter id="validation" label="Situação de revisão interna" value={status} onChange={setStatus}>
            <option>{ALL}</option>{data.dominios.status.map((item) => <option key={item}>{item}</option>)}
          </Filter>
          <Filter id="line" label="Linha de cuidado" value={line} onChange={setLine}>
            <option>{ALL}</option>{data.dominios.linhas.map((item) => <option key={item}>{item}</option>)}
          </Filter>
          <Filter id="region" label="Região intermediária IBGE" value={region} onChange={changeRegion}>
            <option>{ALL}</option>{data.dominios.regioesIntermediarias.map((item) => <option key={item}>{item}</option>)}
          </Filter>
          <Filter id="municipality" label="Município" value={municipality} onChange={setMunicipality}>
            <option value={ALL}>{ALL}</option>{municipalityOptions.map((item) => <option key={item.codigo} value={item.codigo}>{item.nome}</option>)}
          </Filter>
          <Filter id="metric" label="Métrica do mapa" value={metric} onChange={setMetric}>
            {Object.entries(MAP_METRICS).map(([key, item]) => <option key={key} value={key}>{item.label}</option>)}
          </Filter>
        </section>

        <section className="kpi-grid" aria-label="Indicadores principais">
          <KpiCard value={formatInteger.format(summary.selectedRecords)} label="registros de habilitação" />
          <KpiCard value={formatInteger.format(summary.distinctEstablishments)} label="estabelecimentos distintos (CNES)" />
          <KpiCard value={formatInteger.format(summary.distinctMunicipalities)} label="municípios com registro" />
          <KpiCard value={formatInteger.format(summary.distinctQualificationTypes)} label="tipos (código + tipo)" />
          <KpiCard value={summary.validationRate === null ? "—" : `${formatPercent.format(summary.validationRate)}%`} label="registros validados" accent />
        </section>

        <aside className="method-alert">
          <span className="alert-icon" aria-hidden="true">!</span>
          <p><strong>{formatInteger.format(summary.validatedRecords)} com status interno Validado • {formatInteger.format(summary.reviewRecords)} sob revisão.</strong> Classificação interna do projeto, sem homologação normativa. Cadastro não comprova funcionamento, produção, acesso ou suficiência.</p>
        </aside>

        <div className="primary-grid">
          <MapPanel municipalities={view.byMunicipality} metric={metric} selectedMunicipality={municipality} onSelectMunicipality={setMunicipality} />
          <LinesPanel stats={view.byCareLine} />
        </div>
        <div className="secondary-grid">
          <RegionsPanel stats={view.byIntermediateRegion} />
          <RankingPanel ranking={view.ranking} />
        </div>

        <section className="methodology" aria-labelledby="methodology-title">
          <div><p className="eyebrow">Como ler este MVP</p><h2 id="methodology-title">Escopo e rastreabilidade</h2></div>
          <div className="methodology-grid">
            <article><strong>Fonte</strong><p>CNES/MS, instantâneo {data.metadata.competencia} processado no repositório coletivo.</p></article>
            <article><strong>Recorte</strong><p><code>usar_observatorio = Sim</code>; Validado e Revisar permanecem visíveis.</p></article>
            <article><strong>Território</strong><p>Malha e regiões geográficas intermediárias do IBGE; região de saúde indisponível até validação documental. Município gestor não comprova localização física.</p></article>
            <article><strong>Limite</strong><p>Instantâneo cadastral, sem população, produção assistencial, qualidade ou desfechos.</p></article>
          </div>
        </section>
      </main>

      <footer>
        <div><strong>Observatório SUS-ES • MVP técnico v2</strong><span>Gerado em {formatDate.format(new Date(`${data.metadata.geradoEm}T00:00:00Z`))}</span></div>
        <p>Fonte: CNES/MS e IBGE. Metodologia, dicionário, testes e hashes acompanham o pacote.</p>
      </footer>
    </>
  );
}
