import './Header.css'

export default function Header({ value, onChange }) {
  return (
    <div className="app-header">
      <label className="header-label" htmlFor="chart-select">
        Select chart:
      </label>
      <select
        id="chart-select"
        className="header-select"
        value={value}
        onChange={(e) => onChange(e.target.value)}
      >
        <option value="categories">Unemployment by social groups</option>
        <option value="real-registered">Unemployment vs. Registered unemployment</option>
        <option value="regions">Unemployment by regions</option>
      </select>
    </div>
  );
}
