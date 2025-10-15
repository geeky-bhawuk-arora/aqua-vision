import React from 'react';

import { motion } from 'framer-motion';

const AboutPage = ({ isDark }) => {
  return (
    <div className="min-h-[calc(100vh-4rem)] py-12 px-4">
      <div className="max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1 className={`text-4xl font-bold mb-6 ${isDark ? 'text-white' : 'text-slate-900'}`}>
            About AquaVision
          </h1>
          
          <div className={`p-8 rounded-2xl mb-8 ${isDark ? 'bg-slate-800/50' : 'bg-white/50'} backdrop-blur-sm border ${isDark ? 'border-slate-700' : 'border-slate-200'}`}>
            <h2 className={`text-2xl font-semibold mb-4 ${isDark ? 'text-white' : 'text-slate-900'}`}>
              Our AI Model
            </h2>
            <p className={`mb-4 ${isDark ? 'text-slate-300' : 'text-slate-700'}`}>
              AquaVision uses a state-of-the-art convolutional neural network trained on over 100,000 underwater images. 
              Our model specializes in color correction, dehazing, and contrast enhancement to reveal hidden details beneath the surface.
            </p>
            <p className={`mb-4 ${isDark ? 'text-slate-300' : 'text-slate-700'}`}>
              The architecture combines U-Net for spatial restoration with attention mechanisms for color balance, 
              achieving superior results compared to traditional image processing techniques.
            </p>
          </div>

          <div className={`p-8 rounded-2xl mb-8 ${isDark ? 'bg-slate-800/50' : 'bg-white/50'} backdrop-blur-sm border ${isDark ? 'border-slate-700' : 'border-slate-200'}`}>
            <h2 className={`text-2xl font-semibold mb-4 ${isDark ? 'text-white' : 'text-slate-900'}`}>
              Coming Soon
            </h2>
            <div className="space-y-4">
              <div className={`p-4 rounded-lg ${isDark ? 'bg-slate-700/50' : 'bg-slate-100'}`}>
                <h3 className={`font-semibold mb-2 ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`}>📡 Live Feed Processing</h3>
                <p className={isDark ? 'text-slate-300' : 'text-slate-700'}>
                  Real-time video enhancement for underwater drones and ROVs
                </p>
              </div>
              <div className={`p-4 rounded-lg ${isDark ? 'bg-slate-700/50' : 'bg-slate-100'}`}>
                <h3 className={`font-semibold mb-2 ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`}>🗺️ 3D Depth Map Generation</h3>
                <p className={isDark ? 'text-slate-300' : 'text-slate-700'}>
                  Reconstruct underwater environments in three dimensions
                </p>
              </div>
              <div className={`p-4 rounded-lg ${isDark ? 'bg-slate-700/50' : 'bg-slate-100'}`}>
                <h3 className={`font-semibold mb-2 ${isDark ? 'text-cyan-400' : 'text-cyan-600'}`}>🤖 Object Detection</h3>
                <p className={isDark ? 'text-slate-300' : 'text-slate-700'}>
                  Automatic identification of marine life and underwater structures
                </p>
              </div>
            </div>
          </div>

          <div className={`p-8 rounded-2xl ${isDark ? 'bg-gradient-to-br from-slate-800 to-slate-900' : 'bg-gradient-to-br from-cyan-50 to-blue-50'} border ${isDark ? 'border-slate-700' : 'border-slate-200'}`}>
            <h2 className={`text-2xl font-semibold mb-4 ${isDark ? 'text-white' : 'text-slate-900'}`}>
              Get in Touch
            </h2>
            <p className={`mb-4 ${isDark ? 'text-slate-300' : 'text-slate-700'}`}>
              Have questions or want to collaborate? We'd love to hear from you.
            </p>
            <div className="flex flex-col sm:flex-row gap-4">
              <a href="mailto:info@aquavision.ai" className={`px-6 py-3 rounded-lg text-center ${isDark ? 'bg-slate-700 text-white' : 'bg-white text-slate-900'} font-semibold hover:scale-105 transition-transform`}>
                Email Us
              </a>
              <a href="#" className={`px-6 py-3 rounded-lg text-center ${isDark ? 'bg-slate-700 text-white' : 'bg-white text-slate-900'} font-semibold hover:scale-105 transition-transform`}>
                Documentation
              </a>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default AboutPage;
