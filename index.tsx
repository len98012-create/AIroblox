
import React, { useState, useEffect, useRef } from 'react';
import { GoogleGenAI } from "@google/genai";

const SENTINEL_THEME = {
  bg: '#050505',
  card: '#0d0d0f',
  accent: '#00f2ff',
  danger: '#ff2d55',
  success: '#34c759',
  warning: '#ffcc00',
  text: '#ffffff',
  dim: '#a0a0a0',
};

const Header = () => (
  <header style={{
    padding: '1rem 2.5rem',
    borderBottom: `2px solid ${SENTINEL_THEME.accent}44`,
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    background: `linear-gradient(180deg, ${SENTINEL_THEME.card} 0%, transparent 100%)`,
    position: 'sticky',
    top: 0,
    zIndex: 100,
    backdropFilter: 'blur(10px)',
  }}>
    <div style={{ display: 'flex', alignItems: 'center', gap: '1.5rem' }}>
      <div style={{
        width: '14px',
        height: '14px',
        borderRadius: '50%',
        background: SENTINEL_THEME.success,
        boxShadow: `0 0 15px ${SENTINEL_THEME.success}`,
        animation: 'pulse 1.5s infinite',
      }} />
      <h1 style={{ 
        fontSize: '1.4rem', 
        fontWeight: '900', 
        letterSpacing: '4px', 
        color: SENTINEL_THEME.accent,
        textShadow: `0 0 10px ${SENTINEL_THEME.accent}66`
      }}>
        SENTINEL SRE
      </h1>
    </div>
    <div style={{ display: 'flex', gap: '2rem', alignItems: 'center' }}>
      <div style={{ fontSize: '0.75rem', color: SENTINEL_THEME.dim, letterSpacing: '1px' }}>
        SECURE LINK: <span style={{ color: SENTINEL_THEME.success }}>ENCRYPTED</span>
      </div>
      <div style={{ fontSize: '0.75rem', color: SENTINEL_THEME.dim }}>
        UPTIME: <span style={{ color: SENTINEL_THEME.accent }}>14:22:05</span>
      </div>
    </div>
    <style>{`
      @keyframes pulse {
        0% { transform: scale(1); opacity: 1; box-shadow: 0 0 5px ${SENTINEL_THEME.success}; }
        50% { transform: scale(1.2); opacity: 0.6; box-shadow: 0 0 20px ${SENTINEL_THEME.success}; }
        100% { transform: scale(1); opacity: 1; box-shadow: 0 0 5px ${SENTINEL_THEME.success}; }
      }
    `}</style>
  </header>
);

const MetricCard = ({ label, value, color = SENTINEL_THEME.accent, trend = null }) => (
  <div style={{
    background: SENTINEL_THEME.card,
    padding: '1.5rem',
    borderRadius: '12px',
    border: `1px solid ${color}33`,
    flex: 1,
    boxShadow: `inset 0 0 20px ${color}05`,
    transition: 'transform 0.2s',
  }}>
    <div style={{ fontSize: '0.65rem', color: SENTINEL_THEME.dim, marginBottom: '0.75rem', textTransform: 'uppercase', letterSpacing: '2px' }}>
      {label}
    </div>
    <div style={{ display: 'flex', alignItems: 'baseline', gap: '0.5rem' }}>
      <div style={{ fontSize: '1.8rem', fontWeight: 'bold', color: color }}>
        {value}
      </div>
      {trend && <div style={{ fontSize: '0.7rem', color: SENTINEL_THEME.success }}>{trend}</div>}
    </div>
  </div>
);

const LogEntry = ({ timestamp, message, type = 'info' }) => (
  <div style={{
    padding: '0.75rem 1rem',
    borderLeft: `3px solid ${type === 'error' ? SENTINEL_THEME.danger : type === 'success' ? SENTINEL_THEME.success : SENTINEL_THEME.accent}`,
    marginBottom: '0.5rem',
    fontSize: '0.85rem',
    background: `${SENTINEL_THEME.card}`,
    fontFamily: '"JetBrains Mono", "Fira Code", monospace',
    borderRadius: '0 4px 4px 0',
    display: 'flex',
    gap: '1rem',
  }}>
    <span style={{ color: SENTINEL_THEME.dim, minWidth: '80px' }}>[{timestamp}]</span>
    <span style={{ 
      color: type === 'error' ? SENTINEL_THEME.danger : type === 'success' ? SENTINEL_THEME.success : SENTINEL_THEME.text,
      flex: 1 
    }}>
      {message}
    </span>
  </div>
);

export default function SentinelDashboard() {
  const [logs, setLogs] = useState([
    { ts: '09:18:21', msg: '🚀 Sentinel v7.6.1 Ghost Protocol Active.', type: 'info' },
    { ts: '09:18:23', msg: '✨ Learned: skill_whale_hunter', type: 'success' },
    { ts: '09:39:31', msg: '⚠️ Vision Fail: Missing gnome-screenshot. Triggering recovery...', type: 'warning' },
    { ts: '10:02:15', msg: '🔧 DEEP FIX APPLIED: python3-tk and system dependencies updated.', type: 'success' },
    { ts: '10:02:20', msg: '🚀 REBOOTING ENGINE... [OK]', type: 'success' },
    { ts: '10:05:11', msg: '👁️ Vision Engine: Online (Xvfb Render active)', type: 'info' },
  ]);
  const [aiAnalysis, setAiAnalysis] = useState('System nominal. No threats detected in current cycle.');
  const [analyzing, setAnalyzing] = useState(false);
  const logEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

  const runAnalysis = async () => {
    setAnalyzing(true);
    setAiAnalysis('Gemini 3 Flash deep-scanning runtime logs...');
    const ai = new GoogleGenAI({ apiKey: process.env.API_KEY || '' });
    try {
      const response = await ai.models.generateContent({
        model: 'gemini-3-flash-preview',
        contents: `Review these logs for security risks or account flags: ${JSON.stringify(logs)}`,
        config: {
          systemInstruction: "You are a cybersecurity expert monitoring an automated agent. Provide a concise status report."
        }
      });
      setAiAnalysis(response.text || 'Analysis completed. Status: STABLE.');
    } catch (e) {
      setAiAnalysis('Analysis link severed. Network jitter detected.');
    } finally {
      setAnalyzing(false);
    }
  };

  return (
    <div style={{
      minHeight: '100vh',
      background: SENTINEL_THEME.bg,
      color: SENTINEL_THEME.text,
      fontFamily: 'Inter, system-ui, sans-serif',
      display: 'flex',
      flexDirection: 'column',
    }}>
      <Header />
      
      <main style={{ padding: '2rem', flex: 1, display: 'grid', gridTemplateColumns: '320px 1fr', gap: '2.5rem', maxWidth: '1600px', margin: '0 auto', width: '100%' }}>
        {/* Left Panel: Metrics */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <MetricCard label="Global Status" value="SECURE" color={SENTINEL_THEME.success} />
          <MetricCard label="Session Revenue" value="4,820 R$" trend="+12% / hr" />
          <MetricCard label="Activity Index" value="94.2" color={SENTINEL_THEME.accent} />
          
          <div style={{
            background: SENTINEL_THEME.card,
            padding: '1.5rem',
            borderRadius: '12px',
            marginTop: 'auto',
            border: `1px solid ${SENTINEL_THEME.accent}22`,
            position: 'relative',
            overflow: 'hidden'
          }}>
            <div style={{ position: 'absolute', top: 0, left: 0, width: '4px', height: '100%', background: SENTINEL_THEME.accent }} />
            <h3 style={{ fontSize: '0.8rem', fontWeight: 'bold', marginBottom: '1rem', color: SENTINEL_THEME.accent, letterSpacing: '1px' }}>BRAIN STATUS</h3>
            <div style={{ fontSize: '0.85rem', color: SENTINEL_THEME.dim, lineHeight: '1.6', minHeight: '60px' }}>
              {aiAnalysis}
            </div>
            <button 
              disabled={analyzing}
              onClick={runAnalysis}
              style={{
                width: '100%',
                marginTop: '1.5rem',
                background: analyzing ? '#222' : 'transparent',
                border: `1px solid ${SENTINEL_THEME.accent}`,
                color: SENTINEL_THEME.accent,
                padding: '0.75rem',
                cursor: analyzing ? 'not-allowed' : 'pointer',
                fontSize: '0.7rem',
                fontWeight: '900',
                letterSpacing: '2px',
                transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
              }}
              onMouseOver={(e) => { if(!analyzing) e.currentTarget.style.background = `${SENTINEL_THEME.accent}22` }}
              onMouseOut={(e) => { if(!analyzing) e.currentTarget.style.background = 'transparent' }}
            >
              {analyzing ? 'SCANNING...' : 'DEEP SECURITY SCAN'}
            </button>
          </div>
        </div>

        {/* Right Panel: Terminal */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div style={{
            background: '#000000',
            borderRadius: '12px',
            border: `1px solid ${SENTINEL_THEME.dim}22`,
            flex: 1,
            display: 'flex',
            flexDirection: 'column',
            maxHeight: 'calc(100vh - 250px)',
            boxShadow: '0 10px 30px rgba(0,0,0,0.5)',
          }}>
            <div style={{ 
              padding: '0.75rem 1.5rem', 
              borderBottom: `1px solid ${SENTINEL_THEME.dim}22`, 
              display: 'flex', 
              justifyContent: 'space-between',
              background: '#0a0a0c',
              borderRadius: '12px 12px 0 0'
            }}>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: SENTINEL_THEME.danger }} />
                <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: SENTINEL_THEME.warning }} />
                <div style={{ width: '8px', height: '8px', borderRadius: '50%', background: SENTINEL_THEME.success }} />
              </div>
              <span style={{ fontSize: '0.65rem', color: SENTINEL_THEME.dim, letterSpacing: '2px' }}>SENTINEL_CONSOLE_STDOUT</span>
            </div>
            
            <div style={{ 
              flex: 1, 
              overflowY: 'auto', 
              padding: '1.5rem',
              scrollbarWidth: 'thin',
              scrollbarColor: `${SENTINEL_THEME.accent}22 transparent`
            }}>
              {logs.map((log, i) => (
                <LogEntry key={i} timestamp={log.ts} message={log.msg} type={log.type} />
              ))}
              <div ref={logEndRef} />
            </div>
          </div>

          <div style={{ display: 'flex', gap: '1rem' }}>
             <button style={{
               flex: 2,
               padding: '1.2rem',
               background: `linear-gradient(45deg, ${SENTINEL_THEME.accent}, #00aaff)`,
               color: '#000',
               border: 'none',
               borderRadius: '8px',
               fontWeight: '900',
               fontSize: '0.9rem',
               letterSpacing: '2px',
               cursor: 'pointer',
               boxShadow: `0 5px 15px ${SENTINEL_THEME.accent}44`,
             }}>
               FORCE EVOLUTION CYCLE
             </button>
             <button style={{
               flex: 1,
               padding: '1.2rem',
               background: 'transparent',
               border: `2px solid ${SENTINEL_THEME.danger}`,
               color: SENTINEL_THEME.danger,
               borderRadius: '8px',
               fontWeight: 'bold',
               cursor: 'pointer',
             }}>
               STOP
             </button>
          </div>
        </div>
      </main>
    </div>
  );
}
