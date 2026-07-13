import React, { useState } from 'react';
import { Activity, Database, LayoutDashboard, BookOpen, FlaskConical, Shield, GitBranch } from 'lucide-react';
import Dashboard from './components/Dashboard';
import CorpusExplorer from './components/CorpusExplorer';
import AuditRuns from './components/AuditRuns';
import Library from './components/Library';
import PatternDetail from './components/PatternDetail';
import Autoresearch from './components/Autoresearch';
import Scanner from './components/Scanner';
import AttackGraph from './components/AttackGraph';

function App() {
  const [currentTab, setCurrentTab] = useState('library');
  const [selectedPattern, setSelectedPattern] = useState(null);

  const handleSelectPattern = (slug) => {
    setSelectedPattern(slug);
    setCurrentTab('pattern-detail');
  };

  const handleBackToLibrary = () => {
    setSelectedPattern(null);
    setCurrentTab('library');
  };

  const renderContent = () => {
    switch(currentTab) {
      case 'dashboard': return <Dashboard />;
      case 'corpus': return <CorpusExplorer />;
      case 'audits': return <AuditRuns />;
      case 'library': return <Library onSelectPattern={handleSelectPattern} />;
      case 'pattern-detail': return <PatternDetail slug={selectedPattern} onBack={handleBackToLibrary} />;
      case 'autoresearch': return <Autoresearch />;
      case 'scanner': return <Scanner onSelectPattern={handleSelectPattern} />;
      case 'attack-graph': return <AttackGraph onSelectPattern={handleSelectPattern} />;
      default: return <Library onSelectPattern={handleSelectPattern} />;
    }
  };

  return (
    <div className="app-container">
      <header className="header">
        <h1>Bricklane</h1>
        <nav className="nav-links">
          <a 
            className={currentTab === 'library' || currentTab === 'pattern-detail' ? 'active' : ''} 
            onClick={() => setCurrentTab('library')}
          >
            <BookOpen size={18} style={{marginRight: '6px', verticalAlign: 'text-bottom'}}/>
            Library
          </a>
          <a 
            className={currentTab === 'scanner' ? 'active' : ''} 
            onClick={() => setCurrentTab('scanner')}
          >
            <Shield size={18} style={{marginRight: '6px', verticalAlign: 'text-bottom'}}/>
            Scanner
          </a>
          <a 
            className={currentTab === 'attack-graph' ? 'active' : ''} 
            onClick={() => setCurrentTab('attack-graph')}
          >
            <GitBranch size={18} style={{marginRight: '6px', verticalAlign: 'text-bottom'}}/>
            Attack Graph
          </a>
          <a 
            className={currentTab === 'autoresearch' ? 'active' : ''} 
            onClick={() => setCurrentTab('autoresearch')}
          >
            <FlaskConical size={18} style={{marginRight: '6px', verticalAlign: 'text-bottom'}}/>
            Autoresearch
          </a>
          <a 
            className={currentTab === 'corpus' ? 'active' : ''} 
            onClick={() => setCurrentTab('corpus')}
          >
            <Database size={18} style={{marginRight: '6px', verticalAlign: 'text-bottom'}}/>
            Corpus
          </a>
          <a 
            className={currentTab === 'audits' ? 'active' : ''} 
            onClick={() => setCurrentTab('audits')}
          >
            <Activity size={18} style={{marginRight: '6px', verticalAlign: 'text-bottom'}}/>
            Audit Runs
          </a>
          <a 
            className={currentTab === 'dashboard' ? 'active' : ''} 
            onClick={() => setCurrentTab('dashboard')}
          >
            <LayoutDashboard size={18} style={{marginRight: '6px', verticalAlign: 'text-bottom'}}/>
            Overview
          </a>
        </nav>
      </header>
      
      <main className="main-content animate-fade-in" key={currentTab}>
        {renderContent()}
      </main>
    </div>
  );
}

export default App;
