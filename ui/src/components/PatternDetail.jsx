import React, { useEffect, useState, useRef } from 'react';
import { ArrowLeft, FileText, Code, Link2, Tag, AlertTriangle, Loader, GitBranch, Play, Wand2, Zap } from 'lucide-react';
import SimulationNotebook from './SimulationNotebook';

const API_BASE = 'http://127.0.0.1:8000';

const DOMAIN_COLORS = {
  defi: '#58a6ff',
  security: '#ff7b72',
  economics: '#d2a8ff',
  infrastructure: '#a5d6ff',
  governance: '#ffa657',
  mev: '#f0883e',
};

const SEVERITY_MAP = {
  critical: 'severity-critical',
  high: 'severity-high',
  medium: 'severity-medium',
  low: 'severity-low',
  informational: 'severity-informational',
};

function ChipList({ items, color }) {
  if (!items || items.length === 0) return null;
  return (
    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
      {items.map((item, i) => (
        <span
          key={i}
          style={{
            display: 'inline-block',
            padding: '3px 10px',
            borderRadius: '10px',
            fontSize: '0.75rem',
            fontWeight: 600,
            background: `${color}18`,
            color: color,
            border: `1px solid ${color}40`,
          }}
        >
          {item}
        </span>
      ))}
    </div>
  );
}

// Mermaid diagram renderer
function MermaidDiagram({ diagram, index }) {
  const containerRef = useRef(null);
  const [svg, setSvg] = useState('');
  const [error, setError] = useState(null);

  useEffect(() => {
    if (!diagram?.mermaid) return;

    const renderDiagram = async () => {
      try {
        // Dynamically load mermaid if not loaded
        if (!window.mermaid) {
          const script = document.createElement('script');
          script.src = 'https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.min.js';
          script.onload = () => {
            window.mermaid.initialize({
              startOnLoad: false,
              theme: 'dark',
              themeVariables: {
                primaryColor: '#58a6ff',
                primaryTextColor: '#c9d1d9',
                primaryBorderColor: '#30363d',
                lineColor: '#8b949e',
                secondaryColor: '#161b22',
                tertiaryColor: '#0d1117',
                background: '#0d1117',
                mainBkg: '#161b22',
                nodeBorder: '#30363d',
                clusterBkg: '#161b2280',
                clusterBorder: '#30363d',
                titleColor: '#c9d1d9',
                edgeLabelBackground: '#0d1117',
                fontSize: '14px',
              },
            });
            doRender();
          };
          document.head.appendChild(script);
        } else {
          doRender();
        }

        async function doRender() {
          try {
            const id = `mermaid-${index}-${Date.now()}`;
            const { svg: renderedSvg } = await window.mermaid.render(id, diagram.mermaid);
            setSvg(renderedSvg);
          } catch (e) {
            console.error('Mermaid render error:', e);
            setError(e.message || 'Failed to render diagram');
          }
        }
      } catch (e) {
        setError(e.message);
      }
    };

    renderDiagram();
  }, [diagram, index]);

  return (
    <div className="glass-panel" style={{ marginBottom: '1rem' }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
        <GitBranch size={15} style={{ color: '#58a6ff' }} />
        <h4 style={{ margin: 0, fontSize: '0.95rem', fontWeight: 600 }}>{diagram.title}</h4>
        <span style={{ fontSize: '0.7rem', color: 'var(--text-secondary)', marginLeft: 'auto' }}>{diagram.type}</span>
      </div>

      {error ? (
        <div style={{ padding: '1rem', background: '#161b22', borderRadius: '8px', fontSize: '0.8rem' }}>
          <div style={{ color: '#ff7b72', marginBottom: '0.5rem' }}>Diagram render error: {error}</div>
          <pre style={{ color: '#8b949e', margin: 0, fontSize: '0.75rem', whiteSpace: 'pre-wrap' }}>
            {diagram.mermaid}
          </pre>
        </div>
      ) : svg ? (
        <div
          ref={containerRef}
          dangerouslySetInnerHTML={{ __html: svg }}
          style={{
            background: '#0d1117',
            borderRadius: '8px',
            padding: '1rem',
            display: 'flex',
            justifyContent: 'center',
            overflow: 'auto',
          }}
        />
      ) : (
        <div style={{ padding: '2rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
          <Loader size={16} style={{ animation: 'spin 1s linear infinite', marginRight: '0.5rem' }} />
          Rendering diagram...
        </div>
      )}
    </div>
  );
}


export default function PatternDetail({ slug, onBack }) {
  const [data, setData] = useState(null);
  const [content, setContent] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [generating, setGenerating] = useState(false);
  const [showVideoScript, setShowVideoScript] = useState(false);
  const [expandedEntry, setExpandedEntry] = useState(null);
  const [entryLoading, setEntryLoading] = useState(false);

  const fetchEntry = (entryId) => {
    if (expandedEntry?.id === entryId) {
      setExpandedEntry(null);
      return;
    }
    setEntryLoading(true);
    fetch(`${API_BASE}/api/corpus/${entryId}`)
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(entry => {
        setExpandedEntry(entry);
        setEntryLoading(false);
      })
      .catch(() => {
        setEntryLoading(false);
      });
  };

  useEffect(() => {
    if (!slug) return;
    setLoading(true);
    setError(null);

    Promise.all([
      fetch(`${API_BASE}/api/library/patterns/${slug}`).then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      }),
      fetch(`${API_BASE}/api/content/${slug}`).then(r => r.ok ? r.json() : null).catch(() => null),
    ])
      .then(([patternData, contentData]) => {
        setData(patternData);
        setContent(contentData);
        setLoading(false);
      })
      .catch(e => {
        console.error(e);
        setError(e.message);
        setLoading(false);
      });
  }, [slug]);

  const handleGenerate = () => {
    setGenerating(true);
    fetch(`${API_BASE}/api/content/${slug}/generate`, { method: 'POST' })
      .then(r => r.json())
      .then(() => {
        // Refetch content
        fetch(`${API_BASE}/api/content/${slug}`)
          .then(r => r.ok ? r.json() : null)
          .then(data => {
            setContent(data);
            setGenerating(false);
          });
      })
      .catch(() => setGenerating(false));
  };

  if (loading) {
    return (
      <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
        <Loader size={28} style={{ marginBottom: '1rem', opacity: 0.5, animation: 'spin 1s linear infinite' }} />
        <div>Loading pattern…</div>
        <style>{`@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}</style>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '3rem' }}>
        <button onClick={onBack} style={backBtnStyle}>
          <ArrowLeft size={16} /> Back to Library
        </button>
        <div style={{ marginTop: '2rem', color: 'var(--critical)', textAlign: 'center' }}>
          Failed to load pattern: {error}
        </div>
      </div>
    );
  }

  const { pattern, synthesis, related_entries, contract_source, severity_profile } = data;
  const domainColor = DOMAIN_COLORS[pattern?.domain] || 'var(--primary)';
  const hasDiagrams = content?.diagrams && content.diagrams.length > 0;
  const hasVideoScript = content?.video_script;
  const hasSimulation = content?.simulation && content.simulation.steps?.length > 0;

  const SEV_COLORS = { Critical: '#ff4757', High: '#ff6b6b', Medium: '#ffa502', Low: '#2ed573', Informational: '#54a0ff', Gas: '#a4b0be', Unknown: '#636e72' };
  const SEV_ORDER = ['Critical', 'High', 'Medium', 'Low', 'Informational', 'Gas'];

  return (
    <div className="animate-fade-in" style={{ maxWidth: hasSimulation ? '1400px' : '900px' }}>
      {/* Back Button */}
      <button onClick={onBack} style={backBtnStyle}>
        <ArrowLeft size={16} /> Back to Library
      </button>

      {/* Title + Domain Badge */}
      <div style={{ marginTop: '1.5rem', marginBottom: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', flexWrap: 'wrap' }}>
          <h1 style={{ margin: 0, fontSize: '1.75rem', fontWeight: 700, color: 'var(--text-primary)' }}>
            {pattern?.title}
          </h1>
          <span style={{
            display: 'inline-block',
            padding: '3px 12px',
            borderRadius: '12px',
            fontSize: '0.75rem',
            fontWeight: 600,
            background: `${domainColor}22`,
            color: domainColor,
            border: `1px solid ${domainColor}44`,
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
          }}>
            {pattern?.domain}
          </span>
        </div>
      </div>

      {/* Description */}
      <p style={{
        color: 'var(--text-secondary)',
        fontSize: '1rem',
        lineHeight: 1.7,
        marginBottom: '1.5rem',
      }}>
        {pattern?.description}
      </p>

      {/* TWO-COLUMN LAYOUT */}
      <div style={{
        display: hasSimulation ? 'grid' : 'block',
        gridTemplateColumns: hasSimulation ? '1fr 420px' : '1fr',
        gap: '1.5rem',
        alignItems: 'start',
      }}>

      {/* LEFT COLUMN — Main Content */}
      <div>

      {/* Severity Threat Profile */}
      {severity_profile && severity_profile.total > 0 && (
        <div className="glass-panel" style={{
          marginBottom: '1.5rem',
          borderLeft: `3px solid ${severity_profile.critical_ratio >= 0.5 ? '#ff4757' : severity_profile.critical_ratio >= 0.3 ? '#ffa502' : '#2ed573'}`,
        }}>
          <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.75rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <AlertTriangle size={16} style={{ color: severity_profile.critical_ratio >= 0.5 ? '#ff4757' : '#ffa502' }} />
              <span style={{ fontWeight: 700, fontSize: '0.9rem' }}>Threat Profile</span>
            </div>
            <div style={{
              padding: '3px 10px',
              borderRadius: '10px',
              fontSize: '0.75rem',
              fontWeight: 700,
              background: severity_profile.critical_ratio >= 0.5 ? '#ff475722' : severity_profile.critical_ratio >= 0.3 ? '#ffa50222' : '#2ed57322',
              color: severity_profile.critical_ratio >= 0.5 ? '#ff4757' : severity_profile.critical_ratio >= 0.3 ? '#ffa502' : '#2ed573',
              border: `1px solid ${severity_profile.critical_ratio >= 0.5 ? '#ff475744' : severity_profile.critical_ratio >= 0.3 ? '#ffa50244' : '#2ed57344'}`,
            }}>
              {Math.round(severity_profile.critical_ratio * 100)}% Critical/High
            </div>
          </div>

          {/* Severity bar */}
          <div style={{ display: 'flex', height: '8px', borderRadius: '4px', overflow: 'hidden', marginBottom: '0.75rem' }}>
            {SEV_ORDER.map(sev => {
              const count = severity_profile.counts[sev] || 0;
              if (count === 0) return null;
              const pct = (count / severity_profile.total) * 100;
              return (
                <div key={sev} style={{
                  width: `${pct}%`,
                  background: SEV_COLORS[sev],
                  transition: 'width 0.4s ease',
                }} title={`${sev}: ${count}`} />
              );
            })}
          </div>

          {/* Severity legend */}
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.75rem', fontSize: '0.78rem' }}>
            {SEV_ORDER.map(sev => {
              const count = severity_profile.counts[sev] || 0;
              if (count === 0) return null;
              return (
                <span key={sev} style={{ display: 'flex', alignItems: 'center', gap: '0.3rem', color: 'var(--text-secondary)' }}>
                  <span style={{ width: 8, height: 8, borderRadius: '50%', background: SEV_COLORS[sev], display: 'inline-block' }} />
                  <strong style={{ color: SEV_COLORS[sev] }}>{count}</strong> {sev}
                </span>
              );
            })}
            <span style={{ marginLeft: 'auto', color: 'var(--text-secondary)' }}>
              {severity_profile.total} related findings
            </span>
          </div>
        </div>
      )}

      {/* Generate Content Button */}
      {synthesis && (!hasDiagrams || !hasVideoScript) && (
        <button
          className="btn"
          onClick={handleGenerate}
          disabled={generating}
          style={{
            display: 'inline-flex', alignItems: 'center', gap: '0.5rem',
            marginBottom: '1.5rem',
            opacity: generating ? 0.7 : 1,
          }}
        >
          {generating ? (
            <>
              <Loader size={14} style={{ animation: 'spin 1s linear infinite' }} />
              Generating diagrams & video script…
            </>
          ) : (
            <>
              <Wand2 size={14} />
              Generate Diagrams & Video Script
            </>
          )}
        </button>
      )}

      {/* Diagrams Section */}
      {hasDiagrams && (
        <div style={{ marginBottom: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
            <GitBranch size={18} style={{ color: 'var(--primary)' }} />
            <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 700 }}>Diagrams</h3>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
              {content.diagrams.length} diagram{content.diagrams.length !== 1 ? 's' : ''}
            </span>
          </div>

          {content.diagrams.map((diag, i) => (
            <MermaidDiagram key={i} diagram={diag} index={i} />
          ))}
        </div>
      )}

      {/* Synthesis Section */}
      {synthesis ? (
        <div className="glass-panel" style={{ marginBottom: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1.25rem' }}>
            <FileText size={18} style={{ color: 'var(--primary)' }} />
            <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 700 }}>
              {synthesis.title || 'Synthesis'}
            </h3>
          </div>

          {/* Body */}
          <div style={{
            whiteSpace: 'pre-wrap',
            fontSize: '0.9rem',
            lineHeight: 1.8,
            color: 'var(--text-primary)',
            marginBottom: '1.5rem',
            paddingBottom: '1.5rem',
            borderBottom: '1px solid var(--border-color)',
          }}>
            {synthesis.body}
          </div>

          {/* Metadata Chips */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {synthesis.vuln_class && synthesis.vuln_class.length > 0 && (
              <div>
                <div style={sectionLabelStyle}>
                  <AlertTriangle size={13} /> Vulnerability Classes
                </div>
                <ChipList items={synthesis.vuln_class} color="#ff7b72" />
              </div>
            )}

            {synthesis.protocol_category && synthesis.protocol_category.length > 0 && (
              <div>
                <div style={sectionLabelStyle}>
                  <Tag size={13} /> Protocol Categories
                </div>
                <ChipList items={synthesis.protocol_category} color="#d2a8ff" />
              </div>
            )}

            {synthesis.tags && synthesis.tags.length > 0 && (
              <div>
                <div style={sectionLabelStyle}>
                  <Tag size={13} /> Tags
                </div>
                <ChipList items={synthesis.tags} color="#58a6ff" />
              </div>
            )}

            {synthesis.derives_from && synthesis.derives_from.length > 0 && (
              <div>
                <div style={sectionLabelStyle}>
                  <Link2 size={13} /> Derives From ({synthesis.derives_from.length} sources)
                </div>
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.3rem' }}>
                  {synthesis.derives_from.map((id, i) => (
                    <span key={i} style={{
                      fontSize: '0.75rem',
                      padding: '2px 8px',
                      borderRadius: '4px',
                      background: 'var(--bg-surface)',
                      color: 'var(--text-secondary)',
                      fontFamily: "'Fira Code', monospace",
                      border: '1px solid var(--border-color)',
                    }}>
                      {id}
                    </span>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      ) : (
        <div className="glass-panel" style={{
          marginBottom: '1.5rem',
          textAlign: 'center',
          padding: '2.5rem 1.5rem',
          color: 'var(--text-secondary)',
        }}>
          <AlertTriangle size={24} style={{ marginBottom: '0.75rem', opacity: 0.5 }} />
          <div>This pattern has not been synthesized yet.</div>
        </div>
      )}

      {/* Video Script Section */}
      {hasVideoScript && (
        <div style={{ marginBottom: '1.5rem' }}>
          <div
            onClick={() => setShowVideoScript(!showVideoScript)}
            style={{
              display: 'flex', alignItems: 'center', gap: '0.5rem',
              marginBottom: '0.75rem', cursor: 'pointer', userSelect: 'none',
            }}
          >
            <Play size={18} style={{ color: '#3fb950' }} />
            <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 700 }}>
              Manim Video Script
            </h3>
            <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)', marginLeft: '0.5rem' }}>
              {showVideoScript ? '▲ collapse' : '▼ expand'} • run: manim -pql video_script.py PatternExplainer
            </span>
          </div>
          {showVideoScript && (
            <pre className="json-view" style={{ fontSize: '0.78rem', lineHeight: 1.6 }}>
              {content.video_script}
            </pre>
          )}
        </div>
      )}

      {/* Contract Source */}
      {contract_source && (
        <div style={{ marginBottom: '1.5rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
            <Code size={18} style={{ color: 'var(--primary)' }} />
            <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 700 }}>Reference Contract</h3>
          </div>
          <pre className="json-view" style={{ fontSize: '0.82rem', lineHeight: 1.6 }}>
            {contract_source}
          </pre>
        </div>
      )}

      {/* Related Entries */}
      {related_entries && related_entries.length > 0 && (
        <div style={{ marginBottom: '2rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
            <Link2 size={18} style={{ color: 'var(--primary)' }} />
            <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 700 }}>Related Corpus Entries</h3>
            <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>click to expand</span>
          </div>
          <div className="glass-panel" style={{ padding: 0, overflow: 'hidden' }}>
            <div className="data-table-container">
              <table className="data-table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Source</th>
                    <th>Severity</th>
                  </tr>
                </thead>
                <tbody>
                  {related_entries.map((entry, i) => {
                    const sevClass = SEVERITY_MAP[entry.severity?.toLowerCase()] || 'severity-informational';
                    const isSelected = expandedEntry?.id === entry.id;
                    return (
                      <tr
                        key={i}
                        onClick={() => fetchEntry(entry.id)}
                        style={{
                          cursor: 'pointer',
                          background: isSelected ? 'rgba(88,166,255,0.08)' : undefined,
                          borderLeft: isSelected ? '3px solid var(--primary)' : '3px solid transparent',
                          transition: 'all 0.15s ease',
                        }}
                        onMouseEnter={e => { if (!isSelected) e.currentTarget.style.background = 'rgba(255,255,255,0.03)'; }}
                        onMouseLeave={e => { if (!isSelected) e.currentTarget.style.background = ''; }}
                      >
                        <td style={{ fontFamily: "'Fira Code', monospace", fontSize: '0.82rem', color: isSelected ? 'var(--primary)' : 'var(--text-secondary)' }}>
                          {entry.id}
                        </td>
                        <td style={{ color: isSelected ? 'var(--text-primary)' : undefined, fontWeight: isSelected ? 600 : 400 }}>{entry.title}</td>
                        <td style={{ color: 'var(--text-secondary)' }}>{entry.source}</td>
                        <td>
                          <span className={`badge ${sevClass}`}>
                            {entry.severity}
                          </span>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>

          {/* Loading indicator */}
          {entryLoading && (
            <div style={{ padding: '1rem', textAlign: 'center', color: 'var(--text-secondary)', fontSize: '0.85rem' }}>
              <Loader size={16} style={{ animation: 'spin 1s linear infinite', marginRight: 6, verticalAlign: 'middle' }} />
              Loading entry…
            </div>
          )}

          {/* Expanded entry detail panel */}
          {expandedEntry && !entryLoading && (
            <div className="glass-panel animate-fade-in" style={{
              marginTop: '0.75rem',
              borderLeft: '3px solid var(--primary)',
            }}>
              {/* Header row */}
              <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', marginBottom: '1rem' }}>
                <div>
                  <h4 style={{ margin: 0, fontSize: '1.05rem', fontWeight: 700, color: 'var(--text-primary)', marginBottom: 4 }}>
                    {expandedEntry.title}
                  </h4>
                  <div style={{ display: 'flex', gap: 6, alignItems: 'center', flexWrap: 'wrap' }}>
                    <span className={`badge ${SEVERITY_MAP[expandedEntry.severity?.toLowerCase()] || 'severity-informational'}`}>
                      {expandedEntry.severity}
                    </span>
                    <span style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
                      {expandedEntry.source}
                    </span>
                    {expandedEntry.source_url && (
                      <a
                        href={expandedEntry.source_url}
                        target="_blank"
                        rel="noopener noreferrer"
                        style={{ fontSize: '0.78rem', color: 'var(--primary)', textDecoration: 'none', display: 'inline-flex', alignItems: 'center', gap: 3 }}
                      >
                        View source ↗
                      </a>
                    )}
                  </div>
                </div>
                <button
                  onClick={() => setExpandedEntry(null)}
                  style={{ background: 'none', border: 'none', color: 'var(--text-secondary)', cursor: 'pointer', padding: 4, fontSize: '1.1rem', lineHeight: 1 }}
                  title="Close"
                >
                  ✕
                </button>
              </div>

              {/* Vuln classes / categories */}
              {expandedEntry.vuln_class && expandedEntry.vuln_class.length > 0 && (
                <div style={{ marginBottom: '0.75rem' }}>
                  <div style={{ ...sectionLabelStyle, marginBottom: 4 }}>
                    <AlertTriangle size={12} /> Vulnerability Classes
                  </div>
                  <ChipList items={expandedEntry.vuln_class} color="#ff7b72" />
                </div>
              )}
              {expandedEntry.protocol_category && expandedEntry.protocol_category.length > 0 && (
                <div style={{ marginBottom: '0.75rem' }}>
                  <div style={{ ...sectionLabelStyle, marginBottom: 4 }}>
                    <Tag size={12} /> Categories
                  </div>
                  <ChipList items={expandedEntry.protocol_category} color="#d2a8ff" />
                </div>
              )}
              {expandedEntry.related_swc && expandedEntry.related_swc.length > 0 && (
                <div style={{ marginBottom: '0.75rem' }}>
                  <div style={{ ...sectionLabelStyle, marginBottom: 4 }}>
                    <Tag size={12} /> Related SWC
                  </div>
                  <ChipList items={expandedEntry.related_swc} color="#58a6ff" />
                </div>
              )}

              {/* Body text */}
              {expandedEntry.body && (
                <div style={{
                  marginTop: '0.75rem',
                  padding: '0.75rem 1rem',
                  background: 'rgba(0,0,0,0.2)',
                  borderRadius: 6,
                  border: '1px solid rgba(255,255,255,0.05)',
                  maxHeight: '400px',
                  overflowY: 'auto',
                }}>
                  <pre style={{
                    margin: 0,
                    whiteSpace: 'pre-wrap',
                    wordBreak: 'break-word',
                    fontSize: '0.82rem',
                    lineHeight: 1.7,
                    color: 'var(--text-primary)',
                    fontFamily: 'Inter, system-ui, sans-serif',
                  }}>
                    {expandedEntry.body}
                  </pre>
                </div>
              )}

              {/* Entry ID footer */}
              <div style={{ marginTop: '0.75rem', fontSize: '0.75rem', fontFamily: "'Fira Code', monospace", color: 'var(--text-secondary)', opacity: 0.7 }}>
                ID: {expandedEntry.id}
              </div>
            </div>
          )}
        </div>
      )}

      </div>{/* END LEFT COLUMN */}

      {/* RIGHT COLUMN — Simulation Notebook */}
      {hasSimulation && (
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
            <Zap size={18} style={{ color: '#ffa657' }} />
            <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 700 }}>Transaction Trace</h3>
            <span style={{ fontSize: '0.78rem', color: 'var(--text-secondary)' }}>
              Interactive · {content.simulation.steps.length} steps
            </span>
          </div>
          <SimulationNotebook simulation={content.simulation} />
        </div>
      )}

      </div>{/* END GRID */}

      <style>{`@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}

const backBtnStyle = {
  display: 'inline-flex',
  alignItems: 'center',
  gap: '0.4rem',
  background: 'none',
  border: 'none',
  color: 'var(--primary)',
  fontSize: '0.9rem',
  fontWeight: 600,
  cursor: 'pointer',
  padding: '6px 0',
  transition: 'opacity 0.2s ease',
};

const sectionLabelStyle = {
  display: 'flex',
  alignItems: 'center',
  gap: '0.35rem',
  fontSize: '0.78rem',
  fontWeight: 600,
  color: 'var(--text-secondary)',
  textTransform: 'uppercase',
  letterSpacing: '0.05em',
  marginBottom: '0.5rem',
};
