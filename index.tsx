
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
        DISCORD LINK: <span style={{ color: SENTINEL_THEME.success }}>ACTIVE</span>
      </div>
      <div style={{ fontSize: '0.75rem', color: SENTINEL_THEME.dim }}>
        UPTIME: <span style={{ color: SENTINEL_THEME.accent }}>14:22:05</span>
      </div>
    </div>
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
    fontFamily: '"JetBrains Mono", monospace',
    borderRadius: '0 4px 4px 0',
  }}>
    <span style={{ color: SENTINEL_THEME.dim, marginRight: '1rem' }}>[{timestamp}]</span>
    <span style={{ color: type === 'error' ? SENTINEL_THEME.danger : SENTINEL_THEME.text }}>{message}</span>
  </div>
);

export default function SentinelDashboard() {
  const [logs, setLogs] = useState([
    { ts: '10:00:23', msg: '🚀 Sentinel v7.6.2 Ghost Protocol Active.', type: 'info' },
    { ts: '10:00:39', msg: '✨ Learned: skill_whale_hunter', type: 'success' },
    { ts: '10:00:58', msg: '🏪 PLS DONATE: Page Loaded.', type: 'success' },
    { ts: '10:01:05', msg: '📡 DISCORD: Startup Embed Sent.', type: 'info' },
    { ts: '10:10:20', msg: '🚨 THREAT DETECTED: report context found.', type: 'error' },
    { ts: '10:10:21', msg: '📡 DISCORD: Sending Critical Alert...', type: 'info' },
  ]);
  const [aiAnalysis, setAiAnalysis] = useState('Monitoring for Whale Activity and Admin presence.');
  const [analyzing, setAnalyzing] = useState(false);
  const logEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    logEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [logs]);

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
      <main style={{ padding: '2rem', flex: 1, display: 'grid', gridTemplateColumns: '320px 1fr', gap: '2.5rem' }}>
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <MetricCard label="Global Status" value="WATCHING" color={SENTINEL_THEME.warning} />
          <MetricCard label="Discord Link" value="CONNECTED" color={SENTINEL_THEME.success} />
          <MetricCard label="Kill Switch" value="ARMED" color={SENTINEL_THEME.danger} />
        </div>

        <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
          <div style={{
            background: '#000000',
            borderRadius: '12px',
            border: `1px solid ${SENTINEL_THEME.dim}22',
            flex: 1,
            overflowY: 'auto',
            padding: '1.5rem',
            maxHeight: 'calc(100vh - 250px)',
          }}>
            {logs.map((log, i) => (
              <LogEntry key={i} timestamp={log.ts} message={log.msg} type={log.type} />
            ))}
            <div ref={logEndRef} />
          </div>
          <div style={{ textAlign: 'center', color: SENTINEL_THEME.dim, fontSize: '0.7rem' }}>
             ALERTS CONFIGURED FOR: {process.env.DISCORD_WEBHOOK ? 'HIDDEN_WEBHOOK' : 'MISSING_SECRET'}
          </div>
        </div>
      </main>
    </div>
  );
}
