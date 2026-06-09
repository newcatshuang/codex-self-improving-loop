import { chromium } from 'file:///C:/Users/Newcats/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/.pnpm/playwright-core@1.60.0/node_modules/playwright-core/index.mjs';

const url = process.argv[2];
const screenshotPath = process.argv[3];
const edgePath = process.argv[4] || 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe';

if (!url || !screenshotPath) {
  throw new Error('Usage: node tests/webui-browser-qa.mjs <url> <screenshot> [edgePath]');
}

const browser = await chromium.launch({
  executablePath: edgePath,
  headless: true,
});
const page = await browser.newPage({ viewport: { width: 1440, height: 1100 } });
const report = { checks: {}, errors: [] };

page.on('pageerror', (error) => report.errors.push(String(error.message || error)));
page.on('console', (message) => {
  if (message.type() === 'error') {
    report.errors.push(`${message.location().url || ''} ${message.text()}`.trim());
  }
});
page.on('requestfailed', (request) => {
  report.errors.push(`${request.url()} ${request.failure()?.errorText || 'request failed'}`);
});
page.on('response', (response) => {
  if (response.status() >= 400) {
    report.errors.push(`${response.url()} status=${response.status()}`);
  }
});

await page.goto(url, { waitUntil: 'networkidle' });
await page.evaluate(() => {
  window.__confirmCalls = [];
  window.confirm = (message) => {
    window.__confirmCalls.push(message);
    return false;
  };
});

await page.waitForSelector('#dashboardNextActionPanel');
report.checks.title = await page.locator('h1').innerText();
report.checks.dashboardNextAction = await page.locator('#dashboardNextActionCopy').innerText();
report.checks.dashboardPrimaryAction = await page.locator('#dashboardPrimaryAction').innerText();
report.checks.dashboardPriorities = await page.locator('#dashboardPriorityList .dashboard-priority-item').count();
report.checks.noHorizontalOverflowDesktop = await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1);

await page.locator('#tab-workflow').click();
await page.waitForSelector('#workflowActionStrip');
report.checks.workflowNextActionInitial = await page.locator('#workflowNextActionCopy').innerText();
report.checks.workflowPrimaryInitial = await page.locator('#workflowPrimaryAction').innerText();
report.checks.candidateCards = await page.locator('#candidateRows .candidate-card').count();

await page.locator('#workflowPrimaryAction').click();
await page.waitForFunction(() => {
  const text = document.querySelector('#workflowNextActionCopy')?.textContent || '';
  return text.includes('预览') || text.includes('Preview') || text.includes('Diff') || text.includes('diff');
}, null, { timeout: 10000 });
report.checks.workflowNextActionAfterSelect = await page.locator('#workflowNextActionCopy').innerText();
report.checks.workflowPrimaryAfterSelect = await page.locator('#workflowPrimaryAction').innerText();

await page.locator('#workflowPrimaryAction').click();
await page.waitForFunction(() => {
  const text = document.querySelector('#promotionPreviewText')?.textContent || '';
  return text.includes('USER.md') || text.includes('AGENTS.md') || text.includes('Skill') || text.includes('Patch') || text.includes('@@');
}, null, { timeout: 10000 });
report.checks.previewTextHead = (await page.locator('#promotionPreviewText').innerText()).slice(0, 220);
report.checks.workflowNextActionAfterPreview = await page.locator('#workflowNextActionCopy').innerText();

const previewButton = report.checks.workflowPrimaryAfterSelect || '';
let promotionButton = '#promoteSelected';
if (previewButton.includes('AGENTS')) {
  promotionButton = '#promoteAgents';
} else if (previewButton.includes('Patch')) {
  promotionButton = '#promotePatch';
} else if (previewButton.includes('Skill')) {
  promotionButton = '#promoteSkill';
}
report.checks.promotionButtonForPreview = promotionButton;
await page.locator('#candidateActionPanel').scrollIntoViewIfNeeded();
report.checks.promotionButtonVisible = await page.locator(promotionButton).isVisible();
report.checks.promotionButtonEnabled = await page.locator(promotionButton).isEnabled();
await page.locator(promotionButton).click();
await page.waitForTimeout(100);
report.checks.confirmCallsAfterPromoteClick = await page.evaluate(() => window.__confirmCalls.length);
report.checks.confirmPreviewIncluded = await page.evaluate(() => String(window.__confirmCalls[0] || '').includes('Promotion Diff Preview') || String(window.__confirmCalls[0] || '').includes('晋升 Diff 预览'));

await page.locator('#tab-operations').click();
await page.waitForSelector('#operationsLifecycleMap');
report.checks.operationsLifecycleCards = await page.locator('#operationsLifecycleMap article').count();
report.checks.recoveryQueueItems = await page.locator('#recoveryQueueList .recovery-queue-item').count();

await page.setViewportSize({ width: 390, height: 900 });
await page.waitForTimeout(250);
report.checks.noHorizontalOverflowMobile = await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1);
report.checks.mobileScrollWidth = await page.evaluate(() => document.documentElement.scrollWidth);
report.checks.mobileInnerWidth = await page.evaluate(() => window.innerWidth);

await page.screenshot({ path: screenshotPath, fullPage: true });
await browser.close();

console.log(JSON.stringify(report, null, 2));
