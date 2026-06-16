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
report.checks.htmlLang = await page.locator('html').getAttribute('lang');
report.checks.primaryNavItems = await page.locator('#sideNav [data-nav]').evaluateAll((nodes) => nodes.map((node) => node.textContent.trim()));
report.checks.primaryNavKeys = await page.locator('#sideNav [data-nav]').evaluateAll((nodes) => nodes.map((node) => node.dataset.nav));
report.checks.primaryNavCount = report.checks.primaryNavItems.length;
report.checks.hasFunctionalNavigation = ['dashboard', 'workflow', 'data', 'automation', 'skills', 'recall', 'history', 'doctor'].every((key) => report.checks.primaryNavKeys.includes(key));
report.checks.removedDuplicateWorkflowNav = !report.checks.primaryNavKeys.includes('evidence') && !report.checks.primaryNavKeys.includes('approval');
report.checks.navGroupCount = await page.locator('#sideNav .nav-group-label').count();
report.checks.navEnglishLabels = report.checks.primaryNavItems.filter((label) => /Dashboard|Candidates|Evidence|Approval|Data|Automation|Skills|Recall|History|Doctor/.test(label));
report.checks.dashboardNextAction = await page.locator('#dashboardNextActionCopy').innerText();
report.checks.dashboardButtons = await page.locator('[data-view="dashboard"] button').count();
report.checks.dashboardActionButtons = await page.locator('[data-view="dashboard"] [data-action]').count();
report.checks.dashboardNavJumpButtons = await page.locator('[data-view="dashboard"] [data-nav-jump]').count();
report.checks.dashboardWorkflowMapVisible = await page.locator('[data-view="dashboard"] #workflowMap').isVisible().catch(() => false);
report.checks.dashboardPriorities = await page.locator('#dashboardPriorityList .dashboard-priority-item').count();
report.checks.setupChecklistItems = await page.locator('#setupChecklist .setup-check-item').count();
report.checks.operationsViewContainers = await page.locator('[data-view="operations"]').count();
report.checks.noHorizontalOverflowDesktop = await page.evaluate(() => document.documentElement.scrollWidth <= window.innerWidth + 1);
report.checks.dashboardCompactPanels = await page.evaluate(() => {
  const selectors = ['#dailyDigestPanel', '#dashboardNextActionPanel'];
  return selectors.map((selector) => {
    const node = document.querySelector(selector);
    if (!node) {
      return { selector, missing: true };
    }
    const rect = node.getBoundingClientRect();
    return {
      selector,
      width: Math.round(rect.width),
      pageRatio: Number((rect.width / window.innerWidth).toFixed(2)),
      compact: rect.width <= 720,
    };
  });
});
report.checks.dashboardCompactPanelsFit = report.checks.dashboardCompactPanels.every((item) => item.missing || item.compact);
await page.screenshot({ path: screenshotPath.replace(/\.png$/i, '.dashboard.png'), fullPage: true });

await page.locator('#tab-workflow').click();
await page.waitForSelector('#workflowActionStrip');
report.checks.workflowNextActionInitial = await page.locator('#workflowNextActionCopy').innerText();
report.checks.workflowPrimaryInitial = await page.locator('#workflowPrimaryAction').innerText();
report.checks.candidateRows = await page.locator('#candidateRows .candidate-row').count();
report.checks.candidateTableVisible = await page.locator('#workflowReviewQueue table.candidate-table').isVisible();
report.checks.mergeSuggestionPanels = await page.locator('#mergeInlineList, #mergeSuggestionsList').count();
report.checks.mergeSuggestionModuleVisible = await page.locator('#mergeSuggestionsModule').isVisible().catch(() => false);
report.checks.mergeSuggestionModuleButtons = await page.locator('#mergeSuggestionsModule button').evaluateAll((nodes) => nodes.map((node) => node.textContent.trim())).catch(() => []);
report.checks.mergeSuggestionTriggerVisible = await page.locator('#openMergeSuggestions').isVisible();
report.checks.reviewDrawerInitiallyHidden = await page.locator('#candidateReviewDrawer[hidden]').count();
await page.locator('#mergeSuggestionsModule .merge-tool-copy').click();
report.checks.mergeDrawerVisibleFromModuleContent = await page.locator('#mergeSuggestionsDrawer:not([hidden])').isVisible().catch(() => false);
report.checks.mergeDrawerWidth = await page.locator('#mergeSuggestionsDrawer .drawer-panel').evaluate((node) => Math.round(node.getBoundingClientRect().width)).catch(() => 0);
if (report.checks.mergeDrawerVisibleFromModuleContent) {
  await page.locator('#closeMergeSuggestions').click();
}
report.checks.workflowActionStripLayout = await page.locator('#workflowActionStrip').evaluate((node) => {
  const rect = node.getBoundingClientRect();
  return {
    width: Math.round(rect.width),
    pageRatio: Number((rect.width / window.innerWidth).toFixed(2)),
    compact: rect.width <= 780,
  };
});
await page.screenshot({ path: screenshotPath.replace(/\.png$/i, '.workflow.png'), fullPage: true });

await page.locator('#workflowPrimaryAction').click();
await page.waitForSelector('#candidateReviewDrawer:not([hidden])');
report.checks.reviewDrawerVisibleAfterSelect = await page.locator('#candidateReviewDrawer:not([hidden])').isVisible();
report.checks.reviewDrawerTabs = await page.locator('#candidateReviewDrawer [data-drawer-tab]').evaluateAll((nodes) => nodes.map((node) => node.textContent.trim()));
await page.waitForFunction(() => {
  const text = document.querySelector('#workflowNextActionCopy')?.textContent || '';
  return text.includes('预览') || text.includes('Preview') || text.includes('Diff') || text.includes('diff');
}, null, { timeout: 10000 });
report.checks.workflowNextActionAfterSelect = await page.locator('#workflowNextActionCopy').innerText();
report.checks.workflowPrimaryAfterSelect = await page.locator('#workflowPrimaryAction').innerText();

await page.locator('#candidateReviewDrawer [data-rp-tab="approval"]').click();
if (report.checks.workflowPrimaryAfterSelect.includes('Patch')) {
  await page.locator('#previewPatchDiff').click();
} else if (report.checks.workflowPrimaryAfterSelect.includes('Skill')) {
  await page.locator('#previewSkillDiff').click();
} else if (report.checks.workflowPrimaryAfterSelect.includes('AGENTS')) {
  await page.locator('#previewAgentsDiff').click();
} else {
  await page.locator('#previewUserDiff').click();
}
await page.waitForFunction(() => {
  const text = document.querySelector('#promotionPreviewText')?.textContent || '';
  return text.includes('USER.md') || text.includes('AGENTS.md') || text.includes('Skill') || text.includes('Patch') || text.includes('@@');
}, null, { timeout: 10000 });
report.checks.previewTextHead = (await page.locator('#promotionPreviewText').innerText()).slice(0, 220);
report.checks.workflowNextActionAfterPreview = await page.locator('#workflowNextActionCopy').innerText();

const previewButton = `${report.checks.workflowPrimaryAfterSelect || ''} ${report.checks.previewTextHead || ''}`;
let promotionButton = '#promoteSelected';
if (previewButton.includes('AGENTS')) {
  promotionButton = '#promoteAgents';
} else if (previewButton.includes('Patch')) {
  promotionButton = '#promotePatch';
} else if (previewButton.includes('Skill')) {
  promotionButton = '#promoteSkill';
}
report.checks.promotionButtonForPreview = promotionButton;
await page.locator('#candidateReviewDrawer').scrollIntoViewIfNeeded();
report.checks.promotionButtonVisible = await page.locator(promotionButton).isVisible();
report.checks.promotionButtonEnabled = await page.locator(promotionButton).isEnabled();
await page.locator(promotionButton).click();
await page.waitForSelector('#confirmModal:not([hidden])');
report.checks.confirmCallsAfterPromoteClick = await page.evaluate(() => window.__confirmCalls.length);
report.checks.confirmModalVisible = await page.locator('#confirmModal:not([hidden])').isVisible();
report.checks.confirmPreviewIncluded = await page.locator('#confirmModalBody').innerText().then((text) => text.includes('Promotion Diff Preview') || text.includes('晋升 Diff 预览'));
report.checks.confirmModalHasDanger = await page.locator('#confirmModalConfirm.operation-danger').isVisible();
await page.locator('#confirmModalCancel').click();
report.checks.reviewDrawerStillVisible = await page.locator('#candidateReviewDrawer:not([hidden])').isVisible();
await page.locator('#closeCandidateReviewDrawer').click();

await page.locator('#tab-operations').click();
await page.waitForSelector('#operationsConsole');
report.checks.operationsLifecycleVisible = await page.locator('#operationsLifecycleMap').isVisible().catch(() => false);
report.checks.recoveryQueueItems = await page.locator('#recoveryQueueList .recovery-queue-item').count();
report.checks.operationsVisiblePanels = await page.locator('[data-view="operations"].active').count();
await page.screenshot({ path: screenshotPath.replace(/\.png$/i, '.data.png'), fullPage: true });

const moduleExpectations = [
  ['data', '#operationsConsole'],
  ['automation', '.schedule-panel'],
  ['skills', '#skillHealthPanel'],
  ['recall', '#recallWorkbench'],
  ['history', '#runWorkspace'],
  ['doctor', '#doctorPanel'],
];
report.checks.moduleNavigation = {};
for (const [nav, selector] of moduleExpectations) {
  await page.evaluate(() => window.scrollTo(0, 0));
  await page.locator(`#sideNav [data-nav="${nav}"]`).click();
  await page.waitForSelector(`[data-view="operations"].active ${selector}`);
  report.checks.moduleNavigation[nav] = {
    currentNav: await page.locator('#appShell').evaluate((node) => node.dataset.currentNav || ''),
    activeNav: await page.locator(`#sideNav [data-nav="${nav}"]`).evaluate((node) => node.classList.contains('active')),
    hash: await page.evaluate(() => window.location.hash),
    scrollY: await page.evaluate(() => Math.round(window.scrollY)),
    targetVisible: await page.locator(`[data-view="operations"].active ${selector}`).isVisible(),
    visibleSections: await page.locator('[data-view="operations"].active section[data-ops-section]:visible').count(),
  };
}

await page.locator('#sideNav [data-nav="workflow"]').click();
await page.waitForSelector('[data-view="workflow"].active #candidateWorkspace');
report.checks.workflowModuleState = await page.locator('#candidateWorkspace').evaluate((node) => node.dataset.workflowModule || '');

await page.locator('#sideNav [data-nav="skills"]').click();
await page.waitForSelector('#skillCandidatePanel');
report.checks.skillCandidateRows = await page.locator('#skillCandidateRows tr:not(.empty-row)').count();
report.checks.skillCandidateActions = await page.locator('#skillCandidatePanel button[data-skill-candidate-action]').evaluateAll((nodes) => nodes.map((node) => node.textContent.trim()));
await page.locator('#skillCandidatePanel button[data-skill-candidate-action="view"]').first().click();
report.checks.skillCandidateViewOpensDrawer = await page.locator('#candidateReviewDrawer:not([hidden])').isVisible().catch(() => false);
if (report.checks.skillCandidateViewOpensDrawer) {
  await page.locator('#closeCandidateReviewDrawer').click();
}
await page.locator('#sideNav [data-nav="skills"]').click();
await page.waitForSelector('#skillCandidatePanel');
await page.locator('#skillCandidatePanel button[data-skill-candidate-action="preview"]').first().click();
await page.waitForTimeout(250);
report.checks.skillCandidatePreviewOpensDrawer = await page.locator('#candidateReviewDrawer:not([hidden])').isVisible().catch(() => false);
report.checks.skillCandidatePreviewLoadsDiff = await page.locator('#promotionPreviewText').innerText().then((text) => text.includes('Skill') || text.includes('Patch') || text.includes('@@')).catch(() => false);
if (report.checks.skillCandidatePreviewOpensDrawer) {
  await page.locator('#closeCandidateReviewDrawer').click();
}
await page.screenshot({ path: screenshotPath.replace(/\.png$/i, '.skills.png'), fullPage: true });

await page.locator('#themeToggle [data-theme="dark"]').click();
await page.waitForFunction(() => document.body.getAttribute('data-theme') === 'dark');
const darkSelectors = [
  '.setup-wizard',
  '.setup-check-item',
  '.setup-check-status',
  '.summary-card.status',
  '.daily-digest-panel',
  '.next-action-panel',
  '.dashboard-priorities',
  '.dashboard-priority-item',
  '.workflow-stage-rail',
  '.candidate-review-drawer',
  '.drawer-tab-bar',
  '.pagination',
  '.operation-card',
  '.operation-quiet',
  '.filter-select',
  '.diff-preview',
  '.confirm-dialog',
];
report.checks.darkThemeSamples = await page.evaluate((selectors) => {
  const white = new Set(['rgb(255, 255, 255)', 'rgba(255, 255, 255, 1)', 'white']);
  return selectors.map((selector) => {
    const node = document.querySelector(selector);
    if (!node) {
      return { selector, missing: true };
    }
    const styles = getComputedStyle(node);
    const rect = node.getBoundingClientRect();
    return {
      selector,
      visible: rect.width > 0 && rect.height > 0,
      backgroundColor: styles.backgroundColor,
      color: styles.color,
      whiteBackground: white.has(styles.backgroundColor),
    };
  });
}, darkSelectors);
report.checks.darkThemeNoWhiteControls = report.checks.darkThemeSamples.every((sample) => sample.missing || !sample.visible || !sample.whiteBackground);
const darkScreenshotPath = screenshotPath.replace(/\.png$/i, '.dark.png');
await page.screenshot({ path: darkScreenshotPath, fullPage: true });
report.checks.darkScreenshotPath = darkScreenshotPath;

report.checks.darkNavTextReadable = await page.locator('#sideNav [data-nav="history"]').evaluate((node) => {
  const color = getComputedStyle(node).color;
  const match = color.match(/rgba?\(([^)]+)\)/);
  if (!match) {
    return true;
  }
  const parts = match[1].split(',').map((part) => part.trim());
  return parts.length < 4 || Number(parts[3]) >= 0.78;
});

await page.locator('#themeToggle [data-theme="light"]').click();
await page.waitForFunction(() => document.body.getAttribute('data-theme') === 'light');
await page.screenshot({ path: screenshotPath, fullPage: true });
await browser.close();

console.log(JSON.stringify(report, null, 2));
