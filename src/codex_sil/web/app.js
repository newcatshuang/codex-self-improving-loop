const params = new URLSearchParams(location.search);
    const token = params.get("token") || "";
    const translations = {
      en: {
        localOnly: "Local-only control plane",
        subtitle: "Review memory, skill, and skill patch candidates from a token-protected local service. All promotion actions run through this WebUI.",
        tokenProtected: "127.0.0.1 only, token protected",
        navHome: "Home",
        navData: "Data Center",
        navCandidates: "Candidates",
        navPromotion: "Promotion",
        navSkills: "Skills",
        navSchedule: "Schedule",
        navRuns: "Run Logs",
        navRecall: "Session Recall",
        navAudit: "Audit",
        navPromotions: "Promotions",
        navReviews: "Reviews",
        navDoctor: "Doctor",
        dataCenter: "Data Center",
        dataCenterDesc: "Initialize, back up, rebuild, scan, or export the local SQLite learning database.",
        reviewCenter: "Review Center",
        promotionCenter: "Promotion Center",
        promotionCenterDesc: "Select a candidate in Candidate Center, then use the right-side review actions to promote it into USER.md, AGENTS.md, a skill, or a skill patch.",
        skillManagement: "Skill Management",
        skillManagementDesc: "Install local skills, inspect usage telemetry, and review skill patch candidates from the candidate queue.",
        homeTodoTitle: "Pending Workbench",
        homeTodoEmpty: "No open review work.",
        homeTodoCopy: "{review} review / {blocked} blocked",
        homeRiskTitle: "Risk Watch",
        homeRiskEmpty: "No failed runs detected.",
        homeRiskCopy: "{failed} failed run(s) need attention.",
        homePromotionTitle: "Recent Promotions",
        homePromotionEmpty: "No promotions yet.",
        homePromotionCopy: "Latest: {item}",
        homeNextRunTitle: "Next Scheduled Run",
        homeNextRunCopy: "Daily local scan. Use Schedule Center to install or remove it.",
        safeOperationsTitle: "Safe Operations",
        safeOperationsDesc: "Refresh, initialize, back up, or scan without clearing existing review queues.",
        dangerOperationsTitle: "Dangerous Operations",
        dangerOperationsDesc: "Rebuild clears active SQLite tables after creating a backup, then rescans history.",
        exportOperationsTitle: "Export Operations",
        exportOperationsDesc: "Create review files from current data without changing candidate status.",
        candidateActionsTitle: "Action & Risk",
        riskSummaryTitle: "Risk Summary",
        recommendedActionTitle: "Recommended Action",
        operationResultTitle: "Last Operation Result",
        operationResultIdle: "No operation has run in this session.",
        operationResultSuccess: "Completed: {message}",
        riskBlocked: "Blocked or unsafe. Review evidence and resolve conflicts before promotion.",
        riskReview: "Needs human review. Check source files, rewrite, destination, and safety.",
        riskSafe: "No blocking signal detected. Promotion is still explicit and reversible through backups where supported.",
        analysisSummary: "Analysis: {risk}. {step}",
        proposalSummary: "Proposal target: {target}. Manual approval required.",
        recommendMemory: "Promote to USER.md only for durable global preferences; use AGENTS.md for project facts.",
        recommendAgents: "This looks project-scoped. Prefer project AGENTS.md when the fact is not universal.",
        recommendSkill: "Promote as an independent skill when the workflow is reusable across tasks.",
        recommendPatch: "Export as a skill patch artifact, then review before applying it to an existing skill.",
        scheduleTargetTitle: "Schedule Target",
        scheduleCurrentStatusTitle: "Current Status",
        scheduleStatusUnknown: "Schedule status has not loaded yet.",
        scheduleStatusInstalled: "Installed on {system}.",
        scheduleStatusNotInstalled: "Not installed on {system}.",
        nextRunTimeText: "下一次运行: daily 03:00",
        lastRunTitle: "Last Run Result",
        schedulerCommandTitle: "Command Preview",
        lastRunCopy: "{status} · {time} · {detail}",
        recallTypeSession: "Sessions",
        recallTypeCandidate: "Candidates",
        recallResultCount: "{count} result(s)",
        auditSearchPlaceholder: "Filter audit actions",
        reviewHistorySearchPlaceholder: "Filter review history",
        statusReviewed: "Reviewed",
        timelineTitle: "Timeline",
        doctorHealthTitle: "Health Check",
        doctorRuntimeOk: "Runtime paths are available.",
        doctorRuntimeWarn: "Runtime paths have not loaded yet.",
        doctorDbOk: "SQLite database path is configured.",
        doctorDbWarn: "Database path is missing.",
        doctorHostOk: "Service is bound to 127.0.0.1.",
        doctorHostWarn: "Service host needs review.",
        doctorRunOk: "Latest run completed successfully.",
        doctorRunWarn: "No successful recent run found.",
        openDataCenter: "Open Data Center",
        targetChangeTitle: "Target Change Summary",
        targetChangeEmpty: "Select a promotion to see target and backup details.",
        recentRuns: "Recent Runs",
        errorAlerts: "Error Alerts",
        runLogs: "Run Logs",
        runSteps: "Run Steps",
        recallTitle: "Cross-Session Recall",
        auditCenter: "Audit Center",
        promotionHistory: "Promotion History",
        reviewHistory: "Review History",
        rollbackPreview: "Rollback Preview",
        rollbackHint: "Select a promotion to view the backup path and a copy-only restore command. The WebUI does not run rollback automatically.",
        doctorTitle: "Doctor",
        doctorKeyHeader: "Key",
        doctorValueHeader: "Value",
        memoryCandidates: "Memory Candidates",
        skillCandidates: "Skill Candidates",
        skillPatchCandidates: "Skill Patch Candidates",
        openReviewItems: "Open Review Items",
        skillUsage: "Skill Usage",
        statusSummary: "Status Summary",
        skillUsageBreakdown: "{success} success / {failed} failed",
        skillUsageEmpty: "No skill usage yet",
        skillUsageItem: "{name}: {total}",
        statusBreakdown: "{promoted} promoted / {rejected} rejected / {archived} archived",
        destinationBreakdown: "Destinations: {items}",
        candidateCenter: "Candidate Center",
        candidateCenterDesc: "Refresh, initialize, scan, rebuild, or export the local SQLite learning database.",
        refresh: "Refresh",
        initializeData: "Initialize Database",
        backupDatabase: "Backup Database",
        installSkills: "Install / Update Skills",
        rebuildDatabase: "Rebuild Database",
        scanOnce: "Scan Once",
        exportDigest: "Export Digest",
        exportCandidates: "Export Candidates",
        archiveSelected: "Archive Selected",
        rejectSelected: "Reject Selected",
        promoteUser: "Promote Selected To USER.md",
        promoteAgents: "Promote To Project AGENTS.md",
        promoteSkill: "Promote As Skill",
        promotePatch: "Promote As Skill Patch",
        recallPlaceholder: "Search sessions and candidates",
        recallButton: "Search",
        scheduleCenter: "Schedule Center",
        scheduleDesc: "Install or remove the daily 03:00 scan and desktop WebUI launcher. The scheduled task runs sil.py scan --once.",
        installSchedule: "Install Schedule",
        uninstallSchedule: "Uninstall Schedule",
        installShortcut: "Install Desktop Shortcut",
        uninstallShortcut: "Uninstall Desktop Shortcut",
        recordsTitle: "Candidate Records",
        filterAll: "All",
        filterMemory: "Memory",
        filterSkill: "Skill",
        filterPatch: "Skill Patch",
        statusAll: "All Statuses",
        statusReview: "Review",
        statusPromoted: "Promoted",
        statusRejected: "Rejected",
        statusArchived: "Archived",
        statusBlocked: "Blocked",
        searchPlaceholder: "Search candidates",
        typeHeader: "Type",
        destinationHeader: "Destination",
        candidateHeader: "Candidate",
        statusHeader: "Status",
        createdAtHeader: "Created",
        updatedAtHeader: "Updated",
        runKindHeader: "Kind",
        runReasonHeader: "Reason",
        actionHeader: "Action",
        targetHeader: "Target",
        detailHeader: "Detail",
        backupHeader: "Backup",
        loading: "Loading data...",
        emptyCandidates: "No candidates match the current view.",
        emptyRuns: "No run logs yet.",
        emptyErrors: "No failed runs.",
        emptyRecall: "No matching sessions or candidates.",
        emptyAudit: "No audit records yet.",
        emptyPromotions: "No promotions yet.",
        emptyReviews: "No review history yet.",
        prevPage: "Previous",
        nextPage: "Next",
        pageSizeLabel: "Rows per page",
        pageLabel: "Page {page} / {pages}",
        selectedRecord: "Selected Record",
        noneSelected: "None",
        selectCandidateHint: "Select a row to inspect the full candidate and promotion suggestion.",
        destinationLabel: "Destination",
        statusLabel: "Status",
        safetyLabel: "Safety",
        confidenceLabel: "Confidence",
        sourceCountLabel: "Sources",
        sourceFilesLabel: "Source Files",
        createdAtLabel: "Created",
        updatedAtLabel: "Updated",
        candidateTextLabel: "Candidate",
        rewriteSuggestionLabel: "Rewrite Suggestion",
        reviewNoteLabel: "Review Note",
        reviewNotePlaceholder: "Optional review note",
        reviewRewriteLabel: "Reviewed Rewrite",
        reviewRewritePlaceholder: "Optional reviewed rewrite",
        copyRewrite: "Copy Rewrite",
        copyRollback: "Copy Rollback Command",
        previewRollback: "Preview",
        rollbackUnavailable: "No backup is available for this promotion.",
        rollbackCanRestore: "Backup exists and can be restored manually.",
        rollbackCommandLabel: "Restore command",
        backupPathLabel: "Backup path",
        targetPathLabel: "Target path",
        saveReview: "Save Review",
        visibleItems: "{count} visible",
        toastLoaded: "Dashboard refreshed.",
        toastInitialized: "Database initialized.",
        toastBackupCreated: "Database backup created.",
        toastSkillsInstalled: "Skills installed or updated.",
        toastScanned: "Scan completed.",
        toastRebuilt: "Database rebuilt from historical sessions.",
        toastRebuildStarted: "Database rebuild started.",
        toastDigestExported: "Digest exported.",
        toastCandidatesExported: "Candidates exported.",
        toastArchived: "Candidate archived.",
        toastRejected: "Candidate rejected.",
        toastReviewSaved: "Review saved.",
        toastPromotedUser: "Candidate promoted to USER.md.",
        toastPromotedAgents: "Candidate promoted to AGENTS.md.",
        toastPromotedSkill: "Skill created from selected candidate.",
        toastPromotedPatch: "Skill patch artifact exported.",
        toastScheduleInstalled: "Schedule installed.",
        toastScheduleUninstalled: "Schedule uninstalled.",
        toastShortcutInstalled: "Desktop shortcut installed.",
        toastShortcutUninstalled: "Desktop shortcut uninstalled.",
        toastCopied: "Rewrite suggestion copied.",
        toastRollbackCopied: "Rollback command copied.",
        toastCopyFailed: "Copy failed. Select and copy the rewrite text manually.",
        toastLoadFailed: "Failed to load dashboard data.",
        selectCandidateFirst: "Select a candidate first.",
        progressIdle: "No active job.",
        rebuildInProgress: "Rebuilding database...",
        rebuildCompleted: "Rebuild completed.",
        rebuildFailed: "Rebuild failed.",
        progressLatest: "Latest: {detail}",
        confirmActionLabel: "Action",
        confirmFilesLabel: "Files",
        confirmResultLabel: "Result",
        confirmInitializeData: {
          action: "Initialize the local SQLite database and refresh the WebUI file.",
          files: "$HOME/.codex/self-improving-loop/self-improving-loop.sqlite and codex-self-improving-loop.html may be created or updated.",
          result: "The dashboard becomes ready for scans and review. Existing candidate data is preserved.",
        },
        confirmBackupDatabase: {
          action: "Create a timestamped backup of the current SQLite database.",
          files: "Writes a copy under $HOME/.codex/self-improving-loop/backups/.",
          result: "No candidate data changes. You get a restore point before risky operations.",
        },
        confirmScanOnce: {
          action: "Scan local Codex sessions once and extract new memory, skill, and skill patch candidates.",
          files: "Updates $HOME/.codex/self-improving-loop/self-improving-loop.sqlite.",
          result: "New candidates, run logs, and skill usage records may appear in the WebUI.",
        },
        confirmRebuildDatabase: {
          action: "Backup the current database, clear active SQLite tables, and rescan all historical sessions.",
          files: "Updates self-improving-loop.sqlite and writes a backup under $HOME/.codex/self-improving-loop/backups/.",
          result: "Current review queues are rebuilt from history. Existing manual review state inside SQLite can be replaced by the rebuild.",
        },
        confirmExportDigest: {
          action: "Export a review digest from current SQLite data.",
          files: "Writes a Markdown export under $HOME/.codex/self-improving-loop/exports/.",
          result: "No candidates are promoted or changed.",
        },
        confirmExportCandidates: {
          action: "Export current candidates from SQLite.",
          files: "Writes an export file under $HOME/.codex/self-improving-loop/exports/.",
          result: "No candidates are promoted or changed.",
        },
        confirmInstallSkills: {
          action: "Install or update the bundled session-recall and memory-capture skills.",
          files: "Writes under $HOME/.agents/skills/ and uses the installed app copy under $HOME/.agents/codex-self-improving-loop/.",
          result: "New Codex sessions can discover the updated skills after restart or reload.",
        },
        confirmSaveReview: {
          action: "Save the selected candidate review status, note, and reviewed rewrite text.",
          files: "Updates the reviews and candidates tables in self-improving-loop.sqlite.",
          result: "The candidate is marked reviewed and appears in Review History.",
        },
        confirmArchiveSelected: {
          action: "Archive the selected candidate.",
          files: "Updates the candidate status and audit tables in self-improving-loop.sqlite.",
          result: "The candidate leaves the active review queue but remains visible in history.",
        },
        confirmRejectSelected: {
          action: "Reject the selected candidate.",
          files: "Updates the candidate status and audit tables in self-improving-loop.sqlite.",
          result: "The candidate is marked rejected and will not be promoted unless reviewed again manually.",
        },
        confirmPromoteUser: {
          action: "Promote the selected candidate into global USER.md memory.",
          files: "Writes $HOME/.codex/memories/USER.md and creates a backup first when the file already exists.",
          result: "Future Codex sessions may load this as a global memory rule.",
        },
        confirmPromoteAgents: {
          action: "Promote the selected candidate into the current project's AGENTS.md.",
          files: "Writes AGENTS.md under the active Codex root and creates a backup first when the file already exists.",
          result: "Future work in that project may follow this project-level learned fact.",
        },
        confirmPromoteSkill: {
          action: "Create an independent learned skill from the selected candidate.",
          files: "Writes a SKILL.md under $HOME/.agents/skills/.",
          result: "New Codex sessions may discover and use the generated skill after restart or reload.",
        },
        confirmPromotePatch: {
          action: "Export the selected candidate as a reviewed skill patch artifact.",
          files: "Writes a Markdown patch under $HOME/.codex/self-improving-loop/exports/.",
          result: "No existing skill is patched automatically; the artifact is ready for manual review.",
        },
        confirmInstallSchedule: {
          action: "Install or replace the daily 03:00 self-improvement scan schedule.",
          files: "Writes the OS scheduler entry for this user and points it at $HOME/.agents/codex-self-improving-loop/sil.py scan --once.",
          result: "The scan will run automatically each day at 03:00 without keeping the WebUI open.",
        },
        confirmUninstallSchedule: {
          action: "Remove the installed daily self-improvement scan schedule.",
          files: "Deletes or disables the OS scheduler entry for this user.",
          result: "Automatic daily scanning stops. Manual scans and WebUI use still work.",
        },
        confirmInstallShortcut: {
          action: "Install a desktop shortcut that starts the temporary local WebUI service.",
          files: "Writes or replaces the desktop launcher for the current user.",
          result: "Opening the shortcut starts a fresh tokenized 127.0.0.1 WebUI session.",
        },
        confirmUninstallShortcut: {
          action: "Remove the desktop WebUI launcher.",
          files: "Deletes the desktop shortcut for the current user.",
          result: "The WebUI can still be started from the command line.",
        },
        type_memory: "Memory",
        type_skill: "Skill",
        type_skill_patch: "Skill Patch",
        sourcesCount: "{count} source(s)",
        setupWizardTitle: "First Run Wizard",
        setupWizardDesc: "Initialize the local database, rebuild history, install skills, then install the daily schedule.",
        setupReady: "Ready",
        setupNeedsWork: "Needs setup",
        openSkillManagement: "Open Skills",
        openScheduleCenter: "Open Schedule",
        openCandidates: "Open Candidates",
        dailyDigestTitle: "Daily Review Digest",
        dailyDigestEmpty: "No digest has been generated yet.",
        digestMetricNew: "New candidates",
        digestMetricPromote: "AI/rule promote",
        digestMetricRisk: "Risk items",
        digestMetricSkill: "Skill usage",
        digestMetricFailed: "Failed runs",
        exportBundle: "Export Bundle",
        importPreview: "Import Preview",
        importPreviewLabel: "Import Bundle Preview Path",
        importPreviewPlaceholder: "Paste bundle .zip path for dry-run preview",
        mergeSuggestionsTitle: "Merge Suggestions",
        emptyMergeSuggestions: "No merge suggestions.",
        applyMerge: "Apply Merge",
        promotionPreviewTitle: "Promotion Diff Preview",
        promotionPreviewEmpty: "Select a promotion action to preview the diff.",
        skillHealthTitle: "Skill Health",
        emptySkillHealth: "No skill health data yet.",
        skillNameHeader: "Skill",
        skillStatusHeader: "Status",
        skillUsageHeader: "Uses",
        skillLastUsedHeader: "Last Used",
        skillPatchHeader: "Patches",
        skillActionHeader: "Recommended Action",
        recommendationFromBackend: "{action}: {reason}",
        toastBundleExported: "Bundle exported.",
        toastImportPreviewed: "Import preview generated.",
        toastMergeApplied: "Merge suggestion applied.",
        confirmExportBundle: {
          action: "Export a migration and backup bundle.",
          files: "Writes a zip under $HOME/.codex/self-improving-loop/exports/ containing SQLite, memories, AGENTS.md, skills, and audit history when present.",
          result: "No local data changes. The bundle can be checked with import dry-run before use.",
        },
        confirmImportPreview: {
          action: "Dry-run inspect a bundle path.",
          files: "Reads the selected zip only; no files are overwritten.",
          result: "Shows entries and targets that would be touched by a future import.",
        },
        confirmApplyMerge: {
          action: "Apply a merge suggestion.",
          files: "Updates duplicate candidate statuses and audit_log in self-improving-loop.sqlite.",
          result: "Original evidence remains in SQLite; duplicate candidates move to merged status.",
        }
      },
      zh: {
        localOnly: "本机专用控制台",
        subtitle: "从受令牌保护的本地服务中审阅记忆、技能和技能补丁候选；所有晋升操作都可以在 WebUI 中点击完成。",
        tokenProtected: "仅绑定 127.0.0.1，并启用令牌保护",
        navHome: "首页",
        navData: "数据中心",
        navCandidates: "候选中心",
        navPromotion: "晋升中心",
        navSkills: "Skill 管理",
        navSchedule: "调度中心",
        navRuns: "运行日志",
        navRecall: "跨会话检索",
        navAudit: "审计",
        navPromotions: "晋升历史",
        navReviews: "审阅历史",
        navDoctor: "诊断",
        dataCenter: "数据中心",
        dataCenterDesc: "初始化、备份、重建、扫描或导出本地 SQLite 学习数据库。",
        reviewCenter: "审阅中心",
        promotionCenter: "晋升中心",
        promotionCenterDesc: "先在候选中心选择一条记录，再使用右侧审阅操作晋升到 USER.md、AGENTS.md、技能或技能补丁。",
        skillManagement: "Skill 管理",
        skillManagementDesc: "安装本地技能，查看技能使用遥测，并从候选队列处理技能补丁。",
        homeTodoTitle: "待处理工作台",
        homeTodoEmpty: "暂无待处理审阅工作。",
        homeTodoCopy: "{review} 个待审 / {blocked} 个阻断",
        homeRiskTitle: "风险观察",
        homeRiskEmpty: "暂无失败运行。",
        homeRiskCopy: "{failed} 个失败运行需要关注。",
        homePromotionTitle: "最近晋升",
        homePromotionEmpty: "暂无晋升记录。",
        homePromotionCopy: "最近：{item}",
        homeNextRunTitle: "下一次运行",
        homeNextRunCopy: "每日本地扫描。可在调度中心安装或移除。",
        safeOperationsTitle: "安全操作",
        safeOperationsDesc: "刷新、初始化、备份或扫描，不会清空已有审阅队列。",
        dangerOperationsTitle: "危险操作",
        dangerOperationsDesc: "重建会先备份，再清空当前 SQLite 表，并重新扫描历史。",
        exportOperationsTitle: "导出操作",
        exportOperationsDesc: "从当前数据生成审阅文件，不改变候选状态。",
        candidateActionsTitle: "操作与风险",
        riskSummaryTitle: "风险摘要",
        recommendedActionTitle: "推荐动作",
        operationResultTitle: "最近操作结果",
        operationResultIdle: "本次页面会话尚未执行操作。",
        operationResultSuccess: "已完成：{message}",
        riskBlocked: "存在阻断或不安全信号。晋升前需要核对证据并处理冲突。",
        riskReview: "需要人工审阅。请核对来源、改写、归属和安全状态。",
        riskSafe: "未发现阻断信号。晋升仍需要明确点击，支持备份的目标可按历史回滚。",
        analysisSummary: "分析：{risk}。{step}",
        proposalSummary: "建议目标：{target}。需要人工审批。",
        recommendMemory: "只有稳定的全局偏好才晋升到 USER.md；项目事实优先放 AGENTS.md。",
        recommendAgents: "这更像项目级事实。若不是全局规则，优先晋升到项目 AGENTS.md。",
        recommendSkill: "当该流程可跨任务复用时，适合晋升为独立技能。",
        recommendPatch: "导出为技能补丁产物，再人工复核后应用到已有技能。",
        scheduleTargetTitle: "调度目标",
        scheduleCurrentStatusTitle: "当前状态",
        scheduleStatusUnknown: "尚未加载调度状态。",
        scheduleStatusInstalled: "已在 {system} 安装。",
        scheduleStatusNotInstalled: "未在 {system} 安装。",
        nextRunTimeText: "下一次运行: daily 03:00",
        lastRunTitle: "最近运行结果",
        schedulerCommandTitle: "命令预览",
        lastRunCopy: "{status} · {time} · {detail}",
        recallTypeSession: "会话",
        recallTypeCandidate: "候选",
        recallResultCount: "{count} 条结果",
        auditSearchPlaceholder: "筛选审计操作",
        reviewHistorySearchPlaceholder: "筛选审阅历史",
        statusReviewed: "已审阅",
        timelineTitle: "时间线",
        doctorHealthTitle: "健康检查",
        doctorRuntimeOk: "运行目录已可用。",
        doctorRuntimeWarn: "运行目录尚未加载。",
        doctorDbOk: "SQLite 数据库路径已配置。",
        doctorDbWarn: "数据库路径缺失。",
        doctorHostOk: "服务绑定在 127.0.0.1。",
        doctorHostWarn: "服务绑定地址需要检查。",
        doctorRunOk: "最近运行已成功完成。",
        doctorRunWarn: "暂无成功的最近运行。",
        openDataCenter: "打开数据中心",
        targetChangeTitle: "目标文件变更摘要",
        targetChangeEmpty: "选择晋升记录后查看目标和备份详情。",
        recentRuns: "最近运行",
        errorAlerts: "错误提示",
        runLogs: "运行日志",
        runSteps: "运行步骤",
        recallTitle: "跨会话检索",
        auditCenter: "审计中心",
        promotionHistory: "晋升历史",
        reviewHistory: "审阅历史",
        rollbackPreview: "回滚预览",
        rollbackHint: "选择一条晋升记录后，可查看备份路径和仅复制用途的恢复命令。WebUI 不会自动执行回滚。",
        doctorTitle: "诊断",
        doctorKeyHeader: "项目",
        doctorValueHeader: "值",
        memoryCandidates: "记忆候选",
        skillCandidates: "技能候选",
        skillPatchCandidates: "技能补丁候选",
        openReviewItems: "待审阅项",
        skillUsage: "技能使用",
        statusSummary: "状态统计",
        skillUsageBreakdown: "{success} 成功 / {failed} 失败",
        skillUsageEmpty: "暂无技能使用记录",
        skillUsageItem: "{name}: {total}",
        statusBreakdown: "{promoted} 已晋升 / {rejected} 已拒绝 / {archived} 已归档",
        destinationBreakdown: "归属：{items}",
        candidateCenter: "候选中心",
        candidateCenterDesc: "刷新、初始化、扫描、重建或导出本地 SQLite 学习数据库。",
        refresh: "刷新",
        initializeData: "初始化数据库",
        backupDatabase: "备份数据库",
        installSkills: "安装 / 更新技能",
        rebuildDatabase: "重建数据库",
        scanOnce: "扫描一次",
        exportDigest: "导出摘要",
        exportCandidates: "导出候选",
        archiveSelected: "归档所选",
        rejectSelected: "拒绝所选",
        promoteUser: "晋升到 USER.md",
        promoteAgents: "晋升到项目 AGENTS.md",
        promoteSkill: "晋升为技能",
        promotePatch: "晋升为技能补丁",
        recallPlaceholder: "搜索历史会话和已入库候选",
        recallButton: "搜索",
        scheduleCenter: "调度中心",
        scheduleDesc: "安装或移除每天 03:00 的扫描任务和桌面 WebUI 快捷方式。定时任务会运行 sil.py scan --once。",
        installSchedule: "安装定时任务",
        uninstallSchedule: "卸载定时任务",
        installShortcut: "安装桌面快捷方式",
        uninstallShortcut: "卸载桌面快捷方式",
        recordsTitle: "候选记录",
        filterAll: "全部",
        filterMemory: "记忆",
        filterSkill: "技能",
        filterPatch: "技能补丁",
        statusAll: "全部状态",
        statusReview: "待审阅",
        statusPromoted: "已晋升",
        statusRejected: "已拒绝",
        statusArchived: "已归档",
        statusBlocked: "已阻断",
        searchPlaceholder: "搜索候选内容",
        typeHeader: "类型",
        destinationHeader: "归属",
        candidateHeader: "候选内容",
        statusHeader: "状态",
        createdAtHeader: "落库时间",
        updatedAtHeader: "更新时间",
        runKindHeader: "类型",
        runReasonHeader: "原因",
        actionHeader: "操作",
        targetHeader: "目标",
        detailHeader: "详情",
        backupHeader: "备份",
        loading: "正在加载数据...",
        emptyCandidates: "当前视图没有匹配的候选。",
        emptyRuns: "暂无运行日志。",
        emptyErrors: "暂无失败运行。",
        emptyRecall: "没有匹配的历史会话或候选。",
        emptyAudit: "暂无审计记录。",
        emptyPromotions: "暂无晋升记录。",
        emptyReviews: "暂无审阅历史。",
        prevPage: "上一页",
        nextPage: "下一页",
        pageSizeLabel: "每页条数",
        pageLabel: "第 {page} / {pages} 页",
        selectedRecord: "所选记录",
        noneSelected: "未选择",
        selectCandidateHint: "选择一行记录后，可查看完整候选内容和晋升建议。",
        destinationLabel: "归属",
        statusLabel: "状态",
        safetyLabel: "安全状态",
        confidenceLabel: "置信度",
        sourceCountLabel: "来源",
        sourceFilesLabel: "来源文件",
        createdAtLabel: "落库时间",
        updatedAtLabel: "更新时间",
        candidateTextLabel: "候选内容",
        rewriteSuggestionLabel: "改写建议",
        reviewNoteLabel: "审阅备注",
        reviewNotePlaceholder: "可选审阅备注",
        reviewRewriteLabel: "审阅后改写",
        reviewRewritePlaceholder: "可选审阅后改写",
        copyRewrite: "复制改写建议",
        copyRollback: "复制回滚命令",
        previewRollback: "预览",
        rollbackUnavailable: "这条晋升记录没有可用备份。",
        rollbackCanRestore: "备份存在，可手动恢复。",
        rollbackCommandLabel: "恢复命令",
        backupPathLabel: "备份路径",
        targetPathLabel: "目标路径",
        saveReview: "保存审阅",
        visibleItems: "当前显示 {count} 条",
        toastLoaded: "控制台已刷新。",
        toastInitialized: "数据库已初始化。",
        toastBackupCreated: "数据库备份已创建。",
        toastSkillsInstalled: "技能已安装或更新。",
        toastScanned: "扫描已完成。",
        toastRebuilt: "数据库已按历史会话重建。",
        toastRebuildStarted: "数据库重建已启动。",
        toastDigestExported: "摘要已导出。",
        toastCandidatesExported: "候选已导出。",
        toastArchived: "候选已归档。",
        toastRejected: "候选已拒绝。",
        toastReviewSaved: "审阅已保存。",
        toastPromotedUser: "候选已晋升到 USER.md。",
        toastPromotedAgents: "候选已晋升到 AGENTS.md。",
        toastPromotedSkill: "已基于候选创建独立技能。",
        toastPromotedPatch: "技能补丁产物已导出。",
        toastScheduleInstalled: "定时任务已安装。",
        toastScheduleUninstalled: "定时任务已卸载。",
        toastShortcutInstalled: "桌面快捷方式已安装。",
        toastShortcutUninstalled: "桌面快捷方式已卸载。",
        toastCopied: "改写建议已复制。",
        toastRollbackCopied: "回滚命令已复制。",
        toastCopyFailed: "复制失败，请手动选择改写建议文本。",
        toastLoadFailed: "加载控制台数据失败。",
        selectCandidateFirst: "请先选择一个候选。",
        progressIdle: "当前没有运行中的任务。",
        rebuildInProgress: "正在重建数据库...",
        rebuildCompleted: "重建已完成。",
        rebuildFailed: "重建失败。",
        progressLatest: "最新步骤：{detail}",
        confirmActionLabel: "将执行",
        confirmFilesLabel: "会修改",
        confirmResultLabel: "执行结果",
        confirmInitializeData: {
          action: "初始化本地 SQLite 数据库，并刷新 WebUI 文件。",
          files: "可能创建或更新 $HOME/.codex/self-improving-loop/self-improving-loop.sqlite 和 codex-self-improving-loop.html。",
          result: "控制台可用于扫描和审阅；已有候选数据会保留。",
        },
        confirmBackupDatabase: {
          action: "为当前 SQLite 数据库创建带时间戳的备份。",
          files: "在 $HOME/.codex/self-improving-loop/backups/ 下写入一份副本。",
          result: "候选数据不会变化；会得到一个可恢复点。",
        },
        confirmScanOnce: {
          action: "扫描一次本地 Codex 会话，并提取新的记忆、技能、技能补丁候选。",
          files: "更新 $HOME/.codex/self-improving-loop/self-improving-loop.sqlite。",
          result: "WebUI 中可能新增候选、运行日志和 skill 使用记录。",
        },
        confirmRebuildDatabase: {
          action: "先备份当前数据库，再清空当前 SQLite 表，并全量重扫历史会话。",
          files: "更新 self-improving-loop.sqlite，并在 $HOME/.codex/self-improving-loop/backups/ 下写入备份。",
          result: "当前审阅队列会按历史会话重建；SQLite 内已有人工审阅状态可能被重建结果替换。",
        },
        confirmExportDigest: {
          action: "从当前 SQLite 数据导出审阅摘要。",
          files: "在 $HOME/.codex/self-improving-loop/exports/ 下写入 Markdown 导出文件。",
          result: "不会晋升或修改候选。",
        },
        confirmExportCandidates: {
          action: "导出当前候选数据。",
          files: "在 $HOME/.codex/self-improving-loop/exports/ 下写入导出文件。",
          result: "不会晋升或修改候选。",
        },
        confirmInstallSkills: {
          action: "安装或更新内置的 session-recall 和 memory-capture 技能。",
          files: "写入 $HOME/.agents/skills/，并使用 $HOME/.agents/codex-self-improving-loop/ 下的安装副本。",
          result: "重启或重新加载后，新 Codex 会话可以发现更新后的技能。",
        },
        confirmSaveReview: {
          action: "保存所选候选的审阅状态、备注和审阅后改写内容。",
          files: "更新 self-improving-loop.sqlite 中的 reviews 和 candidates 表。",
          result: "候选会标记为已审阅，并出现在审阅历史中。",
        },
        confirmArchiveSelected: {
          action: "归档所选候选。",
          files: "更新 self-improving-loop.sqlite 中的候选状态和审计表。",
          result: "候选会离开活跃审阅队列，但仍可在历史中查看。",
        },
        confirmRejectSelected: {
          action: "拒绝所选候选。",
          files: "更新 self-improving-loop.sqlite 中的候选状态和审计表。",
          result: "候选会标记为已拒绝，除非再次人工审阅，否则不会被晋升。",
        },
        confirmPromoteUser: {
          action: "将所选候选晋升到全局 USER.md 记忆。",
          files: "写入 $HOME/.codex/memories/USER.md；如果文件已存在，会先创建备份。",
          result: "后续 Codex 会话可能把它作为全局记忆规则加载。",
        },
        confirmPromoteAgents: {
          action: "将所选候选晋升到当前项目的 AGENTS.md。",
          files: "写入当前 Codex root 下的 AGENTS.md；如果文件已存在，会先创建备份。",
          result: "后续在该项目工作时，可能遵循这条项目级学习事实。",
        },
        confirmPromoteSkill: {
          action: "基于所选候选创建一个独立 learned skill。",
          files: "在 $HOME/.agents/skills/ 下写入一个 SKILL.md。",
          result: "重启或重新加载后，新 Codex 会话可能发现并使用该技能。",
        },
        confirmPromotePatch: {
          action: "将所选候选导出为已审阅的 skill patch 产物。",
          files: "在 $HOME/.codex/self-improving-loop/exports/ 下写入 Markdown patch。",
          result: "不会自动修改已有 skill；该产物供人工复核。",
        },
        confirmInstallSchedule: {
          action: "安装或替换每天 03:00 的自改进扫描定时任务。",
          files: "写入当前用户的系统调度项，并指向 $HOME/.agents/codex-self-improving-loop/sil.py scan --once。",
          result: "无需打开 WebUI，系统每天 03:00 自动扫描一次。",
        },
        confirmUninstallSchedule: {
          action: "移除已安装的每日自改进扫描定时任务。",
          files: "删除或禁用当前用户的系统调度项。",
          result: "自动每日扫描停止；手动扫描和 WebUI 仍可使用。",
        },
        confirmInstallShortcut: {
          action: "安装一个桌面快捷方式，用于启动临时本地 WebUI 服务。",
          files: "写入或替换当前用户桌面启动器。",
          result: "点击快捷方式会启动新的 127.0.0.1 token 化 WebUI 会话。",
        },
        confirmUninstallShortcut: {
          action: "移除桌面 WebUI 快捷方式。",
          files: "删除当前用户桌面快捷方式。",
          result: "仍可通过命令行启动 WebUI。",
        },
        type_memory: "记忆",
        type_skill: "技能",
        type_skill_patch: "技能补丁",
        sourcesCount: "{count} 个来源",
        setupWizardTitle: "首次运行向导",
        setupWizardDesc: "初始化本地数据库、全量重扫历史、安装技能，然后安装每日调度。",
        setupReady: "已就绪",
        setupNeedsWork: "待初始化",
        openSkillManagement: "打开 Skill 管理",
        openScheduleCenter: "打开调度中心",
        openCandidates: "打开候选中心",
        dailyDigestTitle: "每日审阅摘要",
        dailyDigestEmpty: "尚未生成 digest。",
        digestMetricNew: "新增候选",
        digestMetricPromote: "建议晋升",
        digestMetricRisk: "风险项",
        digestMetricSkill: "技能使用",
        digestMetricFailed: "失败运行",
        exportBundle: "导出迁移包",
        importPreview: "导入预览",
        importPreviewLabel: "导入包预览路径",
        importPreviewPlaceholder: "粘贴 bundle .zip 路径，仅做 dry-run 预览",
        mergeSuggestionsTitle: "合并建议",
        emptyMergeSuggestions: "暂无合并建议。",
        applyMerge: "应用合并",
        promotionPreviewTitle: "晋升 Diff 预览",
        promotionPreviewEmpty: "选择晋升动作后预览 diff。",
        skillHealthTitle: "Skill 健康",
        emptySkillHealth: "暂无 skill 健康数据。",
        skillNameHeader: "Skill",
        skillStatusHeader: "状态",
        skillUsageHeader: "使用次数",
        skillLastUsedHeader: "最近使用",
        skillPatchHeader: "补丁数",
        skillActionHeader: "建议动作",
        recommendationFromBackend: "{action}: {reason}",
        toastBundleExported: "迁移包已导出。",
        toastImportPreviewed: "导入预览已生成。",
        toastMergeApplied: "合并建议已应用。",
        confirmExportBundle: {
          action: "导出迁移和备份包。",
          files: "在 $HOME/.codex/self-improving-loop/exports/ 下写入 zip，包含 SQLite、记忆、AGENTS.md、skills 和审计历史（如存在）。",
          result: "不会改变本机数据；导入前可先做 dry-run 预览。",
        },
        confirmImportPreview: {
          action: "对指定 bundle 路径做 dry-run 检查。",
          files: "只读取所选 zip，不覆盖任何文件。",
          result: "展示包内条目和未来导入可能影响的目标。",
        },
        confirmApplyMerge: {
          action: "应用一组合并建议。",
          files: "更新 self-improving-loop.sqlite 中重复候选状态和 audit_log。",
          result: "原始 evidence 仍保留在 SQLite；重复候选状态变为 merged。",
        }
      }
    };

    let currentLanguage = initialLanguage();
    let allCandidates = [];
    let selectedCandidate = null;
    let currentFilter = "all";
    let statusFilter = "all";
    let createdAtFilter = "";
    let searchTerm = "";
    let currentPage = 1;
    let pageSize = 20;
    let toastTimer = null;
    let activeRunId = null;
    let activeRunTimer = null;
    let currentView = "home";
    let latestRuns = [];
    let latestRunSteps = [];
    let selectedRunId = null;
    let scheduleInfo = null;
    let recallMatches = [];
    let recallTypeFilter = "all";
    let doctorInfo = {};
    let auditItems = [];
    let auditSearch = "";
    let promotionItems = [];
    let reviewItems = [];
    let reviewHistoryStatusFilter = "all";
    let reviewHistorySearch = "";
    let rollbackInfo = null;
    let lastOperationMessage = "";
    let setupStatus = null;
    let latestDigest = null;
    let mergeSuggestions = [];
    let skillHealthItems = [];
    let latestPromotionPreview = null;
    window.selectedCandidateId = null;

    function initialLanguage() {
      const savedLanguage = localStorage.getItem("codexSilLanguage");
      if (savedLanguage === "zh" || savedLanguage === "en") {
        return savedLanguage;
      }
      const browserLanguage = (navigator.language || "en").toLowerCase();
      return browserLanguage.startsWith("zh") ? "zh" : "en";
    }

    function t(key, values = {}) {
      const source = translations[currentLanguage] || translations.en;
      let text = source[key] || translations.en[key] || key;
      for (const [name, value] of Object.entries(values)) {
        text = text.replaceAll(`{${name}}`, String(value));
      }
      return text;
    }

    function applyLanguage() {
      document.documentElement.lang = currentLanguage === "zh" ? "zh-CN" : "en";
      document.querySelectorAll("[data-i18n]").forEach((element) => {
        element.textContent = t(element.dataset.i18n);
      });
      document.querySelectorAll("[data-i18n-placeholder]").forEach((element) => {
        element.setAttribute("placeholder", t(element.dataset.i18nPlaceholder));
      });
      document.querySelectorAll("#languageToggle button").forEach((button) => {
        const active = button.dataset.lang === currentLanguage;
        button.classList.toggle("active", active);
        button.setAttribute("aria-pressed", String(active));
      });
      renderSummary(currentSummary);
      renderCandidates();
      renderSelected();
      renderCandidateActionPanel();
      renderRuns();
      renderRecallResults();
      renderDoctor();
      renderDoctorHealth();
      renderAudit();
      renderPromotions();
      renderReviews();
      renderRollbackPreview();
      renderHomeTasks();
      renderScheduleStatus();
      renderSetupWizard();
      renderDailyDigest();
      renderMergeSuggestions();
      renderSkillHealth();
      renderPromotionPreview(latestPromotionPreview);
      refreshScheduleStatus().catch((error) => console.warn(error));
    }

    let currentSummary = {memory: 0, skill: 0, skill_patch: 0, review: 0};

    async function api(path, options = {}) {
      const headers = Object.assign({"Authorization": `Bearer ${token}`}, options.headers || {});
      const res = await fetch(path, Object.assign({}, options, {headers}));
      if (!res.ok) {
        throw new Error(await res.text());
      }
      return res.json();
    }

    function showToast(message, tone = "ok") {
      const toast = document.getElementById("statusToast");
      toast.textContent = message;
      toast.className = `toast show ${tone}`;
      clearTimeout(toastTimer);
      toastTimer = setTimeout(() => {
        toast.className = "toast";
      }, 3600);
    }

    function setBusy(isBusy) {
      document.querySelectorAll("[data-action]").forEach((button) => {
        button.disabled = isBusy;
      });
    }

    function confirmAction(confirmKey, extra = "") {
      if (!confirmKey) {
        return true;
      }
      const detail = t(confirmKey);
      const message = typeof detail === "object"
        ? `${t("confirmActionLabel")}: ${detail.action}\n\n${t("confirmFilesLabel")}: ${detail.files}\n\n${t("confirmResultLabel")}: ${detail.result}`
        : String(detail);
      return confirm(extra ? `${message}\n\n${extra}` : message);
    }

    function updateProgress(status) {
      const panel = document.getElementById("progressPanel");
      const text = document.getElementById("progressText");
      const count = document.getElementById("progressCount");
      const fill = document.getElementById("progressFill");
      if (!status) {
        panel.classList.remove("active");
        text.textContent = t("progressIdle");
        count.textContent = "0 / 0";
        fill.style.width = "0%";
        return;
      }
      panel.classList.add("active");
      const total = Number(status.total || 0);
      const done = Number(status.processed || 0) + Number(status.skipped || 0);
      const percent = total > 0 ? Math.min(100, Math.round((done / total) * 100)) : status.status === "ok" ? 100 : 8;
      const latest = status.latest_step && status.latest_step.detail ? ` · ${t("progressLatest", {detail: status.latest_step.detail})}` : "";
      const label = status.status === "ok" ? t("rebuildCompleted") : status.status === "failed" ? t("rebuildFailed") : t("rebuildInProgress");
      text.textContent = `${label}${latest}`;
      count.textContent = `${done} / ${total || "?"}`;
      fill.style.width = `${percent}%`;
    }

    function renderSummary(summary) {
      currentSummary = summary || currentSummary;
      document.getElementById("memoryCount").textContent = currentSummary.memory || 0;
      document.getElementById("skillCount").textContent = currentSummary.skill || 0;
      document.getElementById("patchCount").textContent = currentSummary.skill_patch || 0;
      document.getElementById("reviewCount").textContent = currentSummary.review || 0;
      document.getElementById("skillUsageCount").textContent = currentSummary.skill_usage_total || 0;
      document.getElementById("promotedCount").textContent = currentSummary.promoted || 0;
      document.getElementById("skillUsageBreakdown").textContent = t("skillUsageBreakdown", {
        success: currentSummary.skill_usage_success || 0,
        failed: currentSummary.skill_usage_failed || 0,
      });
      renderSkillUsageList(currentSummary.skill_usage_by_skill || []);
      document.getElementById("statusBreakdown").textContent = t("statusBreakdown", {
        promoted: currentSummary.promoted || 0,
        rejected: currentSummary.rejected || 0,
        archived: currentSummary.archived || 0,
      }) + " · " + t("destinationBreakdown", {items: formatDestinationSummary(currentSummary.by_destination)});
      renderHomeTasks();
    }

    function renderSkillUsageList(items) {
      const list = document.getElementById("skillUsageList");
      list.innerHTML = "";
      const topItems = items.slice(0, 5);
      if (!topItems.length) {
        const item = document.createElement("li");
        item.textContent = t("skillUsageEmpty");
        list.appendChild(item);
        return;
      }
      for (const usage of topItems) {
        const item = document.createElement("li");
        item.textContent = t("skillUsageItem", {name: usage.skill_name, total: usage.total});
        list.appendChild(item);
      }
    }

    function renderSetupWizard() {
      const panel = document.getElementById("setupWizard");
      const status = document.getElementById("setupWizardStatus");
      const copy = document.getElementById("setupWizardCopy");
      if (!panel || !status || !copy) {
        return;
      }
      const ready = setupStatus && setupStatus.ready && setupStatus.schedule_installed && setupStatus.skills_installed;
      panel.classList.toggle("collapsed", Boolean(ready));
      status.textContent = ready ? t("setupReady") : t("setupNeedsWork");
      status.className = `tag ${ready ? "status" : "review"}`;
      if (!setupStatus) {
        copy.textContent = t("setupWizardDesc");
        return;
      }
      copy.textContent = [
        `DB: ${setupStatus.database_exists ? "ok" : "missing"}`,
        `sessions: ${setupStatus.session_count || 0}`,
        `candidates: ${setupStatus.candidate_count || 0}`,
        `skills: ${setupStatus.skills_installed ? "ok" : "missing"}`,
        `schedule: ${setupStatus.schedule_installed ? "ok" : "missing"}`,
      ].join(" · ");
    }

    function metric(label, value) {
      const item = document.createElement("div");
      item.className = "digest-metric";
      const strong = document.createElement("strong");
      strong.textContent = value;
      const span = document.createElement("span");
      span.textContent = label;
      item.append(strong, span);
      return item;
    }

    function renderDailyDigest() {
      const copy = document.getElementById("dailyDigestCopy");
      const grid = document.getElementById("dailyDigestMetrics");
      if (!copy || !grid) {
        return;
      }
      grid.innerHTML = "";
      const digest = latestDigest && latestDigest.digest;
      if (!digest) {
        copy.textContent = t("dailyDigestEmpty");
        return;
      }
      copy.textContent = `${digest.digest_date || ""} · ${formatDateTime(digest.created_at)}`;
      grid.append(
        metric(t("digestMetricNew"), digest.new_candidates || 0),
        metric(t("digestMetricPromote"), digest.recommended_promotions || 0),
        metric(t("digestMetricRisk"), digest.risk_items || 0),
        metric(t("digestMetricSkill"), digest.skill_usage_changes || 0),
        metric(t("digestMetricFailed"), digest.failed_runs || 0),
      );
    }

    function formatType(type) {
      return t(`type_${type}`) || type;
    }

    function formatDestinationSummary(destinations) {
      const entries = Object.entries(destinations || {}).sort((a, b) => b[1] - a[1]).slice(0, 3);
      if (!entries.length) {
        return "-";
      }
      return entries.map(([name, count]) => `${name}: ${count}`).join(" / ");
    }

    function dateOnly(value) {
      return String(value || "").slice(0, 10);
    }

    function formatDateTime(value) {
      if (!value) {
        return "-";
      }
      const normalized = String(value).includes("T") ? String(value) : String(value).replace(" ", "T");
      const date = new Date(`${normalized}Z`);
      if (Number.isNaN(date.getTime())) {
        return String(value);
      }
      return new Intl.DateTimeFormat(currentLanguage === "zh" ? "zh-CN" : "en", {
        month: "2-digit",
        day: "2-digit",
        hour: "2-digit",
        minute: "2-digit",
      }).format(date);
    }

    function lastRun() {
      return latestRuns[0] || null;
    }

    function latestFailureCount() {
      return latestRuns.filter((run) => run.status === "failed").length;
    }

    function renderHomeTasks() {
      const todoCount = document.getElementById("homeTodoCount");
      const todoList = document.getElementById("homeTodoList");
      const riskCount = document.getElementById("homeRiskCount");
      const riskCopy = document.getElementById("homeRiskCopy");
      const promotionCount = document.getElementById("homePromotionCount");
      const promotionCopy = document.getElementById("homePromotionCopy");
      if (!todoCount || !todoList || !riskCount || !riskCopy || !promotionCount || !promotionCopy) {
        return;
      }
      const review = currentSummary.review || 0;
      const blocked = currentSummary.blocked || 0;
      todoCount.textContent = review + blocked;
      todoList.textContent = review + blocked ? t("homeTodoCopy", {review, blocked}) : t("homeTodoEmpty");
      const failures = latestFailureCount();
      riskCount.textContent = failures;
      riskCopy.textContent = failures ? t("homeRiskCopy", {failed: failures}) : t("homeRiskEmpty");
      promotionCount.textContent = promotionItems.length;
      const latest = promotionItems[0];
      promotionCopy.textContent = latest
        ? t("homePromotionCopy", {item: `${latest.target_type || "-"} · ${formatDateTime(latest.created_at)}`})
        : t("homePromotionEmpty");
    }

    function renderScheduleStatus() {
      const status = document.getElementById("scheduleCurrentStatus");
      const statusCard = document.getElementById("scheduleCurrentStatusCard");
      const last = document.getElementById("lastScheduledRun");
      const command = document.getElementById("schedulerCommandPreview");
      if (!last || !command) {
        return;
      }
      if (status && statusCard) {
        if (!scheduleInfo) {
          status.textContent = t("scheduleStatusUnknown");
          statusCard.className = "health-card warn";
        } else {
          status.textContent = scheduleInfo.installed
            ? t("scheduleStatusInstalled", {system: scheduleInfo.system || "-"})
            : t("scheduleStatusNotInstalled", {system: scheduleInfo.system || "-"});
          statusCard.className = `health-card ${scheduleInfo.installed ? "ok" : "warn"}`;
        }
      }
      const run = lastRun();
      last.textContent = run ? t("lastRunCopy", {
        status: run.status || "-",
        time: formatDateTime(run.finished_at || run.started_at),
        detail: run.detail || run.kind || "-",
      }) : t("emptyRuns");
      command.textContent = scheduleInfo && scheduleInfo.command ? scheduleInfo.command : "sil.py scan --once";
    }

    function candidateRisk(candidate) {
      if (!candidate) {
        return {className: "", text: t("selectCandidateHint")};
      }
      if (candidate.analysis_risk_level || candidate.analysis_next_step) {
        const riskLevel = String(candidate.analysis_risk_level || "review");
        const className = riskLevel === "high" ? "danger" : riskLevel === "low" ? "safe" : "warning";
        return {
          className,
          text: t("analysisSummary", {
            risk: riskLevel,
            step: candidate.analysis_next_step || t("riskReview"),
          }),
        };
      }
      const status = String(candidate.status || "").toLowerCase();
      const safety = String(candidate.safety || "").toLowerCase();
      if (status === "blocked" || safety.includes("conflict") || safety.includes("unsafe")) {
        return {className: "danger", text: t("riskBlocked")};
      }
      if (status === "review") {
        return {className: "warning", text: t("riskReview")};
      }
      return {className: "safe", text: t("riskSafe")};
    }

    function candidateRecommendation(candidate) {
      if (!candidate) {
        return t("selectCandidateHint");
      }
      if (candidate.suggested_action || candidate.recommendation_reason) {
        const recommendation = t("recommendationFromBackend", {
          action: candidate.suggested_action || "needs_review",
          reason: candidate.recommendation_reason || candidate.recommendation || "",
        });
        if (candidate.proposal_target_type) {
          return `${recommendation}\n${t("proposalSummary", {target: candidate.proposal_target_type})}`;
        }
        return recommendation;
      }
      if (candidate.type === "skill") {
        return t("recommendSkill");
      }
      if (candidate.type === "skill_patch") {
        return t("recommendPatch");
      }
      if (String(candidate.destination || "").toLowerCase().includes("agents")) {
        return t("recommendAgents");
      }
      return t("recommendMemory");
    }

    function renderCandidateActionPanel() {
      const badge = document.getElementById("candidateActionBadge");
      const riskPanel = document.getElementById("candidateRiskSummary");
      const riskCopy = document.getElementById("candidateRiskCopy");
      const recommendation = document.getElementById("candidateRecommendationCopy");
      const result = document.getElementById("operationResultCopy");
      if (!badge || !riskPanel || !riskCopy || !recommendation || !result) {
        return;
      }
      if (!selectedCandidate) {
        badge.textContent = t("noneSelected");
        badge.className = "tag status";
        riskPanel.className = "action-card";
        riskCopy.textContent = t("selectCandidateHint");
        recommendation.textContent = t("selectCandidateHint");
      } else {
        const risk = candidateRisk(selectedCandidate);
        badge.textContent = selectedCandidate.status || t("noneSelected");
        badge.className = `tag ${selectedCandidate.status === "blocked" ? "review" : "status"}`;
        riskPanel.className = `action-card ${risk.className}`.trim();
        riskCopy.textContent = risk.text;
        recommendation.textContent = candidateRecommendation(selectedCandidate);
      }
      result.textContent = lastOperationMessage || t("operationResultIdle");
    }

    function renderPromotionPreview(preview) {
      const element = document.getElementById("promotionPreviewText");
      if (!element) {
        return;
      }
      element.textContent = preview && preview.diff ? preview.diff : t("promotionPreviewEmpty");
    }

    function renderMergeSuggestions() {
      const list = document.getElementById("mergeSuggestionsList");
      if (!list) {
        return;
      }
      list.innerHTML = "";
      if (!mergeSuggestions.length) {
        const item = document.createElement("li");
        item.textContent = t("emptyMergeSuggestions");
        list.appendChild(item);
        return;
      }
      for (const suggestion of mergeSuggestions.slice(0, 8)) {
        const item = document.createElement("li");
        const text = document.createElement("span");
        text.textContent = `${suggestion.reason || ""} #${(suggestion.candidate_ids || []).join(", #")}`;
        const button = document.createElement("button");
        button.type = "button";
        button.className = "secondary";
        button.textContent = t("applyMerge");
        button.addEventListener("click", () => applyMergeSuggestion(suggestion.id));
        item.append(text, button);
        list.appendChild(item);
      }
    }

    function renderSkillHealth() {
      const body = document.getElementById("skillHealthRows");
      if (!body) {
        return;
      }
      body.innerHTML = "";
      if (!skillHealthItems.length) {
        const row = document.createElement("tr");
        const empty = cell("empty-row");
        empty.colSpan = 6;
        empty.textContent = t("emptySkillHealth");
        row.appendChild(empty);
        body.appendChild(row);
        return;
      }
      for (const skill of skillHealthItems.slice(0, 20)) {
        const row = document.createElement("tr");

        const nameCell = cell("col-skill-name");
        const name = document.createElement("strong");
        name.className = "skill-name";
        name.textContent = skill.skill_name || "-";
        nameCell.appendChild(name);
        row.appendChild(nameCell);

        const statusCell = cell("col-skill-status");
        statusCell.appendChild(tag(skill.status || "-", skill.status === "needs_patch" ? "review" : "status"));
        row.appendChild(statusCell);

        const usageCell = cell("col-skill-usage numeric-cell");
        usageCell.textContent = String(skill.usage_count || 0);
        row.appendChild(usageCell);

        const lastUsedCell = cell("col-skill-last-used");
        lastUsedCell.textContent = formatDateTime(skill.last_used_at);
        row.appendChild(lastUsedCell);

        const patchesCell = cell("col-skill-patches numeric-cell");
        patchesCell.textContent = String(skill.patch_candidates || 0);
        row.appendChild(patchesCell);

        const actionCell = cell("col-skill-action");
        actionCell.textContent = skill.recommended_action || "-";
        row.appendChild(actionCell);

        body.appendChild(row);
      }
    }

    function tag(text, className = "") {
      const element = document.createElement("span");
      element.className = `tag ${className}`.trim();
      element.textContent = text;
      return element;
    }

    function cell(className = "") {
      const td = document.createElement("td");
      if (className) {
        td.className = className;
      }
      return td;
    }

    function setView(view) {
      currentView = view;
      document.querySelectorAll("[data-nav]").forEach((button) => {
        const active = button.dataset.nav === view;
        button.classList.toggle("active", active);
        button.setAttribute("aria-current", active ? "page" : "false");
      });
      document.querySelectorAll("[data-view]").forEach((panel) => {
        panel.classList.toggle("active", panel.dataset.view === view);
      });
      if (view === "runs") {
        refreshRuns().catch((error) => showToast(error.message || t("toastLoadFailed"), "error"));
      }
      if (view === "doctor") {
        refreshDoctor().catch((error) => showToast(error.message || t("toastLoadFailed"), "error"));
      }
      if (view === "audit") {
        refreshAudit().catch((error) => showToast(error.message || t("toastLoadFailed"), "error"));
      }
      if (view === "promotions" || view === "reviews") {
        refreshHistory().catch((error) => showToast(error.message || t("toastLoadFailed"), "error"));
      }
    }

    function renderEmptyRow(body, colspan, messageKey) {
      body.innerHTML = "";
      const row = document.createElement("tr");
      const empty = cell("empty-row");
      empty.colSpan = colspan;
      empty.textContent = t(messageKey);
      row.appendChild(empty);
      body.appendChild(row);
    }

    function renderRunRows(body, runs, compact = false) {
      body.innerHTML = "";
      if (!runs.length) {
        renderEmptyRow(body, compact ? 3 : 4, "emptyRuns");
        return;
      }
      for (const run of runs) {
        const row = document.createElement("tr");
        if (!compact) {
          row.dataset.runId = run.id;
          row.classList.add("clickable-row");
          row.classList.toggle("selected-row", String(run.id) === String(selectedRunId));
          row.addEventListener("click", () => {
            selectedRunId = run.id;
            renderRuns();
          });
        }
        const kind = cell();
        kind.textContent = run.kind || "-";
        row.appendChild(kind);
        const status = cell();
        status.appendChild(tag(run.status || "-", run.status === "failed" ? "review" : "status"));
        row.appendChild(status);
        if (!compact) {
          const reason = cell();
          reason.textContent = run.detail || "-";
          row.appendChild(reason);
        }
        const updated = cell();
        updated.textContent = formatDateTime(run.finished_at || run.started_at);
        row.appendChild(updated);
        body.appendChild(row);
      }
    }

    function renderRunSteps() {
      const body = document.getElementById("runStepRows");
      const summary = document.getElementById("selectedRunSummary");
      body.innerHTML = "";
      const run = latestRuns.find((item) => String(item.id) === String(selectedRunId)) || null;
      const steps = selectedRunId ? latestRunSteps.filter((step) => String(step.run_id) === String(selectedRunId)) : latestRunSteps;
      if (summary) {
        summary.textContent = run ? `#${run.id} · ${run.status || "-"}` : t("noneSelected");
        summary.className = `tag ${run && run.status === "failed" ? "review" : "status"}`;
      }
      if (!steps.length) {
        renderEmptyRow(body, 3, "emptyRuns");
        return;
      }
      for (const step of steps) {
        const row = document.createElement("tr");
        const status = cell();
        status.appendChild(tag(step.status || "-", step.status === "failed" ? "review" : "status"));
        row.appendChild(status);
        const detail = cell();
        detail.textContent = step.detail || step.name || "-";
        row.appendChild(detail);
        const updated = cell();
        updated.textContent = formatDateTime(step.finished_at || step.started_at);
        row.appendChild(updated);
        body.appendChild(row);
      }
    }

    function renderErrors() {
      const list = document.getElementById("errorAlerts");
      list.innerHTML = "";
      const failures = latestRuns.filter((run) => run.status === "failed").slice(0, 5);
      if (!failures.length) {
        const item = document.createElement("li");
        item.textContent = t("emptyErrors");
        list.appendChild(item);
        return;
      }
      for (const run of failures) {
        const item = document.createElement("li");
        item.textContent = `${run.kind || "-"} · ${formatDateTime(run.finished_at || run.started_at)} · ${run.detail || run.status}`;
        list.appendChild(item);
      }
    }

    function renderRuns() {
      const homeRows = document.getElementById("homeRunRows");
      const runRows = document.getElementById("runRows");
      if (!selectedRunId && latestRuns.length) {
        selectedRunId = latestRuns[0].id;
      }
      if (homeRows) {
        renderRunRows(homeRows, latestRuns.slice(0, 5), true);
      }
      if (runRows) {
        renderRunRows(runRows, latestRuns, false);
      }
      renderRunSteps();
      renderErrors();
      renderScheduleStatus();
      renderHomeTasks();
    }

    function renderRecallResults() {
      const list = document.getElementById("recallResults");
      const summary = document.getElementById("recallResultSummary");
      const query = document.getElementById("recallSearch") ? document.getElementById("recallSearch").value.trim() : "";
      const filtered = recallMatches.filter((result) => recallTypeFilter === "all" || result.kind === recallTypeFilter);
      list.innerHTML = "";
      if (summary) {
        summary.textContent = filtered.length ? t("recallResultCount", {count: filtered.length}) : t("emptyRecall");
      }
      if (!filtered.length) {
        const item = document.createElement("li");
        item.textContent = t("emptyRecall");
        list.appendChild(item);
        return;
      }
      for (const result of filtered) {
        const item = document.createElement("li");
        item.className = "recall-result";
        const label = [result.kind, result.type, result.destination].filter(Boolean).join(" / ");
        const heading = document.createElement("div");
        heading.className = "candidate-title";
        heading.textContent = `${label || "result"} · ${result.path || "-"}`;
        const snippet = document.createElement("div");
        snippet.className = "candidate-snippet";
        snippet.innerHTML = highlightText(result.snippet || "", query);
        item.append(heading, snippet);
        list.appendChild(item);
      }
    }

    function escapeHtml(text) {
      return String(text || "")
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#039;");
    }

    function highlightText(text, query) {
      const escaped = escapeHtml(text);
      const needle = String(query || "").trim();
      if (!needle) {
        return escaped;
      }
      const escapedNeedle = escapeHtml(needle).replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      return escaped.replace(new RegExp(escapedNeedle, "gi"), (match) => `<mark>${match}</mark>`);
    }

    function renderDoctorHealth() {
      const grid = document.getElementById("doctorHealthGrid");
      if (!grid) {
        return;
      }
      grid.innerHTML = "";
      const latest = lastRun();
      const cards = [
        {
          title: "Runtime",
          tone: doctorInfo.runtime_dir ? "ok" : "warn",
          text: doctorInfo.runtime_dir ? t("doctorRuntimeOk") : t("doctorRuntimeWarn"),
        },
        {
          title: "SQLite",
          tone: doctorInfo.database ? "ok" : "warn",
          text: doctorInfo.database ? t("doctorDbOk") : t("doctorDbWarn"),
        },
        {
          title: "127.0.0.1",
          tone: doctorInfo.service_host === "127.0.0.1" ? "ok" : "error",
          text: doctorInfo.service_host === "127.0.0.1" ? t("doctorHostOk") : t("doctorHostWarn"),
        },
        {
          title: t("lastRunTitle"),
          tone: latest && latest.status === "ok" ? "ok" : "warn",
          text: latest && latest.status === "ok" ? t("doctorRunOk") : t("doctorRunWarn"),
        },
      ];
      for (const card of cards) {
        const item = document.createElement("article");
        item.className = `health-card ${card.tone}`;
        const title = document.createElement("h3");
        title.textContent = card.title;
        const text = document.createElement("p");
        text.className = "task-copy";
        text.textContent = card.text;
        item.append(title, text);
        grid.appendChild(item);
      }
    }

    function renderDoctor() {
      const body = document.getElementById("doctorRows");
      if (!body) {
        return;
      }
      body.innerHTML = "";
      const entries = Object.entries(doctorInfo || {});
      if (!entries.length) {
        renderEmptyRow(body, 2, "loading");
        return;
      }
      for (const [key, value] of entries) {
        const row = document.createElement("tr");
        const keyCell = cell();
        keyCell.textContent = key;
        row.appendChild(keyCell);
        const valueCell = cell();
        valueCell.textContent = String(value);
        row.appendChild(valueCell);
        body.appendChild(row);
      }
      renderDoctorHealth();
    }

    function renderAudit() {
      const body = document.getElementById("auditRows");
      if (!body) {
        return;
      }
      body.innerHTML = "";
      const normalized = auditSearch.trim().toLowerCase();
      const items = auditItems.filter((item) => {
        if (!normalized) {
          return true;
        }
        return [item.action, item.target, item.detail].filter(Boolean).join(" ").toLowerCase().includes(normalized);
      });
      if (!items.length) {
        renderEmptyRow(body, 4, "emptyAudit");
        renderTimeline("auditTimeline", [], "emptyAudit", (item) => item);
        return;
      }
      for (const item of items) {
        const row = document.createElement("tr");
        const action = cell();
        action.textContent = item.action || "-";
        row.appendChild(action);
        const target = cell();
        target.textContent = item.target || "-";
        row.appendChild(target);
        const detail = cell();
        detail.textContent = item.detail || "-";
        row.appendChild(detail);
        const created = cell();
        created.textContent = formatDateTime(item.created_at);
        row.appendChild(created);
        body.appendChild(row);
      }
      renderTimeline("auditTimeline", items.slice(0, 12), "emptyAudit", (item) => `${formatDateTime(item.created_at)} · ${item.action || "-"} · ${item.target || "-"}`);
    }

    function renderPromotions() {
      const body = document.getElementById("promotionRows");
      if (!body) {
        return;
      }
      body.innerHTML = "";
      if (!promotionItems.length) {
        renderEmptyRow(body, 6, "emptyPromotions");
        renderTimeline("promotionTimeline", [], "emptyPromotions", (item) => item);
        return;
      }
      for (const item of promotionItems) {
        const row = document.createElement("tr");
        row.dataset.promotionId = item.id;
        row.tabIndex = 0;
        row.classList.toggle("selected-row", rollbackInfo && rollbackInfo.promotion && String(rollbackInfo.promotion.id) === String(item.id));
        row.addEventListener("click", () => selectPromotion(item.id));
        row.addEventListener("keydown", (event) => {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            selectPromotion(item.id);
          }
        });

        const type = cell();
        type.appendChild(tag(item.target_type || "-", "status"));
        row.appendChild(type);
        const candidate = cell();
        candidate.textContent = item.candidate_title || item.detail || "-";
        row.appendChild(candidate);
        const target = cell();
        target.textContent = item.target_path || "-";
        row.appendChild(target);
        const backup = cell();
        backup.textContent = item.backup_path || "-";
        row.appendChild(backup);
        const created = cell();
        created.textContent = formatDateTime(item.created_at);
        row.appendChild(created);
        const action = cell();
        const preview = document.createElement("button");
        preview.className = "secondary";
        preview.type = "button";
        preview.dataset.previewPromotion = item.id;
        preview.textContent = t("previewRollback");
        action.appendChild(preview);
        row.appendChild(action);
        body.appendChild(row);
      }
      renderTimeline("promotionTimeline", promotionItems.slice(0, 12), "emptyPromotions", (item) => `${formatDateTime(item.created_at)} · ${item.target_type || "-"} · ${item.candidate_title || item.detail || "-"}`);
    }

    function renderReviews() {
      const body = document.getElementById("reviewRows");
      if (!body) {
        return;
      }
      body.innerHTML = "";
      const normalized = reviewHistorySearch.trim().toLowerCase();
      const items = reviewItems.filter((item) => {
        if (reviewHistoryStatusFilter !== "all" && item.status !== reviewHistoryStatusFilter) {
          return false;
        }
        if (!normalized) {
          return true;
        }
        return [item.status, item.note, item.rewrite_text, item.candidate_title, item.destination].filter(Boolean).join(" ").toLowerCase().includes(normalized);
      });
      if (!items.length) {
        renderEmptyRow(body, 5, "emptyReviews");
        renderTimeline("reviewTimeline", [], "emptyReviews", (item) => item);
        return;
      }
      for (const item of items) {
        const row = document.createElement("tr");
        const status = cell();
        status.appendChild(tag(item.status || "-", item.status === "rejected" ? "review" : "status"));
        row.appendChild(status);
        const candidate = cell();
        candidate.textContent = item.candidate_title || item.destination || "-";
        row.appendChild(candidate);
        const note = cell();
        note.textContent = item.note || "-";
        row.appendChild(note);
        const rewrite = cell();
        rewrite.textContent = item.rewrite_text || "-";
        row.appendChild(rewrite);
        const created = cell();
        created.textContent = formatDateTime(item.created_at);
        row.appendChild(created);
        body.appendChild(row);
      }
      renderTimeline("reviewTimeline", items.slice(0, 12), "emptyReviews", (item) => `${formatDateTime(item.created_at)} · ${item.status || "-"} · ${item.candidate_title || item.destination || "-"}`);
    }

    function renderTimeline(elementId, items, emptyKey, formatItem) {
      const list = document.getElementById(elementId);
      if (!list) {
        return;
      }
      list.innerHTML = "";
      if (!items.length) {
        const empty = document.createElement("li");
        empty.className = "timeline-item";
        empty.textContent = t(emptyKey);
        list.appendChild(empty);
        return;
      }
      for (const item of items) {
        const row = document.createElement("li");
        row.className = "timeline-item";
        row.textContent = formatItem(item);
        list.appendChild(row);
      }
    }

    function renderTargetChangeSummary() {
      const panel = document.getElementById("targetChangeSummary");
      if (!panel) {
        return;
      }
      panel.innerHTML = "";
      const heading = document.createElement("h3");
      heading.textContent = t("targetChangeTitle");
      panel.appendChild(heading);
      if (!rollbackInfo) {
        const empty = document.createElement("p");
        empty.className = "task-copy";
        empty.textContent = t("targetChangeEmpty");
        panel.appendChild(empty);
        return;
      }
      const values = [
        [t("targetPathLabel"), rollbackInfo.target_path || "-"],
        [t("backupPathLabel"), rollbackInfo.backup_path || "-"],
      ];
      for (const [label, value] of values) {
        const block = document.createElement("div");
        block.className = "action-card";
        const name = document.createElement("div");
        name.className = "detail-label";
        name.textContent = label;
        const text = document.createElement("p");
        text.className = "task-copy";
        text.textContent = value;
        block.append(name, text);
        panel.appendChild(block);
      }
    }

    function renderRollbackPreview() {
      const panel = document.getElementById("rollbackPreview");
      const status = document.getElementById("rollbackStatus");
      const copyButton = document.getElementById("copyRollback");
      if (!panel || !status || !copyButton) {
        return;
      }
      panel.innerHTML = "";
      if (!rollbackInfo) {
        status.textContent = t("noneSelected");
        status.className = "tag status";
        copyButton.disabled = true;
        const description = document.createElement("p");
        description.className = "panel-description";
        description.textContent = t("rollbackHint");
        panel.appendChild(description);
        renderTargetChangeSummary();
        return;
      }
      status.textContent = rollbackInfo.can_restore ? t("rollbackCanRestore") : t("rollbackUnavailable");
      status.className = `tag ${rollbackInfo.can_restore ? "status" : "review"}`;
      copyButton.disabled = !rollbackInfo.restore_command;
      const fields = [
        [t("targetPathLabel"), rollbackInfo.target_path || "-"],
        [t("backupPathLabel"), rollbackInfo.backup_path || "-"],
        [t("rollbackCommandLabel"), rollbackInfo.restore_command || "-"],
      ];
      for (const [label, value] of fields) {
        const block = document.createElement("div");
        block.className = "detail-block";
        const heading = document.createElement("div");
        heading.className = "detail-label";
        heading.textContent = label;
        const text = document.createElement("div");
        text.className = "detail-text";
        text.textContent = value;
        block.append(heading, text);
        panel.appendChild(block);
      }
      renderTargetChangeSummary();
    }

    async function refreshRuns() {
      const payload = await api("/api/runs");
      latestRuns = payload.runs || [];
      latestRunSteps = payload.steps || [];
      if (selectedRunId && !latestRuns.some((run) => String(run.id) === String(selectedRunId))) {
        selectedRunId = null;
      }
      renderRuns();
    }

    async function refreshScheduleStatus() {
      scheduleInfo = await api("/api/schedule/status");
      renderScheduleStatus();
    }

    async function refreshDoctor() {
      doctorInfo = await api("/api/doctor");
      renderDoctor();
    }

    async function refreshAudit() {
      const payload = await api("/api/audit");
      auditItems = payload.audit || [];
      renderAudit();
    }

    async function refreshHistory() {
      const payload = await api("/api/history");
      promotionItems = payload.promotions || [];
      reviewItems = payload.reviews || [];
      renderPromotions();
      renderReviews();
      renderHomeTasks();
    }

    async function refreshSetupStatus() {
      setupStatus = await api("/api/setup/status");
      renderSetupWizard();
    }

    async function refreshDailyDigest() {
      latestDigest = await api("/api/digests/latest");
      renderDailyDigest();
    }

    async function refreshMergeSuggestions() {
      const payload = await api("/api/merge-suggestions");
      mergeSuggestions = payload.merge_suggestions || [];
      renderMergeSuggestions();
    }

    async function regenerateMergeSuggestions() {
      const payload = await api("/api/merge-suggestions/refresh", {method: "POST"});
      mergeSuggestions = payload.merge_suggestions || [];
      renderMergeSuggestions();
    }

    async function refreshSkillHealth() {
      const payload = await api("/api/skills/health");
      skillHealthItems = payload.skills || [];
      renderSkillHealth();
    }

    async function selectPromotion(id) {
      rollbackInfo = await api(`/api/promotions/${id}/rollback-preview`);
      renderPromotions();
      renderRollbackPreview();
    }

    async function runRecallSearch() {
      const input = document.getElementById("recallSearch");
      const limit = document.getElementById("recallLimit").value || "10";
      const query = input.value.trim();
      if (!query) {
        recallMatches = [];
        renderRecallResults();
        return;
      }
      const payload = await api(`/api/recall?q=${encodeURIComponent(query)}&max_results=${encodeURIComponent(limit)}`);
      recallMatches = payload.results || [];
      renderRecallResults();
    }

    async function applyMergeSuggestion(id) {
      if (!confirmAction("confirmApplyMerge")) {
        return;
      }
      setBusy(true);
      try {
        await api(`/api/merge-suggestions/${id}/apply`, {method: "POST"});
        await refresh(false);
        showToast(t("toastMergeApplied"));
      } catch (error) {
        console.error(error);
        showToast(error.message || t("toastLoadFailed"), "error");
      } finally {
        setBusy(false);
      }
    }

    async function previewPromotion(target) {
      if (!window.selectedCandidateId) {
        showToast(t("selectCandidateFirst"), "warn");
        return null;
      }
      latestPromotionPreview = await api(`/api/candidates/${window.selectedCandidateId}/promotion-preview?target=${encodeURIComponent(target)}`);
      renderPromotionPreview(latestPromotionPreview);
      return latestPromotionPreview;
    }

    function visibleCandidates() {
      const normalized = searchTerm.trim().toLowerCase();
      return allCandidates.filter((item) => {
        const typeMatch = currentFilter === "all" || item.type === currentFilter;
        if (!typeMatch) {
          return false;
        }
        if (statusFilter !== "all" && item.status !== statusFilter) {
          return false;
        }
        if (createdAtFilter && dateOnly(item.created_at) !== createdAtFilter) {
          return false;
        }
        if (!normalized) {
          return true;
        }
        const text = [item.type, item.title, item.destination, item.text, item.rewrite_suggestion, item.status, item.safety]
          .filter(Boolean)
          .join(" ")
          .toLowerCase();
        return text.includes(normalized);
      });
    }

    function pagedCandidates(items) {
      const totalPages = Math.max(1, Math.ceil(items.length / pageSize));
      currentPage = Math.min(Math.max(1, currentPage), totalPages);
      const start = (currentPage - 1) * pageSize;
      return {
        pageItems: items.slice(start, start + pageSize),
        totalPages,
      };
    }

    function renderPagination(totalItems, totalPages) {
      document.getElementById("currentPageLabel").textContent = t("pageLabel", {page: currentPage, pages: totalPages});
      document.getElementById("visibleCount").textContent = t("visibleItems", {count: totalItems});
      document.getElementById("prevPage").disabled = currentPage <= 1;
      document.getElementById("nextPage").disabled = currentPage >= totalPages;
      document.getElementById("pageSizeSelect").value = String(pageSize);
    }

    function renderCandidates() {
      const body = document.getElementById("candidateRows");
      const items = visibleCandidates();
      const {pageItems, totalPages} = pagedCandidates(items);
      renderPagination(items.length, totalPages);
      body.innerHTML = "";
      if (!items.length) {
        const empty = document.createElement("div");
        empty.className = "empty-row";
        empty.textContent = t("emptyCandidates");
        body.appendChild(empty);
        return;
      }

      for (const item of pageItems) {
        const card = document.createElement("article");
        card.className = "candidate-card";
        card.dataset.id = item.id;
        card.tabIndex = 0;
        card.setAttribute("role", "listitem");
        card.setAttribute("aria-selected", String(String(item.id) === String(window.selectedCandidateId)));
        card.classList.toggle("selected-card", String(item.id) === String(window.selectedCandidateId));
        card.addEventListener("click", () => selectCandidate(item.id));
        card.addEventListener("keydown", (event) => {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            selectCandidate(item.id);
          }
        });

        const title = document.createElement("div");
        title.className = "candidate-card-title";
        title.textContent = item.title || item.text || "-";
        const snippet = document.createElement("div");
        snippet.className = "candidate-card-snippet";
        snippet.textContent = item.text || "";
        const meta = document.createElement("div");
        meta.className = "candidate-card-meta";
        meta.append(
          tag(formatType(item.type), item.type),
          tag(item.destination || "-", "status"),
          tag(item.status || "-", item.status === "review" ? "review" : "status")
        );
        const time = document.createElement("div");
        time.className = "candidate-card-time";
        time.textContent = `${formatDateTime(item.created_at)} / ${formatDateTime(item.updated_at)}`;
        card.append(meta, title, snippet, time);
        body.appendChild(card);
      }
    }

    function hydrateSelection() {
      if (window.selectedCandidateId) {
        selectedCandidate = allCandidates.find((item) => String(item.id) === String(window.selectedCandidateId)) || null;
      }
      if (!selectedCandidate && allCandidates.length) {
        selectedCandidate = allCandidates[0];
        window.selectedCandidateId = selectedCandidate.id;
      }
      if (!allCandidates.length) {
        selectedCandidate = null;
        window.selectedCandidateId = null;
      }
    }

    function selectCandidate(id) {
      window.selectedCandidateId = id;
      selectedCandidate = allCandidates.find((item) => String(item.id) === String(id)) || null;
      renderCandidates();
      renderSelected();
      renderCandidateActionPanel();
    }

    function renderSelected() {
      const empty = document.getElementById("selectedEmpty");
      const content = document.getElementById("selectedContent");
      const badge = document.getElementById("selectedBadge");
      if (!selectedCandidate) {
        empty.hidden = false;
        content.hidden = true;
        badge.textContent = t("noneSelected");
        badge.className = "tag status";
        return;
      }
      empty.hidden = true;
      content.hidden = false;
      badge.textContent = formatType(selectedCandidate.type);
      badge.className = `tag ${selectedCandidate.type}`;
      document.getElementById("selectedTitle").textContent = selectedCandidate.title || selectedCandidate.text || "-";
      document.getElementById("selectedDestination").textContent = selectedCandidate.destination || "-";
      document.getElementById("selectedStatus").textContent = selectedCandidate.status || "-";
      document.getElementById("selectedSafety").textContent = selectedCandidate.safety || "-";
      document.getElementById("selectedConfidence").textContent = selectedCandidate.confidence === undefined ? "-" : Number(selectedCandidate.confidence).toFixed(2);
      document.getElementById("selectedSources").textContent = t("sourcesCount", {count: selectedCandidate.source_count || 0});
      document.getElementById("selectedCreatedAt").textContent = formatDateTime(selectedCandidate.created_at);
      document.getElementById("selectedUpdatedAt").textContent = formatDateTime(selectedCandidate.updated_at);
      document.getElementById("selectedText").textContent = selectedCandidate.text || "-";
      document.getElementById("selectedRewrite").textContent = selectedCandidate.rewrite_suggestion || selectedCandidate.text || "-";
      document.getElementById("reviewNote").value = "";
      document.getElementById("reviewRewrite").value = selectedCandidate.rewrite_suggestion || selectedCandidate.text || "";
      const sourceFiles = document.getElementById("selectedSourceFiles");
      sourceFiles.innerHTML = "";
      const files = selectedCandidate.source_files || [];
      if (!files.length) {
        const item = document.createElement("li");
        item.textContent = "-";
        sourceFiles.appendChild(item);
      } else {
        for (const file of files) {
          const item = document.createElement("li");
          item.textContent = file;
          sourceFiles.appendChild(item);
        }
      }
    }

    async function refresh(showMessage = false) {
      const payload = await api("/api/summary");
      renderSummary(payload.summary);
      allCandidates = payload.candidates || [];
      hydrateSelection();
      renderCandidates();
      renderSelected();
      renderCandidateActionPanel();
      await refreshRuns();
      await refreshScheduleStatus();
      await refreshHistory();
      await refreshAudit();
      await refreshSetupStatus();
      await refreshDailyDigest();
      await refreshMergeSuggestions();
      await refreshSkillHealth();
      if (showMessage) {
        showToast(t("toastLoaded"));
      }
    }

    async function runAction(action, successKey, options = {}) {
      if (options.needsSelection && !window.selectedCandidateId) {
        showToast(t("selectCandidateFirst"), "warn");
        return;
      }
      let confirmExtra = "";
      if (options.previewTarget) {
        const preview = await previewPromotion(options.previewTarget);
        if (!preview) {
          return;
        }
        confirmExtra = `${t("promotionPreviewTitle")}:\n${preview.diff || ""}`;
      }
      if (!confirmAction(options.confirmKey, confirmExtra)) {
        return;
      }
      setBusy(true);
      try {
        await action();
        if (options.refresh !== false) {
          await refresh(false);
        }
        lastOperationMessage = t("operationResultSuccess", {message: t(successKey)});
        renderCandidateActionPanel();
        showToast(t(successKey));
      } catch (error) {
        console.error(error);
        showToast(error.message || t("toastLoadFailed"), "error");
      } finally {
        setBusy(false);
      }
    }

    async function pollRun(runId) {
      const status = await api(`/api/runs/${runId}`);
      updateProgress(status);
      if (status.status === "running") {
        activeRunTimer = setTimeout(() => pollRun(runId).catch((error) => {
          console.error(error);
          showToast(error.message || t("toastLoadFailed"), "error");
          setBusy(false);
        }), 1000);
        return;
      }
      activeRunId = null;
      clearTimeout(activeRunTimer);
      activeRunTimer = null;
      setBusy(false);
      if (status.status === "ok") {
        await refresh(false);
        await refreshRuns();
        showToast(t("toastRebuilt"));
      } else {
        showToast(`${t("rebuildFailed")} ${status.detail || ""}`, "error");
      }
    }

    async function runRebuild() {
      if (!confirmAction("confirmRebuildDatabase")) {
        return;
      }
      clearTimeout(activeRunTimer);
      setBusy(true);
      try {
        const started = await api("/api/rebuild", {method: "POST"});
        activeRunId = started.run_id;
        updateProgress({status: "running", processed: 0, skipped: 0, total: 0, latest_step: null});
        showToast(t("toastRebuildStarted"));
        await pollRun(activeRunId);
      } catch (error) {
        console.error(error);
        showToast(error.message || t("toastLoadFailed"), "error");
        setBusy(false);
      }
    }

    async function copyText(text) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(text);
        return;
      }
      const textarea = document.createElement("textarea");
      textarea.value = text;
      textarea.setAttribute("readonly", "");
      textarea.style.position = "fixed";
      textarea.style.left = "-9999px";
      document.body.appendChild(textarea);
      textarea.select();
      const copied = document.execCommand("copy");
      textarea.remove();
      if (!copied) {
        throw new Error("copy command failed");
      }
    }

    document.querySelectorAll("#languageToggle button").forEach((button) => {
      button.addEventListener("click", () => {
        currentLanguage = button.dataset.lang;
        localStorage.setItem("codexSilLanguage", currentLanguage);
        applyLanguage();
      });
    });

    document.querySelectorAll("[data-nav]").forEach((button) => {
      button.addEventListener("click", () => setView(button.dataset.nav));
    });

    document.querySelectorAll("[data-nav-jump]").forEach((button) => {
      button.addEventListener("click", () => setView(button.dataset.navJump));
    });

    document.querySelectorAll("[data-filter]").forEach((button) => {
      button.addEventListener("click", () => {
        currentFilter = button.dataset.filter;
        currentPage = 1;
        document.querySelectorAll("[data-filter]").forEach((item) => item.classList.toggle("active", item === button));
        renderCandidates();
      });
    });

    document.getElementById("statusFilter").addEventListener("change", (event) => {
      statusFilter = event.target.value;
      currentPage = 1;
      renderCandidates();
    });

    document.getElementById("createdAtFilter").addEventListener("change", (event) => {
      createdAtFilter = event.target.value;
      currentPage = 1;
      renderCandidates();
    });

    document.getElementById("searchInput").addEventListener("input", (event) => {
      searchTerm = event.target.value;
      currentPage = 1;
      renderCandidates();
    });

    document.getElementById("recallTypeFilter").addEventListener("change", (event) => {
      recallTypeFilter = event.target.value;
      renderRecallResults();
    });

    document.getElementById("auditSearch").addEventListener("input", (event) => {
      auditSearch = event.target.value;
      renderAudit();
    });

    document.getElementById("reviewHistoryStatusFilter").addEventListener("change", (event) => {
      reviewHistoryStatusFilter = event.target.value;
      renderReviews();
    });

    document.getElementById("reviewHistorySearch").addEventListener("input", (event) => {
      reviewHistorySearch = event.target.value;
      renderReviews();
    });

    document.getElementById("doctorRefresh").addEventListener("click", () => refreshDoctor().catch((error) => showToast(error.message || t("toastLoadFailed"), "error")));
    document.getElementById("doctorOpenData").addEventListener("click", () => setView("data"));
    document.getElementById("refreshDigest").addEventListener("click", () => refreshDailyDigest().catch((error) => showToast(error.message || t("toastLoadFailed"), "error")));
    document.getElementById("refreshMergeSuggestions").addEventListener("click", () => regenerateMergeSuggestions().catch((error) => showToast(error.message || t("toastLoadFailed"), "error")));

    document.getElementById("prevPage").addEventListener("click", () => {
      currentPage = Math.max(1, currentPage - 1);
      renderCandidates();
    });

    document.getElementById("nextPage").addEventListener("click", () => {
      currentPage += 1;
      renderCandidates();
    });

    document.getElementById("pageSizeSelect").addEventListener("change", (event) => {
      pageSize = Number(event.target.value) || 20;
      currentPage = 1;
      renderCandidates();
    });

    document.getElementById("refreshButton").addEventListener("click", () => refresh(true).catch((error) => showToast(error.message, "error")));
    document.getElementById("initializeData").addEventListener("click", () => runAction(() => api("/api/init", {method: "POST"}), "toastInitialized", {confirmKey: "confirmInitializeData"}));
    document.getElementById("backupDatabase").addEventListener("click", () => runAction(() => api("/api/backup", {method: "POST"}), "toastBackupCreated", {refresh: false, confirmKey: "confirmBackupDatabase"}));
    document.getElementById("installSkills").addEventListener("click", () => runAction(() => api("/api/install/skills", {method: "POST"}), "toastSkillsInstalled", {refresh: false, confirmKey: "confirmInstallSkills"}));
    document.getElementById("scanButton").addEventListener("click", () => runAction(() => api("/api/scan", {method: "POST"}), "toastScanned", {confirmKey: "confirmScanOnce"}));
    document.getElementById("exportDigest").addEventListener("click", () => runAction(() => api("/api/export/digest", {method: "POST"}), "toastDigestExported", {refresh: false, confirmKey: "confirmExportDigest"}));
    document.getElementById("exportCandidates").addEventListener("click", () => runAction(() => api("/api/export/candidates", {method: "POST"}), "toastCandidatesExported", {refresh: false, confirmKey: "confirmExportCandidates"}));
    document.getElementById("exportBundle").addEventListener("click", () => runAction(() => api("/api/export/bundle", {method: "POST"}), "toastBundleExported", {refresh: false, confirmKey: "confirmExportBundle"}));
    document.getElementById("importPreview").addEventListener("click", () => runAction(async () => {
      const path = document.getElementById("importPreviewPath").value.trim();
      const payload = await api("/api/import/preview", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({path}),
      });
      document.getElementById("importPreviewResult").textContent = JSON.stringify(payload, null, 2);
    }, "toastImportPreviewed", {refresh: false, confirmKey: "confirmImportPreview"}));
    document.getElementById("rebuildButton").addEventListener("click", () => runRebuild());
    document.getElementById("saveReview").addEventListener("click", () => runAction(() => api(`/api/candidates/${window.selectedCandidateId}/review`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        status: "reviewed",
        note: document.getElementById("reviewNote").value,
        rewrite_text: document.getElementById("reviewRewrite").value,
      }),
    }), "toastReviewSaved", {needsSelection: true, confirmKey: "confirmSaveReview"}));
    document.getElementById("archiveSelected").addEventListener("click", () => runAction(() => api(`/api/candidates/${window.selectedCandidateId}/archive`, {method: "POST"}), "toastArchived", {needsSelection: true, confirmKey: "confirmArchiveSelected"}));
    document.getElementById("rejectSelected").addEventListener("click", () => runAction(() => api(`/api/candidates/${window.selectedCandidateId}/reject`, {method: "POST"}), "toastRejected", {needsSelection: true, confirmKey: "confirmRejectSelected"}));
    document.getElementById("promoteSelected").addEventListener("click", () => runAction(() => api(`/api/candidates/${window.selectedCandidateId}/promote`, {method: "POST"}), "toastPromotedUser", {needsSelection: true, confirmKey: "confirmPromoteUser", previewTarget: "user"}));
    document.getElementById("promoteAgents").addEventListener("click", () => runAction(() => api(`/api/candidates/${window.selectedCandidateId}/promote-agents`, {method: "POST"}), "toastPromotedAgents", {needsSelection: true, confirmKey: "confirmPromoteAgents", previewTarget: "agents"}));
    document.getElementById("promoteSkill").addEventListener("click", () => runAction(() => api(`/api/candidates/${window.selectedCandidateId}/promote-skill`, {method: "POST"}), "toastPromotedSkill", {needsSelection: true, confirmKey: "confirmPromoteSkill", previewTarget: "skill"}));
    document.getElementById("promotePatch").addEventListener("click", () => runAction(() => api(`/api/candidates/${window.selectedCandidateId}/promote-patch`, {method: "POST"}), "toastPromotedPatch", {needsSelection: true, confirmKey: "confirmPromotePatch", previewTarget: "patch"}));
    document.getElementById("installSchedule").addEventListener("click", () => runAction(async () => {
      await api("/api/schedule/install", {method: "POST"});
      await refreshScheduleStatus();
    }, "toastScheduleInstalled", {refresh: false, confirmKey: "confirmInstallSchedule"}));
    document.getElementById("uninstallSchedule").addEventListener("click", () => runAction(async () => {
      await api("/api/schedule/uninstall", {method: "POST"});
      await refreshScheduleStatus();
    }, "toastScheduleUninstalled", {refresh: false, confirmKey: "confirmUninstallSchedule"}));
    document.getElementById("installShortcut").addEventListener("click", () => runAction(() => api("/api/shortcut/install", {method: "POST"}), "toastShortcutInstalled", {refresh: false, confirmKey: "confirmInstallShortcut"}));
    document.getElementById("uninstallShortcut").addEventListener("click", () => runAction(() => api("/api/shortcut/uninstall", {method: "POST"}), "toastShortcutUninstalled", {refresh: false, confirmKey: "confirmUninstallShortcut"}));
    document.getElementById("recallButton").addEventListener("click", () => runRecallSearch().catch((error) => showToast(error.message || t("toastLoadFailed"), "error")));
    document.getElementById("promotionRows").addEventListener("click", (event) => {
      const target = event.target.closest("[data-preview-promotion]");
      if (!target) {
        return;
      }
      event.stopPropagation();
      selectPromotion(target.dataset.previewPromotion).catch((error) => showToast(error.message || t("toastLoadFailed"), "error"));
    });
    document.getElementById("refreshAudit").addEventListener("click", () => refreshAudit().catch((error) => showToast(error.message || t("toastLoadFailed"), "error")));
    document.getElementById("refreshPromotions").addEventListener("click", () => refreshHistory().catch((error) => showToast(error.message || t("toastLoadFailed"), "error")));
    document.getElementById("refreshReviews").addEventListener("click", () => refreshHistory().catch((error) => showToast(error.message || t("toastLoadFailed"), "error")));
    document.getElementById("recallSearch").addEventListener("keydown", (event) => {
      if (event.key === "Enter") {
        event.preventDefault();
        runRecallSearch().catch((error) => showToast(error.message || t("toastLoadFailed"), "error"));
      }
    });
    document.getElementById("copyRewrite").addEventListener("click", async () => {
      if (!selectedCandidate) {
        showToast(t("selectCandidateFirst"), "warn");
        return;
      }
      try {
        await copyText(selectedCandidate.rewrite_suggestion || selectedCandidate.text || "");
        showToast(t("toastCopied"));
      } catch (error) {
        console.error(error);
        showToast(t("toastCopyFailed"), "error");
      }
    });
    document.getElementById("copyRollback").addEventListener("click", async () => {
      if (!rollbackInfo || !rollbackInfo.restore_command) {
        showToast(t("rollbackUnavailable"), "warn");
        return;
      }
      try {
        await copyText(rollbackInfo.restore_command);
        showToast(t("toastRollbackCopied"));
      } catch (error) {
        console.error(error);
        showToast(t("toastCopyFailed"), "error");
      }
    });

    applyLanguage();
    refresh(false).catch((error) => {
      console.error(error);
      showToast(`${t("toastLoadFailed")} ${error.message || ""}`, "error");
    });

