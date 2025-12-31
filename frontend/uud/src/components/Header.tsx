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
        <option value="unrate-by-social-group">Unemployment rate by social group</option>
        <option value="real-registered-unemployment">Real unemployment vs. Registered unemployment</option>
        <option value="regions-unemployment">Unemployment rate by regions</option>
      </select>
    </div>
  );
}
