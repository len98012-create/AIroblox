
import React, { useState, useEffect, useRef } from 'react';
import { GoogleGenAI } from "@google/genai";

const SENTINEL_THEME = {
  bg: '#050505',
  card: '#0a0a0c',
  accent: '#00f2ff',
  danger: '#ff2d55',
  success: '#34c759',
  text: '#e0e0e0',
  dim: '#888888',
};

const Header = () => (
  <header style={{
    padding: '1rem 2rem',
    borderBottom: `1px solid ${SENTINEL_THEME.accent}33`,
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    background: `${SENTINEL_THEME.card}`,
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
      <div style={{
        width: '12px',
        height: '12px',
        borderRadius: '50%',
        background: SENTINEL_THEME.success,
        boxShadow: `0 0 10px ${SENTINEL_THEME.success}`,
        animation: 'pulse 2s infinite',
      }} />
      <h1 style={{ fontSize: '1.2rem', fontWeight: 'bold', letterSpacing: '2px', color: SENTINEL_THEME.accent }}>
        SENTINEL SRE COMMAND CENTER
      </h1>
    </div>
    <div style={{ fontSize: '0.8rem', color: SENTINEL_THEME.dim }}>
      V7.6 [GHOST_PROTOCOL_ACTIVE]
    </div>
    <style>{`
      @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.4; }
        100% { opacity: 1; }
      }
    `}</style>
  </header>
);

const MetricCard = ({ label, value, color = SENTINEL_THEME.accent }) => (
  <div style={{
    background: SENTINEL_THEME.card,
    padding: '1.5rem',
    borderRadius: '8px',
    border: `1px solid ${color}22`,
    flex: 1,
  }}>
    <div style={{ fontSize: '0.7rem', color: SENTINEL_THEME.dim, marginBottom: '0.5rem', textTransform: 'uppercase' }}>
      {label}
    </div>
    <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: color }}>
      {value}
    </div>
  </div>
);

const LogEntry = ({ timestamp, message, type = 'info' }) => (
  <div style={{
    padding: '0.5rem 1rem',
    borderLeft: `2px solid ${type === 'error' ? SENTINEL_THEME.danger : type === 'success' ? SENTINEL_THEME.success : SENTINEL_THEME.accent}`,
    marginBottom: '0.4rem',
    fontSize: '0.85rem',
    background: `${SENTINEL_THEME.card}`,
    fontFamily: 'monospace',
  }}>
    <span style={{ color: SENTINEL_THEME.dim, marginRight: '1rem' }}>[{timestamp}]</span>
    <span style={{ color: SENTINEL_THEME.text }}>{message}</span>
  </div>
);

export default function SentinelDashboard() {
  const [logs, setLogs] = useState([
    { ts: '09:18:21', msg: '🚀 Sentinel v7.5 Ghost Protocol Active.', type: 'info' },
    { ts: '09:18:23', msg: '✨ Learned: skill_whale_hunter', type: 'success' },
    { ts: '09:18:23', msg: '✨ Learned: skill_pls_donate_v7', type: 'success' },
    { ts: '09:18:38', msg: '🚀 [LAUNCHER] Loading PlaceID: 8737899170', type: 'info' },
    { ts: '09:18:43', msg: 'Skill error: SentinelAgent object has no attribute driver', type: 'error' },
    { ts: '10:02:15', msg: '🔧 APPLYING HOTFIX: Driver context injected.', type: 'success' },
    { ts: '10:02:20', msg: '🚀 REBOOTING GHOST ENGINE...', type: 'info' },
  ]);
  const [status, setStatus] = useState('ONLINE');
  const [aiAnalysis, setAiAnalysis] = useState('Awaiting log density analysis...');
  const logEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  const runAnalysis = async () => {
    setAiAnalysis('Analyzing system logs via Gemini 3 Flash...');
    const ai = new GoogleGenAI({ apiKey: process.env.API_KEY || '' });
    try {
      const response = await ai.models.generateContent({
        model: 'gemini-3-flash-preview',
        contents: `Analyze these Roblox bot logs and tell me if it is safe or if it is being detected.
        Logs: ${JSON.stringify(logs)}`,
        config: {
          systemInstruction: "You are an expert SRE for an AI botting system. Provide a brief, technical security assessment."
        }
      });
      setAiAnalysis(response.text || 'Analysis failed.');
    } catch (e) {
      setAiAnalysis('Error contacting Brain Service: ' + String(e));
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: SENTINEL_THEME.bg,
      color: SENTINEL_THEME.text,
      fontFamily: 'Inter, sans-serif',
      display: 'flex',
      flexDirection: 'column',
    }}>
      <Header />
      
      <main style={{ padding: '2rem', flex: 1, display: 'grid', gridTemplateColumns: '300px 1fr', gap: '2rem' }}>
        {/* Left Panel: Stats */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <MetricCard label="System Status" value={status} color={SENTINEL_THEME.success} />
          <MetricCard label="Robux Earned" value="1,240 R$" />
          <MetricCard label="Whales Spotted" value="14" />
          <MetricCard label="AFK Prevented" value="238 times" />
          
          <div style={{
            background: SENTINEL_THEME.card,
            padding: '1rem',
            borderRadius: '8px',
            marginTop: 'auto',
            border: `1px solid ${SENTINEL_THEME.accent}44`,
          }}>
            <h3 style={{ fontSize: '0.8rem', marginBottom: '0.5rem', color: SENTINEL_THEME.accent }}>AI BRAIN INSIGHT</h3>
            <div style={{ fontSize: '0.75rem', color: SENTINEL_THEME.dim, lineHeight: '1.4' }}>
              {aiAnalysis}
            </div>
            <button 
              onClick={runAnalysis}
              style={{
                width: '100%',
                marginTop: '1rem',
                background: 'transparent',
                border: `1px solid ${SENTINEL_THEME.accent}`,
                color: SENTINEL_THEME.accent,
                padding: '0.5rem',
                cursor: 'pointer',
                fontSize: '0.7rem',
                fontWeight: 'bold',
                textTransform: 'uppercase',
                transition: 'all 0.2s',
              }}
              onMouseOver={(e) => { e.currentTarget.style.background = `${SENTINEL_THEME.accent}22` }}
              onMouseOut={(e) => { e.currentTarget.style.background = 'transparent' }}
            >
              Analyze Security
            </button>
          </div>
        </div>

        {/* Right Panel: Logs & Terminal */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          <div style={{
            background: '#000',
            borderRadius: '8px',
            border: `1px solid ${SENTINEL_THEME.dim}33`,
            flex: 1,
            overflowY: 'auto',
            padding: '1rem',
            maxHeight: 'calc(100vh - 200px)',
          }}>
            <div style={{ marginBottom: '1rem', borderBottom: `1px solid ${SENTINEL_THEME.dim}33`, paddingBottom: '0.5rem', display: 'flex', justifyContent: 'space-between' }}>
              <span style={{ fontSize: '0.7rem', color: SENTINEL_THEME.dim }}>TERMINAL_OUTPUT_STDOUT</span>
              <span style={{ fontSize: '0.7rem', color: SENTINEL_THEME.accent }}>SECURE_CONNECTION: AES-256</span>
            </div>
            {logs.map((log, i) => (
              <LogEntry key={i} timestamp={log.ts} message={log.msg} type={log.type} />
            ))}
            <div ref={logEndRef} />
          </div>

          <div style={{ display: 'flex', gap: '1rem' }}>
             <button style={{
               flex: 1,
               padding: '1rem',
               background: SENTINEL_THEME.accent,
               color: '#000',
               border: 'none',
               borderRadius: '4px',
               fontWeight: 'bold',
               cursor: 'pointer',
             }}>
               TRIGGER EVOLUTION
             </button>
             <button style={{
               flex: 1,
               padding: '1rem',
               background: 'transparent',
               border: `1px solid ${SENTINEL_THEME.danger}`,
               color: SENTINEL_THEME.danger,
               borderRadius: '4px',
               fontWeight: 'bold',
               cursor: 'pointer',
             }}>
               EMERGENCY SHUTDOWN
             </button>
          </div>
        </div>
      </main>
    </div>
  );
}
