import React, { useEffect, useState } from 'react';
import { Activity, ShieldAlert, CheckCircle, XCircle, ChevronRight, ArrowLeft, FileText, Code, AlertTriangle, Info, Zap, X } from 'lucide-react';

const API = 'http://127.0.0.1:8000';

const SEV_ORDER = ['Critical', 'High', 'Medium', 'Low', 'Informational', 'Gas'];

function PipelineBar({ stages }) {
  return (
    <div style={{display: 'flex', gap: '2px', marginBottom: '1.5rem', flexWrap: 'wrap'}}>
      {stages.map((s, i) => (
        <div key={s.id} style={{
          flex: 1,
          minWidth: '100px',
          padding: '10px 12px',
          background: s.complete ? 'rgba(88, 166, 255, 0.15)' : 'rgba(139, 148, 158, 0.08)',
          borderTop: `3px solid ${s.complete ? 'var(--primary)' : 'var(--border-color)'}`,
          borderRadius: i === 0 ? '8px 0 0 8px' : i === stages.length - 1 ? '0 8px 8px 0' : '0',
          transition: 'all 0.3s ease',
        }}>
          <div style={{display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '4px'}}>
            {s.complete
              ? <CheckCircle size={14} color="var(--primary)"/>
              : <div style={{width: 14, height: 14, borderRadius: '50%', border: '2px solid var(--border-color)'}}/>
            }
            <span style={{fontSize: '0.75rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em', color: s.complete ? 'var(--text-primary)' : 'var(--text-secondary)'}}>
              {s.id}
            </span>
          </div>
          <div style={{fontSize: '0.7rem', color: 'var(--text-secondary)'}}>{s.label}</div>
        </div>
      ))}
    </div>
  );
}

function FindingCard({ finding, index, onClick }) {
  const sev = (finding.severity || 'info').toLowerCase();
  const sevColors = { critical: 'var(--critical)', high: 'var(--high)', medium: 'var(--medium)', low: 'var(--low)', informational: 'var(--info)', gas: 'var(--text-secondary)' };
  const borderColor = sevColors[sev] || 'var(--border-color)';

  return (
    <div
      onClick={onClick}
      style={{
        background: 'var(--bg-surface)',
        padding: '1.25rem',
        borderRadius: '8px',
        borderLeft: `4px solid ${borderColor}`,
        cursor: 'pointer',
        transition: 'all 0.2s ease',
      }}
      onMouseEnter={e => { e.currentTarget.style.background = 'var(--bg-surface-hover)'; e.currentTarget.style.transform = 'translateX(4px)'; }}
      onMouseLeave={e => { e.currentTarget.style.background = 'var(--bg-surface)'; e.currentTarget.style.transform = 'translateX(0)'; }}
    >
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.75rem'}}>
        <div style={{display: 'flex', alignItems: 'center', gap: '8px', flex: 1}}>
          <span style={{color: 'var(--text-secondary)', fontSize: '0.85rem'}}>#{index + 1}</span>
          <strong style={{fontSize: '1rem'}}>{finding.title}</strong>
          {finding.novel && <span style={{fontSize: '0.7rem', padding: '2px 6px', background: 'rgba(210, 168, 255, 0.2)', color: 'var(--medium)', borderRadius: '4px'}}>novel</span>}
        </div>
        <div style={{display: 'flex', alignItems: 'center', gap: '8px'}}>
          <span className={`badge severity-${sev}`}>{finding.severity}</span>
          <ChevronRight size={16} color="var(--text-secondary)"/>
        </div>
      </div>
      <div style={{fontSize: '0.85rem', color: 'var(--text-secondary)', display: 'flex', gap: '1.5rem', flexWrap: 'wrap'}}>
        <span>By: {finding.discovered_by}</span>
        <span>Confidence: {finding.confidence}</span>
        <span>PoC: {finding.poc_status}</span>
        {finding.citations?.length > 0 && <span>Citations: {finding.citations.length}</span>}
      </div>
    </div>
  );
}

function FindingDetail({ runId, findingIdx, finding, onClose }) {
  const [detail, setDetail] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    fetch(`${API}/api/audits/${runId}/findings/${findingIdx}`)
      .then(r => r.json())
      .then(d => { setDetail(d); setLoading(false); })
      .catch(() => setLoading(false));
  }, [runId, findingIdx]);

  if (loading) return <div style={{padding: '2rem'}}>Loading finding details...</div>;

  const f = detail?.finding || finding;
  const pocLogs = detail?.poc_logs || {};
  const sev = (f.severity || 'info').toLowerCase();

  return (
    <div className="animate-fade-in" style={{padding: '0.5rem'}}>
      <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1.5rem'}}>
        <button onClick={onClose} style={{background: 'none', border: 'none', color: 'var(--primary)', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px', padding: '6px 0'}}>
          <ArrowLeft size={18}/> Back to findings
        </button>
        <span className={`badge severity-${sev}`}>{f.severity}</span>
      </div>

      <h2 style={{margin: '0 0 0.5rem 0', fontSize: '1.4rem'}}>{f.title}</h2>

      <div style={{display: 'flex', gap: '1rem', flexWrap: 'wrap', marginBottom: '1.5rem', fontSize: '0.85rem', color: 'var(--text-secondary)'}}>
        <span>Discovered by: <strong style={{color: 'var(--text-primary)'}}>{f.discovered_by}</strong></span>
        <span>Confidence: <strong style={{color: 'var(--text-primary)'}}>{f.confidence}</strong></span>
        <span>PoC: <strong style={{color: f.poc_status === 'reproduced' ? 'var(--primary)' : f.poc_status === 'compile-error' ? 'var(--critical)' : 'var(--text-primary)'}}>{f.poc_status}</strong></span>
        {f.novel && <span style={{color: 'var(--medium)'}}>✦ Novel finding</span>}
      </div>

      {/* Location */}
      {f.location?.length > 0 && (
        <Section icon={<FileText size={16}/>} title="Location">
          {f.location.map((loc, i) => (
            <div key={i} style={{fontFamily: "'Fira Code', monospace", fontSize: '0.85rem', color: 'var(--primary)', marginBottom: '4px'}}>
              {loc.file}:{loc.line_start}{loc.line_end ? `-${loc.line_end}` : ''}
            </div>
          ))}
        </Section>
      )}

      {/* Description */}
      <Section icon={<Info size={16}/>} title="Description">
        <div style={{whiteSpace: 'pre-wrap', lineHeight: 1.7, fontSize: '0.95rem'}}>{f.description}</div>
      </Section>

      {/* Impact */}
      <Section icon={<AlertTriangle size={16}/>} title="Impact">
        <div style={{whiteSpace: 'pre-wrap', lineHeight: 1.7, fontSize: '0.95rem'}}>{f.impact}</div>
      </Section>

      {/* Recommendation */}
      <Section icon={<Zap size={16}/>} title="Recommendation">
        <div style={{whiteSpace: 'pre-wrap', lineHeight: 1.7, fontSize: '0.95rem'}}>{f.recommendation}</div>
      </Section>

      {/* Proof of Concept */}
      {f.proof_of_concept && (
        <Section icon={<Code size={16}/>} title="Proof of Concept">
          <div style={{whiteSpace: 'pre-wrap', lineHeight: 1.7, fontSize: '0.95rem'}}>{f.proof_of_concept}</div>
        </Section>
      )}

      {/* Foundry PoC Code */}
      {f.foundry_poc?.exploit && (
        <Section icon={<Code size={16}/>} title="Foundry PoC – Exploit Code">
          <pre className="json-view" style={{fontSize: '0.8rem'}}>{f.foundry_poc.exploit}</pre>
          {f.foundry_poc.notes && <div style={{marginTop: '0.75rem', fontSize: '0.85rem', color: 'var(--text-secondary)', fontStyle: 'italic'}}>{f.foundry_poc.notes}</div>}
        </Section>
      )}

      {/* PoC Logs */}
      {pocLogs.stdout_log && (
        <Section icon={<FileText size={16}/>} title="PoC stdout">
          <pre className="json-view" style={{fontSize: '0.75rem', maxHeight: '300px', overflowY: 'auto'}}>{pocLogs.stdout_log}</pre>
        </Section>
      )}
      {pocLogs.stderr_log && (
        <Section icon={<FileText size={16}/>} title="PoC stderr">
          <pre className="json-view" style={{fontSize: '0.75rem', maxHeight: '300px', overflowY: 'auto', color: 'var(--critical)'}}>{pocLogs.stderr_log}</pre>
        </Section>
      )}

      {/* Citations */}
      {f.citations?.length > 0 && (
        <Section icon={<FileText size={16}/>} title="Citations">
          <div style={{display: 'flex', flexWrap: 'wrap', gap: '8px'}}>
            {f.citations.map((c, i) => (
              <span key={i} style={{padding: '4px 10px', background: 'rgba(88, 166, 255, 0.12)', border: '1px solid rgba(88, 166, 255, 0.3)', borderRadius: '6px', fontSize: '0.8rem', color: 'var(--primary)'}}>{c}</span>
            ))}
          </div>
        </Section>
      )}
    </div>
  );
}

function Section({ icon, title, children }) {
  return (
    <div style={{marginBottom: '1.5rem'}}>
      <div style={{display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '0.75rem', color: 'var(--text-secondary)', fontWeight: 600, fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.04em'}}>
        {icon} {title}
      </div>
      <div style={{paddingLeft: '24px'}}>{children}</div>
    </div>
  );
}

function ReportView({ runId, onClose }) {
  const [markdown, setMarkdown] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch(`${API}/api/audits/${runId}/report`)
      .then(r => r.json())
      .then(d => { setMarkdown(d.markdown); setLoading(false); })
      .catch(() => { setMarkdown(null); setLoading(false); });
  }, [runId]);

  return (
    <div className="animate-fade-in">
      <div style={{display: 'flex', justifyContent: 'space-between', marginBottom: '1rem'}}>
        <button onClick={onClose} style={{background: 'none', border: 'none', color: 'var(--primary)', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px'}}>
          <ArrowLeft size={18}/> Back
        </button>
        <span style={{color: 'var(--text-secondary)', fontSize: '0.85rem'}}>Full Markdown Report</span>
      </div>
      {loading ? <div>Loading report...</div> :
        markdown ? <pre style={{whiteSpace: 'pre-wrap', lineHeight: 1.6, fontSize: '0.9rem', color: 'var(--text-primary)'}}>{markdown}</pre> :
        <div style={{color: 'var(--text-secondary)'}}>No report available for this run.</div>
      }
    </div>
  );
}


export default function AuditRuns() {
  const [audits, setAudits] = useState([]);
  const [loading, setLoading] = useState(true);
  const [selectedRun, setSelectedRun] = useState(null);
  const [runDetails, setRunDetails] = useState(null);
  const [activeFinding, setActiveFinding] = useState(null); // index
  const [showReport, setShowReport] = useState(false);

  useEffect(() => {
    fetch(`${API}/api/audits`)
      .then(r => r.json())
      .then(data => { setAudits(data); setLoading(false); })
      .catch(() => setLoading(false));
  }, []);

  const loadRunDetails = async (runId) => {
    setSelectedRun(runId);
    setRunDetails(null);
    setActiveFinding(null);
    setShowReport(false);
    try {
      const res = await fetch(`${API}/api/audits/${runId}`);
      const data = await res.json();
      setRunDetails(data);
    } catch (e) {
      console.error(e);
    }
  };

  if (loading) return <div style={{padding: '2rem', color: 'var(--text-secondary)'}}>Loading audit history...</div>;

  // Detail panel content
  const renderDetailContent = () => {
    if (!selectedRun) {
      return (
        <div style={{height: '100%', display: 'flex', alignItems: 'center', justifyContent: 'center', color: 'var(--text-secondary)', flexDirection: 'column', gap: '1rem'}}>
          <Activity size={48} strokeWidth={1}/>
          <span>Select an audit run to view its process</span>
        </div>
      );
    }
    if (!runDetails) return <div style={{padding: '2rem'}}>Loading details...</div>;

    // Show report view
    if (showReport) {
      return <ReportView runId={selectedRun} onClose={() => setShowReport(false)}/>;
    }

    // Show finding detail
    if (activeFinding !== null) {
      const sortedFindings = [...runDetails.findings].sort((a, b) => SEV_ORDER.indexOf(a.severity) - SEV_ORDER.indexOf(b.severity));
      return (
        <FindingDetail
          runId={selectedRun}
          findingIdx={runDetails.findings.indexOf(sortedFindings[activeFinding])}
          finding={sortedFindings[activeFinding]}
          onClose={() => setActiveFinding(null)}
        />
      );
    }

    // Show run overview with pipeline + findings list
    const sortedFindings = [...runDetails.findings].sort((a, b) => SEV_ORDER.indexOf(a.severity) - SEV_ORDER.indexOf(b.severity));

    return (
      <div className="animate-fade-in">
        {/* Run header */}
        <div style={{display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1.5rem'}}>
          <div>
            <h2 style={{margin: '0 0 0.25rem 0'}}>{runDetails.summary.name}</h2>
            <div style={{color: 'var(--text-secondary)', fontSize: '0.9rem'}}>
              {runDetails.summary.target} &middot; {runDetails.summary.kind} &middot; {runDetails.summary.timestamp}
            </div>
          </div>
          {runDetails.pipeline?.some(s => s.id === 'report' && s.complete) && (
            <button className="btn" onClick={() => setShowReport(true)} style={{fontSize: '0.85rem', padding: '8px 16px'}}>
              <FileText size={16} style={{marginRight: '6px', verticalAlign: 'text-bottom'}}/> View Report
            </button>
          )}
        </div>

        {/* Pipeline progress */}
        {runDetails.pipeline && <PipelineBar stages={runDetails.pipeline}/>}

        {/* Static tools */}
        <h3 style={{color: 'var(--text-secondary)', fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem'}}>Static Analysis Tools</h3>
        <div style={{display: 'flex', gap: '0.75rem', marginBottom: '2rem', flexWrap: 'wrap'}}>
          {runDetails.static_tools.map(t => (
            <div key={t.tool} style={{
              display: 'flex', alignItems: 'center', gap: '8px',
              padding: '8px 14px', borderRadius: '8px',
              background: 'var(--bg-surface)',
              border: `1px solid ${t.succeeded ? 'rgba(88, 166, 255, 0.3)' : 'rgba(255, 123, 114, 0.3)'}`,
            }}>
              {t.succeeded ? <CheckCircle size={16} color="var(--primary)"/> : <XCircle size={16} color="var(--critical)"/>}
              <span style={{fontWeight: 600}}>{t.tool}</span>
              {t.version && <span style={{fontSize: '0.75rem', color: 'var(--text-secondary)'}}>{t.version}</span>}
            </div>
          ))}
        </div>

        {/* Findings */}
        <h3 style={{color: 'var(--text-secondary)', fontSize: '0.9rem', textTransform: 'uppercase', letterSpacing: '0.05em', marginBottom: '0.75rem'}}>
          Findings ({sortedFindings.length})
        </h3>
        {sortedFindings.length === 0 ? (
          <div style={{padding: '2rem', textAlign: 'center', color: 'var(--text-secondary)'}}>No findings reported for this run.</div>
        ) : (
          <div style={{display: 'flex', flexDirection: 'column', gap: '0.75rem'}}>
            {sortedFindings.map((f, i) => (
              <FindingCard key={i} finding={f} index={i} onClick={() => setActiveFinding(i)}/>
            ))}
          </div>
        )}
      </div>
    );
  };

  return (
    <div style={{display: 'flex', gap: '1.5rem', height: 'calc(100vh - 100px)'}}>
      {/* Left sidebar — audit run list */}
      <div className="glass-panel" style={{width: '340px', minWidth: '280px', overflowY: 'auto', flexShrink: 0}}>
        <h3 style={{marginTop: 0, paddingBottom: '0.75rem', borderBottom: '1px solid var(--border-color)', fontSize: '1rem'}}>
          Audit Runs ({audits.length})
        </h3>

        {audits.length === 0 ? (
          <div style={{color: 'var(--text-secondary)', padding: '2rem', textAlign: 'center'}}>No audits found.</div>
        ) : (
          <div style={{display: 'flex', flexDirection: 'column', gap: '0.5rem', marginTop: '0.75rem'}}>
            {audits.map(run => {
              const isSelected = selectedRun === run.run_dir;
              return (
                <div
                  key={run.run_dir}
                  onClick={() => loadRunDetails(run.run_dir)}
                  style={{
                    padding: '0.75rem',
                    borderRadius: '8px',
                    border: `1px solid ${isSelected ? 'var(--primary)' : 'var(--border-color)'}`,
                    background: isSelected ? 'rgba(88, 166, 255, 0.1)' : 'transparent',
                    cursor: 'pointer',
                    transition: 'all 0.15s ease',
                  }}
                >
                  <div style={{fontWeight: 600, fontSize: '0.85rem', marginBottom: '0.25rem', color: 'var(--text-primary)', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap'}}>
                    {run.name}
                  </div>
                  <div style={{fontSize: '0.75rem', color: 'var(--text-secondary)', marginBottom: '0.35rem'}}>
                    {run.kind} &middot; {run.timestamp?.substring(0, 10)}
                  </div>
                  <div style={{display: 'flex', gap: '0.75rem', fontSize: '0.8rem'}}>
                    {run.n_findings > 0 ? (
                      <span style={{display: 'flex', alignItems: 'center', gap: '4px'}}>
                        <ShieldAlert size={13} color="var(--critical)"/> {run.n_findings}
                      </span>
                    ) : (
                      <span style={{color: 'var(--text-secondary)'}}>0 findings</span>
                    )}
                    {run.reconciled && <span style={{color: 'var(--primary)', fontSize: '0.7rem'}}>multimodel</span>}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>

      {/* Right main panel */}
      <div className="glass-panel" style={{flex: 1, overflowY: 'auto'}}>
        {renderDetailContent()}
      </div>
    </div>
  );
}
