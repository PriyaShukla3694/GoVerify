import React, { useState, useEffect } from 'react';

export default function OfficerDashboard() {
    const [queue, setQueue] = useState([]);
    const [selectedApp, setSelectedApp] = useState(null);
    const [loading, setLoading] = useState(true);

    const fetchQueue = async () => {
        try {
            const res = await fetch('http://localhost:5000/api/v1/officer/queue');
            const data = await res.json();
            setQueue(data.queue);
        } catch (e) { console.error(e); }
        setLoading(false);
    };

    useEffect(() => { fetchQueue(); }, []);

    const handleSelect = async (id) => {
        try {
            const res = await fetch(`http://localhost:5000/api/v1/officer/applications/${id}`);
            const data = await res.json();
            setSelectedApp(data);
        } catch (e) { console.error(e); }
    };

    const submitReview = async (decision) => {
        try {
            await fetch(`http://localhost:5000/api/v1/officer/applications/${selectedApp.application_id}/review`, {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({decision, notes: 'Reviewed via Dashboard'})
            });
            setSelectedApp(null);
            fetchQueue();
        } catch (e) { console.error(e); }
    };

    const getScoreColor = (score) => {
        if(score >= 0.9) return "bg-green-100 text-green-800";
        if(score >= 0.7) return "bg-yellow-100 text-yellow-800";
        return "bg-red-100 text-red-800 border border-red-200 shadow-sm";
    };

    return (
        <div className="max-w-6xl mx-auto mt-6 grid grid-cols-12 gap-8 px-4 font-sans">
            {/* Sidebar Queue */}
            <div className="col-span-4 bg-white rounded-2xl shadow border border-gray-100 overflow-hidden flex flex-col h-[85vh]">
                <div className="p-4 bg-blue-50 border-b border-blue-100">
                    <h3 className="text-sm font-bold uppercase tracking-wider text-blue-800">Review Queue</h3>
                </div>
                <div className="flex-1 overflow-y-auto p-2 space-y-2">
                    {loading ? <p className="p-4 text-gray-400">Loading...</p> : null}
                    {queue.length === 0 && !loading ? <p className="p-4 text-gray-400 text-center">Queue is empty! 🎉</p> : null}
                    {queue.map(app => (
                        <div key={app.id} onClick={() => handleSelect(app.id)} 
                             className={`p-3 rounded-xl cursor-pointer hover:bg-gray-50 flex items-center justify-between transition ${selectedApp?.application_id === app.id ? 'bg-blue-50 shadow-sm ring-1 ring-blue-200' : 'bg-white border text-gray-600'}`}>
                            <div className="truncate font-medium">{app.submitted_name || "Unknown"}</div>
                            <div className={`text-xs px-2 py-1 rounded-full font-bold ${getScoreColor(app.overall_confidence)}`}>
                                {(app.overall_confidence * 100).toFixed(0)}% Match
                            </div>
                        </div>
                    ))}
                </div>
            </div>

            {/* Main Stage */}
            <div className="col-span-8">
                {selectedApp ? (
                    <div className="bg-white rounded-2xl shadow-xl border border-gray-100 p-8 h-[85vh] overflow-y-auto">
                        <div className="flex justify-between items-start mb-6">
                            <div>
                                <h2 className="text-2xl font-bold text-gray-800">Application: {selectedApp.metadata_comparison.user_provided_name}</h2>
                                <p className="text-sm text-gray-500 font-mono mt-1">ID: {selectedApp.application_id}</p>
                            </div>
                            <div className={`px-4 py-2 rounded-xl text-lg font-bold flex flex-col items-center ${getScoreColor(selectedApp.overall_confidence)}`}>
                                {(selectedApp.overall_confidence * 100).toFixed(0)}%
                                <span className="text-[10px] uppercase opacity-75">Confidence</span>
                            </div>
                        </div>

                        {selectedApp.flags.length > 0 && (
                            <div className="mb-8 bg-red-50 p-4 rounded-xl border border-red-200">
                                <h4 className="font-bold text-red-800 mb-2 flex items-center"><span className="mr-2">⚠️</span> Cross-Validation Flags</h4>
                                <ul className="text-sm text-red-700 space-y-1 ml-6 list-disc">
                                    {selectedApp.flags.map((f, i) => <li key={i}>Mismatch in <b>{f.field}</b>: {f.reason}</li>)}
                                </ul>
                            </div>
                        )}

                        <div className="grid grid-cols-2 gap-8 mb-8">
                            <div className="bg-gray-50 rounded-xl p-6 border border-gray-200">
                                <h4 className="text-xs uppercase tracking-widest font-bold text-gray-500 mb-4 pb-2 border-b">OCR Extracted Data</h4>
                                <div className="space-y-4 text-sm">
                                    {selectedApp.documents_processed.map((doc, i) => (
                                        <div key={i}>
                                            <span className="inline-block px-2 py-0.5 bg-blue-100 text-blue-800 text-xs rounded font-bold mb-2 uppercase">{doc.type}</span>
                                            {Object.entries(doc.extracted_fields).map(([k,v]) => (
                                                <div key={k} className="mb-1 flex justify-between">
                                                    <span className="text-gray-500 capitalize">{k.replace('_', ' ')}:</span>
                                                    <span className="font-medium text-gray-800">{v}</span>
                                                </div>
                                            ))}
                                        </div>
                                    ))}
                                </div>
                            </div>
                            
                            <div className="bg-gray-50 rounded-xl p-6 border border-gray-200">
                                <h4 className="text-xs uppercase tracking-widest font-bold text-gray-500 mb-4 pb-2 border-b">User Provided Metadata</h4>
                                <div className="space-y-3 text-sm">
                                    <div className="flex justify-between">
                                        <span className="text-gray-500">Name:</span>
                                        <span className="font-medium text-gray-800">{selectedApp.metadata_comparison.user_provided_name || '-'}</span>
                                    </div>
                                    <div className="flex justify-between">
                                        <span className="text-gray-500">DOB:</span>
                                        <span className="font-medium text-gray-800">{selectedApp.metadata_comparison.user_provided_dob || '-'}</span>
                                    </div>
                                    <div className="flex flex-col">
                                        <span className="text-gray-500 mb-1">Address:</span>
                                        <span className="font-medium text-gray-800 p-2 bg-white rounded border">{selectedApp.metadata_comparison.user_provided_address || '-'}</span>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <div className="flex space-x-4 border-t pt-6">
                            <button onClick={() => submitReview('approved')} className="flex-1 bg-green-600 hover:bg-green-700 text-white font-bold py-4 rounded-xl shadow-sm transition transform hover:-translate-y-0.5">✅ Approve Application</button>
                            <button onClick={() => submitReview('rejected')} className="flex-1 bg-white border-2 border-red-200 text-red-600 hover:bg-red-50 hover:border-red-600 font-bold py-4 rounded-xl shadow-sm transition">❌ Reject</button>
                        </div>
                    </div>
                ) : (
                    <div className="h-[85vh] flex items-center justify-center bg-gray-50 rounded-2xl border-2 border-dashed border-gray-200 text-gray-400 font-medium text-lg">
                        Select an application from the queue to review
                    </div>
                )}
            </div>
        </div>
    );
}
