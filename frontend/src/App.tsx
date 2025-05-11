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

  const darkMode = () => {
    document.documentElement.classList.toggle('dark');
  }

  if (loading) return <div className="p-4">Loading config...</div>;

  return (
    <div className="m-4">
      <div className="grid grid-flow-col justify-items-end">
        <button onClick={darkMode}>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
            <path strokeLinecap="round" strokeLinejoin="round" d="M21.752 15.002A9.72 9.72 0 0 1 18 15.75c-5.385 0-9.75-4.365-9.75-9.75 0-1.33.266-2.597.748-3.752A9.753 9.753 0 0 0 3 11.25C3 16.635 7.365 21 12.75 21a9.753 9.753 0 0 0 9.002-5.998Z" />
          </svg>
        </button>

        <button onClick={shutdown}>
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={1.5} stroke="currentColor" className="size-6">
            <path strokeLinecap="round" strokeLinejoin="round" d="M5.636 5.636a9 9 0 1 0 12.728 0M12 3v9" />
          </svg>
        </button>
      </div>

      <div className="my-4 columns-2 gap-x-4 rounded-xl bg-slate-50 p-6 shadow-lg outline outline-black/5 dark:bg-slate-900 dark:shadow-none dark:-outline-offset-1 dark:outline-white/10">
        <div>
          <div>
            <label>Brightness</label>
            <input
              type="range"
              min={0}
              max={config.max_brightness}
              value={config.brightness}
              onChange={(e) => handleChange('brightness', Number(e.target.value))}
            />
            <span className="ml-2">{config.brightness}</span>
          </div>
        </div>

        <div>
          <div>
            <label>Preset</label>
            <select
              value={config.preset}
              onChange={(e) => handleChange('preset', e.target.value)}
              className="bg-slate-100 dark:bg-slate-800"
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