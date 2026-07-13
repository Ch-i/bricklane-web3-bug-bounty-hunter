import React, { useState, useRef, useEffect, useCallback } from 'react';

const API_BASE = 'http://127.0.0.1:8000';
import { Play, Pause, SkipForward, SkipBack, RotateCcw, ChevronRight, ExternalLink, Box, Hash } from 'lucide-react';

const CHAIN_COLORS = {
  'Ethereum': '#627EEA',
  'BSC': '#F0B90B',
  'Solana': '#9945FF',
  'Polygon': '#8247E5',
  'Arbitrum': '#28A0F0',
  'Optimism': '#FF0420',
  'Multi-chain': '#8b949e',
};

const EXPLORER_URLS = {
  'Ethereum': 'https://etherscan.io',
  'BSC': 'https://bscscan.com',
  'Polygon': 'https://polygonscan.com',
  'Arbitrum': 'https://arbiscan.io',
  'Optimism': 'https://optimistic.etherscan.io',
};

function getExplorerUrl(chain, type, value) {
  if (type === 'custom') return value; // already a full URL
  const base = EXPLORER_URLS[chain] || EXPLORER_URLS['Ethereum'];
  if (type === 'tx') return `${base}/tx/${value}`;
  if (type === 'address') return `${base}/address/${value}`;
  if (type === 'block') return `${base}/block/${value}`;
  return base;
}

function shortenHash(hash) {
  if (!hash || hash.length < 14) return hash || '';
  return hash.slice(0, 8) + '…' + hash.slice(-6);
}

const ACTOR_COLORS = {
  'Attacker': '#ff4757',
  'Victim': '#ffa502',
  'FlashLender': '#54a0ff',
  'Pool': '#2ed573',
  'DEX': '#2ed573',
  'Oracle': '#d2a8ff',
  'Vault': '#a5d6ff',
  'Proxy': '#a5d6ff',
  'Liquidator': '#ff6b6b',
  'Borrower': '#ffa657',
  'LendingPool': '#54a0ff',
  'PriceOracle': '#d2a8ff',
  'Token': '#2ed573',
  'Governance': '#ffa657',
  'default': '#8b949e',
};

function getActorColor(name) {
  for (const [key, color] of Object.entries(ACTOR_COLORS)) {
    if (name.toLowerCase().includes(key.toLowerCase())) return color;
  }
  return ACTOR_COLORS.default;
}

const SEVERITY_GLOW = {
  'Critical': 'rgba(255, 71, 87, 0.15)',
  'High': 'rgba(255, 107, 107, 0.12)',
  'Medium': 'rgba(255, 165, 2, 0.1)',
};

export default function SimulationNotebook({ simulation, onStepClick }) {
  const [currentStep, setCurrentStep] = useState(-1); // -1 = initial state
  const [isPlaying, setIsPlaying] = useState(false);
  const [speed, setSpeed] = useState(1500); // ms per step
  const [selectedIncident, setSelectedIncident] = useState(0);
  const [verifyResult, setVerifyResult] = useState(null);
  const [verifyLoading, setVerifyLoading] = useState(false);

  const verifyOnChain = () => {
    if (!activeIncident?.tx_hash) return;
    const verifyChain = activeIncident.chain || chain || 'Ethereum';
    setVerifyLoading(true);
    setVerifyResult(null);
    fetch(`${API_BASE}/api/verify/tx/${encodeURIComponent(verifyChain)}/${encodeURIComponent(activeIncident.tx_hash)}`)
      .then(r => r.json())
      .then(data => {
        setVerifyResult(data);
        setVerifyLoading(false);
      })
      .catch(err => {
        setVerifyResult({ verified: false, error: err.message });
        setVerifyLoading(false);
      });
  };
  const canvasRef = useRef(null);
  const containerRef = useRef(null);
  const intervalRef = useRef(null);

  if (!simulation || !simulation.steps || simulation.steps.length === 0) {
    return null;
  }

  const { title, actors, steps, initial_state, incidents, chain } = simulation;
  const totalSteps = steps.length;
  const activeIncident = incidents && incidents.length > 0 ? incidents[selectedIncident] : null;
  const incidentChain = activeIncident?.chain || chain || 'Ethereum';

  // Compute current state at step N
  const computeState = useCallback((upToStep) => {
    const state = { ...(initial_state || {}) };
    for (let i = 0; i <= upToStep && i < steps.length; i++) {
      if (steps[i].state_changes) {
        Object.entries(steps[i].state_changes).forEach(([k, v]) => {
          state[k] = v;
        });
      }
    }
    return state;
  }, [steps, initial_state]);

  const currentState = computeState(currentStep);

  // Auto-play
  useEffect(() => {
    if (isPlaying) {
      intervalRef.current = setInterval(() => {
        setCurrentStep(prev => {
          if (prev >= totalSteps - 1) {
            setIsPlaying(false);
            return prev;
          }
          return prev + 1;
        });
      }, speed);
    }
    return () => clearInterval(intervalRef.current);
  }, [isPlaying, speed, totalSteps]);

  const reset = () => { setCurrentStep(-1); setIsPlaying(false); };
  const nextStep = () => { if (currentStep < totalSteps - 1) setCurrentStep(s => s + 1); };
  const prevStep = () => { if (currentStep > -1) setCurrentStep(s => s - 1); };
  const togglePlay = () => setIsPlaying(!isPlaying);

  // Draw canvas
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;
    const w = containerRef.current?.clientWidth || 400;
    const actorCount = actors.length;
    const actorSpacing = w / (actorCount + 1);
    const headerHeight = 70;
    const stepHeight = 60;
    const h = headerHeight + (totalSteps + 1) * stepHeight + 30;

    canvas.width = w * dpr;
    canvas.height = h * dpr;
    canvas.style.width = w + 'px';
    canvas.style.height = h + 'px';
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);

    // Background
    ctx.fillStyle = '#0d1117';
    ctx.fillRect(0, 0, w, h);

    // Subtle grid
    ctx.strokeStyle = 'rgba(255,255,255,0.02)';
    ctx.lineWidth = 0.5;
    for (let gx = 0; gx < w; gx += 30) {
      ctx.beginPath(); ctx.moveTo(gx, 0); ctx.lineTo(gx, h); ctx.stroke();
    }
    for (let gy = 0; gy < h; gy += 30) {
      ctx.beginPath(); ctx.moveTo(0, gy); ctx.lineTo(w, gy); ctx.stroke();
    }

    // Actor positions
    const actorPositions = actors.map((a, i) => ({
      name: a,
      x: actorSpacing * (i + 1),
      color: getActorColor(a),
    }));

    // Draw actor lifelines
    actorPositions.forEach(a => {
      ctx.strokeStyle = a.color + '20';
      ctx.lineWidth = 1;
      ctx.setLineDash([4, 4]);
      ctx.beginPath();
      ctx.moveTo(a.x, headerHeight);
      ctx.lineTo(a.x, h - 10);
      ctx.stroke();
      ctx.setLineDash([]);
    });

    // Draw actor boxes (header)
    actorPositions.forEach(a => {
      const boxW = Math.min(90, actorSpacing - 10);
      const boxH = 32;
      const bx = a.x - boxW / 2;
      const by = 20;

      // Glow
      ctx.shadowColor = a.color;
      ctx.shadowBlur = 8;
      ctx.fillStyle = a.color + '22';
      ctx.strokeStyle = a.color + '66';
      ctx.lineWidth = 1;
      roundRect(ctx, bx, by, boxW, boxH, 6);
      ctx.fill();
      ctx.stroke();
      ctx.shadowBlur = 0;

      // Label
      ctx.font = 'bold 11px "Fira Code", monospace';
      ctx.fillStyle = a.color;
      ctx.textAlign = 'center';
      ctx.fillText(truncate(a.name, 12), a.x, by + 21);
    });

    // Draw steps
    steps.forEach((step, i) => {
      const isActive = i <= currentStep;
      const isCurrent = i === currentStep;
      const y = headerHeight + (i + 1) * stepHeight;

      const fromIdx = actors.indexOf(step.from);
      const toIdx = actors.indexOf(step.to);
      if (fromIdx < 0 || toIdx < 0) return;

      const fromX = actorPositions[fromIdx].x;
      const toX = actorPositions[toIdx].x;
      const fromColor = actorPositions[fromIdx].color;

      // Step number
      ctx.font = '10px monospace';
      ctx.fillStyle = isActive ? '#e6edf3' : '#30363d';
      ctx.textAlign = 'left';
      ctx.fillText(`${i + 1}`, 6, y + 4);

      if (!isActive) {
        // Dim future steps
        ctx.globalAlpha = 0.15;
      }

      if (isCurrent) {
        // Highlight current step
        ctx.fillStyle = SEVERITY_GLOW[simulation.severity] || 'rgba(88,166,255,0.08)';
        ctx.fillRect(0, y - stepHeight / 2 + 5, w, stepHeight - 10);
      }

      // Arrow line
      ctx.strokeStyle = fromColor;
      ctx.lineWidth = isCurrent ? 2.5 : 1.5;
      ctx.beginPath();
      ctx.moveTo(fromX, y);
      ctx.lineTo(toX, y);
      ctx.stroke();

      // Arrowhead
      const dir = toX > fromX ? 1 : -1;
      const arrowSize = 7;
      ctx.fillStyle = fromColor;
      ctx.beginPath();
      ctx.moveTo(toX, y);
      ctx.lineTo(toX - dir * arrowSize, y - arrowSize / 2);
      ctx.lineTo(toX - dir * arrowSize, y + arrowSize / 2);
      ctx.closePath();
      ctx.fill();

      // Action label (above arrow)
      const midX = (fromX + toX) / 2;
      ctx.font = isCurrent ? 'bold 10px "Fira Code", monospace' : '10px "Fira Code", monospace';
      ctx.fillStyle = isCurrent ? '#e6edf3' : '#8b949e';
      ctx.textAlign = 'center';
      ctx.fillText(truncate(step.action, 35), midX, y - 8);

      // Description (below arrow, smaller)
      if (step.description && isCurrent) {
        ctx.font = '9px Inter, system-ui, sans-serif';
        ctx.fillStyle = '#8b949e';
        ctx.fillText(truncate(step.description, 45), midX, y + 16);
      }

      ctx.globalAlpha = 1;
    });
  }, [currentStep, actors, steps, totalSteps, simulation]);

  return (
    <div className="glass-panel" style={{ overflow: 'hidden' }}>
      {/* Real Incident Header */}
      {incidents && incidents.length > 0 && (
        <div style={{
          padding: '10px 16px',
          borderBottom: '1px solid rgba(255,255,255,0.06)',
          background: 'rgba(255,75,87,0.04)',
        }}>
          <div style={{ fontSize: 10, color: '#8b949e', textTransform: 'uppercase', letterSpacing: 1, marginBottom: 6, fontWeight: 600, display: 'flex', alignItems: 'center', gap: 4 }}>
            <Box size={10} /> Real-World Incident{incidents.length > 1 ? 's' : ''}
          </div>
          {/* Incident selector tabs */}
          {incidents.length > 1 && (
            <div style={{ display: 'flex', gap: 4, marginBottom: 8 }}>
              {incidents.map((inc, i) => (
                <button
                  key={i}
                  onClick={() => setSelectedIncident(i)}
                  style={{
                    background: i === selectedIncident ? 'rgba(255,75,87,0.15)' : 'rgba(255,255,255,0.03)',
                    border: `1px solid ${i === selectedIncident ? 'rgba(255,75,87,0.3)' : 'rgba(255,255,255,0.06)'}`,
                    color: i === selectedIncident ? '#ff4757' : '#8b949e',
                    borderRadius: 4,
                    padding: '3px 8px',
                    fontSize: 10,
                    cursor: 'pointer',
                    fontWeight: i === selectedIncident ? 700 : 400,
                    transition: 'all 0.2s',
                  }}
                >
                  {inc.name}
                </button>
              ))}
            </div>
          )}
          {/* Active incident detail */}
          {activeIncident && (
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 6 }}>
                <span style={{ color: '#e6edf3', fontSize: 13, fontWeight: 700 }}>{activeIncident.name}</span>
                <span style={{
                  fontSize: 10, padding: '1px 6px', borderRadius: 4,
                  background: (CHAIN_COLORS[activeIncident.chain || chain] || '#8b949e') + '22',
                  color: CHAIN_COLORS[activeIncident.chain || chain] || '#8b949e',
                  fontWeight: 600,
                }}>
                  {activeIncident.chain || chain}
                </span>
                {activeIncident.loss_usd && (
                  <span style={{ fontSize: 11, color: '#ffa657', fontWeight: 700 }}>
                    {activeIncident.loss_usd}
                  </span>
                )}
                {activeIncident.date && (
                  <span style={{ fontSize: 10, color: '#8b949e' }}>{activeIncident.date}</span>
                )}
              </div>
              {/* Tx Hash */}
              {activeIncident.tx_hash && (
                <a
                  href={activeIncident.etherscan || activeIncident.explorer || getExplorerUrl(activeIncident.chain || chain, 'tx', activeIncident.tx_hash)}
                  target="_blank"
                  rel="noopener noreferrer"
                  style={{
                    display: 'flex', alignItems: 'center', gap: 4,
                    fontSize: 11, fontFamily: '"Fira Code", monospace',
                    color: '#58a6ff', textDecoration: 'none',
                    marginBottom: 4,
                    transition: 'color 0.2s',
                  }}
                  onMouseEnter={e => e.currentTarget.style.color = '#79c0ff'}
                  onMouseLeave={e => e.currentTarget.style.color = '#58a6ff'}
                >
                  <Hash size={10} />
                  <span>tx: {shortenHash(activeIncident.tx_hash)}</span>
                  <ExternalLink size={10} />
                </a>
              )}
              {/* Addresses */}
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
                {activeIncident.attacker && (
                  <a
                    href={getExplorerUrl(activeIncident.chain || chain, 'address', activeIncident.attacker)}
                    target="_blank" rel="noopener noreferrer"
                    style={{ ...addrTagStyle, color: '#ff4757', background: 'rgba(255,71,87,0.08)', borderColor: 'rgba(255,71,87,0.2)' }}
                  >
                    Attacker: {shortenHash(activeIncident.attacker)} <ExternalLink size={9} />
                  </a>
                )}
                {activeIncident.contract && (
                  <a
                    href={getExplorerUrl(activeIncident.chain || chain, 'address', activeIncident.contract)}
                    target="_blank" rel="noopener noreferrer"
                    style={{ ...addrTagStyle, color: '#58a6ff', background: 'rgba(88,166,255,0.08)', borderColor: 'rgba(88,166,255,0.2)' }}
                  >
                    Contract: {shortenHash(activeIncident.contract)} <ExternalLink size={9} />
                  </a>
                )}
                {activeIncident.block && (
                  <a
                    href={getExplorerUrl(activeIncident.chain || chain, 'block', activeIncident.block)}
                    target="_blank" rel="noopener noreferrer"
                    style={{ ...addrTagStyle, color: '#8b949e', background: 'rgba(255,255,255,0.03)', borderColor: 'rgba(255,255,255,0.08)' }}
                  >
                    Block #{activeIncident.block.toLocaleString()} <ExternalLink size={9} />
                  </a>
                )}
              </div>

              {/* Verify button */}
              {activeIncident.tx_hash && (
                <button
                  onClick={verifyOnChain}
                  disabled={verifyLoading}
                  style={{
                    marginTop: 8,
                    display: 'inline-flex', alignItems: 'center', gap: 5,
                    padding: '5px 12px', borderRadius: 6,
                    fontSize: 11, fontWeight: 600,
                    cursor: verifyLoading ? 'wait' : 'pointer',
                    background: verifyResult?.verified ? 'rgba(63,185,80,0.12)' : 'rgba(88,166,255,0.1)',
                    border: `1px solid ${verifyResult?.verified ? 'rgba(63,185,80,0.3)' : 'rgba(88,166,255,0.25)'}`,
                    color: verifyResult?.verified ? '#3fb950' : '#58a6ff',
                    transition: 'all 0.2s',
                  }}
                >
                  {verifyLoading ? (
                    <><span style={{ display: 'inline-block', width: 12, height: 12, border: '2px solid rgba(88,166,255,0.3)', borderTopColor: '#58a6ff', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }} /> Querying mainnet…</>
                  ) : verifyResult?.verified ? (
                    <><span style={{ fontSize: 14 }}>✓</span> Verified on {activeIncident.chain || chain}</>
                  ) : (
                    <><span style={{ fontSize: 14 }}>⛓</span> Verify On-Chain</>
                  )}
                </button>
              )}
            </div>
          )}

          {/* Verification proof panel */}
          {verifyResult && (
            <div style={{
              marginTop: 8, padding: '10px 14px',
              background: verifyResult.verified ? 'rgba(63,185,80,0.05)' : 'rgba(255,71,87,0.05)',
              borderRadius: 8,
              border: `1px solid ${verifyResult.verified ? 'rgba(63,185,80,0.15)' : 'rgba(255,71,87,0.15)'}`,
            }}>
              {verifyResult.verified ? (
                <>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 8 }}>
                    <span style={{ background: '#3fb950', color: '#0d1117', fontWeight: 800, fontSize: 10, padding: '2px 8px', borderRadius: 4, textTransform: 'uppercase', letterSpacing: 1 }}>✓ VERIFIED</span>
                    <span style={{ fontSize: 10, color: '#8b949e' }}>via {verifyResult.source}</span>
                  </div>
                  <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '4px 12px', fontSize: 11 }}>
                    <div style={proofRowStyle}><span style={proofLabelStyle}>Block</span><span style={proofValueStyle}>#{verifyResult.on_chain.block_number.toLocaleString()}</span></div>
                    <div style={proofRowStyle}><span style={proofLabelStyle}>Status</span><span style={{ ...proofValueStyle, color: verifyResult.on_chain.status === 'Success' ? '#3fb950' : '#ff4757' }}>{verifyResult.on_chain.status}</span></div>
                    <div style={proofRowStyle}><span style={proofLabelStyle}>From</span><span style={proofValueStyle}>{shortenHash(verifyResult.on_chain.from)}</span></div>
                    <div style={proofRowStyle}><span style={proofLabelStyle}>To</span><span style={proofValueStyle}>{shortenHash(verifyResult.on_chain.to)}</span></div>
                    <div style={proofRowStyle}><span style={proofLabelStyle}>Gas Used</span><span style={proofValueStyle}>{verifyResult.on_chain.gas_used.toLocaleString()}</span></div>
                    <div style={proofRowStyle}><span style={proofLabelStyle}>Tx Fee</span><span style={proofValueStyle}>{verifyResult.on_chain.tx_fee} ETH</span></div>
                    <div style={proofRowStyle}><span style={proofLabelStyle}>Event Logs</span><span style={proofValueStyle}>{verifyResult.on_chain.log_count}</span></div>
                    <div style={proofRowStyle}><span style={proofLabelStyle}>Contracts</span><span style={proofValueStyle}>{verifyResult.on_chain.contracts_touched} touched</span></div>
                    <div style={proofRowStyle}><span style={proofLabelStyle}>Calldata</span><span style={proofValueStyle}>{verifyResult.on_chain.input_data_size} bytes</span></div>
                    <div style={proofRowStyle}><span style={proofLabelStyle}>Value</span><span style={proofValueStyle}>{verifyResult.on_chain.value} ETH</span></div>
                  </div>
                  {verifyResult.on_chain.contract_addresses.length > 0 && (
                    <details style={{ marginTop: 6 }}>
                      <summary style={{ fontSize: 10, color: '#8b949e', cursor: 'pointer' }}>Contracts interacted ({verifyResult.on_chain.contracts_touched})</summary>
                      <div style={{ marginTop: 4, display: 'flex', flexWrap: 'wrap', gap: 4 }}>
                        {verifyResult.on_chain.contract_addresses.map((addr, i) => (
                          <a key={i} href={`${verifyResult.explorer_url.split('/tx/')[0]}/address/${addr}`} target="_blank" rel="noopener noreferrer"
                            style={{ fontSize: 9, fontFamily: '"Fira Code", monospace', color: '#58a6ff', textDecoration: 'none', padding: '1px 4px', background: 'rgba(88,166,255,0.06)', borderRadius: 3, border: '1px solid rgba(88,166,255,0.1)' }}>
                            {shortenHash(addr)}
                          </a>
                        ))}
                      </div>
                    </details>
                  )}
                </>
              ) : (
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 6, marginBottom: 6 }}>
                    <span style={{ background: '#d29922', color: '#0d1117', fontWeight: 800, fontSize: 10, padding: '2px 8px', borderRadius: 4, textTransform: 'uppercase' }}>ARCHIVE NEEDED</span>
                    <span style={{ fontSize: 11, color: '#8b949e' }}>Free RPCs only serve recent blocks</span>
                  </div>
                  <div style={{ fontSize: 11, color: '#8b949e', lineHeight: 1.6 }}>
                    Historical exploit transactions require an archive node. Verify manually:
                  </div>
                  {verifyResult.explorer_url && (
                    <a href={verifyResult.explorer_url} target="_blank" rel="noopener noreferrer"
                      style={{ display: 'inline-flex', alignItems: 'center', gap: 4, marginTop: 6, fontSize: 11, color: '#58a6ff', textDecoration: 'none', padding: '4px 10px', background: 'rgba(88,166,255,0.08)', borderRadius: 5, border: '1px solid rgba(88,166,255,0.15)' }}>
                      <ExternalLink size={11} /> Open on Etherscan →
                    </a>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      )}

      {/* Playback Header */}
      <div style={{ padding: '12px 16px', borderBottom: '1px solid rgba(255,255,255,0.06)' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 8 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
            <span style={{
              width: 8, height: 8, borderRadius: '50%',
              background: isPlaying ? '#3fb950' : '#8b949e',
              boxShadow: isPlaying ? '0 0 8px #3fb950' : 'none',
              display: 'inline-block',
            }} />
            <span style={{ color: '#e6edf3', fontSize: 13, fontWeight: 700 }}>
              {title || 'Transaction Trace'}
            </span>
          </div>
          <span style={{ color: '#8b949e', fontSize: 11, fontFamily: 'monospace' }}>
            Step {currentStep + 1}/{totalSteps}
          </span>
        </div>

        {/* Controls */}
        <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
          <button onClick={reset} style={ctrlBtnStyle} title="Reset">
            <RotateCcw size={14} />
          </button>
          <button onClick={prevStep} style={ctrlBtnStyle} title="Previous" disabled={currentStep <= -1}>
            <SkipBack size={14} />
          </button>
          <button onClick={togglePlay} style={{
            ...ctrlBtnStyle,
            background: isPlaying ? 'rgba(63,185,80,0.15)' : 'rgba(88,166,255,0.15)',
            color: isPlaying ? '#3fb950' : '#58a6ff',
            border: `1px solid ${isPlaying ? 'rgba(63,185,80,0.3)' : 'rgba(88,166,255,0.3)'}`,
            padding: '5px 14px',
          }} title={isPlaying ? 'Pause' : 'Play'}>
            {isPlaying ? <Pause size={14} /> : <Play size={14} />}
            <span style={{ fontSize: 11, marginLeft: 4 }}>{isPlaying ? 'Pause' : 'Play'}</span>
          </button>
          <button onClick={nextStep} style={ctrlBtnStyle} title="Next" disabled={currentStep >= totalSteps - 1}>
            <SkipForward size={14} />
          </button>
          <select
            value={speed}
            onChange={e => setSpeed(Number(e.target.value))}
            style={{
              background: 'rgba(255,255,255,0.05)',
              border: '1px solid rgba(255,255,255,0.1)',
              color: '#8b949e',
              borderRadius: 4,
              padding: '3px 6px',
              fontSize: 11,
              marginLeft: 'auto',
            }}
          >
            <option value={2500}>0.5x</option>
            <option value={1500}>1x</option>
            <option value={800}>2x</option>
            <option value={400}>4x</option>
          </select>
        </div>
      </div>

      {/* Canvas */}
      <div ref={containerRef} style={{ padding: 0 }}>
        <canvas ref={canvasRef} style={{ display: 'block', width: '100%' }} />
      </div>

      {/* State panel */}
      {currentStep >= 0 && Object.keys(currentState).length > 0 && (
        <div style={{
          padding: '10px 16px',
          borderTop: '1px solid rgba(255,255,255,0.06)',
          background: 'rgba(255,255,255,0.02)',
        }}>
          <div style={{ fontSize: 10, color: '#8b949e', textTransform: 'uppercase', letterSpacing: 1, marginBottom: 6, fontWeight: 600 }}>
            Current State
          </div>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
            {Object.entries(currentState).map(([key, value]) => {
              const changed = currentStep >= 0 && steps[currentStep]?.state_changes?.[key];
              return (
                <div key={key} style={{
                  background: changed ? 'rgba(255,75,87,0.08)' : 'rgba(255,255,255,0.03)',
                  border: `1px solid ${changed ? 'rgba(255,75,87,0.2)' : 'rgba(255,255,255,0.06)'}`,
                  borderRadius: 6,
                  padding: '4px 8px',
                  fontSize: 11,
                  fontFamily: '"Fira Code", monospace',
                  transition: 'all 0.3s ease',
                }}>
                  <span style={{ color: '#8b949e' }}>{key}: </span>
                  <span style={{ color: changed ? '#ff4757' : '#e6edf3', fontWeight: changed ? 700 : 400 }}>
                    {value}
                  </span>
                </div>
              );
            })}
          </div>
        </div>
      )}

      {/* Current step detail */}
      {currentStep >= 0 && steps[currentStep] && (
        <div style={{
          padding: '10px 16px',
          borderTop: '1px solid rgba(255,255,255,0.06)',
        }}>
          <div style={{ display: 'flex', gap: 8, alignItems: 'flex-start' }}>
            <ChevronRight size={14} style={{ color: '#58a6ff', marginTop: 2, flexShrink: 0 }} />
            <div style={{ flex: 1, minWidth: 0 }}>
              <div style={{ color: '#e6edf3', fontSize: 12, fontWeight: 600, fontFamily: '"Fira Code", monospace' }}>
                {steps[currentStep].action}
              </div>
              <div style={{ color: '#8b949e', fontSize: 11, marginTop: 2 }}>
                {steps[currentStep].description}
              </div>
              {/* Per-step tx hash */}
              {steps[currentStep].tx_hash && (
                <a
                  href={getExplorerUrl(incidentChain, 'tx', steps[currentStep].tx_hash)}
                  target="_blank" rel="noopener noreferrer"
                  style={{
                    display: 'inline-flex', alignItems: 'center', gap: 3,
                    fontSize: 10, fontFamily: '"Fira Code", monospace',
                    color: '#58a6ff', textDecoration: 'none',
                    marginTop: 4,
                    padding: '2px 6px', borderRadius: 3,
                    background: 'rgba(88,166,255,0.06)',
                    border: '1px solid rgba(88,166,255,0.15)',
                  }}
                >
                  <Hash size={9} /> {shortenHash(steps[currentStep].tx_hash)} <ExternalLink size={9} />
                </a>
              )}
              {steps[currentStep].code && (
                <pre style={{
                  marginTop: 6,
                  padding: '6px 10px',
                  background: 'rgba(0,0,0,0.3)',
                  borderRadius: 4,
                  fontSize: 10,
                  color: '#7ee787',
                  fontFamily: '"Fira Code", monospace',
                  overflow: 'auto',
                  border: '1px solid rgba(255,255,255,0.05)',
                }}>
                  {steps[currentStep].code}
                </pre>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

const ctrlBtnStyle = {
  background: 'rgba(255,255,255,0.05)',
  border: '1px solid rgba(255,255,255,0.1)',
  color: '#8b949e',
  borderRadius: 6,
  padding: '5px 8px',
  cursor: 'pointer',
  display: 'flex',
  alignItems: 'center',
  gap: 4,
  transition: 'all 0.2s',
};

const addrTagStyle = {
  display: 'inline-flex',
  alignItems: 'center',
  gap: 3,
  fontSize: 10,
  fontFamily: '"Fira Code", monospace',
  textDecoration: 'none',
  padding: '2px 6px',
  borderRadius: 4,
  border: '1px solid',
  transition: 'opacity 0.2s',
};

const proofRowStyle = { display: 'flex', justifyContent: 'space-between', padding: '2px 0' };
const proofLabelStyle = { color: '#8b949e', fontFamily: '"Fira Code", monospace' };
const proofValueStyle = { color: '#e6edf3', fontWeight: 600, fontFamily: '"Fira Code", monospace' };

function roundRect(ctx, x, y, w, h, r) {
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.lineTo(x + w - r, y);
  ctx.quadraticCurveTo(x + w, y, x + w, y + r);
  ctx.lineTo(x + w, y + h - r);
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
  ctx.lineTo(x + r, y + h);
  ctx.quadraticCurveTo(x, y + h, x, y + h - r);
  ctx.lineTo(x, y + r);
  ctx.quadraticCurveTo(x, y, x + r, y);
  ctx.closePath();
}

function truncate(s, max = 20) {
  return s && s.length > max ? s.slice(0, max - 1) + '…' : (s || '');
}
