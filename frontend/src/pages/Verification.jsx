import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

export default function Verification() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [agreed, setAgreed] = useState(false);

    const handleVerify = (e) => {
        e.preventDefault();
        if (!agreed) {
            alert("Please agree to the declaration before substituting.");
            return;
        }
        setLoading(true);
        setTimeout(() => {
            navigate(`/status/${id}`);
        }, 1500);
    };

    return (
        <div className="max-w-5xl mx-auto mt-4 px-2">
            {/* Header Area mimicking IIT Roorkee */}
            <div className="flex justify-between items-center bg-white p-2 border-b-2 border-blue-800 shadow-sm mb-4">
                <div className="flex items-center space-x-4">
                    <img src="https://upload.wikimedia.org/wikipedia/en/thumb/6/6f/Indian_Institute_of_Technology_Roorkee_logo.png/220px-Indian_Institute_of_Technology_Roorkee_logo.png" alt="Emblem" className="h-16" />
                    <div>
                        <h1 className="text-xl font-bold text-black m-0 leading-tight">आईआईटी रुड़की इंटर्न</h1>
                        <h1 className="text-xl font-bold font-serif text-black m-0 leading-tight tracking-wide">IIT ROORKEE INTERN</h1>
                    </div>
                </div>
            </div>

            <div className="text-center mb-6">
                <h2 className="font-bold text-[17px] text-black m-0">Application Form For Blockathon Internship Registration - 2026</h2>
                <h2 className="font-bold text-[17px] text-black m-0">ब्लॉकथॉन इंटर्नशिप पंजीकरण के लिए आवेदन पत्र-2026</h2>
            </div>

            {/* Progress Bar arrows */}
            <div className="flex text-xs font-bold text-center mb-6 overflow-hidden bg-white shadow-sm border border-gray-200">
                <div className="flex-1 bg-green-200 text-green-800 py-3 relative border-r border-gray-300 flex items-center justify-center">
                    <div>Part I Registration <br/> भाग I पंजीकरण (Completed)</div>
                    <div className="absolute top-0 -right-4 w-0 h-0 border-t-[24px] border-t-transparent border-b-[24px] border-b-transparent border-l-[16px] border-l-green-200 z-10"></div>
                </div>
                <div className="flex-1 bg-green-200 text-green-800 py-3 relative border-r border-gray-300 pl-4 flex items-center justify-center">
                    <div>Payment <br/> भुगतान (Completed)</div>
                    <div className="absolute top-0 -right-4 w-0 h-0 border-t-[24px] border-t-transparent border-b-[24px] border-b-transparent border-l-[16px] border-l-green-200 z-10"></div>
                </div>
                <div className="flex-1 bg-green-200 text-green-800 py-3 relative border-r border-gray-300 pl-4 flex items-center justify-center">
                    <div>Photo, Sign & Identity <br/> फोटो, साइन व पहचान (Completed)</div>
                    <div className="absolute top-0 -right-4 w-0 h-0 border-t-[24px] border-t-transparent border-b-[24px] border-b-transparent border-l-[16px] border-l-green-200 z-10"></div>
                </div>
                <div className="flex-1 bg-yellow-300 py-3 pl-4 flex items-center justify-center text-black">
                    <div>Declaration <br/> घोषणा सहमति</div>
                </div>
            </div>

            <div className="border border-gray-400 bg-white p-8 shadow-sm mb-12">
                <div className="bg-[#0b3d91] text-white font-bold p-2 text-sm mb-6">
                    Final Declaration / अंतिम घोषणा
                </div>
                
                <form onSubmit={handleVerify}>
                    <div className="border border-gray-300 bg-gray-50 p-6 mb-6 text-sm text-gray-800 space-y-4 h-48 overflow-y-auto font-serif">
                        <p><strong>DECLARATION:</strong></p>
                        <p>1. I hereby declare that all statements made in this application are true, complete and correct to the best of my knowledge and belief.</p>
                        <p>2. I understand that in the event of any information being found false or incorrect at any stage or not satisfying the eligibility criteria according to the requirements of the relative examination, my candidature/appointment is liable to be cancelled/terminated.</p>
                        <p>3. I have authorized GovVerify AI-Engine to automatically process my uploaded Identity Documents (Aadhaar/PAN) against the government database to authenticate my identity.</p>
                        <hr className="my-4 border-gray-300" />
                        <p><strong>घोषणा:</strong></p>
                        <p>1. मैं यह घोषणा करता/करती हूँ कि इस आवेदन पत्र में दिए गए सभी विवरण मेरे ज्ञान और विश्वास के अनुसार सत्य, पूर्ण और सही हैं।</p>
                        <p>2. मैं समझता/समझती हूँ कि किसी भी जानकारी के गलत या असत्य पाए जाने की स्थिति में, मेरी उम्मीदवारी रद्द की जा सकती है।</p>
                    </div>

                    <div className="mb-8">
                        <label className="flex items-start space-x-3 p-4 bg-yellow-50 border border-yellow-300 cursor-pointer">
                            <input type="checkbox" className="mt-1 h-5 w-5" checked={agreed} onChange={(e) => setAgreed(e.target.checked)} />
                            <span className="text-sm font-bold text-gray-800">
                                I have read the declaration and I agree. <br className="hidden sm:block"/> (मैंने घोषणा पढ़ ली है और मैं सहमत हूँ।)
                            </span>
                        </label>
                    </div>

                    <div className="mt-6 pt-4 border-t border-gray-300 text-center">
                        <div className="flex justify-center text-[12px] text-red-600 font-bold mb-4">
                           <span className="w-4 h-4 rounded-full border border-red-600 flex items-center justify-center text-[10px] mr-2">!</span>
                           No changes allowed after final submission / अंतिम सबमिशन के बाद कोई बदलाव की अनुमति नहीं है
                        </div>
                        <button 
                            type="submit" 
                            disabled={loading} 
                            className="bg-[#2e7d32] hover:bg-[#1b5e20] text-white text-sm px-10 py-2 font-bold shadow-md transition-colors disabled:opacity-50"
                        >
                            {loading ? 'Submitting Application / सबमिट किया जा रहा है...' : 'Final Submit / अंतिम सबमिट'}
                        </button>
                    </div>
                </form>
            </div>
            
            <div className="border-t border-blue-800 mt-8 pt-2 text-center text-[10px] text-gray-500 font-bold mb-6">
                © IIT ROORKEE
            </div>
        </div>
    );
}
