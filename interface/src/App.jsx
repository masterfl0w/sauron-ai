import React, { useState, useEffect, useRef } from 'react';
import { 
  LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer 
} from 'recharts';
import { 
  Cpu, HardDrive, Activity, Zap, ShieldAlert, CheckCircle2, 
  Info, Terminal, Eye
} from 'lucide-react';
import { css } from '../styled-system/css';
import { flex, stack, vstack, hstack } from '../styled-system/patterns';

const WS_URL = 'ws://127.0.0.1:8000/ws';

export default function App() {
  const [trainingData, setTrainingData] = useState([]);
  const [hardwareStats, setHardwareStats] = useState({ cpu: 0, ram: 0, gpu: [] });
  const [connected, setConnected] = useState(false);
  const scrollRef = useRef(null);
  const wsRef = useRef(null);

  useEffect(() => {
    const connect = () => {
      const ws = new WebSocket(WS_URL);
      wsRef.current = ws;
      ws.onopen = () => setConnected(true);
      ws.onmessage = (e) => {
        const message = JSON.parse(e.data);
        if (message.type === 'training_metrics') {
          setTrainingData((prev) => [...prev, message.data].slice(-1000));
        } else if (message.type === 'hardware_stats') {
          setHardwareStats(message.data);
        }
      };
      ws.onclose = () => {
        setConnected(false);
        wsRef.current = null;
        setTimeout(connect, 2000);
      };
      ws.onerror = () => ws.close();
    };
    connect();
    return () => wsRef.current?.close();
  }, []);

  useEffect(() => {
    if (scrollRef.current) {
      scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
    }
  }, [trainingData]);

  const lastMetrics = trainingData.length > 0 ? trainingData[trainingData.length - 1] : null;
  const last10 = trainingData.slice(-10);
  const last100 = trainingData.slice(-100);
  const avgLoss10 = last10.length > 0 ? last10.reduce((acc, d) => acc + d.loss, 0) / last10.length : 0;
  const avgLoss100 = last100.length > 0 ? last100.reduce((acc, d) => acc + d.loss, 0) / last100.length : 0;
  const minLoss = trainingData.length > 0 ? Math.min(...trainingData.map(d => d.loss)) : 0;
  const isHealthy = trainingData.length < 10 || (avgLoss10 <= avgLoss100 * 1.05);

  const formatScientific = (num) => {
    if (!num || num === 0) return '0.0000';
    if (num >= 0.001) return num.toFixed(6);
    const [base, exp] = num.toExponential(4).split('e');
    return (
      <span className={css({ display: 'inline-flex', alignItems: 'baseline', gap: '1' })}>
        <span className={css({ fontSize: 'xl', fontWeight: 'bold' })}>{base}</span>
        <span className={css({ fontSize: 'xs', opacity: 0.5 })}>×10</span>
        <sup className={css({ fontSize: '10px' })}>{exp}</sup>
      </span>
    );
  };

  return (
    <div className={css({ minH: 'screen', bg: 'bg', color: 'text.primary', display: 'flex', flexDir: 'column', overflow: 'hidden', position: 'relative' })}>
      
      {/* Ambient Background Layer */}
      <div className={css({ 
        position: 'absolute', inset: 0, zIndex: 0, overflow: 'hidden', pointerEvents: 'none',
        bg: 'radial-gradient(circle at 50% 50%, rgba(225, 78, 78, 0.02) 0%, transparent 70%)'
      })}>
        {/* Moving Scanline */}
        <div 
          className={css({
            position: 'absolute', top: 0, left: 0, right: 0, height: '1px',
            bg: 'linear-gradient(to right, transparent, rgba(225, 78, 78, 0.1), transparent)',
            opacity: 0.5
          })} 
          style={{ animation: 'scanline 8s linear infinite' }}
        />
        
        {/* Floating Particles (Cyber Dust) */}
        {[...Array(6)].map((_, i) => (
          <div 
            key={i} 
            className={css({
              position: 'absolute',
              w: '1px', h: '40px',
              bg: 'accent',
              opacity: 0.1,
              left: `${15 + (i * 15)}%`,
              top: `${20 + (i * 10)}%`,
              filter: 'blur(1px)'
            })} 
            style={{ animation: `float ${5 + i}s ease-in-out infinite` }}
          />
        ))}

        {/* Ambient Glows */}
        <div 
          className={css({
            position: 'absolute', bottom: '-10%', left: '-5%', w: '40%', h: '40%',
            bg: 'accent', borderRadius: 'full', filter: 'blur(120px)',
          })} 
          style={{ animation: 'pulse-glow 10s ease-in-out infinite' }}
        />
      </div>

      {/* Top Header */}
      <header className={css({ 
        h: '70px', 
        borderBottom: '1px solid border', 
        display: 'flex', 
        alignItems: 'center', 
        justifyContent: 'space-between',
        px: '8',
        bg: 'rgba(18, 20, 26, 0.8)',
        backdropBlur: 'md',
        position: 'relative',
        zIndex: 10
      })}>
        <div className={hstack({ gap: '4' })}>
          <div className={css({ color: 'accent' })}><Eye size={24} /></div>
          <h1 className={css({ fontSize: 'xl', fontWeight: 'bold', letterSpacing: 'tight' })}>
            SAURON <span className={css({ fontWeight: 'light', opacity: 0.8 })}>AI</span>
          </h1>
          <div className={hstack({ ml: '8', gap: '2', bg: 'rgba(255,255,255,0.03)', px: '3', py: '1.5', borderRadius: 'full', border: '1px solid border' })}>
            <div className={css({ 
              w: '2', h: '2', borderRadius: 'full', 
              bg: connected ? '#22c55e' : '#e14e4e',
              boxShadow: connected ? '0 0 8px #22c55e' : 'none'
            })} />
            <span className={css({ fontSize: '10px', fontWeight: 'black', textTransform: 'uppercase', tracking: 'widest' })}>
              {connected ? 'LIVE_TELEMETRY' : 'OFFLINE'}
            </span>
          </div>
        </div>
        <div className={css({ fontSize: 'xs', color: 'text.secondary', fontWeight: 'bold', tracking: 'widest' })}>
          SESSION: <span className={css({ color: 'accent' })}>ACTIVE_TRAINING</span>
        </div>
      </header>

      {/* Main Content Area */}
      <main className={css({ flex: '1', overflowY: 'auto', p: '8', position: 'relative', zIndex: 10 })}>
        <div className={css({ display: 'grid', gridTemplateColumns: 'repeat(12, 1fr)', gap: '8', maxW: '1800px', mx: 'auto' })}>
          
          {/* Left Column: Analysis */}
          <div className={css({ gridColumn: 'span 3', display: 'flex', flexDir: 'column', gap: '6' })}>
            <div className={css({ bg: 'card', p: '6', borderRadius: 'xl', border: '1px solid border' })}>
              <label className={css({ fontSize: '10px', color: 'text.muted', textTransform: 'uppercase', fontBlack: 'black', mb: '4', display: 'block', tracking: 'widest' })}>Health Diagnostics</label>
              <div className={hstack({ 
                bg: isHealthy ? 'rgba(34, 197, 94, 0.05)' : 'rgba(225, 78, 78, 0.05)',
                p: '4', borderRadius: 'lg', border: '1px solid',
                borderColor: isHealthy ? 'rgba(34, 197, 94, 0.1)' : 'rgba(225, 78, 78, 0.1)'
              })}>
                <div className={css({ color: isHealthy ? '#22c55e' : 'accent' })}>
                  {isHealthy ? <CheckCircle2 size={24} /> : <ShieldAlert size={24} />}
                </div>
                <div>
                  <div className={css({ fontWeight: 'bold', fontSize: 'sm', color: isHealthy ? '#22c55e' : 'accent', tracking: 'tighter' })}>
                    {isHealthy ? 'GRADIENT_STABLE' : 'HIGH_VARIANCE'}
                  </div>
                  <div className={css({ fontSize: '10px', opacity: 0.6, fontWeight: 'medium' })}>Integrity check passing</div>
                </div>
              </div>
            </div>

            <StatCard label="Absolute Min Loss" value={minLoss.toFixed(6)} color="text.primary" />
            <StatCard label="Current LR" value={formatScientific(lastMetrics?.lr)} color="accent" />
            
            <div className={css({ bg: 'card', p: '6', borderRadius: 'xl', border: '1px solid border' })}>
              <label className={css({ fontSize: '10px', color: 'text.muted', textTransform: 'uppercase', mb: '4', display: 'block', tracking: 'widest' })}>Step Aggregates</label>
              <div className={vstack({ gap: '4', align: 'stretch' })}>
                <MiniStat label="Avg Loss (10)" value={avgLoss10.toFixed(4)} />
                <MiniStat label="Avg Loss (100)" value={avgLoss100.toFixed(4)} />
                <MiniStat label="Total Steps" value={lastMetrics?.step || 0} highlight />
              </div>
            </div>
          </div>

          {/* Center Column: Charts & Logs */}
          <div className={css({ gridColumn: 'span 6', display: 'flex', flexDir: 'column', gap: '8' })}>
            <div className={css({ bg: 'card', p: '8', borderRadius: '2xl', border: '1px solid border', flex: '1', minH: '500px' })}>
              <div className={hstack({ justify: 'space-between', mb: '10' })}>
                <div className={hstack({ gap: '3' })}>
                  <div className={css({ color: 'accent' })}><Activity size={22} /></div>
                  <h2 className={css({ fontWeight: 'bold', fontSize: 'lg', tracking: 'tight' })}>Training Dynamics</h2>
                </div>
                <div className={hstack({ gap: '6' })}>
                  <LegendItem color="#e14e4e" label="Loss" />
                  <LegendItem color="#3b82f6" label="Val Loss" />
                </div>
              </div>

              <div className={css({ height: '380px', width: '100%' })}>
                <ResponsiveContainer width="100%" height="100%">
                  <LineChart data={trainingData}>
                    <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.03)" vertical={false} />
                    <XAxis dataKey="step" hide />
                    <YAxis stroke="#475569" fontSize={10} axisLine={false} tickLine={false} />
                    <Tooltip 
                      contentStyle={{ bg: '#12141a', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '12px' }}
                    />
                    <Line type="monotone" dataKey="loss" stroke="#e14e4e" strokeWidth={3} dot={false} isAnimationActive={false} />
                    <Line type="monotone" dataKey="val_loss" stroke="#3b82f6" strokeWidth={3} dot={false} isAnimationActive={false} />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Logs */}
            <div className={css({ bg: 'card', borderRadius: 'xl', border: '1px solid border', height: '300px', display: 'flex', flexDir: 'column' })}>
              <div className={hstack({ p: '4', px: '6', borderBottom: '1px solid border', justify: 'space-between' })}>
                <div className={hstack({ gap: '2' })}>
                  <Terminal size={14} className={css({ color: 'accent' })} />
                  <span className={css({ fontSize: 'xs', fontWeight: 'black', color: 'text.secondary', tracking: 'widest' })}>EXECUTION_STREAM</span>
                </div>
                <div className={css({ fontSize: '10px', color: 'text.muted', fontFamily: 'mono' })}>BUFFER: 100/1000</div>
              </div>
              <div ref={scrollRef} className={css({ flex: '1', overflowY: 'auto', p: '6', fontFamily: 'mono', fontSize: '11px', scrollbarWidth: 'thin' })}>
                {trainingData.slice(-100).map((d, i) => (
                  <div key={i} className={css({ display: 'flex', gap: '6', mb: '1.5', opacity: 0.8 })}>
                    <span className={css({ color: 'text.muted' })}>{new Date(d.timestamp * 1000).toLocaleTimeString()}</span>
                    <span className={css({ color: 'accent', fontWeight: 'bold' })}>STP_{String(d.step).padStart(5, '0')}</span>
                    <span className={css({ color: 'text.secondary' })}>LOSS: <span className={css({ color: 'text.primary', fontWeight: 'bold' })}>{d.loss.toFixed(5)}</span></span>
                    <span className={css({ color: 'text.muted' })}>LR: {d.lr?.toExponential(3)}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Right Column: Hardware */}
          <div className={css({ gridColumn: 'span 3', display: 'flex', flexDir: 'column', gap: '8' })}>
            <div className={css({ bg: 'card', p: '8', borderRadius: 'xl', border: '1px solid border', h: 'full' })}>
              <div className={hstack({ mb: '10', gap: '3' })}>
                <Cpu size={22} className={css({ color: 'accent' })} />
                <h2 className={css({ fontWeight: 'bold', fontSize: 'md', tracking: 'tight' })}>System Telemetry</h2>
              </div>

              <div className={vstack({ gap: '10', align: 'stretch' })}>
                <Progress label="CPU Cluster" value={hardwareStats.cpu} color="#e14e4e" />
                <Progress label="Physical RAM" value={hardwareStats.ram} color="#3b82f6" />
              </div>

              <div className={css({ mt: '12', pt: '6', borderTop: '1px solid border' })}>
                <label className={css({ fontSize: '10px', color: 'text.muted', textTransform: 'uppercase', mb: '6', display: 'block', tracking: 'widest', fontWeight: 'bold' })}>Acceleration Engine</label>
                {hardwareStats.gpu?.length > 0 ? (
                  hardwareStats.gpu.map((gpu, idx) => (
                    <div key={idx} className={css({ bg: 'rgba(255,255,255,0.01)', p: '5', borderRadius: 'xl', border: '1px solid border' })}>
                      <div className={hstack({ justify: 'space-between', mb: '4' })}>
                        <span className={css({ fontSize: '11px', fontWeight: 'black', truncate: true, color: 'text.primary' })}>{gpu.name}</span>
                        {gpu.temp > 0 && <span className={css({ fontSize: '10px', color: 'accent', fontWeight: 'bold' })}>{gpu.temp}°C</span>}
                      </div>
                      <Progress label="Core Load" value={gpu.load} color="#22c55e" mini />
                      {gpu.type === 'apple' && (
                        <div className={css({ mt: '3', fontSize: '9px', color: 'text.muted', fontWeight: 'bold', tracking: 'tighter' })}>UNIFIED_MEMORY_MODE</div>
                      )}
                    </div>
                  ))
                ) : (
                  <div className={css({ textAlign: 'center', p: '8', border: '1px dashed border', borderRadius: 'xl', opacity: 0.4 })}>
                    <Zap size={24} className={css({ mx: 'auto', mb: '3' })} />
                    <span className={css({ fontSize: '10px', fontWeight: 'bold' })}>NO_HARDWARE_ACCELERATION</span>
                  </div>
                )}
              </div>

              <div className={css({ 
                mt: '12',
                bg: 'linear-gradient(to bottom right, rgba(225, 78, 78, 0.05), rgba(59, 130, 246, 0.05))',
                p: '6', borderRadius: '2xl', border: '1px solid border', textAlign: 'center'
              })}>
                <div className={css({ w: '14', h: '14', bg: 'rgba(225, 78, 78, 0.08)', borderRadius: 'full', display: 'flex', alignItems: 'center', justify: 'center', mx: 'auto', mb: '4' })}>
                  <Zap size={28} className={css({ color: 'accent' })} />
                </div>
                <h3 className={css({ fontWeight: 'black', fontSize: 'sm', mb: '1', tracking: 'widest' })}>SAURON_EYE</h3>
                <p className={css({ fontSize: '9px', color: 'text.muted', lineHeight: 'relaxed', fontWeight: 'bold' })}>PROTECTING_EVERY_BYTE</p>
              </div>
            </div>
          </div>

        </div>
      </main>

      <style dangerouslySetInnerHTML={{ __html: `
        .custom-scrollbar::-webkit-scrollbar { width: 4px; }
        .custom-scrollbar::-webkit-scrollbar-track { background: transparent; }
        .custom-scrollbar::-webkit-scrollbar-thumb { background: #334155; border-radius: 10px; }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover { background: #475569; }
      `}} />
    </div>
  );
}

function StatCard({ label, value, color }) {
  return (
    <div className={css({ bg: 'card', p: '6', borderRadius: 'xl', border: '1px solid border' })}>
      <label className={css({ fontSize: '10px', color: 'text.muted', textTransform: 'uppercase', mb: '4', display: 'block', tracking: 'widest' })}>{label}</label>
      <div className={css({ color: color === 'accent' ? 'accent' : 'text.primary' })}>
        {typeof value === 'string' ? <span className={css({ fontSize: '2xl', fontWeight: 'bold', fontFamily: 'mono' })}>{value}</span> : value}
      </div>
    </div>
  );
}

function MiniStat({ label, value, highlight }) {
  return (
    <div className={hstack({ justify: 'space-between', px: '1' })}>
      <span className={css({ fontSize: 'xs', color: 'text.muted', fontWeight: 'medium' })}>{label}</span>
      <span className={css({ fontSize: 'xs', fontWeight: 'bold', color: highlight ? 'accent' : 'text.primary', fontFamily: 'mono' })}>{value}</span>
    </div>
  );
}

function LegendItem({ color, label }) {
  return (
    <div className={hstack({ gap: '2' })}>
      <div 
        className={css({ w: '2.5', h: '2.5', borderRadius: 'full' })} 
        style={{ 
          backgroundColor: color, 
          boxShadow: `0 0 10px ${color}80` 
        }} 
      />
      <span className={css({ fontSize: '10px', fontWeight: 'black', color: 'text.secondary', tracking: 'widest' })}>{label}</span>
    </div>
  );
}

function Progress({ label, value, color, mini }) {
  return (
    <div className={vstack({ gap: mini ? '2' : '3', align: 'stretch' })}>
      <div className={hstack({ justify: 'space-between' })}>
        <span className={css({ fontSize: '10px', fontWeight: 'black', color: 'text.secondary', tracking: 'widest' })}>{label}</span>
        <span className={css({ fontSize: '11px', fontWeight: 'bold', fontFamily: 'mono' })}>{value.toFixed(1)}%</span>
      </div>
      <div className={css({ h: mini ? '1.5' : '2.5', bg: 'rgba(255,255,255,0.03)', borderRadius: 'full', overflow: 'hidden', border: '1px solid rgba(255,255,255,0.02)' })}>
        <div className={css({ 
          h: 'full', bg: color, borderRadius: 'full', 
          transition: 'width 1s cubic-bezier(0.4, 0, 0.2, 1)', width: `${value}%`,
          boxShadow: `0 0 12px ${color}60`
        })} />
      </div>
    </div>
  );
}
