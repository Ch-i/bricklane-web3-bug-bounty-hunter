import React, { useState } from 'react';
import { Search, X, ExternalLink, Tag } from 'lucide-react';

const API_BASE = 'http://127.0.0.1:8000';

const SEVERITY_OPTIONS = ['All', 'Critical', 'High', 'Medium', 'Low', 'Informational', 'Gas'];
const SOURCE_OPTIONS = ['All', 'swc', 'solodit', 'arxiv', 'audit-report', 'rekt', 'synthesis'];

export default function CorpusExplorer() {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [severityFilter, setSeverityFilter] = useState('All');
  const [sourceFilter, setSourceFilter] = useState('All');
  const [detailEntry, setDetailEntry] = useState(null);
  const [detailLoading, setDetailLoading] = useState(false);
  const [stats, setStats] = useState(null);

  // Auto-load high-severity findings on mount
  React.useEffect(() => {
    setLoading(true);
    Promise.all([
      fetch(`${API_BASE}/api/search?query=vulnerability+exploit+attack&severity=Critical&top_k=20`).then(r => r.json()),
      fetch(`${API_BASE}/api/stats`).then(r => r.json()).catch(() => null),
    ]).then(([initialResults, statsData]) => {
      setResults(initialResults);
      setStats(statsData);
    }).catch(console.error).finally(() => setLoading(false));
  }, []);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setDetailEntry(null);
    try {
      const params = new URLSearchParams({ query, top_k: '20' });
      if (severityFilter !== 'All') params.set('severity', severityFilter);
      if (sourceFilter !== 'All') params.set('source', sourceFilter);

      const res = await fetch(`${API_BASE}/api/search?${params.toString()}`);
      const data = await res.json();
      setResults(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const openDetail = async (entryId) => {
    if (detailEntry && detailEntry.id === entryId) {
      setDetailEntry(null);
      return;
    }
    setDetailLoading(true);
    try {
      const res = await fetch(`${API_BASE}/api/corpus/${entryId}`);
      const data = await res.json();
      setDetailEntry(data);
    } catch (err) {
      console.error(err);
    } finally {
      setDetailLoading(false);
    }
  };

  const closeDetail = () => setDetailEntry(null);

  const renderTags = (items, colorVar) => {
    if (!items || items.length === 0) return null;
    return items.map((item, i) => (
      <span
        key={i}
        style={{
          display: 'inline-block',
          padding: '2px 8px',
          borderRadius: '10px',
          fontSize: '0.7rem',
          fontWeight: 600,
          marginRight: '6px',
          marginBottom: '4px',
          background: `color-mix(in srgb, ${colorVar} 15%, transparent)`,
          color: colorVar,
          border: `1px solid color-mix(in srgb, ${colorVar} 40%, transparent)`,
        }}
      >
        {item}
      </span>
    ));
  };

  return (
    <div className="corpus-explorer">
      {/* Stats banner */}
      {stats && stats.corpus && (
        <div style={{ display: 'flex', gap: '1.5rem', marginBottom: '1.25rem', flexWrap: 'wrap' }}>
          <div className="glass-panel" style={{ padding: '0.75rem 1.25rem', flex: '1', minWidth: '150px' }}>
            <div style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-primary)' }}>{stats.corpus.total?.toLocaleString() || '—'}</div>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Total Entries</div>
          </div>
          <div className="glass-panel" style={{ padding: '0.75rem 1.25rem', flex: '1', minWidth: '150px' }}>
            <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#ff4757' }}>{stats.corpus.by_severity?.Critical || 0}</div>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Critical</div>
          </div>
          <div className="glass-panel" style={{ padding: '0.75rem 1.25rem', flex: '1', minWidth: '150px' }}>
            <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#ff6b6b' }}>{stats.corpus.by_severity?.High || 0}</div>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>High</div>
          </div>
          <div className="glass-panel" style={{ padding: '0.75rem 1.25rem', flex: '1', minWidth: '150px' }}>
            <div style={{ fontSize: '1.5rem', fontWeight: 700, color: 'var(--text-secondary)' }}>{stats.corpus.by_source ? Object.keys(stats.corpus.by_source).length : '—'}</div>
            <div style={{ fontSize: '0.78rem', color: 'var(--text-secondary)', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Sources</div>
          </div>
        </div>
      )}

      {/* Search bar */}
      <form onSubmit={handleSearch} className="search-bar">
        <input
          type="text"
          className="search-input"
          placeholder="Search vulnerabilities, protocols, exploits..."
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button type="submit" className="btn" disabled={loading}>
          <Search size={18} style={{ marginRight: '8px', verticalAlign: 'text-bottom' }} />
          {loading ? 'Searching...' : 'Search'}
        </button>
      </form>

      {/* Filter bar */}
      <div
        style={{
          display: 'flex',
          gap: '1rem',
          marginBottom: '1.5rem',
          alignItems: 'center',
          flexWrap: 'wrap',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <label style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Severity
          </label>
          <select
            value={severityFilter}
            onChange={(e) => setSeverityFilter(e.target.value)}
            style={{
              padding: '8px 12px',
              borderRadius: '8px',
              border: '1px solid var(--border-color)',
              background: 'var(--bg-surface)',
              color: 'var(--text-primary)',
              fontSize: '0.9rem',
              cursor: 'pointer',
            }}
          >
            {SEVERITY_OPTIONS.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>

        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <label style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            Source
          </label>
          <select
            value={sourceFilter}
            onChange={(e) => setSourceFilter(e.target.value)}
            style={{
              padding: '8px 12px',
              borderRadius: '8px',
              border: '1px solid var(--border-color)',
              background: 'var(--bg-surface)',
              color: 'var(--text-primary)',
              fontSize: '0.9rem',
              cursor: 'pointer',
            }}
          >
            {SOURCE_OPTIONS.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
        </div>
      </div>

      {/* Main layout: results table + detail panel */}
      <div style={{ display: 'flex', gap: '1.5rem', alignItems: 'flex-start' }}>
        {/* Results table */}
        <div
          className="glass-panel data-table-container"
          style={{
            flex: detailEntry ? '1 1 55%' : '1 1 100%',
            minWidth: 0,
            transition: 'flex 0.3s ease',
          }}
        >
          {results.length === 0 && !loading && (
            <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-secondary)' }}>
              No results found. Try a different query.
            </div>
          )}

          {results.length > 0 && (
            <table className="data-table">
              <thead>
                <tr>
                  <th>Title</th>
                  <th>Severity</th>
                  <th>Source</th>
                  <th style={{ textAlign: 'right' }}>Score</th>
                </tr>
              </thead>
              <tbody>
                {results.map((r) => (
                  <tr
                    key={r.id}
                    onClick={() => openDetail(r.id)}
                    style={{
                      backgroundColor: detailEntry && detailEntry.id === r.id ? 'var(--bg-surface-hover)' : undefined,
                    }}
                  >
                    <td style={{ fontWeight: 500 }}>
                      {r.title.substring(0, 80)}{r.title.length > 80 ? '...' : ''}
                    </td>
                    <td>
                      <span className={`badge severity-${(r.severity || 'info').toLowerCase()}`}>
                        {r.severity || 'Unspecified'}
                      </span>
                    </td>
                    <td style={{ color: 'var(--text-secondary)' }}>{r.source}</td>
                    <td style={{ textAlign: 'right', fontFamily: 'monospace', color: 'var(--text-secondary)' }}>
                      {r.score.toFixed(2)}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* Slide-out detail panel */}
        {(detailEntry || detailLoading) && (
          <div
            className="glass-panel animate-fade-in"
            style={{
              flex: '0 0 42%',
              maxHeight: 'calc(100vh - 220px)',
              overflowY: 'auto',
              position: 'sticky',
              top: '100px',
            }}
          >
            {detailLoading && !detailEntry ? (
              <div style={{ textAlign: 'center', padding: '3rem', color: 'var(--text-secondary)' }}>
                Loading entry...
              </div>
            ) : detailEntry ? (
              <div>
                {/* Close button */}
                <div style={{ display: 'flex', justifyContent: 'flex-end', marginBottom: '0.5rem' }}>
                  <button
                    onClick={closeDetail}
                    style={{
                      background: 'transparent',
                      border: 'none',
                      color: 'var(--text-secondary)',
                      cursor: 'pointer',
                      padding: '4px',
                      borderRadius: '6px',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      transition: 'color 0.2s ease',
                    }}
                    onMouseEnter={(e) => (e.currentTarget.style.color = 'var(--text-primary)')}
                    onMouseLeave={(e) => (e.currentTarget.style.color = 'var(--text-secondary)')}
                  >
                    <X size={20} />
                  </button>
                </div>

                {/* Title */}
                <h2 style={{ margin: '0 0 1rem 0', fontSize: '1.4rem', fontWeight: 700, color: 'var(--text-primary)', lineHeight: 1.3 }}>
                  {detailEntry.title}
                </h2>

                {/* Severity badge */}
                <div style={{ marginBottom: '1rem' }}>
                  <span className={`badge severity-${(detailEntry.severity || 'info').toLowerCase()}`}>
                    {detailEntry.severity || 'Unspecified'}
                  </span>
                </div>

                {/* Source + link */}
                <div style={{ marginBottom: '1rem', display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <span style={{ color: 'var(--text-secondary)', fontSize: '0.85rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                    Source:
                  </span>
                  {detailEntry.source_url ? (
                    <a
                      href={detailEntry.source_url}
                      target="_blank"
                      rel="noopener noreferrer"
                      style={{
                        color: 'var(--primary)',
                        textDecoration: 'none',
                        display: 'inline-flex',
                        alignItems: 'center',
                        gap: '4px',
                        fontSize: '0.9rem',
                      }}
                    >
                      {detailEntry.source}
                      <ExternalLink size={14} />
                    </a>
                  ) : (
                    <span style={{ color: 'var(--text-primary)', fontSize: '0.9rem' }}>
                      {detailEntry.source}
                    </span>
                  )}
                </div>

                {/* vuln_class tags */}
                {detailEntry.vuln_class && detailEntry.vuln_class.length > 0 && (
                  <div style={{ marginBottom: '0.75rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
                      <Tag size={14} style={{ color: 'var(--text-secondary)' }} />
                      <span style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', fontWeight: 600, textTransform: 'uppercase' }}>
                        Vulnerability Class
                      </span>
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap' }}>
                      {renderTags(detailEntry.vuln_class, 'var(--critical)')}
                    </div>
                  </div>
                )}

                {/* protocol_category tags */}
                {detailEntry.protocol_category && detailEntry.protocol_category.length > 0 && (
                  <div style={{ marginBottom: '0.75rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
                      <Tag size={14} style={{ color: 'var(--text-secondary)' }} />
                      <span style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', fontWeight: 600, textTransform: 'uppercase' }}>
                        Protocol Category
                      </span>
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap' }}>
                      {renderTags(detailEntry.protocol_category, 'var(--medium)')}
                    </div>
                  </div>
                )}

                {/* related_swc tags */}
                {detailEntry.related_swc && detailEntry.related_swc.length > 0 && (
                  <div style={{ marginBottom: '1rem' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '6px', marginBottom: '6px' }}>
                      <Tag size={14} style={{ color: 'var(--text-secondary)' }} />
                      <span style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', fontWeight: 600, textTransform: 'uppercase' }}>
                        Related SWC
                      </span>
                    </div>
                    <div style={{ display: 'flex', flexWrap: 'wrap' }}>
                      {renderTags(detailEntry.related_swc, 'var(--low)')}
                    </div>
                  </div>
                )}

                {/* Divider */}
                <hr style={{ border: 'none', borderTop: '1px solid var(--border-color)', margin: '1rem 0' }} />

                {/* Full body text */}
                <div>
                  <span style={{ color: 'var(--text-secondary)', fontSize: '0.8rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
                    Full Text
                  </span>
                  <pre
                    style={{
                      marginTop: '0.5rem',
                      whiteSpace: 'pre-wrap',
                      wordBreak: 'break-word',
                      fontFamily: "'Fira Code', 'Courier New', Courier, monospace",
                      fontSize: '0.82rem',
                      lineHeight: 1.7,
                      color: 'var(--text-secondary)',
                      background: 'var(--bg-surface)',
                      padding: '1rem',
                      borderRadius: '8px',
                      border: '1px solid var(--border-color)',
                      maxHeight: '400px',
                      overflowY: 'auto',
                    }}
                  >
                    {detailEntry.body}
                  </pre>
                </div>
              </div>
            ) : null}
          </div>
        )}
      </div>
    </div>
  );
}
