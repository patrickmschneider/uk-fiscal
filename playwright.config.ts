import {defineConfig,devices} from '@playwright/test';
export default defineConfig({
  testDir:process.env.HOSTED_SMOKE?'tests/hosted':'tests/browser',timeout:30000,fullyParallel:false,
  use:{baseURL:process.env.APP_URL||'http://127.0.0.1:5174/',screenshot:'only-on-failure'},
  projects:[{name:'chromium',use:{...devices['Desktop Chrome']}},{name:'webkit',use:{...devices['Desktop Safari']}}],
});
