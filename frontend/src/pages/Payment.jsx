import React, { useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';

export default function Payment() {
    const { id } = useParams();
    const navigate = useNavigate();
    const [loading, setLoading] = useState(false);
    const [paymentMethod, setPaymentMethod] = useState('');

    const handlePayment = (e) => {
        e.preventDefault();
        if (!paymentMethod) {
            alert("Please select a payment method.");
            return;
        }
        setLoading(true);
        setTimeout(() => {
            navigate(`/verification/${id}`);
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
                <div className="flex-1 bg-yellow-300 py-3 relative border-r border-gray-300 pl-4 flex items-center justify-center text-black">
                    <div>Payment <br/> भुगतान</div>
                    <div className="absolute top-0 -right-4 w-0 h-0 border-t-[24px] border-t-transparent border-b-[24px] border-b-transparent border-l-[16px] border-l-yellow-300 z-10"></div>
                </div>
                <div className="flex-1 bg-gray-200 py-3 relative border-r border-gray-300 pl-4 flex items-center justify-center text-gray-700">
                    <div>Photo, Sign & Photo Identity Card Upload <br/> फोटो, साइन व फोटो पहचान पत्र अपलोड</div>
                    <div className="absolute top-0 -right-4 w-0 h-0 border-t-[24px] border-t-transparent border-b-[24px] border-b-transparent border-l-[16px] border-l-gray-200 z-10"></div>
                </div>
                <div className="flex-1 bg-gray-200 py-3 pl-4 flex items-center justify-center text-gray-700">
                    <div>Center Selection & Agreeing to Declaration <br/> केंद्र चयन व घोषणा सहमति करना</div>
                </div>
            </div>

            <div className="border border-gray-400 bg-white p-8 shadow-sm mb-12">
                <div className="bg-[#0b3d91] text-white font-bold p-2 text-sm mb-6">
                    Payment Gateway Integration / भुगतान गेटवे एकीकरण
                </div>
                
                <form onSubmit={handlePayment}>
                    <div className="mb-6 flex space-x-2 border border-blue-200 bg-blue-50 p-4 font-bold text-blue-800 text-sm">
                        <span>Application fee / आवेदन शुल्क:</span>
                        <span>₹ 100.00</span>
                    </div>

                    <div className="space-y-4 mb-8">
                        <div className="font-bold text-[14px] text-gray-800 border-b border-gray-300 pb-2">Select Payment Method / भुगतान विधि चुनें</div>
                        
                        <label className="flex items-center space-x-3 p-3 border border-gray-300 hover:bg-gray-50 cursor-pointer">
                            <input type="radio" name="payment" value="sbi_netbanking" onChange={(e) => setPaymentMethod(e.target.value)} required />
                            <span className="text-sm font-bold text-gray-700">SBI Net Banking (State Bank of India)</span>
                        </label>
                        <label className="flex items-center space-x-3 p-3 border border-gray-300 hover:bg-gray-50 cursor-pointer">
                            <input type="radio" name="payment" value="upi" onChange={(e) => setPaymentMethod(e.target.value)} required />
                            <span className="text-sm font-bold text-gray-700">UPI (BHIM, Google Pay, PhonePe)</span>
                        </label>
                        <label className="flex items-center space-x-3 p-3 border border-gray-300 hover:bg-gray-50 cursor-pointer">
                            <input type="radio" name="payment" value="card" onChange={(e) => setPaymentMethod(e.target.value)} required />
                            <span className="text-sm font-bold text-gray-700">Credit / Debit Card (Visa, MasterCard, RuPay)</span>
                        </label>
                    </div>

                    <div className="mt-12 pt-4 border-t border-gray-300 text-center">
                        <button 
                            type="submit" 
                            disabled={loading} 
                            className="border border-gray-400 bg-[#e6e6e6] hover:bg-[#d4d4d4] text-black text-sm px-8 py-2 font-bold shadow-sm active:shadow-inner transition-colors disabled:opacity-50"
                        >
                            {loading ? 'Processing Payment / भुगतान संसाधित हो रहा है...' : 'Pay & Continue / भुगतान करें और आगे बढ़ें'}
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
