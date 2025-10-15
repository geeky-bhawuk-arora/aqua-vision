import React from 'react';
import { motion } from 'framer-motion';
import { Sparkles, Clock, Image } from 'lucide-react';

const HomePage = ({ setCurrentPage, isDark }) => {
  return (
    <div className="min-h-[calc(100vh-4rem)] flex items-center justify-center px-4">
      <div className="max-w-5xl mx-auto text-center">
        <motion.div
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
        >
          <motion.div
            className="inline-block mb-6"
            animate={{ rotate: [0, 5, -5, 0] }}
            transition={{ duration: 3, repeat: Infinity }}
          >
            <Sparkles className="w-16 h-16 text-cyan-400 mx-auto" />
          </motion.div>
          
          <h1 className={`text-5xl sm:text-7xl font-bold mb-6 ${isDark ? 'text-white' : 'text-slate-900'}`}>
            See the{' '}
            <span className="bg-gradient-to-r from-cyan-400 via-blue-500 to-purple-600 bg-clip-text text-transparent">
              unseen
            </span>{' '}
            beneath
          </h1>
          
          <p className={`text-xl sm:text-2xl mb-12 ${isDark ? 'text-slate-300' : 'text-slate-600'} max-w-2xl mx-auto`}>
            Transform murky underwater images into crystal-clear visions with AI-powered enhancement technology
          </p>

          <motion.button
            onClick={() => setCurrentPage('upload')}
            className="px-8 py-4 bg-gradient-to-r from-cyan-500 to-blue-600 text-white text-lg font-semibold rounded-full shadow-lg hover:shadow-cyan-500/50 transition-all"
            whileHover={{ scale: 1.05, boxShadow: '0 0 30px rgba(6, 182, 212, 0.5)' }}
            whileTap={{ scale: 0.95 }}
          >
            Try Enhancement
          </motion.button>

          <div className="grid grid-cols-1 sm:grid-cols-3 gap-6 mt-20">
            {[
              { icon: Sparkles, title: 'AI Enhancement', desc: 'Advanced neural networks restore underwater clarity' },
              { icon: Clock, title: 'Instant Processing', desc: 'Get results in seconds, not minutes' },
              { icon: Image, title: 'High Quality', desc: 'Preserve detail while removing water artifacts' }
            ].map((feature, idx) => (
              <motion.div
                key={idx}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.2 * idx }}
                className={`p-6 rounded-2xl ${isDark ? 'bg-slate-800/50' : 'bg-white/50'} backdrop-blur-sm border ${isDark ? 'border-slate-700' : 'border-slate-200'}`}
              >
                <feature.icon className="w-12 h-12 text-cyan-400 mx-auto mb-4" />
                <h3 className={`text-xl font-semibold mb-2 ${isDark ? 'text-white' : 'text-slate-900'}`}>{feature.title}</h3>
                <p className={isDark ? 'text-slate-400' : 'text-slate-600'}>{feature.desc}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>
    </div>
  );
};

export default HomePage;
