import React, { useState } from 'react';
import { Activity, ShieldCheck, Zap, CheckCircle2, XCircle, AlertCircle, Clock } from 'lucide-react';
import EvaluationReport from './EvaluationReport';
import OrchestrationTrace from './OrchestrationTrace';

interface AgentOutput {
  agent_id: string;
  timestamp: string;
  status: string;
  data: any;
  logs: string[];
}

interface SharedContext {
  regime_analysis: any;
  robustness_results: any;
  deployment_decision: string;
  decision_reasoning: string;
  agent_outputs: Record<string, AgentOutput>;
  current_phase: string;
}

interface OrchestratorProps {
  strategyName: string;
  code: string;
  asset: string;
  timeframe: string;
  params: any;
  globalMetrics: any;
  setWorkflowStep: (step: any) => void;
}

const Orchestrator: React.FC<OrchestratorProps> = ({
  strategyName, code, asset, timeframe, params, globalMetrics, setWorkflowStep
}) => {
  const [isOrchestrating, setIsOrchestrating] = useState(false);
  const [context, setContext] = useState<SharedContext | null>(null);

  const runOrchestration = async () => {
    setIsOrchestrating(true);
    setWorkflowStep('EVALUATING');
    setContext(null);
    try {
      const res = await fetch('http://localhost:8000/api/orchestrate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          strategy_name: strategyName,
          strategy_code: code,
          asset: asset,
          timeframe: timeframe,
          parameters: params,
          replay_metrics: globalMetrics
        })
      });
      const data = await res.json();
      setContext(data);
      setWorkflowStep('EVALUATED');
    } catch (e) {
      console.error('Orchestration failed:', e);
    } finally {
      setIsOrchestrating(false);
    }
  };

  const getPhaseColor = (phase: string) => {
    if (phase === 'COMPLETED') return 'text-emerald-400';
    if (phase.includes('FAILED')) return 'text-red-400';
    if (phase === 'PENDING') return 'text-[#858585]';
    return 'text-blue-400 animate-pulse';
  };

  return (
    <div className="flex-1 overflow-y-auto bg-[#1e1e1e] p-10 custom-scrollbar text-[#cccccc]">
      {/* Summary Header (Visible when completed) */}
      {context?.deployment_decision && (
        <div className="mb-10 bg-[#252526] border border-indigo-500/30 rounded-2xl p-10 shadow-[0_0_50px_rgba(99,102,241,0.05)]">
           <div className="flex justify-between items-start mb-8">
              <div>
                <h1 className="text-3xl font-bold text-white mb-2">Evaluation Summary</h1>
                <p className="text-[#858585] font-medium uppercase tracking-widest text-[11px]">Autonomous assessment report — {new Date().toISOString().split('T')[0]}</p>
              </div>
              <div className="text-right">
                <div className={`text-5xl font-black mb-2 ${
                  context.deployment_decision === 'DEPLOY' ? 'text-emerald-500' : 'text-red-500'
                }`}>{context.deployment_decision}</div>
                <div className="text-[11px] font-bold text-[#555] uppercase tracking-widest">Final Status</div>
              </div>
           </div>

           <div className="grid grid-cols-4 gap-8 mb-8 border-y border-[#333] py-8">
              <div>
                <div className="text-[11px] font-bold text-[#555] uppercase tracking-widest mb-2">Backtest ROI</div>
                <div className="text-2xl font-bold text-white">{globalMetrics?.total_return?.toFixed(1)}%</div>
              </div>
              <div>
                <div className="text-[11px] font-bold text-[#555] uppercase tracking-widest mb-2">Robustness</div>
                <div className="text-2xl font-bold text-indigo-400">{context?.robustness_results?.robustness_score}/100</div>
              </div>
              <div>
                <div className="text-[11px] font-bold text-[#555] uppercase tracking-widest mb-2">Suitability</div>
                <div className="text-2xl font-bold text-yellow-500">{context?.regime_analysis?.suitability_score}/100</div>
              </div>
              <div>
                <div className="text-[11px] font-bold text-[#555] uppercase tracking-widest mb-2">Max Drawdown</div>
                <div className="text-2xl font-bold text-red-400">{(globalMetrics?.max_drawdown || 0).toFixed(1)}%</div>
              </div>
           </div>

           <div className="bg-[#1e1e1e] p-6 rounded-xl border border-[#333]">
              <h3 className="text-[11px] font-bold text-[#555] uppercase tracking-widest mb-3">Deployment Rationale</h3>
              <p className="text-[#cccccc] text-[15px] leading-relaxed italic">"{context.decision_reasoning}"</p>
           </div>
        </div>
      )}

      {/* Header */}
      <div className="flex justify-between items-center mb-10 border-b border-[#333] pb-6">
        <div className="flex items-center space-x-3">
          <div className="w-4 h-4 bg-indigo-500 rounded-full shadow-[0_0_10px_rgba(99,102,241,0.5)]"></div>
          <h2 className="text-2xl font-bold text-white">Autonomous evaluation</h2>
          <span className="text-sm text-[#858585] ml-4">{strategyName} — {asset}</span>
        </div>
        <div className="flex items-center space-x-6">
          <div className="text-sm">
            <span className="uppercase tracking-widest text-[11px] font-bold text-[#555] mr-2">Workflow status:</span>
            <span className={`font-mono font-bold ${getPhaseColor(context?.current_phase || (isOrchestrating ? 'RUNNING' : 'IDLE'))}`}>
              {context?.current_phase || (isOrchestrating ? 'RUNNING' : 'IDLE')}
            </span>
          </div>
          <button 
            onClick={runOrchestration}
            disabled={isOrchestrating || !globalMetrics}
            className={`flex items-center space-x-2 px-6 py-2.5 rounded-lg text-sm font-bold transition-all ${
              isOrchestrating || !globalMetrics
              ? 'bg-[#252526] text-[#555] cursor-not-allowed border border-[#333]' 
              : 'bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-500/20'
            }`}
          >
            <Activity className={`w-4 h-4 ${isOrchestrating ? 'animate-spin' : ''}`} />
            <span>{isOrchestrating ? 'Evaluating...' : !globalMetrics ? 'Simulation data required' : 'Start autonomous workflow'}</span>
          </button>
        </div>
      </div>

      <div className="grid grid-cols-3 gap-8">
        {/* Left Column: Agent Cards */}
        <div className="col-span-2 space-y-6">
          {/* Agent 1: Regime Classifier */}
          <AgentCard 
            title="Agent 1: Regime Classifier"
            icon={<Zap className="w-5 h-5 text-yellow-500" />}
            output={context?.agent_outputs?.['RegimeClassifier']}
            data={context?.regime_analysis}
            metrics={[
              { label: 'Volatility', value: `${context?.regime_analysis?.volatility_score}%` },
              { label: 'Trend Strength', value: `${context?.regime_analysis?.trend_strength}%` },
              { label: 'Suitability', value: `${context?.regime_analysis?.suitability_score}/100` }
            ]}
          />

          {/* Agent 2: Robustness Tester */}
          <AgentCard 
            title="Agent 2: Robustness Tester"
            icon={<ShieldCheck className="w-5 h-5 text-emerald-500" />}
            output={context?.agent_outputs?.['RobustnessTester']}
            data={context?.robustness_results}
            metrics={[
              { label: 'Robustness Score', value: `${context?.robustness_results?.robustness_score}/100` },
              { label: 'Overfit Risk', value: context?.robustness_results?.overfitting_risk },
              { label: 'Stability', value: context?.robustness_results?.sharpe_stability }
            ]}
          />

          {/* Final Decision Panel */}
          {context?.deployment_decision && (
            <div className={`p-8 rounded-2xl border-2 bg-opacity-5 flex flex-col space-y-4 ${
              context.deployment_decision === 'DEPLOY' ? 'bg-emerald-500 border-emerald-500/30' : 
              context.deployment_decision === 'REJECT' ? 'bg-red-500 border-red-500/30' : 
              'bg-yellow-500 border-yellow-500/30'
            }`}>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  {context.deployment_decision === 'DEPLOY' ? <CheckCircle2 className="w-8 h-8 text-emerald-500" /> : 
                   context.deployment_decision === 'REJECT' ? <XCircle className="w-8 h-8 text-red-500" /> : 
                   <AlertCircle className="w-8 h-8 text-yellow-500" />}
                  <h3 className="text-2xl font-bold text-white tracking-tight">System Recommendation: {context.deployment_decision}</h3>
                </div>
                <div className="text-right">
                  <div className="text-[11px] font-bold text-[#858585] uppercase tracking-widest">Confidence</div>
                  <div className="text-2xl font-mono text-white">94.2%</div>
                </div>
              </div>
              <p className="text-[15px] text-[#cccccc] leading-relaxed border-t border-[#333] pt-4 italic">
                "{context.decision_reasoning}"
              </p>
            </div>
          )}
        </div>

        {/* Right Column: Timeline & Meta */}
        <div className="space-y-6">
           {/* Timeline View */}
           <div className="bg-[#252526] border border-[#333] rounded-xl p-6">
             <h3 className="text-[12px] font-bold text-[#858585] uppercase tracking-widest mb-6 flex items-center">
               <Clock className="w-4 h-4 mr-2" />
               Orchestration Timeline
             </h3>
             <div className="space-y-6 relative">
                <div className="absolute left-2.5 top-2 bottom-2 w-px bg-[#333]"></div>
                {getAllLogs(context).map((log, i) => (
                  <div key={i} className="relative pl-8 text-[13px]">
                    <div className="absolute left-0 top-1 w-5 h-5 bg-[#1e1e1e] border-2 border-indigo-500/50 rounded-full flex items-center justify-center">
                      <div className="w-1.5 h-1.5 bg-indigo-500 rounded-full"></div>
                    </div>
                    <div className="text-[#555] font-mono text-[11px] mb-0.5">{log.timestamp}</div>
                    <div className="text-[#cccccc] leading-snug">{log.message}</div>
                  </div>
                ))}
                {(!context && !isOrchestrating) && (
                  <div className="text-[13px] text-[#444] italic pl-8">Awaiting workflow start...</div>
                )}
             </div>
           </div>

           {/* Summary Stats */}
           <div className="bg-indigo-500/5 border border-indigo-500/20 rounded-xl p-6">
             <h3 className="text-[12px] font-bold text-indigo-400 uppercase tracking-widest mb-4">Workflow Metadata</h3>
             <div className="space-y-3">
                <MetaItem label="Strategy ID" value="STR-042" />
                <MetaItem label="Asset" value={asset} />
                <MetaItem label="Timeframe" value={timeframe} />
                <MetaItem label="Analysis Depth" value="L3 (Robust)" />
             </div>
           </div>
        </div>
      </div>

      {/* Orchestration Trace Visualization */}
      <OrchestrationTrace 
        traces={context?.traces || []} 
        isOrchestrating={isOrchestrating}
      />
      
      {/* Detailed Evaluation Report */}
      {context?.deployment_decision && (
        <div className="mt-16">
          <EvaluationReport 
            strategyName={strategyName}
            asset={asset}
            timeframe={timeframe}
            context={context}
            globalMetrics={globalMetrics}
          />
        </div>
      )}
    </div>
  );
};

const AgentCard: React.FC<{title: string, icon: any, output?: AgentOutput, data?: any, metrics: any[]}> = ({
  title, icon, output, data, metrics
}) => {
  if (!output) {
    return (
      <div className="bg-[#1a1a1b] border border-[#333] rounded-xl p-6 opacity-40">
        <div className="flex items-center space-x-3 mb-4">
          {icon}
          <h3 className="text-[14px] font-bold text-[#858585]">{title}</h3>
        </div>
        <div className="h-20 flex items-center justify-center italic text-sm text-[#444]">Pending pipeline sequence...</div>
      </div>
    );
  }

  return (
    <div className="bg-[#252526] border border-[#333] rounded-xl p-6 shadow-sm">
      <div className="flex justify-between items-center mb-6">
        <div className="flex items-center space-x-3">
          {icon}
          <h3 className="text-[16px] font-bold text-white">{title}</h3>
        </div>
        <span className="text-[11px] font-mono text-[#555]">{output.timestamp.split('T')[1].split('.')[0]}</span>
      </div>

      <div className="grid grid-cols-3 gap-4 mb-6">
        {metrics.map((m, i) => (
          <div key={i} className="bg-[#1e1e1e] p-4 rounded-lg border border-[#333]">
            <div className="text-[10px] font-bold text-[#555] uppercase tracking-widest mb-1">{m.label}</div>
            <div className="text-xl font-bold text-white font-mono">{m.value || '---'}</div>
          </div>
        ))}
      </div>

      {data?.reasoning && (
        <div className="bg-[#1e1e1e] p-4 rounded-lg border border-indigo-500/10 text-[13px] text-[#858585] italic leading-relaxed">
          "{data.reasoning}"
        </div>
      )}
    </div>
  );
};

const MetaItem: React.FC<{label: string, value: string}> = ({label, value}) => (
  <div className="flex justify-between items-center text-[13px]">
    <span className="text-[#555] font-semibold uppercase text-[10px] tracking-wider">{label}</span>
    <span className="text-[#cccccc] font-mono">{value}</span>
  </div>
);

const getAllLogs = (context: SharedContext | null) => {
  if (!context) return [];
  const logs: {timestamp: string, message: string}[] = [];
  Object.values(context.agent_outputs).forEach(out => {
    out.logs.forEach(l => {
      logs.push({
        timestamp: out.timestamp.split('T')[1].split('.')[0],
        message: l
      });
    });
  });
  return logs.sort((a, b) => a.timestamp.localeCompare(b.timestamp));
};

export default Orchestrator;
