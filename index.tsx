
import React, { useState, useEffect, useRef } from 'react';
import { GoogleGenAI } from "@google/genai";

const THEME = {
  bg: '#020202',
  panel: '#0a0a0c',
  primary: '#00f2ff', // Cyan
  secondary: '#7000ff', // Purple
  success: '#00ff9d',
  danger: '#ff0055',
  text: '#e0e0e0',
  mono: '"Fira Code", monospace'
};

const Header = () => (
  <header style={{
    padding: '1.5rem',
    borderBottom: `1px solid ${THEME.primary}33`,
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    background: `linear-gradient(90deg, ${THEME.panel} 0%, rgba(0,0,0,0) 100%)`
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
      <div style={{
        width: '12px', height: '12px', background: THEME.primary,
        borderRadius: '50%', boxShadow: `0 0 10px ${THEME.primary}`
      }} />
      <h1 style={{ fontFamily: THEME.mono, fontSize: '1.2rem', color: THEME.text, letterSpacing: '2px' }}>
        SENTINEL <span style={{ color: THEME.primary }}>V7.7.0</span>
      </h1>
    </div>
    <div style={{ fontFamily: THEME.mono, fontSize: '0.8rem', color: '#666' }}>
      PROTOCOL: <span style={{ color: THEME.success }}>CYBER-WRAITH</span>
    </div>
  </header>
);

const LogViewer = ({ logs }) => {
  const endRef = useRef<HTMLDivElement>(null);
  useEffect(() => endRef.current?.scrollIntoView({ behavior: 'smooth' }), [logs]);

  return (
    <div style={{
      background: '#000',
      border: `1px solid ${THEME.primary}22`,
      borderRadius: '8px',
      height: '400px',
      overflowY: 'auto',
      padding: '1rem',
      fontFamily: THEME.mono,
      fontSize: '0.85rem'
    }}>
      {logs.map((l, i) => (
        <div key={i} style={{ marginBottom: '6px', display: 'flex', gap: '10px' }}>
          <span style={{ color: '#555' }}>[{l.time}]</span>
          <span style={{ 
            color: l.type === 'error' ? THEME.danger : l.type === 'success' ? THEME.success : THEME.text 
          }}>
            {l.msg}
          </span>
        </div>
      ))}
      <div ref={endRef} />
    </div>
  );
};

export default function Dashboard() {
  const [logs, setLogs] = useState([
    { time: '10:00:01', msg: 'System initialized.', type: 'info' },
    { time: '10:00:05', msg: 'Connected to Brain (Gemini 2.0).', type: 'success' },
    { time: '10:01:20', msg: 'Ghost Protocol active. Mouse spline loaded.', type: 'info' },
  ]);

  return (
    <div style={{ minHeight: '100vh', background: THEME.bg, color: THEME.text }}>
      <Header />
      <main style={{ padding: '2rem', maxWidth: '1200px', margin: '0 auto', display: 'grid', gridTemplateColumns: '1fr 300px', gap: '2rem' }}>
        
        {/* Main Log Area */}
        <section>
          <h2 style={{ fontFamily: THEME.mono, fontSize: '1rem', marginBottom: '1rem', color: THEME.primary }}>
            > LIVE_TERMINAL_FEED
          </h2>
          <LogViewer logs={logs} />
          
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginTop: '1rem' }}>
            <div style={{ padding: '1rem', background: THEME.panel, borderLeft: `3px solid ${THEME.secondary}` }}>
              <div style={{ fontSize: '0.7rem', color: '#888' }}>MEMORY USAGE</div>
              <div style={{ fontSize: '1.5rem', fontFamily: THEME.mono }}>248 MB</div>
            </div>
            <div style={{ padding: '1rem', background: THEME.panel, borderLeft: `3px solid ${THEME.success}` }}>
              <div style={{ fontSize: '0.7rem', color: '#888' }}>UPTIME</div>
              <div style={{ fontSize: '1.5rem', fontFamily: THEME.mono }}>00:42:15</div>
            </div>
          </div>
        </section>

        {/* Sidebar */}
        <aside style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div style={{ padding: '1.5rem', background: THEME.panel, borderRadius: '8px', border: `1px solid ${THEME.danger}44` }}>
            <h3 style={{ margin: 0, fontSize: '0.9rem', color: THEME.danger }}>THREAT LEVEL</h3>
            <div style={{ fontSize: '2rem', fontWeight: 'bold', marginTop: '0.5rem' }}>LOW</div>
          </div>

          <div style={{ padding: '1.5rem', background: THEME.panel, borderRadius: '8px' }}>
            <h3 style={{ margin: '0 0 1rem 0', fontSize: '0.9rem', color: THEME.primary }}>SYSTEM HEALTH</h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', fontSize: '0.8rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span>Vision Core</span>
                <span style={{ color: THEME.success }}>ONLINE</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span>Brain Link</span>
                <span style={{ color: THEME.success }}>STABLE</span>
              </div>
              <div style={{ display: 'flex', justifyContent: 'space-between' }}>
                <span>Recovery</span>
                <span style={{ color: '#aaa' }}>IDLE</span>
              </div>
            </div>
          </div>
        </aside>

      </main>
    </div>
  );
}
