import { useState, useEffect, useCallback } from 'react';
import {
  Shield,
  AlertTriangle,
  ChevronDown,
  ChevronRight,
  Loader2,
  FileCode2,
  CheckSquare,
  ExternalLink,
  Scan,
  Fingerprint,
} from 'lucide-react';

const API_BASE = 'http://127.0.0.1:8000';

const SEVERITY_COLORS = {
  critical: '#ff4757',
  high: '#ff6b6b',
  medium: '#ffa502',
};

const SEVERITY_ORDER = { critical: 0, high: 1, medium: 2, low: 3, informational: 4 };

function severityColor(severity) {
  return SEVERITY_COLORS[severity?.toLowerCase()] || '#79c0ff';
}

function severityClass(severity) {
  const s = severity?.toLowerCase();
  if (s === 'critical') return 'severity-critical';
  if (s === 'high') return 'severity-high';
  if (s === 'medium') return 'severity-medium';
  if (s === 'low') return 'severity-low';
  return 'severity-informational';
}

/* ---------- sub-components ---------- */

function SignaturesBar({ signatures }) {
  if (!signatures) return null;

  const severityCounts = {};
  (signatures.patterns || signatures || []).forEach((p) => {
    const s = (p.severity || 'info').toLowerCase();
    severityCounts[s] = (severityCounts[s] || 0) + 1;
  });

  const total =
    Object.values(severityCounts).reduce((a, b) => a + b, 0) || 0;

  return (
    <div className="glass-panel animate-fade-in" style={{ marginBottom: '1.5rem', display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
      <Fingerprint size={18} style={{ color: 'var(--primary)', flexShrink: 0 }} />
      <span style={{ fontWeight: 600, color: 'var(--text-primary)', marginRight: 4 }}>
        {total} pattern signatures loaded
      </span>
      {Object.entries(severityCounts)
        .sort(([a], [b]) => (SEVERITY_ORDER[a] ?? 99) - (SEVERITY_ORDER[b] ?? 99))
        .map(([sev, count]) => (
          <span key={sev} className={`badge ${severityClass(sev)}`}>
            {count} {sev}
          </span>
        ))}
    </div>
  );
}

function SummaryBar({ matches }) {
  const total = matches.length;
  const criticalCount = matches.filter((m) => m.severity?.toLowerCase() === 'critical').length;
  const highCount = matches.filter((m) => m.severity?.toLowerCase() === 'high').length;

  return (
    <div
      className="glass-panel animate-fade-in"
      style={{
        display: 'flex',
        alignItems: 'center',
        gap: '0.75rem',
        marginBottom: '1.5rem',
        flexWrap: 'wrap',
      }}
    >
      <Shield size={20} style={{ color: 'var(--primary)' }} />
      <span style={{ fontWeight: 600 }}>
        {total} pattern{total !== 1 ? 's' : ''} detected
      </span>
      <span style={{ color: 'var(--text-secondary)' }}>—</span>
      {criticalCount > 0 && (
        <span style={{ fontWeight: 700, color: SEVERITY_COLORS.critical }}>
          {criticalCount} Critical
        </span>
      )}
      {highCount > 0 && (
        <span style={{ fontWeight: 700, color: SEVERITY_COLORS.high }}>
          {highCount} High
        </span>
      )}
      {criticalCount === 0 && highCount === 0 && (
        <span style={{ color: 'var(--text-secondary)' }}>No critical or high findings</span>
      )}
    </div>
  );
}

function ConfidenceBar({ confidence, severity }) {
  const pct = Math.min(100, Math.max(0, confidence ?? 0));
  const color = severityColor(severity);

  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', margin: '0.75rem 0' }}>
      <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)', minWidth: 72 }}>
        Confidence
      </span>
      <div
        style={{
          flex: 1,
          height: 8,
          borderRadius: 4,
          background: 'rgba(255,255,255,0.06)',
          overflow: 'hidden',
        }}
      >
        <div
          style={{
            width: `${pct}%`,
            height: '100%',
            borderRadius: 4,
            background: color,
            transition: 'width 0.5s ease',
          }}
        />
      </div>
      <span style={{ fontSize: '0.85rem', fontWeight: 600, color, minWidth: 40, textAlign: 'right' }}>
        {pct}%
      </span>
    </div>
  );
}

function MatchedLines({ lines, severity }) {
  if (!lines || lines.length === 0) return null;
  const sev = severity?.toLowerCase();
  const highlightBg =
    sev === 'critical'
      ? 'rgba(255, 71, 87, 0.12)'
      : sev === 'high'
        ? 'rgba(255, 107, 107, 0.12)'
        : 'transparent';
  const highlightBorder =
    sev === 'critical'
      ? SEVERITY_COLORS.critical
      : sev === 'high'
        ? SEVERITY_COLORS.high
        : 'transparent';

  return (
    <div style={{ marginTop: '0.75rem' }}>
      <h4 style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.5rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
        Matched Lines
      </h4>
      <div
        style={{
          background: '#0d1117',
          borderRadius: 8,
          padding: '0.75rem 1rem',
          overflowX: 'auto',
          border: '1px solid var(--border-color)',
        }}
      >
        {lines.map((line, i) => (
          <div
            key={i}
            style={{
              fontFamily: "'Fira Code', 'Courier New', monospace",
              fontSize: '0.82rem',
              lineHeight: 1.7,
              padding: '2px 6px',
              borderRadius: 4,
              background: highlightBg,
              borderLeft: highlightBorder !== 'transparent' ? `3px solid ${highlightBorder}` : '3px solid transparent',
              marginBottom: 2,
            }}
          >
            <span style={{ color: 'var(--text-secondary)', marginRight: 12, userSelect: 'none' }}>
              L{line.number ?? line.line_number ?? i + 1}:
            </span>
            <span style={{ color: 'var(--text-primary)' }}>{line.content ?? line.text ?? String(line)}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

function AuditChecklist({ items }) {
  if (!items || items.length === 0) return null;

  return (
    <div style={{ marginTop: '0.75rem' }}>
      <h4 style={{ fontSize: '0.85rem', color: 'var(--text-secondary)', marginBottom: '0.5rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>
        Audit Checklist
      </h4>
      <ul style={{ listStyle: 'none', padding: 0, margin: 0 }}>
        {items.map((item, i) => (
          <li
            key={i}
            style={{
              display: 'flex',
              alignItems: 'flex-start',
              gap: '0.5rem',
              padding: '4px 0',
              fontSize: '0.88rem',
              color: 'var(--text-primary)',
            }}
          >
            <CheckSquare size={16} style={{ color: 'var(--text-secondary)', flexShrink: 0, marginTop: 2 }} />
            <span>{typeof item === 'string' ? item : item.label ?? item.text ?? JSON.stringify(item)}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

function MatchCard({ match, onSelectPattern }) {
  const [expanded, setExpanded] = useState(false);
  const sev = match.severity?.toLowerCase() || 'medium';

  return (
    <div
      className="glass-panel animate-fade-in"
      style={{
        marginBottom: '1rem',
        cursor: 'pointer',
        transition: 'border-color 0.2s ease, box-shadow 0.2s ease',
        borderLeft: `3px solid ${severityColor(sev)}`,
      }}
    >
      {/* Header – always visible */}
      <div
        onClick={() => setExpanded((v) => !v)}
        style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}
      >
        {expanded ? (
          <ChevronDown size={18} style={{ color: 'var(--text-secondary)', flexShrink: 0 }} />
        ) : (
          <ChevronRight size={18} style={{ color: 'var(--text-secondary)', flexShrink: 0 }} />
        )}
        <span style={{ fontWeight: 600, flex: 1 }}>{match.title || match.pattern || match.name}</span>
        <span className={`badge ${severityClass(sev)}`}>{sev}</span>
      </div>

      {/* Expanded body */}
      {expanded && (
        <div style={{ marginTop: '0.75rem', paddingLeft: 26 }}>
          <ConfidenceBar confidence={match.confidence} severity={sev} />
          <MatchedLines lines={match.matched_lines || match.lines || []} severity={sev} />
          <AuditChecklist items={match.audit_checklist || match.checklist || []} />

          {/* Link to full pattern */}
          {match.slug && onSelectPattern && (
            <button
              onClick={(e) => {
                e.stopPropagation();
                onSelectPattern(match.slug);
              }}
              style={{
                marginTop: '0.75rem',
                display: 'inline-flex',
                alignItems: 'center',
                gap: 6,
                background: 'none',
                border: '1px solid var(--border-color)',
                borderRadius: 6,
                padding: '6px 14px',
                color: 'var(--primary)',
                cursor: 'pointer',
                fontSize: '0.85rem',
                fontWeight: 500,
                transition: 'background 0.2s ease',
              }}
              onMouseEnter={(e) => (e.currentTarget.style.background = 'var(--bg-surface-hover)')}
              onMouseLeave={(e) => (e.currentTarget.style.background = 'none')}
            >
              <ExternalLink size={14} />
              View Full Pattern
            </button>
          )}
        </div>
      )}
    </div>
  );
}

/* ---------- main component ---------- */

export default function Scanner({ onSelectPattern }) {
  const [sourceCode, setSourceCode] = useState('');
  const [scanning, setScanning] = useState(false);
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [signatures, setSignatures] = useState(null);

  /* Fetch signatures on mount */
  useEffect(() => {
    fetch(`${API_BASE}/api/scan/signatures`)
      .then((r) => r.json())
      .then(setSignatures)
      .catch(() => {});
  }, []);

  const handleScan = useCallback(async () => {
    if (!sourceCode.trim()) return;
    setScanning(true);
    setError(null);
    setResults(null);

    try {
      const res = await fetch(`${API_BASE}/api/scan`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ source_code: sourceCode, name: 'pasted contract' }),
      });

      if (!res.ok) throw new Error(`Server responded with ${res.status}`);
      const data = await res.json();
      setResults(data);
    } catch (err) {
      setError(err.message || 'Scan failed');
    } finally {
      setScanning(false);
    }
  }, [sourceCode]);

  /* Sort matches by severity */
  const sortedMatches = (results?.matches || results?.results || [])
    .slice()
    .sort(
      (a, b) =>
        (SEVERITY_ORDER[a.severity?.toLowerCase()] ?? 99) -
        (SEVERITY_ORDER[b.severity?.toLowerCase()] ?? 99)
    );

  return (
    <div className="animate-fade-in" style={{ maxWidth: 960, margin: '0 auto' }}>
      {/* Signature summary */}
      <SignaturesBar signatures={signatures} />

      {/* Source code input */}
      <div className="glass-panel" style={{ marginBottom: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.75rem' }}>
          <FileCode2 size={20} style={{ color: 'var(--primary)' }} />
          <h3 style={{ margin: 0, fontSize: '1.1rem', fontWeight: 600 }}>Solidity Source</h3>
        </div>

        <textarea
          value={sourceCode}
          onChange={(e) => setSourceCode(e.target.value)}
          placeholder="Paste Solidity source code here..."
          spellCheck={false}
          style={{
            width: '100%',
            minHeight: 400,
            fontFamily: "'Fira Code', 'Courier New', monospace",
            fontSize: '0.88rem',
            lineHeight: 1.6,
            background: '#0d1117',
            color: 'var(--text-primary)',
            border: '1px solid var(--border-color)',
            borderRadius: 8,
            padding: '1rem',
            resize: 'vertical',
            outline: 'none',
            transition: 'border-color 0.2s ease, box-shadow 0.2s ease',
            boxSizing: 'border-box',
          }}
          onFocus={(e) => {
            e.target.style.borderColor = 'var(--primary)';
            e.target.style.boxShadow = '0 0 0 2px rgba(88, 166, 255, 0.3)';
          }}
          onBlur={(e) => {
            e.target.style.borderColor = 'var(--border-color)';
            e.target.style.boxShadow = 'none';
          }}
        />

        <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '0.75rem' }}>
          <button
            className="btn"
            onClick={handleScan}
            disabled={scanning || !sourceCode.trim()}
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: 8,
              opacity: scanning || !sourceCode.trim() ? 0.6 : 1,
              cursor: scanning || !sourceCode.trim() ? 'not-allowed' : 'pointer',
            }}
          >
            {scanning ? (
              <Loader2 size={18} className="spin-icon" style={{ animation: 'spin 1s linear infinite' }} />
            ) : (
              <Scan size={18} />
            )}
            {scanning ? 'Scanning…' : 'Scan Contract'}
          </button>
        </div>
      </div>

      {/* Error */}
      {error && (
        <div
          className="glass-panel animate-fade-in"
          style={{
            borderLeft: `3px solid ${SEVERITY_COLORS.critical}`,
            marginBottom: '1.5rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.75rem',
          }}
        >
          <AlertTriangle size={20} style={{ color: SEVERITY_COLORS.critical }} />
          <span style={{ color: SEVERITY_COLORS.critical, fontWeight: 500 }}>{error}</span>
        </div>
      )}

      {/* Results */}
      {results && (
        <div className="animate-fade-in">
          <SummaryBar matches={sortedMatches} />

          {sortedMatches.length === 0 && (
            <div
              className="glass-panel"
              style={{ textAlign: 'center', padding: '2rem', color: 'var(--text-secondary)' }}
            >
              <Shield size={36} style={{ marginBottom: '0.5rem', opacity: 0.5 }} />
              <p style={{ margin: 0 }}>No vulnerability patterns detected — looking clean!</p>
            </div>
          )}

          {sortedMatches.map((match, i) => (
            <MatchCard key={match.slug || i} match={match} onSelectPattern={onSelectPattern} />
          ))}
        </div>
      )}

      {/* Spinner keyframes (injected once) */}
      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}
