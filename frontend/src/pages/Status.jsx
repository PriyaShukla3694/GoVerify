import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';

export default function Status() {
    const { id } = useParams();
    const [report, setReport] = useState(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchStatus = async () => {
            try {
                const res = await fetch(`http://localhost:5000/api/v1/applications/${id}/report`);
                const data = await res.json();
                setReport(data);
            } catch(e) {
                console.error(e);
            } finally {
                setLoading(false);
            }
        };
        fetchStatus();
    }, [id]);

    if (loading) return <div className="text-center mt-20 text-gray-500 font-medium">Looking up your application...</div>;
    if (!report || report.error) return <div className="text-center mt-20 text-red-500 font-bold text-xl">Application Not Found</div>;

    const getStatusUI = () => {
        switch(report.recommendation) {
            case 'auto_approve': 
                return { color: 'text-green-600', bg: 'bg-green-50 text-green-700', icon: '✅', text: 'Auto-Verified' };
            case 'flag_for_review':
                return { color: 'text-yellow-600', bg: 'bg-yellow-50 text-yellow-700', icon: '⏳', text: 'Under Manual Review' };
            default:
                return { color: 'text-red-600', bg: 'bg-red-50 text-red-700', icon: '⚠️', text: 'Manual Intervention Required' };
        }
    };

    const ui = getStatusUI();

    return (
        <div className="max-w-2xl mx-auto mt-12 bg-white p-8 rounded-2xl shadow-xl border border-gray-100 font-sans">
            <div className="text-center mb-8">
                <div className="text-5xl mb-4">{ui.icon}</div>
                <h2 className="text-3xl font-bold text-gray-800">Application Status</h2>
                <p className="text-gray-500 mt-2 font-mono text-sm">Tracking ID: {id}</p>
            </div>

            <div className={`p-4 rounded-xl mb-8 flex items-center justify-center font-bold text-lg border ${ui.bg.replace('text', 'border')}`}>
                {ui.text}
            </div>

            <div className="grid grid-cols-2 gap-4 mb-8">
                <div className="bg-gray-50 p-4 rounded-xl border">
                    <p className="text-xs text-gray-500 font-bold uppercase tracking-wider mb-1">Submitted Name</p>
                    <p className="font-medium text-gray-800">{report.metadata_comparison.user_provided_name}</p>
                </div>
                <div className="bg-gray-50 p-4 rounded-xl border">
                    <p className="text-xs text-gray-500 font-bold uppercase tracking-wider mb-1">Documents Scanned</p>
                    <p className="font-medium text-gray-800">{report.documents_processed.length} Files</p>
                </div>
            </div>

            <div className="mb-8">
                <h3 className="font-bold text-gray-800 border-b pb-2 mb-4">Verification Checkpoints</h3>
                <ul className="space-y-3 text-sm">
                    <li className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                        <span className="font-medium text-gray-700">Name Match (Aadhaar &harr; PAN)</span>
                        <span>{report.validation_results.name_match ? '✅ Verified' : '❌ Mismatch'}</span>
                    </li>
                    <li className="flex justify-between items-center p-3 bg-gray-50 rounded-lg">
                        <span className="font-medium text-gray-700">Date of Birth Verification</span>
                        <span>{report.validation_results.dob_match ? '✅ Verified' : '❌ Mismatch'}</span>
                    </li>
                </ul>
            </div>

            <div className="text-center pt-6 border-t font-medium">
                <Link to="/" className="text-blue-600 hover:text-blue-800 underline">Submit Another Application</Link>
            </div>
        </div>
    );
}
