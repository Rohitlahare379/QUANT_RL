import re

with open("/Users/rohitdiliplahare/Desktop/QUANT_RL/frontend/src/App.tsx", "r") as f:
    content = f.read()

# 1. Add state variables for custom dates
state_injection = """  const [activeRegime, setActiveRegime] = useState('full_history');
  const [customStart, setCustomStart] = useState('2021-01-01');
  const [customEnd, setCustomEnd] = useState('2021-06-01');"""

content = re.sub(r"const \[activeRegime, setActiveRegime\] = useState\('covid_2020'\);", state_injection, content)

# 2. Update getRegimeName
get_regime_name = """  const getRegimeName = () => {
     switch(activeRegime) {
        case 'full_history': return 'Full Market Cycle';
        case 'covid_2020': return 'COVID 2020';
        case 'ftx_collapse': return 'FTX Collapse';
        case '2018_bear': return '2018 Bear Market';
        case 'bull_market': return 'Bull Market';
        case 'sideways': return 'Sideways Market';
        case 'custom': return `Custom (${customStart} to ${customEnd})`;
        default: return activeRegime;
     }
  };"""

content = re.sub(r"const getRegimeName = \(\) => \{[\s\S]*?\};\n", get_regime_name + "\n", content)

# 3. Update startSimulation payload
start_sim = """    socket.onopen = () => {
      socket.send(JSON.stringify({
        code: code,
        symbol: activeAsset,
        speed_multiplier: 20.0,
        regime: activeRegime,
        start_time: customStart + 'T00:00:00Z',
        end_time: customEnd + 'T00:00:00Z'
      }));
    };"""

content = re.sub(r"socket\.onopen = \(\) => \{[\s\S]*?\}\);[\s\S]*?\};", start_sim, content)

# 4. Update the Regimes Grid
regimes_grid = """            {/* Regimes Grid */}
            <div className="grid grid-cols-4 gap-6">
              <div onClick={() => setActiveRegime('full_history')} className={`cursor-pointer bg-[#252526] border p-5 rounded-xl ${activeRegime === 'full_history' ? 'border-[#666]' : 'border-[#333]'}`}>
                <div className="flex justify-between items-center mb-3">
                   <span className="text-[14px] text-white font-bold">Full Market Cycle</span>
                   {activeRegime === 'full_history' && <span className="bg-orange-500/20 text-orange-400 text-[10px] px-2 py-0.5 rounded-full uppercase font-bold tracking-wider">active</span>}
                </div>
                <div className="text-2xl font-light text-emerald-500 mb-1">2017-Present</div>
                <div className="text-[12px] text-[#858585]">Full backtest</div>
              </div>

              <div onClick={() => setActiveRegime('covid_2020')} className={`cursor-pointer bg-[#252526] border p-5 rounded-xl ${activeRegime === 'covid_2020' ? 'border-[#666]' : 'border-[#333]'}`}>
                <div className="flex justify-between items-center mb-3">
                   <span className="text-[14px] text-white font-bold">COVID Crash</span>
                   {activeRegime === 'covid_2020' && <span className="bg-orange-500/20 text-orange-400 text-[10px] px-2 py-0.5 rounded-full uppercase font-bold tracking-wider">active</span>}
                </div>
                <div className="text-2xl font-light text-orange-500 mb-1">Feb-May '20</div>
                <div className="text-[12px] text-[#858585]">High volatility</div>
              </div>
              
              <div onClick={() => setActiveRegime('ftx_collapse')} className={`cursor-pointer bg-[#252526] border p-5 rounded-xl ${activeRegime === 'ftx_collapse' ? 'border-[#666]' : 'border-[#333]'}`}>
                <div className="flex justify-between items-center mb-3">
                   <span className="text-[14px] text-white font-bold">FTX Collapse</span>
                   {activeRegime === 'ftx_collapse' && <span className="bg-orange-500/20 text-orange-400 text-[10px] px-2 py-0.5 rounded-full uppercase font-bold tracking-wider">active</span>}
                </div>
                <div className="text-2xl font-light text-red-500 mb-1">Nov-Dec '22</div>
                <div className="text-[12px] text-[#858585]">Black swan</div>
              </div>

              <div className="bg-[#252526] border border-[#333] p-5 rounded-xl flex flex-col items-center justify-center row-span-2">
                <div className="text-[12px] font-bold text-[#858585] uppercase tracking-widest mb-3">ROBUSTNESS</div>
                <div className="text-4xl font-light text-orange-500 mb-3">54/100</div>
                <div className="text-[13px] text-orange-500 flex items-center font-bold"><span className="mr-2">⚠</span> moderate</div>
              </div>

              <div onClick={() => setActiveRegime('2018_bear')} className={`cursor-pointer bg-[#252526] border p-5 rounded-xl ${activeRegime === '2018_bear' ? 'border-[#666]' : 'border-[#333]'}`}>
                <div className="flex justify-between items-center mb-3">
                   <span className="text-[14px] text-white font-bold">2018 Bear Market</span>
                   {activeRegime === '2018_bear' && <span className="bg-orange-500/20 text-orange-400 text-[10px] px-2 py-0.5 rounded-full uppercase font-bold tracking-wider">active</span>}
                </div>
                <div className="text-2xl font-light text-red-500 mb-1">2018 Year</div>
                <div className="text-[12px] text-[#858585]">Extended drawdown</div>
              </div>

              <div onClick={() => setActiveRegime('bull_market')} className={`cursor-pointer bg-[#252526] border p-5 rounded-xl ${activeRegime === 'bull_market' ? 'border-[#666]' : 'border-[#333]'}`}>
                <div className="flex justify-between items-center mb-3">
                   <span className="text-[14px] text-white font-bold">Bull Market</span>
                   {activeRegime === 'bull_market' && <span className="bg-orange-500/20 text-orange-400 text-[10px] px-2 py-0.5 rounded-full uppercase font-bold tracking-wider">active</span>}
                </div>
                <div className="text-2xl font-light text-emerald-500 mb-1">2020-2021</div>
                <div className="text-[12px] text-[#858585]">Up only</div>
              </div>

              <div onClick={() => setActiveRegime('sideways')} className={`cursor-pointer bg-[#252526] border p-5 rounded-xl ${activeRegime === 'sideways' ? 'border-[#666]' : 'border-[#333]'}`}>
                <div className="flex justify-between items-center mb-3">
                   <span className="text-[14px] text-white font-bold">Sideways Market</span>
                   {activeRegime === 'sideways' && <span className="bg-orange-500/20 text-orange-400 text-[10px] px-2 py-0.5 rounded-full uppercase font-bold tracking-wider">active</span>}
                </div>
                <div className="text-2xl font-light text-[#ccc] mb-1">Mid 2023</div>
                <div className="text-[12px] text-[#858585]">Chop / Range bound</div>
              </div>

              <div onClick={() => setActiveRegime('custom')} className={`cursor-pointer bg-[#252526] border p-5 rounded-xl col-span-2 ${activeRegime === 'custom' ? 'border-indigo-500/50 bg-indigo-500/5' : 'border-[#333]'}`}>
                <div className="flex justify-between items-center mb-3">
                   <span className="text-[14px] text-white font-bold">Custom Date Range</span>
                   {activeRegime === 'custom' && <span className="bg-indigo-500/20 text-indigo-400 text-[10px] px-2 py-0.5 rounded-full uppercase font-bold tracking-wider">active</span>}
                </div>
                <div className="flex items-center space-x-4 mt-4" onClick={e => e.stopPropagation()}>
                    <div className="flex flex-col">
                       <label className="text-[11px] text-[#858585] mb-1 uppercase tracking-widest font-bold">Start Date</label>
                       <input type="date" value={customStart} onChange={e => {setCustomStart(e.target.value); setActiveRegime('custom');}} className="bg-[#1e1e1e] border border-[#444] rounded px-3 py-1.5 text-sm text-white focus:outline-none focus:border-indigo-500" />
                    </div>
                    <span className="text-[#858585] mt-4">→</span>
                    <div className="flex flex-col">
                       <label className="text-[11px] text-[#858585] mb-1 uppercase tracking-widest font-bold">End Date</label>
                       <input type="date" value={customEnd} onChange={e => {setCustomEnd(e.target.value); setActiveRegime('custom');}} className="bg-[#1e1e1e] border border-[#444] rounded px-3 py-1.5 text-sm text-white focus:outline-none focus:border-indigo-500" />
                    </div>
                </div>
              </div>
            </div>"""

content = re.sub(r"\{\/\* Regimes Grid \*\/\}.*?<\/div>[\s\n]*<\/div>[\s\n]*\)}", regimes_grid + "\n\n         </div>\n      )}", content, flags=re.DOTALL)

with open("/Users/rohitdiliplahare/Desktop/QUANT_RL/frontend/src/App.tsx", "w") as f:
    f.write(content)

print("Updated App.tsx successfully.")
