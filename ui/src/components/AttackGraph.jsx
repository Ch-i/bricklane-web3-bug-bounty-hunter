import { useState, useEffect, useRef, useCallback } from 'react';
import { Network, AlertTriangle, TrendingUp, DollarSign, ExternalLink, X, Loader2 } from 'lucide-react';

const API_BASE = 'http://127.0.0.1:8000';

const DOMAIN_COLORS = {
  defi: '#58a6ff',
  security: '#ff7b72',
  economics: '#d2a8ff',
  infrastructure: '#a5d6ff',
  governance: '#ffa657',
  mev: '#f0883e',
};

const DOMAIN_LABELS = {
  defi: 'DeFi Primitives',
  security: 'Security',
  economics: 'Economics',
  infrastructure: 'Infrastructure',
  governance: 'Governance',
  mev: 'MEV',
};

const SEVERITY_COLORS = {
  Critical: '#ff4757',
  High: '#ff6b6b',
  Medium: '#ffa502',
};

const CANVAS_HEIGHT = 500;
const BG_COLOR = '#0d1117';

/* ─── Force simulation constants ─── */
const REPULSION_STRENGTH = 8000;
const SPRING_STRENGTH = 0.004;
const SPRING_REST_LENGTH = 140;
const CENTER_GRAVITY = 0.01;
const DAMPING = 0.88;
const MIN_VELOCITY = 0.01;

function truncate(str, max = 25) {
  return str.length > max ? str.slice(0, max - 1) + '…' : str;
}

function formatLosses(totalUsd) {
  if (totalUsd >= 1e9) return `$${(totalUsd / 1e9).toFixed(1)}B`;
  if (totalUsd >= 1e6) return `$${(totalUsd / 1e6).toFixed(1)}M`;
  if (totalUsd >= 1e3) return `$${(totalUsd / 1e3).toFixed(1)}K`;
  return `$${totalUsd}`;
}

function parseLossUsd(str) {
  if (!str) return 0;
  const cleaned = str.replace(/[^0-9.BMKbmk]/g, '');
  const num = parseFloat(cleaned);
  if (isNaN(num)) return 0;
  const upper = str.toUpperCase();
  if (upper.includes('B')) return num * 1e9;
  if (upper.includes('M')) return num * 1e6;
  if (upper.includes('K')) return num * 1e3;
  return num;
}

/* ─── Physics helpers ─── */
function dist(a, b) {
  const dx = a.x - b.x;
  const dy = a.y - b.y;
  return Math.sqrt(dx * dx + dy * dy) || 1;
}

export default function AttackGraph({ onSelectPattern }) {
  const canvasRef = useRef(null);
  const containerRef = useRef(null);
  const animRef = useRef(null);
  const simNodesRef = useRef([]);
  const simEdgesRef = useRef([]);
  const interactionRef = useRef({
    hoveredNode: null,
    hoveredEdge: null,
    selectedNode: null,
    selectedEdge: null,
    dragNode: null,
    dragOffsetX: 0,
    dragOffsetY: 0,
    mouseX: 0,
    mouseY: 0,
    isDragging: false,
    width: 800,
    pulsePhase: 0,
  });

  const [graphData, setGraphData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [selectedNode, setSelectedNode] = useState(null);
  const [selectedEdge, setSelectedEdge] = useState(null);
  const [stats, setStats] = useState({ patterns: 0, chains: 0, incidents: 0, totalLoss: 0 });

  /* ─── Fetch data ─── */
  useEffect(() => {
    let cancelled = false;
    async function fetchGraph() {
      try {
        const res = await fetch(`${API_BASE}/api/graph/compositions`);
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        if (!cancelled) {
          setGraphData(data);
          setLoading(false);

          /* Compute stats */
          const incidentCount = data.edges.reduce((sum, e) => sum + (e.incidents?.length || 0), 0);
          const totalLoss = data.edges.reduce(
            (sum, e) => sum + (e.incidents || []).reduce((s, i) => s + parseLossUsd(i.loss_usd), 0),
            0
          );
          setStats({
            patterns: data.nodes.length,
            chains: data.edges.length,
            incidents: incidentCount,
            totalLoss,
          });
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.message);
          setLoading(false);
        }
      }
    }
    fetchGraph();
    return () => { cancelled = true; };
  }, []);

  /* ─── Initialize simulation nodes & edges ─── */
  useEffect(() => {
    if (!graphData) return;
    const { nodes, edges } = graphData;
    const w = containerRef.current?.clientWidth || 800;
    const h = CANVAS_HEIGHT;
    interactionRef.current.width = w;

    /* Count edges per node for radius sizing */
    const edgeCounts = {};
    nodes.forEach((n) => { edgeCounts[n.slug] = 0; });
    edges.forEach((e) => {
      edgeCounts[e.source] = (edgeCounts[e.source] || 0) + 1;
      edgeCounts[e.target] = (edgeCounts[e.target] || 0) + 1;
    });

    const simNodes = nodes.map((n, i) => {
      const angle = (2 * Math.PI * i) / nodes.length;
      const spread = Math.min(w, h) * 0.3;
      return {
        ...n,
        x: w / 2 + Math.cos(angle) * spread + (Math.random() - 0.5) * 40,
        y: h / 2 + Math.sin(angle) * spread + (Math.random() - 0.5) * 40,
        vx: 0,
        vy: 0,
        radius: Math.max(10, Math.min(30, 8 + (edgeCounts[n.slug] || 0) * 3)),
        color: DOMAIN_COLORS[n.domain] || '#8b949e',
      };
    });

    const nodeMap = {};
    simNodes.forEach((n, i) => { nodeMap[n.slug] = i; });

    const simEdges = edges.map((e) => ({
      ...e,
      sourceIdx: nodeMap[e.source],
      targetIdx: nodeMap[e.target],
      color: SEVERITY_COLORS[e.severity] || '#8b949e',
      thickness: Math.max(1, Math.min(6, (e.weight || 1) * 1.5)),
    }));

    simNodesRef.current = simNodes;
    simEdgesRef.current = simEdges;
  }, [graphData]);

  /* ─── Canvas interaction handlers ─── */
  const getCanvasCoords = useCallback((e) => {
    const canvas = canvasRef.current;
    if (!canvas) return { x: 0, y: 0 };
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    return {
      x: (e.clientX - rect.left) * scaleX,
      y: (e.clientY - rect.top) * scaleY,
    };
  }, []);

  const findNodeAt = useCallback((mx, my) => {
    const nodes = simNodesRef.current;
    for (let i = nodes.length - 1; i >= 0; i--) {
      const n = nodes[i];
      const d = dist(n, { x: mx, y: my });
      if (d <= n.radius + 4) return i;
    }
    return -1;
  }, []);

  const findEdgeAt = useCallback((mx, my) => {
    const nodes = simNodesRef.current;
    const edges = simEdgesRef.current;
    for (let i = 0; i < edges.length; i++) {
      const e = edges[i];
      const a = nodes[e.sourceIdx];
      const b = nodes[e.targetIdx];
      if (!a || !b) continue;
      /* Point-to-segment distance */
      const dx = b.x - a.x;
      const dy = b.y - a.y;
      const lenSq = dx * dx + dy * dy;
      if (lenSq === 0) continue;
      let t = ((mx - a.x) * dx + (my - a.y) * dy) / lenSq;
      t = Math.max(0, Math.min(1, t));
      const px = a.x + t * dx;
      const py = a.y + t * dy;
      const d = Math.sqrt((mx - px) ** 2 + (my - py) ** 2);
      if (d <= Math.max(e.thickness + 4, 8)) return i;
    }
    return -1;
  }, []);

  const handleMouseDown = useCallback((e) => {
    const { x, y } = getCanvasCoords(e);
    const ni = findNodeAt(x, y);
    if (ni >= 0) {
      const node = simNodesRef.current[ni];
      interactionRef.current.dragNode = ni;
      interactionRef.current.dragOffsetX = node.x - x;
      interactionRef.current.dragOffsetY = node.y - y;
      interactionRef.current.isDragging = false;
    }
  }, [getCanvasCoords, findNodeAt]);

  const handleMouseMove = useCallback((e) => {
    const { x, y } = getCanvasCoords(e);
    interactionRef.current.mouseX = x;
    interactionRef.current.mouseY = y;
    const canvas = canvasRef.current;

    if (interactionRef.current.dragNode !== null) {
      interactionRef.current.isDragging = true;
      const ni = interactionRef.current.dragNode;
      const node = simNodesRef.current[ni];
      node.x = x + interactionRef.current.dragOffsetX;
      node.y = y + interactionRef.current.dragOffsetY;
      node.vx = 0;
      node.vy = 0;
      if (canvas) canvas.style.cursor = 'grabbing';
      return;
    }

    const ni = findNodeAt(x, y);
    if (ni >= 0) {
      interactionRef.current.hoveredNode = ni;
      interactionRef.current.hoveredEdge = null;
      if (canvas) canvas.style.cursor = 'pointer';
    } else {
      interactionRef.current.hoveredNode = null;
      const ei = findEdgeAt(x, y);
      interactionRef.current.hoveredEdge = ei >= 0 ? ei : null;
      if (canvas) canvas.style.cursor = ei >= 0 ? 'pointer' : 'default';
    }
  }, [getCanvasCoords, findNodeAt, findEdgeAt]);

  const handleMouseUp = useCallback((e) => {
    const wasDragging = interactionRef.current.isDragging;
    const dragIdx = interactionRef.current.dragNode;
    interactionRef.current.dragNode = null;
    interactionRef.current.isDragging = false;

    if (wasDragging) return;

    const { x, y } = getCanvasCoords(e);
    const ni = findNodeAt(x, y);
    if (ni >= 0) {
      const node = simNodesRef.current[ni];
      setSelectedNode(node);
      setSelectedEdge(null);
      interactionRef.current.selectedNode = ni;
      interactionRef.current.selectedEdge = null;
      return;
    }
    const ei = findEdgeAt(x, y);
    if (ei >= 0) {
      const edge = simEdgesRef.current[ei];
      setSelectedEdge(edge);
      setSelectedNode(null);
      interactionRef.current.selectedEdge = ei;
      interactionRef.current.selectedNode = null;
      return;
    }
    /* Click on empty → deselect */
    setSelectedNode(null);
    setSelectedEdge(null);
    interactionRef.current.selectedNode = null;
    interactionRef.current.selectedEdge = null;
  }, [getCanvasCoords, findNodeAt, findEdgeAt]);

  const handleMouseLeave = useCallback(() => {
    interactionRef.current.hoveredNode = null;
    interactionRef.current.hoveredEdge = null;
    interactionRef.current.dragNode = null;
    interactionRef.current.isDragging = false;
  }, []);

  /* ─── Render loop ─── */
  useEffect(() => {
    if (!graphData) return;
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const dpr = window.devicePixelRatio || 1;

    function resize() {
      const w = containerRef.current?.clientWidth || 800;
      interactionRef.current.width = w;
      canvas.width = w * dpr;
      canvas.height = CANVAS_HEIGHT * dpr;
      canvas.style.width = w + 'px';
      canvas.style.height = CANVAS_HEIGHT + 'px';
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    resize();
    window.addEventListener('resize', resize);

    function simulate() {
      const nodes = simNodesRef.current;
      const edges = simEdgesRef.current;
      const w = interactionRef.current.width;
      const h = CANVAS_HEIGHT;
      const cx = w / 2;
      const cy = h / 2;

      /* Repulsion (Coulomb) */
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const a = nodes[i];
          const b = nodes[j];
          const dx = a.x - b.x;
          const dy = a.y - b.y;
          const d = Math.sqrt(dx * dx + dy * dy) || 1;
          const force = REPULSION_STRENGTH / (d * d);
          const fx = (dx / d) * force;
          const fy = (dy / d) * force;
          a.vx += fx;
          a.vy += fy;
          b.vx -= fx;
          b.vy -= fy;
        }
      }

      /* Attraction (spring along edges) */
      for (const e of edges) {
        const a = nodes[e.sourceIdx];
        const b = nodes[e.targetIdx];
        if (!a || !b) continue;
        const dx = b.x - a.x;
        const dy = b.y - a.y;
        const d = Math.sqrt(dx * dx + dy * dy) || 1;
        const displacement = d - SPRING_REST_LENGTH;
        const force = SPRING_STRENGTH * displacement;
        const fx = (dx / d) * force;
        const fy = (dy / d) * force;
        a.vx += fx;
        a.vy += fy;
        b.vx -= fx;
        b.vy -= fy;
      }

      /* Center gravity + damping + integration */
      for (const n of nodes) {
        n.vx += (cx - n.x) * CENTER_GRAVITY;
        n.vy += (cy - n.y) * CENTER_GRAVITY;
        n.vx *= DAMPING;
        n.vy *= DAMPING;
        if (Math.abs(n.vx) < MIN_VELOCITY) n.vx = 0;
        if (Math.abs(n.vy) < MIN_VELOCITY) n.vy = 0;
        n.x += n.vx;
        n.y += n.vy;
        /* Clamp to canvas bounds */
        n.x = Math.max(n.radius, Math.min(w - n.radius, n.x));
        n.y = Math.max(n.radius, Math.min(h - n.radius, n.y));
      }
    }

    function draw() {
      const nodes = simNodesRef.current;
      const edges = simEdgesRef.current;
      const w = interactionRef.current.width;
      const h = CANVAS_HEIGHT;
      const {
        hoveredNode,
        hoveredEdge,
        selectedNode: selNodeIdx,
        selectedEdge: selEdgeIdx,
      } = interactionRef.current;
      interactionRef.current.pulsePhase += 0.03;
      const pulse = interactionRef.current.pulsePhase;
      const pulseAlpha = 0.5 + 0.5 * Math.sin(pulse);

      ctx.clearRect(0, 0, w, h);
      /* Background */
      ctx.fillStyle = BG_COLOR;
      ctx.fillRect(0, 0, w, h);

      /* Subtle grid */
      ctx.strokeStyle = 'rgba(255,255,255,0.03)';
      ctx.lineWidth = 0.5;
      for (let gx = 0; gx < w; gx += 40) {
        ctx.beginPath();
        ctx.moveTo(gx, 0);
        ctx.lineTo(gx, h);
        ctx.stroke();
      }
      for (let gy = 0; gy < h; gy += 40) {
        ctx.beginPath();
        ctx.moveTo(0, gy);
        ctx.lineTo(w, gy);
        ctx.stroke();
      }

      /* Determine connected set for hover highlight */
      const connectedNodes = new Set();
      const connectedEdges = new Set();
      if (hoveredNode !== null) {
        connectedNodes.add(hoveredNode);
        edges.forEach((e, i) => {
          if (e.sourceIdx === hoveredNode || e.targetIdx === hoveredNode) {
            connectedEdges.add(i);
            connectedNodes.add(e.sourceIdx);
            connectedNodes.add(e.targetIdx);
          }
        });
      }
      const hasHover = hoveredNode !== null;

      /* Draw edges */
      edges.forEach((e, i) => {
        const a = nodes[e.sourceIdx];
        const b = nodes[e.targetIdx];
        if (!a || !b) return;

        let alpha = 1;
        if (hasHover && !connectedEdges.has(i)) alpha = 0.1;
        if (selEdgeIdx === i) alpha = 1;

        ctx.save();
        ctx.globalAlpha = alpha;
        ctx.strokeStyle = e.color;
        ctx.lineWidth = e.thickness;

        /* Pulse animation for Critical edges */
        if (e.severity === 'Critical') {
          ctx.lineWidth = e.thickness + pulseAlpha * 2;
          ctx.shadowColor = e.color;
          ctx.shadowBlur = pulseAlpha * 12;
        }

        ctx.beginPath();
        ctx.moveTo(a.x, a.y);
        ctx.lineTo(b.x, b.y);
        ctx.stroke();
        ctx.restore();

        /* Arrow direction indicator */
        const midX = (a.x + b.x) / 2;
        const midY = (a.y + b.y) / 2;
        const angle = Math.atan2(b.y - a.y, b.x - a.x);
        const arrowSize = 6;
        ctx.save();
        ctx.globalAlpha = alpha * 0.7;
        ctx.fillStyle = e.color;
        ctx.beginPath();
        ctx.moveTo(
          midX + Math.cos(angle) * arrowSize,
          midY + Math.sin(angle) * arrowSize
        );
        ctx.lineTo(
          midX + Math.cos(angle + 2.5) * arrowSize,
          midY + Math.sin(angle + 2.5) * arrowSize
        );
        ctx.lineTo(
          midX + Math.cos(angle - 2.5) * arrowSize,
          midY + Math.sin(angle - 2.5) * arrowSize
        );
        ctx.closePath();
        ctx.fill();
        ctx.restore();
      });

      /* Draw nodes */
      nodes.forEach((n, i) => {
        let alpha = 1;
        if (hasHover && !connectedNodes.has(i)) alpha = 0.15;

        ctx.save();
        ctx.globalAlpha = alpha;

        /* Glow for hovered / selected */
        if (i === hoveredNode || i === selNodeIdx) {
          ctx.shadowColor = n.color;
          ctx.shadowBlur = 20;
        }

        /* Node circle */
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.radius, 0, Math.PI * 2);
        ctx.fillStyle = n.color;
        ctx.fill();

        /* Inner highlight */
        const grad = ctx.createRadialGradient(
          n.x - n.radius * 0.3,
          n.y - n.radius * 0.3,
          0,
          n.x,
          n.y,
          n.radius
        );
        grad.addColorStop(0, 'rgba(255,255,255,0.25)');
        grad.addColorStop(1, 'rgba(255,255,255,0)');
        ctx.fillStyle = grad;
        ctx.fill();

        /* Outline */
        ctx.strokeStyle =
          i === hoveredNode || i === selNodeIdx
            ? 'rgba(255,255,255,0.8)'
            : 'rgba(255,255,255,0.15)';
        ctx.lineWidth = i === hoveredNode || i === selNodeIdx ? 2 : 1;
        ctx.stroke();

        /* Label */
        ctx.shadowBlur = 0;
        ctx.font = '11px Inter, system-ui, sans-serif';
        ctx.textAlign = 'center';
        ctx.fillStyle = 'rgba(255,255,255,0.85)';
        ctx.fillText(truncate(n.title), n.x, n.y + n.radius + 14);

        ctx.restore();
      });

      /* Tooltip on hovered node */
      if (hoveredNode !== null) {
        const n = nodes[hoveredNode];
        const tooltipW = 180;
        const tooltipH = 50;
        let tx = n.x + n.radius + 10;
        let ty = n.y - tooltipH / 2;
        if (tx + tooltipW > w) tx = n.x - n.radius - 10 - tooltipW;
        if (ty < 0) ty = 4;
        if (ty + tooltipH > h) ty = h - tooltipH - 4;

        ctx.save();
        ctx.fillStyle = 'rgba(22, 27, 34, 0.92)';
        ctx.strokeStyle = 'rgba(255,255,255,0.1)';
        ctx.lineWidth = 1;
        roundRect(ctx, tx, ty, tooltipW, tooltipH, 6);
        ctx.fill();
        ctx.stroke();
        ctx.font = 'bold 12px Inter, system-ui, sans-serif';
        ctx.fillStyle = '#e6edf3';
        ctx.textAlign = 'left';
        ctx.fillText(truncate(n.title, 22), tx + 10, ty + 20);
        ctx.font = '11px Inter, system-ui, sans-serif';
        ctx.fillStyle = n.color;
        ctx.fillText(DOMAIN_LABELS[n.domain] || n.domain, tx + 10, ty + 38);
        ctx.restore();
      }

      /* Tooltip on hovered edge */
      if (hoveredEdge !== null && hoveredNode === null) {
        const e = edges[hoveredEdge];
        const a = nodes[e.sourceIdx];
        const b = nodes[e.targetIdx];
        if (a && b) {
          const mx = (a.x + b.x) / 2;
          const my = (a.y + b.y) / 2;
          const tooltipW = 200;
          const tooltipH = 44;
          let tx = mx + 10;
          let ty = my - tooltipH / 2;
          if (tx + tooltipW > w) tx = mx - 10 - tooltipW;
          if (ty < 0) ty = 4;
          if (ty + tooltipH > h) ty = h - tooltipH - 4;

          ctx.save();
          ctx.fillStyle = 'rgba(22, 27, 34, 0.92)';
          ctx.strokeStyle = 'rgba(255,255,255,0.1)';
          ctx.lineWidth = 1;
          roundRect(ctx, tx, ty, tooltipW, tooltipH, 6);
          ctx.fill();
          ctx.stroke();
          ctx.font = 'bold 11px Inter, system-ui, sans-serif';
          ctx.fillStyle = e.color;
          ctx.textAlign = 'left';
          ctx.fillText(`${e.severity} · ${e.incidents?.length || 0} incidents`, tx + 10, ty + 18);
          ctx.font = '10px Inter, system-ui, sans-serif';
          ctx.fillStyle = '#8b949e';
          ctx.fillText(truncate(e.description || '', 30), tx + 10, ty + 34);
          ctx.restore();
        }
      }

      /* Legend (top-right) */
      const legendX = w - 160;
      const legendY = 12;
      const legendW = 148;
      const domains = Object.entries(DOMAIN_COLORS);
      const legendH = 28 + domains.length * 18;
      ctx.save();
      ctx.fillStyle = 'rgba(13, 17, 23, 0.85)';
      ctx.strokeStyle = 'rgba(255,255,255,0.08)';
      ctx.lineWidth = 1;
      roundRect(ctx, legendX, legendY, legendW, legendH, 6);
      ctx.fill();
      ctx.stroke();
      ctx.font = 'bold 10px Inter, system-ui, sans-serif';
      ctx.fillStyle = '#8b949e';
      ctx.textAlign = 'left';
      ctx.fillText('DOMAINS', legendX + 12, legendY + 16);
      domains.forEach(([key, color], idx) => {
        const ly = legendY + 28 + idx * 18;
        ctx.fillStyle = color;
        ctx.beginPath();
        ctx.arc(legendX + 18, ly, 4, 0, Math.PI * 2);
        ctx.fill();
        ctx.font = '10px Inter, system-ui, sans-serif';
        ctx.fillStyle = '#c9d1d9';
        ctx.fillText(DOMAIN_LABELS[key] || key, legendX + 28, ly + 3);
      });
      ctx.restore();
    }

    function loop() {
      if (interactionRef.current.dragNode === null) {
        simulate();
      } else {
        /* Still simulate but pin the dragged node */
        const pinIdx = interactionRef.current.dragNode;
        const saved = { x: simNodesRef.current[pinIdx].x, y: simNodesRef.current[pinIdx].y };
        simulate();
        simNodesRef.current[pinIdx].x = saved.x;
        simNodesRef.current[pinIdx].y = saved.y;
        simNodesRef.current[pinIdx].vx = 0;
        simNodesRef.current[pinIdx].vy = 0;
      }
      draw();
      animRef.current = requestAnimationFrame(loop);
    }

    animRef.current = requestAnimationFrame(loop);

    return () => {
      window.removeEventListener('resize', resize);
      if (animRef.current) cancelAnimationFrame(animRef.current);
    };
  }, [graphData]);

  /* ─── Find connected edges for selected node ─── */
  const connectedEdgesForNode = selectedNode
    ? (graphData?.edges || []).filter(
        (e) => e.source === selectedNode.slug || e.target === selectedNode.slug
      )
    : [];

  /* ─── Render ─── */
  if (loading) {
    return (
      <div className="glass-panel animate-fade-in" style={{ padding: 40, textAlign: 'center' }}>
        <Loader2 size={32} style={{ animation: 'spin 1s linear infinite', color: '#58a6ff' }} />
        <p style={{ color: '#8b949e', marginTop: 12 }}>Loading attack composition graph…</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="glass-panel animate-fade-in" style={{ padding: 24, textAlign: 'center' }}>
        <AlertTriangle size={28} style={{ color: '#ff7b72' }} />
        <p style={{ color: '#ff7b72', marginTop: 8 }}>Failed to load graph: {error}</p>
      </div>
    );
  }

  return (
    <div className="animate-fade-in" ref={containerRef}>
      {/* Stats bar */}
      <div
        className="glass-panel"
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: 20,
          padding: '12px 20px',
          marginBottom: 12,
          alignItems: 'center',
        }}
      >
        <StatItem icon={<Network size={16} />} label="patterns" value={stats.patterns} color="#58a6ff" />
        <StatItem icon={<TrendingUp size={16} />} label="attack chains" value={stats.chains} color="#d2a8ff" />
        <StatItem icon={<AlertTriangle size={16} />} label="real incidents" value={stats.incidents} color="#ff7b72" />
        <StatItem icon={<DollarSign size={16} />} label="total losses" value={formatLosses(stats.totalLoss)} color="#ffa657" />
      </div>

      {/* Canvas */}
      <div
        className="glass-panel"
        style={{ padding: 0, overflow: 'hidden', borderRadius: 12 }}
      >
        <canvas
          ref={canvasRef}
          style={{ display: 'block', width: '100%', height: CANVAS_HEIGHT, background: BG_COLOR }}
          onMouseDown={handleMouseDown}
          onMouseMove={handleMouseMove}
          onMouseUp={handleMouseUp}
          onMouseLeave={handleMouseLeave}
        />
      </div>

      {/* Detail panel */}
      {selectedNode && (
        <div className="glass-panel animate-fade-in" style={{ marginTop: 12, padding: 20 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <h3 style={{ color: '#e6edf3', margin: 0, fontSize: 18 }}>{selectedNode.title}</h3>
              <span
                className="badge"
                style={{
                  background: DOMAIN_COLORS[selectedNode.domain] + '22',
                  color: DOMAIN_COLORS[selectedNode.domain],
                  marginTop: 6,
                  display: 'inline-block',
                }}
              >
                {selectedNode.domain_label || selectedNode.domain}
              </span>
            </div>
            <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
              {onSelectPattern && (
                <button
                  onClick={() => onSelectPattern(selectedNode.slug)}
                  style={{
                    background: 'rgba(88,166,255,0.15)',
                    border: '1px solid rgba(88,166,255,0.3)',
                    color: '#58a6ff',
                    borderRadius: 6,
                    padding: '6px 14px',
                    cursor: 'pointer',
                    fontSize: 13,
                    display: 'flex',
                    alignItems: 'center',
                    gap: 6,
                    transition: 'all 0.2s',
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.background = 'rgba(88,166,255,0.25)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.background = 'rgba(88,166,255,0.15)';
                  }}
                >
                  View Pattern <ExternalLink size={13} />
                </button>
              )}
              <button
                onClick={() => {
                  setSelectedNode(null);
                  interactionRef.current.selectedNode = null;
                }}
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: '#8b949e',
                  cursor: 'pointer',
                  padding: 4,
                }}
              >
                <X size={18} />
              </button>
            </div>
          </div>

          {connectedEdgesForNode.length > 0 && (
            <div style={{ marginTop: 16 }}>
              <h4 style={{ color: '#8b949e', fontSize: 12, textTransform: 'uppercase', letterSpacing: 1, marginBottom: 10 }}>
                Connected Attack Chains ({connectedEdgesForNode.length})
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                {connectedEdgesForNode.map((edge, idx) => {
                  const otherSlug = edge.source === selectedNode.slug ? edge.target : edge.source;
                  const otherNode = graphData.nodes.find((n) => n.slug === otherSlug);
                  return (
                    <div
                      key={idx}
                      onClick={() => {
                        setSelectedEdge(edge);
                        setSelectedNode(null);
                        interactionRef.current.selectedNode = null;
                      }}
                      style={{
                        background: 'rgba(255,255,255,0.03)',
                        border: '1px solid rgba(255,255,255,0.06)',
                        borderRadius: 8,
                        padding: '10px 14px',
                        cursor: 'pointer',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        transition: 'background 0.2s',
                      }}
                      onMouseEnter={(e) => {
                        e.currentTarget.style.background = 'rgba(255,255,255,0.06)';
                      }}
                      onMouseLeave={(e) => {
                        e.currentTarget.style.background = 'rgba(255,255,255,0.03)';
                      }}
                    >
                      <div>
                        <span style={{ color: '#e6edf3', fontSize: 13 }}>
                          → {otherNode?.title || otherSlug}
                        </span>
                        <span
                          style={{
                            color: '#8b949e',
                            fontSize: 11,
                            display: 'block',
                            marginTop: 2,
                          }}
                        >
                          {edge.description}
                        </span>
                      </div>
                      <div style={{ display: 'flex', gap: 8, alignItems: 'center', flexShrink: 0 }}>
                        <span
                          className="badge"
                          style={{
                            background: (SEVERITY_COLORS[edge.severity] || '#8b949e') + '22',
                            color: SEVERITY_COLORS[edge.severity] || '#8b949e',
                          }}
                        >
                          {edge.severity}
                        </span>
                        <span style={{ color: '#8b949e', fontSize: 11 }}>
                          {edge.incidents?.length || 0} incidents
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          )}
        </div>
      )}

      {selectedEdge && !selectedNode && (
        <div className="glass-panel animate-fade-in" style={{ marginTop: 12, padding: 20 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
            <div>
              <div style={{ display: 'flex', gap: 8, alignItems: 'center', marginBottom: 4 }}>
                <span
                  className="badge"
                  style={{
                    background: (SEVERITY_COLORS[selectedEdge.severity] || '#8b949e') + '22',
                    color: SEVERITY_COLORS[selectedEdge.severity] || '#8b949e',
                  }}
                >
                  {selectedEdge.severity}
                </span>
                <span style={{ color: '#8b949e', fontSize: 12 }}>
                  Weight: {selectedEdge.weight}
                </span>
              </div>
              <p style={{ color: '#c9d1d9', fontSize: 14, margin: '6px 0 0' }}>
                {selectedEdge.description}
              </p>
              <div style={{ color: '#8b949e', fontSize: 12, marginTop: 4 }}>
                {graphData.nodes.find((n) => n.slug === selectedEdge.source)?.title || selectedEdge.source}
                {' → '}
                {graphData.nodes.find((n) => n.slug === selectedEdge.target)?.title || selectedEdge.target}
              </div>
            </div>
            <button
              onClick={() => {
                setSelectedEdge(null);
                interactionRef.current.selectedEdge = null;
              }}
              style={{
                background: 'transparent',
                border: 'none',
                color: '#8b949e',
                cursor: 'pointer',
                padding: 4,
              }}
            >
              <X size={18} />
            </button>
          </div>

          {selectedEdge.incidents && selectedEdge.incidents.length > 0 && (
            <div style={{ marginTop: 16 }}>
              <h4 style={{ color: '#8b949e', fontSize: 12, textTransform: 'uppercase', letterSpacing: 1, marginBottom: 10 }}>
                Real-World Incidents ({selectedEdge.incidents.length})
              </h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
                {selectedEdge.incidents.map((inc, idx) => (
                  <div
                    key={idx}
                    style={{
                      background: 'rgba(255,255,255,0.03)',
                      border: '1px solid rgba(255,255,255,0.06)',
                      borderRadius: 8,
                      padding: '10px 14px',
                      cursor: 'pointer',
                      transition: 'all 0.2s',
                    }}
                    onMouseEnter={(e) => {
                      e.currentTarget.style.background = 'rgba(255,75,87,0.08)';
                      e.currentTarget.style.borderColor = 'rgba(255,75,87,0.2)';
                    }}
                    onMouseLeave={(e) => {
                      e.currentTarget.style.background = 'rgba(255,255,255,0.03)';
                      e.currentTarget.style.borderColor = 'rgba(255,255,255,0.06)';
                    }}
                    onClick={() => {
                      window.open(`https://rekt.news/search/?q=${encodeURIComponent(inc.name)}`, '_blank');
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <div>
                        <span style={{ color: '#e6edf3', fontSize: 13, fontWeight: 600 }}>
                          {inc.name}
                        </span>
                        {inc.description && (
                          <span
                            style={{
                              color: '#8b949e',
                              fontSize: 11,
                              display: 'block',
                              marginTop: 2,
                            }}
                          >
                            {inc.description}
                          </span>
                        )}
                      </div>
                      <div style={{ display: 'flex', gap: 12, alignItems: 'center', flexShrink: 0 }}>
                        <span style={{ color: '#ffa657', fontSize: 13, fontWeight: 600 }}>
                          {inc.loss_usd}
                        </span>
                        <span style={{ color: '#8b949e', fontSize: 11 }}>{inc.date}</span>
                        <ExternalLink size={12} style={{ color: '#8b949e' }} />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* View Pattern links */}
          {onSelectPattern && (
            <div style={{ display: 'flex', gap: 8, marginTop: 14 }}>
              <button
                onClick={() => onSelectPattern(selectedEdge.source)}
                style={{
                  background: 'rgba(88,166,255,0.1)',
                  border: '1px solid rgba(88,166,255,0.2)',
                  color: '#58a6ff',
                  borderRadius: 6,
                  padding: '5px 12px',
                  cursor: 'pointer',
                  fontSize: 12,
                  display: 'flex',
                  alignItems: 'center',
                  gap: 4,
                  transition: 'all 0.2s',
                }}
              >
                View {graphData.nodes.find((n) => n.slug === selectedEdge.source)?.title || selectedEdge.source} <ExternalLink size={11} />
              </button>
              <button
                onClick={() => onSelectPattern(selectedEdge.target)}
                style={{
                  background: 'rgba(88,166,255,0.1)',
                  border: '1px solid rgba(88,166,255,0.2)',
                  color: '#58a6ff',
                  borderRadius: 6,
                  padding: '5px 12px',
                  cursor: 'pointer',
                  fontSize: 12,
                  display: 'flex',
                  alignItems: 'center',
                  gap: 4,
                  transition: 'all 0.2s',
                }}
              >
                View {graphData.nodes.find((n) => n.slug === selectedEdge.target)?.title || selectedEdge.target} <ExternalLink size={11} />
              </button>
            </div>
          )}
        </div>
      )}

      <style>{`
        @keyframes spin {
          from { transform: rotate(0deg); }
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
}

/* ─── Small stat display ─── */
function StatItem({ icon, label, value, color }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
      <span style={{ color, display: 'flex', alignItems: 'center' }}>{icon}</span>
      <span style={{ color: '#e6edf3', fontWeight: 700, fontSize: 16 }}>{value}</span>
      <span style={{ color: '#8b949e', fontSize: 13 }}>{label}</span>
    </div>
  );
}

/* ─── Canvas rounded rect helper ─── */
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
