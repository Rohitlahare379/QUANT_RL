import React from 'react';
import Editor from '@monaco-editor/react';
import { Play, Save, Target, FolderOpen } from 'lucide-react';

interface WorkshopProps {
  strategyName: string;
  setStrategyName: (name: string) => void;
  code: string;
  setCode: (code: string | undefined) => void;
  activeAsset: string;
  setActiveAsset: (asset: string) => void;
  activeTimeframe: string;
  setActiveTimeframe: (tf: string) => void;
  params: any;
  setParams: (params: any) => void;
  validationStatus: string;
  validationMessage: string;
  validateStrategy: () => void;
  saveStrategy: () => void;
  setActiveRoom: (room: string) => void;
}

const Workshop: React.FC<WorkshopProps> = ({
  strategyName, setStrategyName,
  code, setCode,
  activeAsset, setActiveAsset,
  activeTimeframe, setActiveTimeframe,
  params, setParams,
  validationStatus, validationMessage,
  validateStrategy, saveStrategy,
  setActiveRoom
}) => {
  return (
    <div className="flex-1 flex flex-col bg-[#1e1e1e] overflow-hidden">
      {/* Workshop Header */}
      <div className="h-16 border-b border-[#333] flex items-center justify-between px-6 bg-[#1e1e1e]">
        <div className="flex items-center space-x-4 flex-1">
          <div className="flex items-center space-x-2 bg-[#252526] px-3 py-1.5 rounded border border-[#444]">
             <FolderOpen className="w-4 h-4 text-[#858585]" />
             <input 
               value={strategyName}
               onChange={(e) => setStrategyName(e.target.value)}
               className="bg-transparent text-sm font-medium text-[#cccccc] focus:outline-none w-64"
               placeholder="Strategy name..."
             />
          </div>
          <div className={`text-[11px] font-bold px-2 py-0.5 rounded border ${
            validationStatus === 'valid' ? 'bg-emerald-500/10 text-emerald-500 border-emerald-500/30' :
            validationStatus === 'error' ? 'bg-red-500/10 text-red-500 border-red-500/30' :
            'bg-[#333] text-[#858585] border-[#444]'
          }`}>
            {validationMessage.toUpperCase()}
          </div>
        </div>
        
        <div className="flex items-center space-x-3">
          <button onClick={saveStrategy} className="flex items-center space-x-2 border border-[#444] bg-[#252526] hover:bg-[#333] text-white px-5 py-2.5 rounded-lg text-[13px] font-semibold transition-none shadow-sm">
            <Save className="w-4 h-4 text-[#858585]" />
            <span>Save</span>
          </button>
          <button 
            onClick={() => setActiveRoom('r2')} 
            disabled={validationStatus !== 'valid'}
            className={`flex items-center space-x-2 border border-[#444] px-5 py-2.5 rounded-lg text-[13px] font-semibold transition-none shadow-sm ${
              validationStatus === 'valid' 
                ? 'bg-[#252526] hover:bg-[#333] text-white' 
                : 'bg-[#1a1a1b] text-[#555] cursor-not-allowed opacity-50'
            }`}
          >
            <Target className={`w-4 h-4 ${validationStatus === 'valid' ? 'text-indigo-400' : 'text-[#444]'}`} />
            <span>{validationStatus === 'valid' ? 'Ready for simulation' : 'Validate first'}</span>
          </button>
          <button onClick={validateStrategy} className="flex items-center space-x-2 border border-[#444] bg-indigo-500/10 hover:bg-indigo-500/20 text-indigo-400 px-5 py-2.5 rounded-lg text-[13px] font-semibold transition-none shadow-sm">
            <Play className="w-4 h-4" />
            <span>Run</span>
          </button>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        {/* Monaco Editor */}
        <div className="flex-1 relative">
          <Editor
            height="100%"
            defaultLanguage="python"
            theme="vs-dark"
            value={code}
            onChange={setCode}
            options={{
              minimap: { enabled: false },
              fontSize: 14,
              fontFamily: "'JetBrains Mono', 'Fira Code', monospace",
              lineNumbers: 'on',
              roundedSelection: false,
              scrollBeyondLastLine: false,
              readOnly: false,
              automaticLayout: true,
              padding: { top: 20 }
            }}
          />
        </div>

        {/* Property Panel */}
        <div className="w-80 border-l border-[#333] bg-[#1e1e1e] p-6 overflow-y-auto custom-scrollbar">
          <div className="space-y-8">
            <section>
              <h3 className="text-[11px] font-bold text-[#858585] uppercase tracking-widest mb-4">Market context</h3>
              <div className="space-y-4">
                <div>
                  <label className="text-[11px] text-[#555] font-bold uppercase mb-1.5 block">Target Asset</label>
                  <select 
                    value={activeAsset}
                    onChange={(e) => setActiveAsset(e.target.value)}
                    className="w-full bg-[#252526] border border-[#333] text-sm text-white p-2.5 rounded-lg focus:outline-none focus:border-indigo-500/50"
                  >
                    <option value="BTCUSDT">Bitcoin (BTC/USDT)</option>
                    <option value="ETHUSDT">Ethereum (ETH/USDT)</option>
                    <option value="SOLUSDT">Solana (SOL/USDT)</option>
                  </select>
                </div>
                <div>
                  <label className="text-[11px] text-[#555] font-bold uppercase mb-1.5 block">Timeframe</label>
                  <select 
                    value={activeTimeframe}
                    onChange={(e) => setActiveTimeframe(e.target.value)}
                    className="w-full bg-[#252526] border border-[#333] text-sm text-white p-2.5 rounded-lg focus:outline-none focus:border-indigo-500/50"
                  >
                    <option value="1m">1 minute</option>
                    <option value="5m">5 minutes</option>
                    <option value="1h">1 hour</option>
                    <option value="1d">1 day</option>
                  </select>
                </div>
              </div>
            </section>

            <section>
              <h3 className="text-[11px] font-bold text-[#858585] uppercase tracking-widest mb-4">Parameters</h3>
              <div className="space-y-4">
                {Object.entries(params).map(([key, val]) => (
                  <div key={key}>
                    <label className="text-[11px] text-[#555] font-bold uppercase mb-1.5 block">{key.replace(/([A-Z])/g, ' $1')}</label>
                    <input 
                      type="number"
                      value={val as number}
                      onChange={(e) => setParams({...params, [key]: parseFloat(e.target.value)})}
                      className="w-full bg-[#252526] border border-[#333] text-sm text-white p-2.5 rounded-lg focus:outline-none focus:border-indigo-500/50"
                    />
                  </div>
                ))}
              </div>
            </section>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Workshop;
