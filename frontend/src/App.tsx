import { useEffect, useState } from 'react';
import axios from 'axios';


export default function App() {
  const [config, setConfig] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    axios.get('/config').then((res) => {
      setConfig(res.data);
      setLoading(false);
    });
  }, []);

  const handleChange = (key: string, value: any) => {
    setConfig((prev: any) => ({ ...prev, [key]: value }));
  };

  const save = () => {
    axios.post('/config', config);
  };

  const shutdown = () => {
    axios.post('/shutdown').then(() => {
      alert("🛑 Raspberry Pi is shutting down...");
    }).catch(() => {
      alert("❌ Shutdown command failed");
    });
  };

  if (loading) return <div className="p-4">Loading config...</div>;

  return (
    <div className="m-4">
      <div className="grid grid-flow-col justify-items-end">
        <button onClick={shutdown}>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
            <path strokeLinecap="round" strokeLinejoin="round" d="M5.636 5.636a9 9 0 1 0 12.728 0M12 3v9" />
          </svg>
        </button>
      </div>

      <div className="my-4 grid grid-cols-1 md:grid-cols-2 gap-4 rounded-md p-6 bg-slate-900">
        <div>
          <div>
            <label>Brightness</label>
            <div className="flex items-center h-48 overflow-visible">
              <input
                type="range"
                min={0}
                max={Math.round(config.max_brightness * 100)}
                value={Math.round(config.brightness * 100)}
                onChange={(e) => handleChange('brightness', Math.round(Number(e.target.value)) / 100)}
                className="-rotate-90 h-10 bg-slate-800 rounded-lg appearance-none cursor-pointer range-lg"
              />
            </div>
            <span>{Math.round(config.brightness * 100)}%</span>
          </div>
        </div>

        <div>
          <div>
            <label>Preset</label>
            <select
              value={config.preset}
              onChange={(e) => handleChange('preset', e.target.value)}
              className="bg-slate-800"
            >
              {['default', 'directional'].map((preset) => (
                <option key={preset} value={preset}>
                  {preset}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>

      <div className="grid grid-flow-col justify-items-end">
        <button
          className="bg-indigo-500 hover:bg-indigo-800 text-white px-4 py-2 rounded"
          onClick={save}
        >
          Save
        </button>
      </div>
    </div>
  );
}