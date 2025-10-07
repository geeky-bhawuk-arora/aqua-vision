import React from 'react';
import { motion } from 'framer-motion';
import { CheckCircle, AlertCircle, Info } from 'lucide-react';

const Toast = ({ message, type }) => {
  const icons = {
    success: <CheckCircle className="w-5 h-5" />,
    error: <AlertCircle className="w-5 h-5" />,
    info: <Info className="w-5 h-5" />
  };

  const colors = {
    success: 'bg-emerald-500',
    error: 'bg-red-500',
    info: 'bg-blue-500'
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: -50 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -50 }}
      className={`fixed top-4 right-4 ${colors[type]} text-white px-6 py-4 rounded-lg shadow-lg flex items-center gap-3 z-50`}
    >
      {icons[type]}
      <span>{message}</span>
    </motion.div>
  );
};

export default Toast;