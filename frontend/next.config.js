/** @type {import('next').NextConfig} */
const nextConfig = {
  // Improve webpack performance
  webpack: (config, { dev, isServer }) => {
    // Only enable in development
    if (dev && !isServer) {
      // Reduce compilation warnings
      config.ignoreWarnings = [{ module: /node_modules\/webpack-hot-middleware/ }];
    }

    return config;
  },

  // Optimize output
  output: 'standalone',

  // Disable static export for development
  trailingSlash: false,

  // Optimize images if any
  images: {
    unoptimized: true, // For development
  },

  // Enable experimental features that might help
  experimental: {
    webpackBuildWorker: false, // Disable worker threads if causing issues
  },
};

module.exports = nextConfig;