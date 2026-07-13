import React, { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

export default function Dashboard() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch('http://127.0.0.1:8000/api/stats')
      .then(r => r.json())
      .then(data => {
        setStats(data);
        setLoading(false);
      })
      .catch(e => {
        console.error(e);
        setLoading(false);
      });
  }, []);

  if (loading) return <div>Loading dashboard...</div>;
  if (!stats) return <div>Failed to load stats</div>;

  const { corpus, queue } = stats;
  
  const vulnData = corpus?.top_vuln_classes?.map(v => ({
    name: v.vuln_class,
    count: v.count
  })) || [];

  return (
    <div className="dashboard-container">
      <div className="dashboard-grid">
        <div className="glass-panel stat-card">
          <div className="stat-label">Total Corpus Entries</div>
          <div className="stat-value">{corpus?.total || 0}</div>
        </div>
        <div className="glass-panel stat-card">
          <div className="stat-label">Candidates Queue</div>
          <div className="stat-value">{queue?.total_candidates || 0}</div>
        </div>
        <div className="glass-panel stat-card">
          <div className="stat-label">Corpus Sources</div>
          <div className="stat-value" style={{fontSize: '1.2rem', marginTop: '1rem'}}>
            {Object.entries(corpus?.by_source || {}).map(([s, c]) => (
              <div key={s} style={{display:'flex', justifyContent:'space-between', color:'var(--text-secondary)'}}>
                <span>{s}</span> <span>{c}</span>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="glass-panel" style={{marginTop: '2rem'}}>
        <h3 style={{marginTop: 0, marginBottom: '1.5rem', color: 'var(--text-secondary)'}}>Top Vulnerability Classes in Corpus</h3>
        <ResponsiveContainer width="100%" height={350} minWidth={300}>
          <BarChart data={vulnData} layout="vertical" margin={{ top: 5, right: 30, left: 100, bottom: 5 }}>
            <CartesianGrid strokeDasharray="3 3" stroke="#30363d" horizontal={false}/>
            <XAxis type="number" stroke="#8b949e" />
            <YAxis dataKey="name" type="category" stroke="#8b949e" width={100} tick={{fontSize: 12}} />
            <Tooltip 
              contentStyle={{backgroundColor: '#161b22', borderColor: '#30363d', borderRadius: '8px'}}
              itemStyle={{color: '#58a6ff'}}
            />
            <Bar dataKey="count" fill="#58a6ff" radius={[0, 4, 4, 0]} />
          </BarChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
