import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

/*export default defineConfig({
	plugins: [sveltekit()]
});*/


export default defineConfig({
    plugins: [sveltekit()],
    server: {
        proxy: {
            '/api': {
                target: 'http://localhost:8000', // Your backend API URL
                changeOrigin: true,
                rewrite: (path) => path.replace(/^\/api/, '')
            }
        }
    }
});