import React, { useEffect, useState, useCallback, useRef } from 'react';
import { FlaskConical, Play, Circle, RefreshCw, CheckCircle, AlertCircle, Terminal, ChevronDown, ChevronUp } from 'lucide-react';

const API_BASE = 'http://127.0.0.1:8000';

const STATUS_COLORS = {
  done: '#3fb950',
  pending: '#d29922',
  running: '#58a6ff',
  failed: '#ff7b72',
};

const DOMAIN_COLORS = {
  defi: '#58a6ff',
  security: '#ff7b72',
  economics: '#d2a8ff',
  infrastructure: '#a5d6ff',
  governance: '#ffa657',
  mev: '#f0883e',
};

const LEVEL_COLORS = {
  start: '#58a6ff',
  progress: '#8b949e',
  synth_start: '#d2a8ff',
  synth_done: '#3fb950',
  synth_fail: '#ff7b72',
  synth_error: '#ff7b72',
  wait: '#8b949e',
  complete: '#3fb950',
  session_done: '#58a6ff',
  info: '#c9d1d9',
};

// Live Process Banner
function LiveBanner({ liveState }) {
  if (!liveState || liveState.status === 'idle') return null;

  const isActive = liveState.status === 'synthesizing' || liveState.status === 'running' || liveState.status === 'waiting';
  const statusColor = liveState.status === 'synthesizing' ? '#d2a8ff'
    : liveState.status === 'waiting' ? '#d29922'
    : liveState.status === 'complete' ? '#3fb950'
    : '#58a6ff';

  return (
    <div className="glass-panel" style={{
      marginBottom: '1.5rem',
      padding: '1rem 1.25rem',
      borderLeft: `3px solid ${statusColor}`,
      animation: isActive ? 'pulse-border 2s ease-in-out infinite' : 'none',
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
        {isActive && (
          <RefreshCw size={16} style={{ color: statusColor, animation: 'spin 2s linear infinite' }} />
        )}
        {liveState.status === 'complete' && <CheckCircle size={16} style={{ color: statusColor }} />}

        <div style={{ flex: 1 }}>
          <div style={{ fontWeight: 600, fontSize: '0.9rem', color: statusColor, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            {liveState.status === 'synthesizing' ? '● Synthesizing' :
             liveState.status === 'waiting' ? '◌ Waiting for next topic' :
             liveState.status === 'complete' ? '✓ Queue Complete' :
             `● ${liveState.status}`}
          </div>

          {liveState.current_topic && (
            <div style={{ marginTop: '0.25rem', color: 'var(--text-primary)', fontSize: '0.95rem' }}>
              <strong>{liveState.current_topic.title}</strong>
              <span style={{ marginLeft: '0.5rem', color: DOMAIN_COLORS[liveState.current_topic.domain] || 'var(--text-secondary)', fontSize: '0.8rem' }}>
                {liveState.current_topic.domain}
              </span>
            </div>
          )}

          {liveState.current_topic?.seed_query && (
            <div style={{ marginTop: '0.15rem', color: 'var(--text-secondary)', fontSize: '0.8rem', fontFamily: 'var(--font-mono, "Fira Code", monospace)' }}>
              seed: {liveState.current_topic.seed_query}
            </div>
          )}
        </div>

        <div style={{ textAlign: 'right', fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
          <div style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)' }}>
            {liveState.completed_this_session || 0}
          </div>
          <div>synthesized<br/>this session</div>
        </div>
      </div>
    </div>
  );
}

// Terminal-style log viewer
function LogTerminal({ logs, expanded, onToggle }) {
  const termRef = useRef(null);

  useEffect(() => {
    if (termRef.current && expanded) {
      termRef.current.scrollTop = termRef.current.scrollHeight;
    }
  }, [logs, expanded]);

  return (
    <div className="glass-panel" style={{ marginBottom: '1.5rem', padding: 0, overflow: 'hidden' }}>
      <div
        onClick={onToggle}
        style={{
          display: 'flex', alignItems: 'center', gap: '0.5rem',
          padding: '0.75rem 1.25rem',
          cursor: 'pointer',
          borderBottom: expanded ? '1px solid var(--border-color)' : 'none',
          userSelect: 'none',
        }}
      >
        <Terminal size={16} style={{ color: '#3fb950' }} />
        <span style={{ fontWeight: 600, fontSize: '0.9rem', flex: 1 }}>Process Output</span>
        <span style={{ fontSize: '0.75rem', color: 'var(--text-secondary)' }}>
          {logs.length} entries
        </span>
        {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
      </div>

      {expanded && (
        <div
          ref={termRef}
          style={{
            background: '#0d1117',
            padding: '1rem',
            fontFamily: '"Fira Code", "Cascadia Code", "JetBrains Mono", monospace',
            fontSize: '0.78rem',
            lineHeight: 1.7,
            maxHeight: '400px',
            overflowY: 'auto',
            overflowX: 'auto',
          }}
        >
          {logs.length === 0 ? (
            <div style={{ color: '#484f58' }}>No logs yet. Start the autoresearch loop to see output.</div>
          ) : (
            logs.map((entry, i) => {
              const color = LEVEL_COLORS[entry.level] || '#c9d1d9';
              const ts = entry.ts ? new Date(entry.ts).toLocaleTimeString() : '';
              const icon = entry.level === 'synth_done' ? '✓'
                : entry.level === 'synth_fail' || entry.level === 'synth_error' ? '✗'
                : entry.level === 'synth_start' ? '▶'
                : entry.level === 'progress' ? '◆'
                : entry.level === 'wait' ? '◌'
                : entry.level === 'start' || entry.level === 'session_done' ? '●'
                : entry.level === 'complete' ? '★'
                : '·';

              return (
                <div key={i} style={{ color, whiteSpace: 'pre-wrap', wordBreak: 'break-word' }}>
                  <span style={{ color: '#484f58' }}>{ts} </span>
                  <span>{icon} </span>
                  <span>{entry.msg}</span>
                  {entry.slug && entry.level === 'synth_start' && (
                    <span style={{ color: '#484f58' }}> [{entry.slug}]</span>
                  )}
                  {entry.error && (
                    <span style={{ color: '#ff7b72' }}> — {entry.error}</span>
                  )}
                  {entry.domain && entry.level === 'synth_start' && (
                    <span style={{ color: DOMAIN_COLORS[entry.domain] || '#8b949e' }}> ({entry.domain})</span>
                  )}
                </div>
              );
            })
          )}
          <div style={{ color: '#3fb950', animation: 'blink 1s step-end infinite' }}>▊</div>
        </div>
      )}

      <style>{`
        @keyframes blink { 50% { opacity: 0; } }
        @keyframes pulse-border { 0%, 100% { opacity: 1; } 50% { opacity: 0.7; } }
      `}</style>
    </div>
  );
}


export default function Autoresearch() {
  const [topics, setTopics] = useState([]);
  const [domains, setDomains] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [running, setRunning] = useState(false);
  const [runResult, setRunResult] = useState(null);
  const [liveState, setLiveState] = useState(null);
  const [logs, setLogs] = useState([]);
  const [termExpanded, setTermExpanded] = useState(true);

  const fetchData = useCallback(() => {
    setLoading(true);
    setError(null);

    Promise.all([
      fetch(`${API_BASE}/api/autoresearch/topics`).then(r => {
        if (!r.ok) throw new Error(`Topics: HTTP ${r.status}`);
        return r.json();
      }),
      fetch(`${API_BASE}/api/autoresearch/domains`).then(r => {
        if (!r.ok) throw new Error(`Domains: HTTP ${r.status}`);
        return r.json();
      }),
    ])
      .then(([topicsData, domainsData]) => {
        setTopics(topicsData);
        setDomains(domainsData);
        setLoading(false);
      })
      .catch(e => {
        console.error(e);
        setError(e.message);
        setLoading(false);
      });
  }, []);

  // Fetch live state + logs every 3 seconds
  useEffect(() => {
    const poll = () => {
      fetch(`${API_BASE}/api/autoresearch/live`)
        .then(r => r.ok ? r.json() : null)
        .then(data => { if (data) setLiveState(data); })
        .catch(() => {});

      fetch(`${API_BASE}/api/autoresearch/logs?tail=200`)
        .then(r => r.ok ? r.json() : null)
        .then(data => {
          if (data?.entries) setLogs(data.entries);
        })
        .catch(() => {});
    };

    poll(); // initial
    const interval = setInterval(poll, 3000);
    return () => clearInterval(interval);
  }, []);

  // Refresh topics/domains every 15 seconds (less frequent)
  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 15000);
    return () => clearInterval(interval);
  }, [fetchData]);

  const handleRunBatch = () => {
    setRunning(true);
    setRunResult(null);

    fetch(`${API_BASE}/api/autoresearch/run`, { method: 'POST' })
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(result => {
        setRunResult(result);
        setRunning(false);
        fetchData();
      })
      .catch(e => {
        console.error(e);
        setRunResult({ error: e.message });
        setRunning(false);
      });
  };

  // Sort topics by domain, then by status
  const sortedTopics = [...topics].sort((a, b) => {
    if (a.domain < b.domain) return -1;
    if (a.domain > b.domain) return 1;
    const statusOrder = { running: 0, pending: 1, done: 2, failed: 3 };
    return (statusOrder[a.status] || 99) - (statusOrder[b.status] || 99);
  });

  if (loading && topics.length === 0) {
    return (
      <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
        <RefreshCw size={28} style={{ marginBottom: '1rem', opacity: 0.5, animation: 'spin 1s linear infinite' }} />
        <div>Loading autoresearch data…</div>
        <style>{`@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}</style>
      </div>
    );
  }

  if (error && topics.length === 0) {
    return (
      <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--critical)' }}>
        <AlertCircle size={28} style={{ marginBottom: '1rem' }} />
        <div>Failed to load: {error}</div>
        <button className="btn" onClick={fetchData} style={{ marginTop: '1rem' }}>
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="animate-fade-in">
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <FlaskConical size={24} style={{ color: 'var(--primary)' }} />
          <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 700 }}>Autoresearch Engine</h2>
          <span style={{ color: 'var(--text-secondary)', fontSize: '0.9rem' }}>
            {topics.filter(t => t.status === 'done').length}/{topics.length} synthesized
          </span>
        </div>

        <button
          className="btn"
          onClick={handleRunBatch}
          disabled={running}
          style={{
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem',
            opacity: running ? 0.7 : 1,
            cursor: running ? 'wait' : 'pointer',
          }}
        >
          {running ? (
            <>
              <RefreshCw size={16} style={{ animation: 'spin 1s linear infinite' }} />
              Running…
            </>
          ) : (
            <>
              <Play size={16} />
              Run Next Batch
            </>
          )}
        </button>
      </div>

      {/* Live Process Banner */}
      <LiveBanner liveState={liveState} />

      {/* Terminal Log */}
      <LogTerminal logs={logs} expanded={termExpanded} onToggle={() => setTermExpanded(!termExpanded)} />

      {/* Run Result */}
      {runResult && (
        <div className="glass-panel" style={{ marginBottom: '1.5rem', padding: '1rem 1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.5rem' }}>
            {runResult.error ? (
              <AlertCircle size={16} style={{ color: 'var(--critical)' }} />
            ) : (
              <CheckCircle size={16} style={{ color: '#3fb950' }} />
            )}
            <span style={{
              fontWeight: 600,
              fontSize: '0.9rem',
              color: runResult.error ? 'var(--critical)' : '#3fb950',
            }}>
              {runResult.error ? 'Batch Failed' : 'Batch Complete'}
            </span>
            <button
              onClick={() => setRunResult(null)}
              style={{
                marginLeft: 'auto',
                background: 'none',
                border: 'none',
                color: 'var(--text-secondary)',
                cursor: 'pointer',
                fontSize: '0.85rem',
              }}
            >
              ✕
            </button>
          </div>
          <pre className="json-view" style={{ margin: 0, fontSize: '0.8rem' }}>
            {JSON.stringify(runResult, null, 2)}
          </pre>
        </div>
      )}

      {/* Domain Summary Cards */}
      <div className="dashboard-grid">
        {domains.map((d, i) => {
          const total = d.total || 0;
          const done = d.done || 0;
          const pending = d.pending || 0;
          const pct = total > 0 ? Math.round((done / total) * 100) : 0;
          const domainColor = DOMAIN_COLORS[d.domain] || 'var(--primary)';

          return (
            <div key={i} className="glass-panel stat-card">
              <div style={{
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'space-between',
                marginBottom: '0.25rem',
              }}>
                <span className="stat-label" style={{ margin: 0 }}>
                  {d.label || d.domain}
                </span>
                <span style={{
                  fontSize: '0.75rem',
                  fontWeight: 600,
                  color: domainColor,
                }}>
                  {pct}%
                </span>
              </div>

              <div className="stat-value" style={{ fontSize: '2rem' }}>
                {total}
              </div>

              <div style={{ display: 'flex', gap: '1rem', fontSize: '0.82rem', marginBottom: '0.75rem' }}>
                <span style={{ color: '#3fb950' }}>
                  ● {done} done
                </span>
                <span style={{ color: '#d29922' }}>
                  ● {pending} pending
                </span>
              </div>

              {/* Progress Bar */}
              <div style={{
                width: '100%',
                height: '4px',
                background: 'var(--border-color)',
                borderRadius: '2px',
                overflow: 'hidden',
              }}>
                <div style={{
                  width: `${pct}%`,
                  height: '100%',
                  background: `linear-gradient(90deg, #3fb950, ${domainColor})`,
                  borderRadius: '2px',
                  transition: 'width 0.4s ease',
                }} />
              </div>
            </div>
          );
        })}
      </div>

      {/* Topics Table */}
      <div className="glass-panel" style={{ padding: 0, overflow: 'hidden' }}>
        <div style={{ padding: '1rem 1.25rem 0.75rem', borderBottom: '1px solid var(--border-color)' }}>
          <h3 style={{ margin: 0, fontSize: '1rem', fontWeight: 700, color: 'var(--text-primary)' }}>
            All Topics
          </h3>
        </div>
        <div className="data-table-container">
          <table className="data-table">
            <thead>
              <tr>
                <th style={{ width: '90px' }}>Status</th>
                <th>Topic Title</th>
                <th style={{ width: '140px' }}>Domain</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {sortedTopics.map((topic, i) => {
                const statusColor = STATUS_COLORS[topic.status] || 'var(--text-secondary)';
                const domainColor = DOMAIN_COLORS[topic.domain] || 'var(--primary)';
                const isCurrentTopic = liveState?.current_topic?.slug === topic.slug;

                return (
                  <tr key={i} style={{
                    background: isCurrentTopic ? 'rgba(210, 168, 255, 0.08)' : undefined,
                    borderLeft: isCurrentTopic ? '3px solid #d2a8ff' : '3px solid transparent',
                  }}>
                    <td>
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                        {isCurrentTopic ? (
                          <RefreshCw size={10} style={{ color: '#d2a8ff', animation: 'spin 2s linear infinite' }} />
                        ) : (
                          <Circle size={8} fill={statusColor} stroke="none" />
                        )}
                        <span style={{
                          fontSize: '0.8rem',
                          fontWeight: 500,
                          color: statusColor,
                          textTransform: 'capitalize',
                        }}>
                          {isCurrentTopic ? 'active' : topic.status}
                        </span>
                      </div>
                    </td>
                    <td style={{ fontWeight: 500 }}>{topic.title}</td>
                    <td>
                      <span style={{
                        display: 'inline-block',
                        padding: '2px 8px',
                        borderRadius: '10px',
                        fontSize: '0.72rem',
                        fontWeight: 600,
                        background: `${domainColor}18`,
                        color: domainColor,
                        border: `1px solid ${domainColor}40`,
                      }}>
                        {topic.domain}
                      </span>
                    </td>
                    <td style={{
                      color: 'var(--text-secondary)',
                      fontSize: '0.85rem',
                      maxWidth: '400px',
                      overflow: 'hidden',
                      textOverflow: 'ellipsis',
                      whiteSpace: 'nowrap',
                    }}>
                      {topic.description}
                    </td>
                  </tr>
                );
              })}
              {sortedTopics.length === 0 && (
                <tr>
                  <td colSpan={4} style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}>
                    No topics in the queue.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>

      <style>{`@keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }`}</style>
    </div>
  );
}
