import { FileText } from 'lucide-react';
import './Header.css';

function Header() {
  return (
    <header className="header">
      <div className="header-content">
        <div className="header-title">
          <FileText size={32} />
          <h1>AI Meeting Summarizer</h1>
        </div>
        <p className="header-subtitle">
          Automatically transcribe, summarize, and generate meeting minutes
        </p>
      </div>
    </header>
  );
}

export default Header;
