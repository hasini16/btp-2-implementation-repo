import React, { useState } from 'react';
import toast from 'react-hot-toast';

const CadAutomation: React.FC = () => {
  const [file, setFile] = useState<File | null>(null);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [result, setResult] = useState<any>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setFile(e.target.files[0]);
      toast.success(`Selected file: ${e.target.files[0].name}`, {
        icon: '📁',
      });
    }
  };

  const handleUpload = async () => {
    if (!file) {
      toast.error('Please select a .SLDPRT file first.');
      return;
    }
    
    setIsProcessing(true);
    setResult(null);
    
    // Create a loading toast that we can dismiss/update later
    const toastId = toast.loading('Connecting and processing CAD data...');

    // Mocking the backend call
    setTimeout(() => {
      setIsProcessing(false);
      
      // Update the existing loading toast to a success toast
      toast.success('Extracted features & generated G-Code successfully!', {
        id: toastId,
      });

      setResult({
        status: 'Completed successfully',
        faces: Math.floor(Math.random() * 50) + 12,
        edges: Math.floor(Math.random() * 100) + 40,
        gcode: 'G21 G90 G17\nM06 T1\nM03 S1200\nG00 X0 Y0 Z50\n...'
      });

    }, 2500);
  };

  return (
    <div className="module-container">
      <h2>CAD/CAM Automation Generator</h2>
      <p style={{ color: 'var(--text-muted)', marginBottom: '32px' }}>
        Upload a SolidWorks (.SLDPRT) file to automatically extract B-Rep logic 
        and compile the respective CAMWorks machine G-Code operations.
      </p>
      
      <div className="upload-section" style={{marginBottom: '32px'}}>
        <input 
          type="file" 
          accept=".SLDPRT" 
          onChange={handleFileChange} 
          disabled={isProcessing}
        />
        <button className="primary-btn" onClick={handleUpload} disabled={isProcessing || !file}>
          {isProcessing ? 'Processing Model...' : 'Run Automated Extraction'}
        </button>
      </div>

      {result && (
        <div className="status-card" style={{animation: 'fadeIn 0.4s ease-out'}}>
          <div className="status-indicators">
             <div className="status-item">
                 <div className="status-label">Overall Status</div>
                 <div className="status-value text-healthy">{result.status}</div>
             </div>
             <div className="status-item">
                 <div className="status-label">Faces Recognized</div>
                 <div className="status-value">{result.faces} features</div>
             </div>
             <div className="status-item">
                 <div className="status-label">Edges Intersected</div>
                 <div className="status-value">{result.edges} links</div>
             </div>
          </div>
          <div style={{ marginTop: '16px' }}>
            <div className="status-label">Generated G-Code Preview</div>
            <pre style={{
              background: 'var(--bg-primary)', 
              padding: '16px', 
              borderRadius: '8px', 
              color: 'var(--accent-purple)',
              fontFamily: 'monospace',
              marginTop: '8px',
              border: '1px solid var(--glass-border)'
            }}>
              {result.gcode}
            </pre>
          </div>
        </div>
      )}
    </div>
  );
};

export default CadAutomation;
