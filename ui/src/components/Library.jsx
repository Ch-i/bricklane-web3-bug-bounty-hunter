import React, { useEffect, useState } from 'react';
import { BookOpen, Circle, ArrowRight, Layers } from 'lucide-react';

const API_BASE = 'http://127.0.0.1:8000';

const DOMAIN_COLORS = {
  defi: '#58a6ff',
  security: '#ff7b72',
  economics: '#d2a8ff',
  infrastructure: '#a5d6ff',
  governance: '#ffa657',
  mev: '#f0883e',
};

const DOMAIN_FILTERS = [
  { key: 'all', label: 'All' },
  { key: 'defi', label: 'DeFi Primitives' },
  { key: 'security', label: 'Security Patterns' },
  { key: 'economics', label: 'Economic Logic' },
  { key: 'infrastructure', label: 'Infrastructure' },
  { key: 'governance', label: 'Governance' },
  { key: 'mev', label: 'MEV & Ordering' },
];

export default function Library({ onSelectPattern }) {
  const [patterns, setPatterns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [activeDomain, setActiveDomain] = useState('all');

  useEffect(() => {
    fetch(`${API_BASE}/api/library/patterns`)
      .then(r => {
        if (!r.ok) throw new Error(`HTTP ${r.status}`);
        return r.json();
      })
      .then(data => {
        setPatterns(data);
        setLoading(false);
      })
      .catch(e => {
        console.error(e);
        setError(e.message);
        setLoading(false);
      });
  }, []);

  const filtered = activeDomain === 'all'
    ? patterns
    : patterns.filter(p => p.domain === activeDomain);

  if (loading) {
    return (
      <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
        <Layers size={32} style={{ marginBottom: '1rem', opacity: 0.5 }} />
        <div>Loading pattern library…</div>
      </div>
    );
  }

  if (error) {
    return (
      <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--critical)' }}>
        Failed to load patterns: {error}
      </div>
    );
  }

  return (
    <div className="animate-fade-in">
      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.5rem' }}>
        <BookOpen size={24} style={{ color: 'var(--primary)' }} />
        <h2 style={{ margin: 0, fontSize: '1.5rem', fontWeight: 700 }}>Pattern Library</h2>
        <span style={{ color: 'var(--text-secondary)', fontSize: '0.9rem', marginLeft: '0.5rem' }}>
          {filtered.length} pattern{filtered.length !== 1 ? 's' : ''}
        </span>
      </div>

      {/* Domain Filter Pills */}
      <div style={{
        display: 'flex',
        flexWrap: 'wrap',
        gap: '0.5rem',
        marginBottom: '2rem',
      }}>
        {DOMAIN_FILTERS.map(df => {
          const isActive = activeDomain === df.key;
          const color = df.key === 'all' ? 'var(--primary)' : (DOMAIN_COLORS[df.key] || 'var(--primary)');
          return (
            <button
              key={df.key}
              onClick={() => setActiveDomain(df.key)}
              style={{
                padding: '6px 16px',
                borderRadius: '20px',
                border: `1px solid ${isActive ? color : 'var(--border-color)'}`,
                background: isActive ? `${color}22` : 'transparent',
                color: isActive ? color : 'var(--text-secondary)',
                fontSize: '0.85rem',
                fontWeight: 600,
                cursor: 'pointer',
                transition: 'all 0.2s ease',
              }}
            >
              {df.label}
            </button>
          );
        })}
      </div>

      {/* Pattern Card Grid */}
      {filtered.length === 0 ? (
        <div style={{ padding: '3rem', textAlign: 'center', color: 'var(--text-secondary)' }}>
          No patterns found for this domain.
        </div>
      ) : (
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fill, minmax(320px, 1fr))',
          gap: '1.25rem',
        }}>
          {filtered.map(pattern => {
            const domainColor = DOMAIN_COLORS[pattern.domain] || 'var(--primary)';
            const isDone = pattern.status === 'done';

            return (
              <div
                key={pattern.slug}
                className="glass-panel"
                style={{
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '0.75rem',
                  transition: 'transform 0.2s ease, box-shadow 0.2s ease',
                  cursor: 'pointer',
                }}
                onMouseEnter={e => {
                  e.currentTarget.style.transform = 'translateY(-2px)';
                  e.currentTarget.style.boxShadow = '0 12px 40px 0 rgba(0,0,0,0.4)';
                }}
                onMouseLeave={e => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.boxShadow = '0 8px 32px 0 rgba(0,0,0,0.3)';
                }}
                onClick={() => onSelectPattern && onSelectPattern(pattern.slug)}
              >
                {/* Domain Tag */}
                <div>
                  <span style={{
                    display: 'inline-block',
                    padding: '2px 10px',
                    borderRadius: '10px',
                    fontSize: '0.7rem',
                    fontWeight: 600,
                    background: `${domainColor}22`,
                    color: domainColor,
                    border: `1px solid ${domainColor}44`,
                    textTransform: 'uppercase',
                    letterSpacing: '0.05em',
                  }}>
                    {pattern.domain_label}
                  </span>
                </div>

                {/* Title */}
                <h3 style={{
                  margin: 0,
                  fontSize: '1.05rem',
                  fontWeight: 700,
                  color: 'var(--text-primary)',
                  lineHeight: 1.3,
                }}>
                  {pattern.title}
                </h3>

                {/* Description */}
                <p style={{
                  margin: 0,
                  color: 'var(--text-secondary)',
                  fontSize: '0.85rem',
                  lineHeight: 1.6,
                  display: '-webkit-box',
                  WebkitLineClamp: 3,
                  WebkitBoxOrient: 'vertical',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  flex: 1,
                }}>
                  {pattern.description}
                </p>

                {/* Footer: Status + Read Link */}
                <div style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  marginTop: 'auto',
                  paddingTop: '0.75rem',
                  borderTop: '1px solid var(--border-color)',
                }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem' }}>
                    <Circle
                      size={8}
                      fill={isDone ? '#3fb950' : '#d29922'}
                      stroke="none"
                    />
                    <span style={{
                      fontSize: '0.78rem',
                      color: isDone ? '#3fb950' : '#d29922',
                      fontWeight: 500,
                    }}>
                      {isDone ? 'Synthesized' : 'Pending'}
                    </span>
                  </div>

                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      onSelectPattern && onSelectPattern(pattern.slug);
                    }}
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.35rem',
                      background: 'none',
                      border: 'none',
                      color: 'var(--primary)',
                      fontSize: '0.85rem',
                      fontWeight: 600,
                      cursor: 'pointer',
                      padding: 0,
                      transition: 'gap 0.2s ease',
                    }}
                    onMouseEnter={e => e.currentTarget.style.gap = '0.6rem'}
                    onMouseLeave={e => e.currentTarget.style.gap = '0.35rem'}
                  >
                    Read <ArrowRight size={14} />
                  </button>
                </div>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
