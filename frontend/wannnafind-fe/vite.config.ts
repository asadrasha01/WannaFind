import { defineConfig } from 'vite';
import angular from '@analogjs/vite-plugin-angular';

export default defineConfig({
  plugins: [angular()],
  ssr: {
    noExternal: true, // Add this to avoid externalizing Angular dependencies
  },
  build: {
    ssr: false, // Correctly specify false here
  },
});
