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
    <div className="p-4 space-y-4">
      <h1 className="text-2xl font-bold">SoundLocator Control Panel</h1>

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

      <div>
        <label>Max Brightness</label>
        <input
          type="range"
          min={1}
          max={255}
          value={config.max_brightness}
          onChange={(e) => handleChange('max_brightness', Number(e.target.value))}
        />
        <span className="ml-2">{config.max_brightness}</span>
      </div>

      <div>
        <label>Preset</label>
        <select
          value={config.preset}
          onChange={(e) => handleChange('preset', e.target.value)}
        >
          {['default', 'directional'].map((preset) => (
            <option key={preset} value={preset}>
              {preset}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label>Color Scheme</label>
        <select
          value={config.color_scheme}
          onChange={(e) => handleChange('color_scheme', e.target.value)}
        >
          {['default'].map((cs) => (
            <option key={cs} value={cs}>
              {cs}
            </option>
          ))}
        </select>
      </div>

      <div className="space-x-4">
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded"
          onClick={save}
        >
          Save Changes
        </button>

        <button
          className="bg-red-500 text-white px-4 py-2 rounded"
          onClick={shutdown}
        >
          Shutdown
        </button>
      </div>
    </div>
  );
}