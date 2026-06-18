const params = new URLSearchParams(location.search);
    const token = params.get("token") || "";
    const translations = {
      en: {
        localOnly: "Local-only control plane",
        subtitle: "Review memory, skill, and skill patch candidates from a token-protected local service. All promotion actions run through this WebUI.",
        tokenProtected: "127.0.0.1 only, token protected",
        navHome: "Home",
        navData: "Data",
        navCandidates: "Candidates",
        navPromotion: "Promotion",
        navSkills: "Skills",
        navSchedule: "Schedule",
        navRuns: "Run Logs",
        navRecall: "Recall",
        navAudit: "Audit",
        navPromotions: "Promotions",
        navReviews: "Reviews",
        navDoctor: "Doctor",
        navDashboard: "Dashboard",
        navWorkflow: "Review Workflow",
        navOperations: "Operations",
        navGroupWorkspace: "Workspace",
        navGroupReview: "Review",
        navGroupOps: "Operations",
        navEvidence: "Evidence",
        navApproval: "Approval",
        navAutomation: "Automation",
        navHistory: "History",
        opsTabData: "Data",
        opsTabAutomation: "Automation",
        opsTabKnowledge: "Knowledge",
        opsTabHistory: "History",
        rpTabDetail: "Detail",
        rpTabProposal: "LLM Proposal",
        candidateReviewDrawerEyebrow: "Candidate review",
        candidateReviewDrawerTitle: "Unified Candidate Review",
        drawerTabOverview: "Overview",
        drawerTabEvidence: "Evidence",
        drawerTabProposal: "LLM Proposal",
        drawerTabApproval: "Diff & Approval",
        dataCenter: "Data Center",
        dataCenterDesc: "Initialize, back up, rebuild, scan, or export the local SQLite learning database.",
        reviewCenter: "Review Center",
        promotionCenter: "Promotion Center",
        promotionCenterDesc: "Select a candidate in Candidate Center, then use the right-side review actions to promote it into USER.md, AGENTS.md, a skill, or a skill patch.",
        skillManagement: "Skill Management",
        skillManagementDesc: "Install local skills, inspect usage telemetry, and review skill patch candidates from the candidate queue.",
        skillCandidatePanelTitle: "Skill Candidate Actions",
        emptySkillCandidates: "No skill candidates yet.",
        skillActionView: "Review",
        skillActionPreview: "Preview Diff",
        skillActionApply: "Apply",
        skillActionPromote: "Promote",
        homeTodoTitle: "Pending Workbench",
        homeTodoEmpty: "No open review work.",
        homeTodoCopy: "{review} review / {blocked} blocked",
        homeRiskTitle: "Risk Watch",
        homeRiskEmpty: "No failed runs detected.",
        homeRiskCopy: "{failed} failed run(s) need attention.",
        homePromotionTitle: "Recent Promotions",
        homePromotionEmpty: "No promotions yet.",
        homePromotionCopy: "Latest: {item}",
        dashboardTopPrioritiesTitle: "Top Review Priorities",
        dashboardTopPrioritiesEmpty: "No review priorities yet.",
        dashboardPrioritySummary: "{label} · score {score}",
        dashboardNextActionTitle: "Next Best Action",
        dashboardNextActionLoading: "Loading the current workflow state...",
        dashboardStateSetup: "Setup",
        dashboardStateRecovery: "Recovery",
        dashboardStateReview: "Review",
        dashboardStateScan: "Scan",
        dashboardNextSetup: "Initialize the database and install the local loop before collecting new evidence.",
        dashboardNextRecovery: "A failed run is visible. Review run logs and audit signals before starting more scans.",
        dashboardNextReview: "{count} candidate(s) are waiting for manual review. Start with the highest-priority evidence package.",
        dashboardNextScan: "No active review work is visible. Run a scan to let Codex extract and analyze fresh candidates.",
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
        evolutionProposalTitle: "LLM Analysis & Proposal",
        manualApprovalRequired: "Manual approval",
        manualApprovalUnknown: "Review required",
        manualApprovalDockTitle: "Manual Approval Dock",
        proposalTargetTitle: "Proposal Target",
        proposalEvidenceTitle: "Evidence Assessment",
        proposalRationaleTitle: "Rationale",
        proposalVerificationTitle: "Verification",
        proposalTextTitle: "Proposed Text",
        proposalTextEmpty: "Select a candidate to load the proposed text.",
        analysisLoading: "Loading LLM analysis...",
        analysisUnavailable: "No analysis is available for this candidate yet.",
        workflowMapScanTitle: "Scan & Analyze",
        workflowMapScanCopy: "Run scan/rebuild, let Codex extract and analyze candidates, and keep fallback rules available.",
        workflowMapReviewTitle: "Review Evidence",
        workflowMapReviewCopy: "Inspect evidence, risk, proposal text, rationale, and verification before changing durable memory.",
        workflowMapApproveTitle: "Approve Manually",
        workflowMapApproveCopy: "Use the Manual Approval Dock for confirmed writes, then audit history and rollback previews.",
        workflowStageQueue: "Queue",
        workflowStageEvidence: "Evidence",
        workflowStageProposal: "LLM Proposal",
        workflowStagePreview: "Diff Preview",
        workflowStageApproval: "Manual Approval",
        workflowStageHistory: "History",
        workflowContextTitle: "Review Context",
        workflowContextEmpty: "Select a candidate to see the current review context.",
        workflowContextNextLabel: "Next step",
        workflowContextDetailAction: "Open detail",
        workflowContextApprovalAction: "Open approval",
        workflowSourceEyebrow: "Source",
        workflowSourceSkillsTitle: "From skill candidates",
        workflowSourceSkillsCopy: "This review was opened from Skill Management.",
        returnToSkills: "Return to Skills",
        workflowReadinessTitle: "Review Readiness",
        workflowReadinessSelected: "Candidate selected",
        workflowReadinessEvidence: "Evidence available",
        workflowReadinessAnalysis: "LLM analysis loaded",
        workflowReadinessPreview: "Promotion diff previewed",
        workflowReadinessManual: "Manual confirmation still required",
        approvalReady: "Ready for manual confirmation after reviewing the diff.",
        approvalBlocked: "Select a candidate, review evidence, load analysis, and preview a diff before approval.",
        workflowNextActionTitle: "Current Review Step",
        workflowNextSelectCandidate: "Select a candidate to start evidence review.",
        workflowNextLoadAnalysis: "Review evidence and wait for the LLM analysis package to load.",
        workflowNextPreviewDiff: "Review the proposal, then preview a promotion diff. Preview does not write memory.",
        workflowNextManualApproval: "Diff is loaded. Use the Manual Approval Dock below for the final explicit confirmation.",
        workflowPrimarySelectCandidate: "Select Top Candidate",
        workflowPrimaryPreviewUser: "Preview USER.md",
        workflowPrimaryPreviewAgents: "Preview AGENTS.md",
        workflowPrimaryPreviewSkill: "Preview Skill",
        workflowPrimaryPreviewPatch: "Preview Patch",
        workflowPrimaryApprovalDock: "Go To Approval Dock",
        workflowSecondaryRefreshCandidates: "Refresh Queue",
        workflowSecondaryCopyRewrite: "Copy Rewrite",
        workflowSecondarySaveReview: "Save Review",
        operationsIndexData: "Data",
        operationsIndexAutomation: "Automation",
        operationsIndexKnowledge: "Knowledge",
        operationsIndexEvidence: "Evidence",
        operationsLifecycleDataTitle: "Data Lifecycle",
        operationsLifecycleDataCopy: "Initialize, back up, scan, rebuild, export, and dry-run imports from one place.",
        operationsLifecycleAutomationTitle: "Automation",
        operationsLifecycleAutomationCopy: "Install the daily scan and launcher, then review results from the WebUI queue.",
        operationsLifecycleKnowledgeTitle: "Knowledge",
        operationsLifecycleKnowledgeCopy: "Track skill health, recall prior sessions, and route candidates back into manual review.",
        operationsLifecycleEvidenceTitle: "Evidence",
        operationsLifecycleEvidenceCopy: "Use run logs, audit history, promotion history, and rollback previews for recovery decisions.",
        operationsRecoveryTitle: "Recovery Queue",
        operationsRecoveryDesc: "Review failed runs, audit signals, and rollback previews before taking manual recovery action.",
        recoveryQueueEmpty: "No recovery work is visible.",
        recoveryQueueRunFailure: "Failed run",
        recoveryQueueAuditSignal: "Recent audit signal",
        recoveryQueueRollbackSignal: "Rollback preview available",
        recoveryQueueOpenRuns: "Open Run Logs",
        recoveryQueueOpenAudit: "Open Audit",
        recoveryQueueOpenPromotions: "Open Promotions",
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
        installUserTemplate: "Initialize USER.md Template",
        rebuildDatabase: "Rebuild Database",
        scanOnce: "Scan Once",
        scanAndAnalyze: "Scan & Analyze",
        toastScannedAnalyzed: "Scan & analysis completed: {new} new candidates, {analyzed} analyzed.",
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
        priorityReviewFirst: "Priority first",
        priorityHeader: "Priority",
        sortNewest: "Newest",
        sortOldest: "Oldest",
        sortConfidence: "Confidence",
        priorityHighRisk: "High risk",
        priorityReadyReview: "Ready review",
        prioritySkillChange: "Skill change",
        priorityNormal: "Normal",
        priorityReasonsTitle: "Priority Rationale",
        priorityReasonReview: "Open review item",
        priorityReasonRisk: "Safety or conflict needs attention",
        priorityReasonEvidence: "Evidence and confidence are strong enough to review",
        priorityReasonSkill: "Skill-related change needs careful inspection",
        priorityReasonProposal: "LLM proposal target is available",
        priorityReasonNormal: "No special priority signal",
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
        toastUserTemplateInstalled: "USER.md template initialized.",
        toastScanned: "Scan completed.",
        toastScanAnalyzedComplete: "Scan and analysis completed.",
        toastScanStarted: "Scan started.",
        toastScanAnalyzeStarted: "Scan and analysis started.",
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
        confirmModalTitle: "Confirm Operation",
        confirmModalCancel: "Cancel",
        confirmModalConfirm: "Confirm",
        confirmDryRunPreviewLabel: "Dry-run preview",
        confirmActualEffectLabel: "Actual execution effect",
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
          files: "Writes only under $HOME/.agents/skills/.",
          result: "New Codex sessions can discover the updated skills after restart or reload. USER.md and AGENTS.md are not modified.",
        },
        confirmInstallUserTemplate: {
          action: "Create the default USER.md memory template if it is missing.",
          files: "Writes $HOME/.codex/memories/USER.md only when that file does not already exist.",
          result: "Existing USER.md content is preserved; this only initializes a missing global memory file.",
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
        setupCheckDone: "Done",
        setupCheckTodo: "To do",
        setupCheckDatabaseTitle: "Initialize database",
        setupCheckDatabaseCopy: "Create the local SQLite store and WebUI assets.",
        setupCheckHistoryTitle: "Rebuild history",
        setupCheckHistoryCopy: "Scan historical sessions into the review queue.",
        setupCheckSkillsTitle: "Install skills",
        setupCheckSkillsCopy: "Install bundled recall and memory capture skills.",
        setupCheckScheduleTitle: "Install schedule",
        setupCheckScheduleCopy: "Create the daily local scan runner.",
        setupStepDatabaseDone: "SQLite database is available.",
        setupStepDatabaseTodo: "Create the local SQLite database first.",
        setupStepHistoryDone: "Historical sessions have been scanned.",
        setupStepHistoryTodo: "Run a rebuild or scan to collect first evidence.",
        setupStepSkillsDone: "Bundled skills are installed.",
        setupStepSkillsTodo: "Install or update bundled skills.",
        setupStepScheduleDone: "Daily schedule is installed.",
        setupStepScheduleTodo: "Install the daily scan schedule when ready.",
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
        mergeSuggestionsModuleCopy: "Review duplicate candidate groups without duplicating the candidate list.",
        emptyMergeSuggestions: "No merge suggestions.",
        applyMerge: "Apply Merge",
        promotionPreviewTitle: "Promotion Diff Preview",
        promotionPreviewEmpty: "Select a promotion action to preview the diff.",
        previewOnlyTitle: "Preview Only",
        previewOnlyCopy: "Load a diff without promoting. Promotion still requires the buttons below and a confirmation dialog.",
        previewUserDiff: "Preview USER.md",
        previewAgentsDiff: "Preview AGENTS.md",
        previewSkillDiff: "Preview Skill",
        previewPatchDiff: "Preview Patch",
        toastPreviewLoaded: "Preview loaded. No promotion was written.",
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
        },
        reviewProgressIdle: "-",
        reviewProgressLabel: "Reviewed {reviewed} / {total}",
      },
      zh: {
        localOnly: "本机专用控制台",
        subtitle: "从受令牌保护的本地服务中审阅记忆、技能和技能补丁候选；所有晋升操作都可以在 WebUI 中点击完成。",
        tokenProtected: "仅绑定 127.0.0.1，并启用令牌保护",
        navHome: "首页",
        navData: "数据",
        navCandidates: "候选",
        navPromotion: "晋升中心",
        navSkills: "技能",
        navSchedule: "调度中心",
        navRuns: "运行日志",
        navRecall: "检索",
        navAudit: "审计",
        navPromotions: "晋升历史",
        navReviews: "审阅历史",
        navDoctor: "诊断",
        navDashboard: "总览",
        navWorkflow: "审阅工作流",
        navOperations: "运维与历史",
        navGroupWorkspace: "工作台",
        navGroupReview: "审阅",
        navGroupOps: "运维",
        navEvidence: "证据",
        navApproval: "审批",
        navAutomation: "自动化",
        navHistory: "历史",
        opsTabData: "数据",
        opsTabAutomation: "自动化",
        opsTabKnowledge: "知识",
        opsTabHistory: "历史",
        rpTabDetail: "详情",
        rpTabProposal: "LLM 建议",
        candidateReviewDrawerEyebrow: "候选审阅",
        candidateReviewDrawerTitle: "统一候选审阅",
        drawerTabOverview: "概览",
        drawerTabEvidence: "证据",
        drawerTabProposal: "LLM 建议",
        drawerTabApproval: "Diff 与审批",
        dataCenter: "数据中心",
        dataCenterDesc: "初始化、备份、重建、扫描或导出本地 SQLite 学习数据库。",
        reviewCenter: "审阅中心",
        promotionCenter: "晋升中心",
        promotionCenterDesc: "先在候选中心选择一条记录，再使用右侧审阅操作晋升到 USER.md、AGENTS.md、技能或技能补丁。",
        skillManagement: "Skill 管理",
        skillManagementDesc: "安装本地技能，查看技能使用遥测，并从候选队列处理技能补丁。",
        skillCandidatePanelTitle: "技能候选待处理",
        emptySkillCandidates: "暂无技能候选。",
        skillActionView: "查看",
        skillActionPreview: "预览",
        skillActionApply: "应用",
        skillActionPromote: "晋升",
        homeTodoTitle: "待处理工作台",
        homeTodoEmpty: "暂无待处理审阅工作。",
        homeTodoCopy: "{review} 个待审 / {blocked} 个阻断",
        homeRiskTitle: "风险观察",
        homeRiskEmpty: "暂无失败运行。",
        homeRiskCopy: "{failed} 个失败运行需要关注。",
        homePromotionTitle: "最近晋升",
        homePromotionEmpty: "暂无晋升记录。",
        homePromotionCopy: "最近：{item}",
        dashboardTopPrioritiesTitle: "优先审阅候选",
        dashboardTopPrioritiesEmpty: "暂无优先审阅项。",
        dashboardPrioritySummary: "{label} · 分数 {score}",
        dashboardNextActionTitle: "下一步建议",
        dashboardNextActionLoading: "正在读取当前流程状态...",
        dashboardStateSetup: "初始化",
        dashboardStateRecovery: "恢复",
        dashboardStateReview: "审阅",
        dashboardStateScan: "扫描",
        dashboardNextSetup: "先初始化数据库并安装本地循环，再开始收集新证据。",
        dashboardNextRecovery: "当前有失败运行。建议先查看运行日志和审计信号，再继续发起扫描。",
        dashboardNextReview: "有 {count} 条候选等待人工审阅。优先处理证据最充分、风险最高的候选包。",
        dashboardNextScan: "当前没有活跃审阅工作。可以扫描一次，让 Codex 提取并分析新的候选。",
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
        evolutionProposalTitle: "LLM 分析与进化建议",
        manualApprovalRequired: "需要人工审批",
        manualApprovalUnknown: "需要复核",
        manualApprovalDockTitle: "人工审批操作台",
        proposalTargetTitle: "建议目标",
        proposalEvidenceTitle: "证据评估",
        proposalRationaleTitle: "建议理由",
        proposalVerificationTitle: "验证步骤",
        proposalTextTitle: "建议文本",
        proposalTextEmpty: "选择候选后加载建议文本。",
        analysisLoading: "正在加载 LLM 分析...",
        analysisUnavailable: "这条候选暂无可用分析。",
        workflowMapScanTitle: "扫描与分析",
        workflowMapScanCopy: "运行 scan/rebuild，让 Codex 提取并分析候选，同时保留规则兜底。",
        workflowMapReviewTitle: "审阅证据",
        workflowMapReviewCopy: "在改变长期记忆前，核对证据、风险、建议文本、理由和验证步骤。",
        workflowMapApproveTitle: "人工审批",
        workflowMapApproveCopy: "只通过人工审批操作台执行确认写入，再从审计历史和回滚预览复核。",
        workflowStageQueue: "队列",
        workflowStageEvidence: "证据",
        workflowStageProposal: "LLM 建议",
        workflowStagePreview: "Diff 预览",
        workflowStageApproval: "人工审批",
        workflowStageHistory: "历史",
        workflowContextTitle: "审阅上下文",
        workflowContextEmpty: "选择候选后在这里查看当前处理上下文。",
        workflowContextNextLabel: "下一步",
        workflowContextDetailAction: "打开详情",
        workflowContextApprovalAction: "打开审批",
        workflowSourceEyebrow: "来源",
        workflowSourceSkillsTitle: "来自技能候选",
        workflowSourceSkillsCopy: "这条候选从技能管理页打开，处理完成后可直接返回。",
        returnToSkills: "返回技能",
        workflowReadinessTitle: "审阅就绪度",
        workflowReadinessSelected: "已选择候选",
        workflowReadinessEvidence: "已有证据",
        workflowReadinessAnalysis: "LLM 分析已加载",
        workflowReadinessPreview: "已预览晋升 diff",
        workflowReadinessManual: "仍需人工确认",
        approvalReady: "已具备人工确认前的审阅条件，请核对 diff 后手动确认。",
        approvalBlocked: "请先选择候选、核对证据、加载分析，并预览 diff 后再审批。",
        workflowNextActionTitle: "当前审阅步骤",
        workflowNextSelectCandidate: "选择一条候选，开始核对证据。",
        workflowNextLoadAnalysis: "核对候选证据，并等待 LLM 分析包加载完成。",
        workflowNextPreviewDiff: "核对建议目标和建议文本后，先预览晋升 diff。预览不会写入记忆。",
        workflowNextManualApproval: "Diff 已加载。最终写入只能在下方人工审批操作台显式确认。",
        workflowPrimarySelectCandidate: "选择最高优先级",
        workflowPrimaryPreviewUser: "预览 USER.md",
        workflowPrimaryPreviewAgents: "预览 AGENTS.md",
        workflowPrimaryPreviewSkill: "预览 Skill",
        workflowPrimaryPreviewPatch: "预览 Patch",
        workflowPrimaryApprovalDock: "前往审批操作台",
        workflowSecondaryRefreshCandidates: "刷新队列",
        workflowSecondaryCopyRewrite: "复制改写",
        workflowSecondarySaveReview: "保存审阅",
        operationsIndexData: "数据",
        operationsIndexAutomation: "自动化",
        operationsIndexKnowledge: "知识",
        operationsIndexEvidence: "证据",
        operationsLifecycleDataTitle: "数据生命周期",
        operationsLifecycleDataCopy: "集中处理初始化、备份、扫描、重建、导出和导入 dry-run 预览。",
        operationsLifecycleAutomationTitle: "自动化",
        operationsLifecycleAutomationCopy: "安装每日扫描和桌面入口，再从 WebUI 队列审阅结果。",
        operationsLifecycleKnowledgeTitle: "知识资产",
        operationsLifecycleKnowledgeCopy: "查看 Skill 健康、跨会话检索，并把候选重新引回人工审阅。",
        operationsLifecycleEvidenceTitle: "证据与恢复",
        operationsLifecycleEvidenceCopy: "通过运行日志、审计、晋升历史和回滚预览支撑恢复决策。",
        operationsRecoveryTitle: "恢复复盘队列",
        operationsRecoveryDesc: "先复盘失败运行、审计信号和回滚预览，再手动执行恢复动作。",
        recoveryQueueEmpty: "暂无可见恢复事项。",
        recoveryQueueRunFailure: "失败运行",
        recoveryQueueAuditSignal: "最近审计信号",
        recoveryQueueRollbackSignal: "可查看回滚预览",
        recoveryQueueOpenRuns: "打开运行日志",
        recoveryQueueOpenAudit: "打开审计",
        recoveryQueueOpenPromotions: "打开晋升历史",
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
        installUserTemplate: "初始化 USER.md 模板",
        rebuildDatabase: "重建数据库",
        scanOnce: "扫描一次",
        scanAndAnalyze: "扫描并分析",
        toastScannedAnalyzed: "扫描与分析完成：新增 {new} 个候选，分析 {analyzed} 个。",
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
        priorityReviewFirst: "优先处理",
        priorityHeader: "优先级",
        sortNewest: "最新",
        sortOldest: "最早",
        sortConfidence: "置信度",
        priorityHighRisk: "高风险",
        priorityReadyReview: "可审阅",
        prioritySkillChange: "技能变更",
        priorityNormal: "普通",
        priorityReasonsTitle: "优先级依据",
        priorityReasonReview: "仍在待审队列",
        priorityReasonRisk: "安全或冲突信号需要关注",
        priorityReasonEvidence: "证据数量和置信度足够进入审阅",
        priorityReasonSkill: "技能相关变更需要谨慎检查",
        priorityReasonProposal: "已有 LLM 建议目标",
        priorityReasonNormal: "没有特殊优先级信号",
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
        toastUserTemplateInstalled: "USER.md 模板已初始化。",
        toastScanned: "扫描已完成。",
        toastScanAnalyzedComplete: "扫描与分析已完成。",
        toastScanStarted: "扫描已启动。",
        toastScanAnalyzeStarted: "扫描与分析已启动。",
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
        confirmModalTitle: "确认操作",
        confirmModalCancel: "取消",
        confirmModalConfirm: "确认执行",
        confirmDryRunPreviewLabel: "Dry-run 预览",
        confirmActualEffectLabel: "实际执行影响",
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
          files: "只写入 $HOME/.agents/skills/。",
          result: "重启或重新加载后，新 Codex 会话可以发现更新后的技能；不会修改 USER.md 或 AGENTS.md。",
        },
        confirmInstallUserTemplate: {
          action: "当 USER.md 不存在时，创建默认全局记忆模板。",
          files: "仅在 $HOME/.codex/memories/USER.md 不存在时写入该文件。",
          result: "已有 USER.md 内容会保留；这个操作只负责初始化缺失的全局记忆文件。",
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
        setupCheckDone: "已完成",
        setupCheckTodo: "待执行",
        setupCheckDatabaseTitle: "初始化数据库",
        setupCheckDatabaseCopy: "创建本地 SQLite 存储和 WebUI 文件。",
        setupCheckHistoryTitle: "重建历史",
        setupCheckHistoryCopy: "把历史会话扫描进入审阅队列。",
        setupCheckSkillsTitle: "安装技能",
        setupCheckSkillsCopy: "安装内置的召回和记忆捕获技能。",
        setupCheckScheduleTitle: "安装调度",
        setupCheckScheduleCopy: "创建每日本地扫描任务。",
        setupStepDatabaseDone: "SQLite 数据库已可用。",
        setupStepDatabaseTodo: "先创建本地 SQLite 数据库。",
        setupStepHistoryDone: "历史会话已完成扫描。",
        setupStepHistoryTodo: "运行重建或扫描，收集第一批证据。",
        setupStepSkillsDone: "内置技能已安装。",
        setupStepSkillsTodo: "安装或更新内置技能。",
        setupStepScheduleDone: "每日调度已安装。",
        setupStepScheduleTodo: "准备好后安装每日扫描调度。",
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
        mergeSuggestionsModuleCopy: "集中处理重复候选分组，不在候选列表外重复渲染明细。",
        emptyMergeSuggestions: "暂无合并建议。",
        applyMerge: "应用合并",
        promotionPreviewTitle: "晋升 Diff 预览",
        promotionPreviewEmpty: "选择晋升动作后预览 diff。",
        previewOnlyTitle: "仅预览",
        previewOnlyCopy: "只加载 diff，不执行晋升。真正晋升仍必须点击下方按钮并通过确认弹窗。",
        previewUserDiff: "预览 USER.md",
        previewAgentsDiff: "预览 AGENTS.md",
        previewSkillDiff: "预览 Skill",
        previewPatchDiff: "预览 Patch",
        toastPreviewLoaded: "已加载预览，未执行晋升写入。",
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
        },
        reviewProgressIdle: "-",
        reviewProgressLabel: "已审阅 {reviewed} / {total}",
      }
    };

    let currentTheme = initialTheme();
    let currentLanguage = initialLanguage();
    let allCandidates = [];
    let selectedCandidate = null;
    let currentFilter = "all";
    let statusFilter = "all";
    let createdAtFilter = "";
    let searchTerm = "";
    let candidateSortMode = "priority";
    let currentPage = 1;
    let pageSize = 20;
    let toastTimer = null;
    let activeRunId = null;
    let activeRunTimer = null;
    let currentView = "dashboard";
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
    let selectedAnalysisPayload = null;
    let selectedAnalysisLoading = false;
    let workflowSourceContext = null;
    let pendingConfirmResolve = null;
    window.selectedCandidateId = null;

    function initialLanguage() {
      const savedLanguage = localStorage.getItem("codexSilLanguage");
      if (savedLanguage === "zh" || savedLanguage === "en") {
        return savedLanguage;
      }
      return "zh";
    }

    function initialTheme() {
      const saved = localStorage.getItem("codexSilTheme");
      if (saved === "light" || saved === "dark") {
        return saved;
      }
      return window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light";
    }

    function applyTheme() {
      document.body.setAttribute("data-theme", currentTheme);
      document.querySelectorAll("#themeToggle button").forEach((button) => {
        const active = button.dataset.theme === currentTheme;
        button.classList.toggle("active", active);
        button.setAttribute("aria-pressed", String(active));
      });
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
      renderEvolutionProposalBoard();
      renderWorkflowReadiness();
      renderWorkflowNextAction();
      renderRuns();
      renderRecallResults();
      renderDoctor();
      renderDoctorHealth();
      renderAudit();
      renderPromotions();
      renderReviews();
      renderRollbackPreview();
      renderOperationsRecoveryQueue();
      renderHomeTasks();
      renderScheduleStatus();
      renderSetupWizard();
      renderDailyDigest();
      renderDashboardTopPriorities();
      renderMergeSuggestions();
      renderSkillHealth();
      renderSkillCandidates();
      renderPromotionPreview(latestPromotionPreview);
      renderReviewProgress();
      renderWorkflowContextPanel();
      applyTheme();
      refreshScheduleStatus().catch((error) => console.warn(error));
    }

    let currentSummary = {memory: 0, skill: 0, skill_patch: 0, review: 0};

    function mountOperationsSections() {
      const target = document.getElementById("operationsDynamicSections");
      if (!target) {
        return;
      }
      document.querySelectorAll(".operations-template-fragment").forEach((fragment) => {
        while (fragment.firstElementChild) {
          target.appendChild(fragment.firstElementChild);
        }
        fragment.remove();
      });
    }

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
        if (!button.closest("#sideNav, #themeToggle, #languageToggle")) {
          button.disabled = isBusy;
        }
      });
    }

    function operationPlanSuffix(confirmKey) {
      if (confirmKey === "confirmInstallSchedule" && scheduleInfo && scheduleInfo.operation_plan) {
        const plan = scheduleInfo.operation_plan;
        return `${t("confirmDryRunPreviewLabel")}:\n${plan.dry_run_preview || "-"}\n\n${t("confirmActualEffectLabel")}:\n${plan.actual_effect || "-"}`;
      }
      if (confirmKey === "confirmInstallShortcut" && scheduleInfo && scheduleInfo.shortcut_plan) {
        const plan = scheduleInfo.shortcut_plan || {};
        return `${t("confirmDryRunPreviewLabel")}:\n${plan.dry_run_preview || "-"}\n\n${t("confirmActualEffectLabel")}:\n${plan.actual_effect || "-"}`;
      }
      return "";
    }

    function closeConfirmModal(result) {
      const modal = document.getElementById("confirmModal");
      if (modal) {
        modal.hidden = true;
      }
      if (pendingConfirmResolve) {
        pendingConfirmResolve(Boolean(result));
        pendingConfirmResolve = null;
      }
    }

    function confirmAction(confirmKey, extra = "") {
      if (!confirmKey) {
        return Promise.resolve(true);
      }
      const detail = t(confirmKey);
      const body = document.getElementById("confirmModalBody");
      const modal = document.getElementById("confirmModal");
      const dialog = modal && modal.querySelector(".confirm-dialog");
      if (!body || !modal) {
        return Promise.resolve(false);
      }
      const parts = [];
      if (typeof detail === "object") {
        parts.push([t("confirmActionLabel"), detail.action || "-"]);
        parts.push([t("confirmFilesLabel"), detail.files || "-"]);
        parts.push([t("confirmResultLabel"), detail.result || "-"]);
      } else {
        parts.push([t("confirmActionLabel"), String(detail)]);
      }
      const plan = operationPlanSuffix(confirmKey);
      body.innerHTML = "";
      for (const [label, value] of parts) {
        const section = document.createElement("section");
        section.className = "confirm-section";
        const heading = document.createElement("h3");
        heading.textContent = label;
        const text = document.createElement("p");
        text.textContent = value;
        section.append(heading, text);
        body.appendChild(section);
      }
      for (const block of [plan, extra].filter(Boolean)) {
        const pre = document.createElement("pre");
        pre.className = "diff-preview confirm-preview";
        pre.textContent = block;
        body.appendChild(pre);
      }
      modal.hidden = false;
      if (dialog) {
        dialog.focus();
      }
      return new Promise((resolve) => {
        pendingConfirmResolve = resolve;
      });
    }

    function bindConfirmModal() {
      const confirm = document.getElementById("confirmModalConfirm");
      const cancel = document.getElementById("confirmModalCancel");
      const backdrop = document.getElementById("confirmModalBackdrop");
      if (confirm) {
        confirm.addEventListener("click", () => closeConfirmModal(true));
      }
      if (cancel) {
        cancel.addEventListener("click", () => closeConfirmModal(false));
      }
      if (backdrop) {
        backdrop.addEventListener("click", () => closeConfirmModal(false));
      }
      document.addEventListener("keydown", (event) => {
        const modal = document.getElementById("confirmModal");
        if (event.key === "Escape" && modal && !modal.hidden) {
          closeConfirmModal(false);
        }
      });
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
      const steps = {
        database: Boolean(setupStatus.database_exists),
        history: Boolean((setupStatus.session_count || 0) > 0 || (setupStatus.candidate_count || 0) > 0),
        skills: Boolean(setupStatus.skills_installed),
        schedule: Boolean(setupStatus.schedule_installed),
      };
      for (const [step, done] of Object.entries(steps)) {
        const row = document.querySelector(`[data-setup-step="${step}"]`);
        const badge = document.getElementById(`setupCheck${step.charAt(0).toUpperCase()}${step.slice(1)}`);
        const copyText = row && row.querySelector(".task-copy");
        if (row) {
          row.classList.toggle("setup-done", done);
          row.classList.toggle("setup-todo", !done);
        }
        if (badge) {
          badge.textContent = done ? t("setupCheckDone") : t("setupCheckTodo");
          badge.className = `setup-check-status ${done ? "status" : "review"}`;
        }
        if (copyText) {
          copyText.textContent = done ? t(`setupStep${step.charAt(0).toUpperCase()}${step.slice(1)}Done`) : t(`setupStep${step.charAt(0).toUpperCase()}${step.slice(1)}Todo`);
        }
      }
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

    function dashboardNextActionState() {
      const ready = setupStatus && setupStatus.ready && setupStatus.schedule_installed && setupStatus.skills_installed;
      const openReviews = (currentSummary.review || 0) + (currentSummary.blocked || 0);
      const failures = latestFailureCount();
      if (!ready) {
        return {
          tone: "review",
          badge: t("dashboardStateSetup"),
          copy: t("dashboardNextSetup"),
        };
      }
      if (failures) {
        return {
          tone: "review",
          badge: t("dashboardStateRecovery"),
          copy: t("dashboardNextRecovery"),
        };
      }
      if (openReviews) {
        return {
          tone: "status",
          badge: t("dashboardStateReview"),
          copy: t("dashboardNextReview", {count: openReviews}),
        };
      }
      return {
        tone: "status",
        badge: t("dashboardStateScan"),
        copy: t("dashboardNextScan"),
      };
    }

    function renderDashboardNextAction() {
      const badge = document.getElementById("dashboardNextActionBadge");
      const copy = document.getElementById("dashboardNextActionCopy");
      if (!badge || !copy) {
        return;
      }
      const state = dashboardNextActionState();
      badge.textContent = state.badge;
      badge.className = `next-action-state ${state.tone}`;
      copy.textContent = state.copy;
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

    function dashboardPriorityItem(item) {
      const card = document.createElement("article");
      card.className = "dashboard-priority-item";
      const title = document.createElement("strong");
      title.textContent = item.title || item.text || "-";
      const summary = document.createElement("span");
      summary.textContent = t("dashboardPrioritySummary", {
        label: candidatePriorityLabel(item),
        score: candidatePriorityScore(item),
      });
      const reasons = document.createElement("small");
      reasons.textContent = candidatePriorityReasons(item).join(" / ");
      card.append(title, summary, reasons);
      return card;
    }

    function renderDashboardTopPriorities() {
      const list = document.getElementById("dashboardPriorityList");
      if (!list) {
        return;
      }
      list.innerHTML = "";
      const priorities = sortedCandidates(
        allCandidates.filter((item) => ["review", "blocked"].includes(String(item.status || "").toLowerCase()))
      ).slice(0, 3);
      if (!priorities.length) {
        const empty = document.createElement("div");
        empty.className = "empty-row";
        empty.textContent = t("dashboardTopPrioritiesEmpty");
        list.appendChild(empty);
        return;
      }
      for (const item of priorities) {
        list.appendChild(dashboardPriorityItem(item));
      }
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
      renderDashboardTopPriorities();
      renderDashboardNextAction();
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
      const commandLines = [scheduleInfo && scheduleInfo.command ? scheduleInfo.command : "sil.py scan --once"];
      if (scheduleInfo && scheduleInfo.operation_plan) {
        commandLines.push("");
        commandLines.push(`${t("confirmDryRunPreviewLabel")}: ${scheduleInfo.operation_plan.dry_run_preview || "-"}`);
        commandLines.push(`${t("confirmActualEffectLabel")}: ${scheduleInfo.operation_plan.actual_effect || "-"}`);
      }
      if (scheduleInfo && scheduleInfo.shortcut_plan) {
        commandLines.push("");
        commandLines.push(`${t("installShortcut")} ${t("confirmDryRunPreviewLabel")}: ${scheduleInfo.shortcut_plan.dry_run_preview || "-"}`);
        commandLines.push(`${t("installShortcut")} ${t("confirmActualEffectLabel")}: ${scheduleInfo.shortcut_plan.actual_effect || "-"}`);
      }
      command.textContent = commandLines.join("\n");
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
      } else {
        badge.textContent = selectedCandidate.status || t("noneSelected");
        badge.className = `tag ${selectedCandidate.status === "blocked" ? "review" : "status"}`;
      }
      result.textContent = lastOperationMessage || t("operationResultIdle");
      renderEvolutionProposalBoard();
    }

    function setText(id, text) {
      const element = document.getElementById(id);
      if (element) {
        element.textContent = text;
      }
    }

    function renderEvolutionProposalBoard() {
      const riskPanel = document.getElementById("candidateRiskSummary");
      const manualBadge = document.getElementById("proposalManualApproval");
      if (!riskPanel || !manualBadge) {
        return;
      }
      if (!selectedCandidate) {
        riskPanel.className = "action-card";
        setText("candidateRiskCopy", t("selectCandidateHint"));
        setText("candidateRecommendationCopy", t("selectCandidateHint"));
        setText("proposalTarget", t("selectCandidateHint"));
        setText("proposalEvidence", t("selectCandidateHint"));
        setText("proposalRationale", t("selectCandidateHint"));
        setText("proposalVerification", t("selectCandidateHint"));
        setText("proposalText", t("proposalTextEmpty"));
        manualBadge.textContent = t("manualApprovalUnknown");
        manualBadge.className = "tag status";
        return;
      }
      const risk = candidateRisk(selectedCandidate);
      riskPanel.className = `action-card ${risk.className}`.trim();
      setText("candidateRiskCopy", risk.text);
      setText("candidateRecommendationCopy", candidateRecommendation(selectedCandidate));
      if (selectedAnalysisLoading) {
        setText("proposalTarget", selectedCandidate.proposal_target_type || "-");
        setText("proposalEvidence", t("analysisLoading"));
        setText("proposalRationale", t("analysisLoading"));
        setText("proposalVerification", t("analysisLoading"));
        setText("proposalText", t("analysisLoading"));
        manualBadge.textContent = t("manualApprovalUnknown");
        manualBadge.className = "tag review";
        return;
      }
      const analysis = selectedAnalysisPayload && selectedAnalysisPayload.analysis;
      const proposal = selectedAnalysisPayload && selectedAnalysisPayload.proposal;
      setText("proposalTarget", proposal
        ? `${proposal.target_type || "-"} · ${proposal.target_path || "-"}`
        : selectedCandidate.proposal_target_type || t("analysisUnavailable"));
      setText("proposalEvidence", analysis
        ? `${analysis.evidence_assessment || "-"}\n${analysis.conflicts || ""}\n${analysis.rewrite_quality || ""}`.trim()
        : selectedCandidate.analysis_next_step || t("analysisUnavailable"));
      setText("proposalRationale", proposal ? proposal.rationale || "-" : t("analysisUnavailable"));
      setText("proposalVerification", proposal ? proposal.verification || "-" : t("analysisUnavailable"));
      const proposalText = document.getElementById("proposalText");
      if (proposalText) {
        if (proposal && proposal.proposed_text) {
          proposalText.innerHTML = renderDiff(proposal.proposed_text);
          proposalText.className = "diff-view";
        } else {
          proposalText.textContent = t("proposalTextEmpty");
          proposalText.className = "diff-preview";
        }
      }
      const manual = !proposal || proposal.requires_manual_approval !== false;
      manualBadge.textContent = manual ? t("manualApprovalRequired") : t("manualApprovalUnknown");
      manualBadge.className = `tag ${manual ? "review" : "status"}`;
    }

    async function loadCandidateAnalysis(id) {
      selectedAnalysisPayload = null;
      selectedAnalysisLoading = true;
      renderEvolutionProposalBoard();
      renderWorkflowNextAction();
      try {
        const payload = await api(`/api/candidates/${id}/analysis`);
        if (String(window.selectedCandidateId) === String(id)) {
          selectedAnalysisPayload = payload;
        }
      } catch (error) {
        console.warn(error);
        if (String(window.selectedCandidateId) === String(id)) {
          selectedAnalysisPayload = null;
        }
      } finally {
        if (String(window.selectedCandidateId) === String(id)) {
          selectedAnalysisLoading = false;
          renderEvolutionProposalBoard();
          renderWorkflowReadiness();
        }
      }
    }

    function renderPromotionPreview(preview) {
      const element = document.getElementById("promotionPreviewText");
      if (!element) {
        return;
      }
      if (preview && preview.diff) {
        element.innerHTML = renderDiff(preview.diff);
        element.className = "diff-view";
      } else {
        element.textContent = t("promotionPreviewEmpty");
        element.className = "diff-preview";
      }
      renderWorkflowReadiness();
    }

    function workflowReadinessSteps() {
      const hasSelection = Boolean(selectedCandidate);
      const hasEvidence = hasSelection && Number(selectedCandidate.source_count || 0) > 0;
      const hasAnalysis = hasSelection && !selectedAnalysisLoading && Boolean(selectedAnalysisPayload && selectedAnalysisPayload.analysis);
      const hasPreview = hasSelection
        && Boolean(latestPromotionPreview && latestPromotionPreview.diff)
        && String(latestPromotionPreview.candidate_id || window.selectedCandidateId) === String(window.selectedCandidateId);
      return [
        {stage: "queue", key: "workflowReadinessSelected", done: hasSelection},
        {stage: "evidence", key: "workflowReadinessEvidence", done: hasEvidence},
        {stage: "proposal", key: "workflowReadinessAnalysis", done: hasAnalysis},
        {stage: "preview", key: "workflowReadinessPreview", done: hasPreview},
        {stage: "approval", key: "workflowReadinessManual", done: hasPreview},
      ];
    }

    function proposalTargetType() {
      const proposal = selectedAnalysisPayload && selectedAnalysisPayload.proposal;
      const target = proposal && proposal.target_type ? proposal.target_type : selectedCandidate && selectedCandidate.proposal_target_type;
      const normalized = String(target || selectedCandidate && selectedCandidate.destination || "").toLowerCase();
      if (normalized.includes("agents") || normalized === "project") {
        return "agents";
      }
      if (normalized.includes("skill_patch") || normalized.includes("patch")) {
        return "patch";
      }
      if (normalized.includes("skill")) {
        return "skill";
      }
      return "user";
    }

    function workflowPrimaryPreviewLabel(target) {
      const keys = {
        agents: "workflowPrimaryPreviewAgents",
        skill: "workflowPrimaryPreviewSkill",
        patch: "workflowPrimaryPreviewPatch",
        user: "workflowPrimaryPreviewUser",
      };
      return t(keys[target] || keys.user);
    }

    function renderWorkflowNextAction() {
      const copy = document.getElementById("workflowNextActionCopy");
      const primary = document.getElementById("workflowPrimaryAction");
      const secondary = document.getElementById("workflowSecondaryAction");
      if (!copy || !primary || !secondary) {
        return;
      }
      const steps = workflowReadinessSteps();
      const previewLoaded = steps.find((step) => step.stage === "preview").done;
      if (!selectedCandidate) {
        copy.textContent = t("workflowNextSelectCandidate");
        primary.textContent = t("workflowPrimarySelectCandidate");
        secondary.textContent = t("workflowSecondaryRefreshCandidates");
        primary.dataset.workflowAction = "select";
        secondary.dataset.workflowAction = "refresh";
        return;
      }
      if (selectedAnalysisLoading || !selectedAnalysisPayload) {
        copy.textContent = t("workflowNextLoadAnalysis");
        primary.textContent = t("workflowPrimarySelectCandidate");
        secondary.textContent = t("workflowSecondaryRefreshCandidates");
        primary.dataset.workflowAction = "noop";
        secondary.dataset.workflowAction = "refresh";
        return;
      }
      if (!previewLoaded) {
        const target = proposalTargetType();
        copy.textContent = t("workflowNextPreviewDiff");
        primary.textContent = workflowPrimaryPreviewLabel(target);
        secondary.textContent = t("workflowSecondaryCopyRewrite");
        primary.dataset.workflowAction = `preview:${target}`;
        secondary.dataset.workflowAction = "copy";
        return;
      }
      copy.textContent = t("workflowNextManualApproval");
      primary.textContent = t("workflowPrimaryApprovalDock");
      secondary.textContent = t("workflowSecondarySaveReview");
      primary.dataset.workflowAction = "approval";
      secondary.dataset.workflowAction = "review";
    }

    function workflowContextNextText() {
      if (!selectedCandidate) {
        return t("workflowNextSelectCandidate");
      }
      const steps = workflowReadinessSteps();
      const previewLoaded = steps.find((step) => step.stage === "preview").done;
      if (selectedAnalysisLoading || !selectedAnalysisPayload) {
        return t("workflowNextLoadAnalysis");
      }
      return previewLoaded ? t("workflowNextManualApproval") : t("workflowNextPreviewDiff");
    }

    function renderWorkflowContextPanel() {
      const panel = document.getElementById("workflowContextPanel");
      if (!panel) {
        return;
      }
      const source = document.getElementById("workflowSourceContext");
      const empty = document.getElementById("workflowContextEmpty");
      const content = document.getElementById("workflowContextContent");
      const badge = document.getElementById("workflowContextBadge");
      if (source) {
        source.hidden = !(workflowSourceContext && workflowSourceContext.type === "skills");
      }
      if (!selectedCandidate) {
        if (empty) empty.hidden = false;
        if (content) content.hidden = true;
        if (badge) {
          badge.textContent = t("noneSelected");
          badge.className = "tag status";
        }
        return;
      }
      if (empty) empty.hidden = true;
      if (content) content.hidden = false;
      if (badge) {
        badge.textContent = selectedCandidate.status || t("noneSelected");
        badge.className = `tag ${selectedCandidate.status === "blocked" ? "review" : "status"}`;
      }
      setText("workflowContextCandidateTitle", selectedCandidate.title || selectedCandidate.text || "-");
      setText("workflowContextType", formatType(selectedCandidate.type));
      const type = document.getElementById("workflowContextType");
      if (type) {
        type.className = `tag ${selectedCandidate.type || "status"}`;
      }
      const priorityLabel = candidatePriorityLabel(selectedCandidate);
      setText("workflowContextPriority", `${priorityLabel} · ${candidatePriorityScore(selectedCandidate)}`);
      setText("workflowContextStatus", selectedCandidate.status || "-");
      setText("workflowContextSources", t("sourcesCount", {count: selectedCandidate.source_count || 0}));
      setText("workflowContextDestination", selectedCandidate.destination || "-");
      setText("workflowContextNextAction", workflowContextNextText());
    }

    function renderWorkflowReadiness() {
      const list = document.getElementById("workflowReadinessList");
      const summary = document.getElementById("approvalReadiness");
      const rail = document.getElementById("workflowStageRail");
      if (!list || !summary || !rail) {
        return;
      }
      const steps = workflowReadinessSteps();
      const ready = steps.every((step) => step.done);
      summary.textContent = ready ? t("approvalReady") : t("approvalBlocked");
      summary.className = `task-copy ${ready ? "approvalReady" : "approvalBlocked"}`;
      list.innerHTML = "";
      for (const step of steps) {
        const item = document.createElement("li");
        item.className = step.done ? "readiness-done" : "readiness-pending";
        item.textContent = `${step.done ? "OK" : "--"} ${t(step.key)}`;
        list.appendChild(item);
      }
      const completedStages = new Set(steps.filter((step) => step.done).map((step) => step.stage));
      const firstOpen = steps.find((step) => !step.done);
      rail.querySelectorAll("[data-workflow-stage]").forEach((stage) => {
        const name = stage.dataset.workflowStage;
        const done = completedStages.has(name);
        const current = firstOpen ? name === firstOpen.stage : name === "approval";
        stage.classList.toggle("workflow-stage-done", done);
        stage.classList.toggle("workflow-stage-current", current);
      });
      renderWorkflowNextAction();
      renderWorkflowContextPanel();
    }

    function setDrawerTab(tab) {
      document.querySelectorAll("[data-rp-tab]").forEach((button) => {
        const active = button.dataset.rpTab === tab;
        button.classList.toggle("active", active);
        button.setAttribute("aria-selected", String(active));
      });
      document.querySelectorAll("[data-rp-content]").forEach((content) => {
        content.classList.toggle("active", content.dataset.rpContent === tab);
      });
    }

    function openCandidateReviewDrawer(tab = "detail") {
      const drawer = document.getElementById("candidateReviewDrawer");
      if (!drawer) {
        return;
      }
      drawer.hidden = false;
      document.body.classList.add("drawer-open");
      setDrawerTab(tab);
    }

    function closeCandidateReviewDrawer() {
      const drawer = document.getElementById("candidateReviewDrawer");
      if (!drawer) {
        return;
      }
      drawer.hidden = true;
      document.body.classList.remove("drawer-open");
    }

    function openMergeSuggestionsDrawer() {
      const drawer = document.getElementById("mergeSuggestionsDrawer");
      if (!drawer) {
        return;
      }
      drawer.hidden = false;
      document.body.classList.add("drawer-open");
      refreshMergeSuggestions().catch((error) => showToast(error.message || t("toastLoadFailed"), "error"));
    }

    function closeMergeSuggestionsDrawer() {
      const drawer = document.getElementById("mergeSuggestionsDrawer");
      if (!drawer) {
        return;
      }
      drawer.hidden = true;
      document.body.classList.remove("drawer-open");
    }

    function shouldSkipMergeModuleOpen(target) {
      return Boolean(target.closest("button, a, input, select, textarea, [data-skip-module-open]"));
    }

    function handleSkillCandidateAction(button) {
      const candidateId = button.dataset.candidateId;
      const candidate = allCandidates.find((item) => String(item.id) === String(candidateId));
      if (!candidate) {
        showToast(t("selectCandidateFirst"), "warn");
        return;
      }
      setView("workflow");
      selectCandidate(candidate.id, {sourceContext: {type: "skills"}, openDrawer: true});
      if (button.dataset.skillCandidateAction === "view") {
        openCandidateReviewDrawer("detail");
        return;
      }
      const target = candidate.type === "skill_patch" ? "patch" : "skill";
      if (button.dataset.skillCandidateAction === "preview") {
        previewPromotion(target)
          .then(() => openCandidateReviewDrawer("approval"))
          .catch((error) => showToast(error.message || t("toastLoadFailed"), "error"));
        return;
      }
      const action = target === "patch"
        ? () => api(`/api/candidates/${window.selectedCandidateId}/promote-patch`, {method: "POST"})
        : () => api(`/api/candidates/${window.selectedCandidateId}/promote-skill`, {method: "POST"});
      const successKey = target === "patch" ? "toastPromotedPatch" : "toastPromotedSkill";
      const confirmKey = target === "patch" ? "confirmPromotePatch" : "confirmPromoteSkill";
      runAction(action, successKey, {needsSelection: true, confirmKey, previewTarget: target})
        .catch((error) => showToast(error.message || t("toastLoadFailed"), "error"));
    }

    function renderMergeSuggestions() {
      renderMergeSuggestionsList(document.getElementById("mergeSuggestionsList"), true);
      const countEl = document.getElementById("mergeInlineCount");
      if (countEl) {
        countEl.textContent = String(mergeSuggestions.length);
      }
    }

    function renderMergeSuggestionsList(list, showEmptyRow) {
      if (!list) {
        return;
      }
      list.innerHTML = "";
      if (!mergeSuggestions.length) {
        if (showEmptyRow) {
          const item = document.createElement("li");
          item.textContent = t("emptyMergeSuggestions");
          list.appendChild(item);
        }
        return;
      }
      for (const suggestion of mergeSuggestions.slice(0, 8)) {
        const item = document.createElement("div");
        item.className = "merge-inline-item";
        const text = document.createElement("span");
        text.className = "merge-text";
        text.textContent = `${suggestion.reason || ""} #${(suggestion.candidate_ids || []).join(", #")}`;
        const action = document.createElement("div");
        action.className = "merge-action";
        const button = document.createElement("button");
        button.type = "button";
        button.className = "secondary";
        button.textContent = t("applyMerge");
        button.addEventListener("click", () => applyMergeSuggestion(suggestion.id));
        action.appendChild(button);
        item.append(text, action);
        list.appendChild(item);
      }
    }

    function renderReviewProgress() {
      const fill = document.getElementById("reviewProgressFill");
      const label = document.getElementById("reviewProgressLabel");
      if (!fill || !label) {
        return;
      }
      const total = allCandidates.length;
      const reviewed = allCandidates.filter((c) =>
        ["reviewed", "promoted", "rejected", "archived", "merged"].includes(String(c.status || "").toLowerCase())
      ).length;
      const pending = total - reviewed;
      const pct = total > 0 ? Math.round((reviewed / total) * 100) : 0;
      fill.style.width = `${pct}%`;
      label.textContent = total > 0
        ? t("reviewProgressLabel", {reviewed, total})
        : t("reviewProgressIdle");
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

    function skillCandidates() {
      return allCandidates
        .filter((item) => ["skill", "skill_patch"].includes(String(item.type || "").toLowerCase()))
        .filter((item) => ["review", "blocked"].includes(String(item.status || "").toLowerCase()))
        .sort((a, b) => candidatePriorityScore(b) - candidatePriorityScore(a))
        .slice(0, 12);
    }

    function renderSkillCandidates() {
      const body = document.getElementById("skillCandidateRows");
      const count = document.getElementById("skillCandidatePanelCount");
      if (!body) {
        return;
      }
      const items = skillCandidates();
      if (count) {
        count.textContent = String(items.length);
      }
      body.innerHTML = "";
      if (!items.length) {
        const row = document.createElement("tr");
        const empty = cell("empty-row");
        empty.colSpan = 4;
        empty.textContent = t("emptySkillCandidates");
        row.appendChild(empty);
        body.appendChild(row);
        return;
      }
      for (const item of items) {
        const row = document.createElement("tr");
        row.dataset.skillCandidateId = item.id;

        const titleCell = cell();
        const title = document.createElement("strong");
        title.className = "candidate-title";
        title.textContent = item.title || item.text || "-";
        const note = document.createElement("div");
        note.className = "candidate-row-note";
        note.textContent = candidatePriorityReasons(item).join(" / ");
        titleCell.append(title, note);
        row.appendChild(titleCell);

        const typeCell = cell();
        typeCell.appendChild(tag(formatType(item.type), item.type));
        row.appendChild(typeCell);

        const targetCell = cell();
        targetCell.textContent = item.proposal_target_type || item.destination || "-";
        row.appendChild(targetCell);

        const actionCell = cell("skill-candidate-actions");
        const view = document.createElement("button");
        view.type = "button";
        view.className = "secondary operation-quiet";
        view.dataset.skillCandidateAction = "view";
        view.dataset.candidateId = item.id;
        view.textContent = t("skillActionView");
        const preview = document.createElement("button");
        preview.type = "button";
        preview.className = "secondary operation-quiet";
        preview.dataset.skillCandidateAction = "preview";
        preview.dataset.candidateId = item.id;
        preview.textContent = t("skillActionPreview");
        const apply = document.createElement("button");
        apply.type = "button";
        apply.className = "operation-danger";
        apply.dataset.skillCandidateAction = "apply";
        apply.dataset.candidateId = item.id;
        apply.textContent = item.type === "skill_patch" ? t("skillActionApply") : t("skillActionPromote");
        actionCell.append(view, preview, apply);
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

    const navViewMap = {
      dashboard: {view: "dashboard"},
      home: {view: "dashboard", nav: "dashboard"},
      workflow: {view: "workflow", workflowModule: "queue", nav: "workflow"},
      candidates: {view: "workflow", workflowModule: "queue", nav: "workflow"},
      evidence: {view: "workflow", workflowModule: "queue", nav: "workflow", drawerTab: "evidence"},
      approval: {view: "workflow", workflowModule: "queue", nav: "workflow", drawerTab: "approval"},
      promotion: {view: "workflow", workflowModule: "queue", nav: "workflow", drawerTab: "approval"},
      data: {view: "operations", opsModule: "data", nav: "data"},
      operations: {view: "operations", opsModule: "data", nav: "data"},
      automation: {view: "operations", opsModule: "automation", nav: "automation"},
      schedule: {view: "operations", opsModule: "automation", nav: "automation"},
      skills: {view: "operations", opsModule: "skills", nav: "skills"},
      recall: {view: "operations", opsModule: "recall", nav: "recall"},
      history: {view: "operations", opsModule: "history", nav: "history"},
      runs: {view: "operations", opsModule: "history", nav: "history"},
      audit: {view: "operations", opsModule: "history", nav: "history"},
      promotions: {view: "operations", opsModule: "history", nav: "history"},
      reviews: {view: "operations", opsModule: "history", nav: "history"},
      doctor: {view: "operations", opsModule: "doctor", nav: "doctor"},
    };

    function setView(view) {
      const target = navViewMap[view] || navViewMap.dashboard;
      currentView = target.view;
      const activeNav = target.nav || target.view;
      const shell = document.getElementById("appShell");
      if (shell) {
        shell.dataset.currentNav = activeNav;
      }
      document.querySelectorAll("[data-nav]").forEach((button) => {
        const active = button.dataset.nav === activeNav;
        button.classList.toggle("active", active);
        button.setAttribute("aria-current", active ? "page" : "false");
      });
      document.querySelectorAll("[data-view]").forEach((panel) => {
        panel.classList.toggle("active", panel.dataset.view === target.view);
      });
      if (target.view === "workflow") {
        switchWorkflowModule(target.workflowModule || "queue");
        if (target.drawerTab) {
          openCandidateReviewDrawer(target.drawerTab);
        }
      }
      if (target.view === "operations") {
        switchOpsTab(target.opsModule || "data");
        refreshRuns().catch((error) => showToast(error.message || t("toastLoadFailed"), "error"));
        refreshDoctor().catch((error) => showToast(error.message || t("toastLoadFailed"), "error"));
        refreshAudit().catch((error) => showToast(error.message || t("toastLoadFailed"), "error"));
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

    function moduleForOperationsAnchor(id) {
      const target = document.getElementById(id);
      const section = target && (target.matches("[data-ops-section]") ? target : target.closest("[data-ops-section]"));
      if (!section) {
        return "data";
      }
      return (section.dataset.opsSection || "data").split(",").map((item) => item.trim())[0] || "data";
    }

    function scrollToOperationsAnchor(id) {
      setView(moduleForOperationsAnchor(id));
    }

    function recoveryQueueItem(kind, title, detail, actionLabel, targetId) {
      const item = document.createElement("button");
      item.type = "button";
      item.className = "recovery-queue-item";
      item.addEventListener("click", () => scrollToOperationsAnchor(targetId));
      const kindLabel = document.createElement("span");
      kindLabel.className = "tag review";
      kindLabel.textContent = kind;
      const heading = document.createElement("strong");
      heading.textContent = title;
      const copy = document.createElement("small");
      copy.textContent = detail;
      const action = document.createElement("em");
      action.textContent = actionLabel;
      item.append(kindLabel, heading, copy, action);
      return item;
    }

    function renderOperationsRecoveryQueue() {
      const list = document.getElementById("recoveryQueueList");
      const count = document.getElementById("recoveryQueueCount");
      if (!list || !count) {
        return;
      }
      list.innerHTML = "";
      const items = [];
      for (const run of latestRuns.filter((item) => item.status === "failed").slice(0, 3)) {
        items.push(recoveryQueueItem(
          t("recoveryQueueRunFailure"),
          `${run.kind || "-"} #${run.id}`,
          run.detail || formatDateTime(run.finished_at || run.started_at),
          t("recoveryQueueOpenRuns"),
          "runWorkspace",
        ));
      }
      for (const audit of auditItems.slice(0, 2)) {
        items.push(recoveryQueueItem(
          t("recoveryQueueAuditSignal"),
          audit.action || "-",
          [audit.target, audit.detail, formatDateTime(audit.created_at)].filter(Boolean).join(" · "),
          t("recoveryQueueOpenAudit"),
          "auditRecoveryPanel",
        ));
      }
      if (promotionItems.length) {
        const latest = promotionItems[0];
        items.push(recoveryQueueItem(
          t("recoveryQueueRollbackSignal"),
          latest.target_type || "-",
          latest.target_path || latest.candidate_title || "-",
          t("recoveryQueueOpenPromotions"),
          "promotionHistoryPanel",
        ));
      }
      count.textContent = String(items.length);
      if (!items.length) {
        const empty = document.createElement("div");
        empty.className = "empty-row";
        empty.textContent = t("recoveryQueueEmpty");
        list.appendChild(empty);
        return;
      }
      for (const item of items) {
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

    function renderDiff(text) {
      const lines = String(text || "").split("\n");
      const result = [];
      for (const line of lines) {
        const cls = line.startsWith("+") ? "added" : line.startsWith("-") ? "removed" : line.startsWith("@@") || line.startsWith("---") || line.startsWith("+++") ? "header" : "context";
        result.push(`<div class="diff-line ${cls}">${escapeHtml(line)}</div>`);
      }
      return result.join("");
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
      renderDashboardNextAction();
      renderOperationsRecoveryQueue();
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
      renderOperationsRecoveryQueue();
    }

    async function refreshHistory() {
      const payload = await api("/api/history");
      promotionItems = payload.promotions || [];
      reviewItems = payload.reviews || [];
      renderPromotions();
      renderReviews();
      renderHomeTasks();
      renderOperationsRecoveryQueue();
    }

    async function refreshSetupStatus() {
      setupStatus = await api("/api/setup/status");
      renderSetupWizard();
      renderDashboardNextAction();
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
      if (!(await confirmAction("confirmApplyMerge"))) {
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

    async function runPreviewOnly(target) {
      setBusy(true);
      try {
        const preview = await previewPromotion(target);
        if (preview) {
          setView("approval");
          showToast(t("toastPreviewLoaded"));
        }
      } catch (error) {
        console.error(error);
        showToast(error.message || t("toastLoadFailed"), "error");
      } finally {
        setBusy(false);
      }
    }

    async function runScanOnce() {
      await runTrackedJob("/api/scan", "confirmScanOnce", "toastScanStarted", "toastScanned");
    }

    async function runScanAndAnalyze() {
      await runTrackedJob("/api/scan-and-analyze", "confirmScanOnce", "toastScanAnalyzeStarted", "toastScanAnalyzedComplete");
      setView("workflow");
    }

    async function runBatchAnalyze() {
      setBusy(true);
      try {
        const result = await api("/api/analyze/batch", {method: "POST"});
        await refresh(false);
        showToast(`Analysis completed: ${result.analyzed || 0} candidates analyzed.`, "ok");
      } catch (error) {
        console.error(error);
        showToast(error.message || t("toastLoadFailed"), "error");
      } finally {
        setBusy(false);
      }
    }

    function topReviewCandidate() {
      return sortedCandidates(
        allCandidates.filter((item) => ["review", "blocked"].includes(String(item.status || "").toLowerCase()))
      )[0] || sortedCandidates(visibleCandidates())[0] || allCandidates[0] || null;
    }

    async function runWorkflowPrimaryAction() {
      const action = document.getElementById("workflowPrimaryAction").dataset.workflowAction || "select";
      if (action === "select") {
        const candidate = topReviewCandidate();
        if (candidate) {
          selectCandidate(candidate.id);
        } else {
          showToast(t("emptyCandidates"), "warn");
        }
        return;
      }
      if (action.startsWith("preview:")) {
        await runPreviewOnly(action.split(":")[1] || "user");
        openCandidateReviewDrawer("approval");
        return;
      }
      if (action === "approval") {
        openCandidateReviewDrawer("approval");
        return;
      }
      showToast(t("analysisLoading"), "warn");
    }

    async function runWorkflowSecondaryAction() {
      const action = document.getElementById("workflowSecondaryAction").dataset.workflowAction || "refresh";
      if (action === "copy") {
        if (!selectedCandidate) {
          showToast(t("selectCandidateFirst"), "warn");
          return;
        }
        await copyText(selectedCandidate.rewrite_suggestion || selectedCandidate.text || "");
        showToast(t("toastCopied"));
      } else if (action === "review") {
        document.getElementById("saveReview").click();
      } else {
        await refresh(true);
      }
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

    function candidatePriorityScore(item) {
      let score = 0;
      const safety = String(item.safety || "").toLowerCase();
      const status = String(item.status || "").toLowerCase();
      const type = String(item.type || "").toLowerCase();
      const sourceCount = Number(item.source_count || 0);
      const confidence = Number(item.confidence || 0);
      if (status === "review") {
        score += 30;
      }
      if (safety === "blocked" || safety === "conflict_review" || safety === "unsafe") {
        score += 45;
      } else if (sourceCount >= 2 && confidence >= 0.7) {
        score += 28;
      }
      if (type === "skill_patch") {
        score += 18;
      } else if (type === "skill") {
        score += 12;
      }
      if (item.proposal_target_type) {
        score += 8;
      }
      return score;
    }

    function candidatePriorityReasons(item) {
      const reasons = [];
      const safety = String(item.safety || "").toLowerCase();
      const status = String(item.status || "").toLowerCase();
      const type = String(item.type || "").toLowerCase();
      const sourceCount = Number(item.source_count || 0);
      const confidence = Number(item.confidence || 0);
      if (status === "review") {
        reasons.push(t("priorityReasonReview"));
      }
      if (safety === "blocked" || safety === "conflict_review" || safety === "unsafe") {
        reasons.push(t("priorityReasonRisk"));
      } else if (sourceCount >= 2 && confidence >= 0.7) {
        reasons.push(t("priorityReasonEvidence"));
      }
      if (type === "skill" || type === "skill_patch") {
        reasons.push(t("priorityReasonSkill"));
      }
      if (item.proposal_target_type) {
        reasons.push(t("priorityReasonProposal"));
      }
      return reasons.length ? reasons : [t("priorityReasonNormal")];
    }

    function candidatePriorityLabel(item) {
      const safety = String(item.safety || "").toLowerCase();
      const type = String(item.type || "").toLowerCase();
      const sourceCount = Number(item.source_count || 0);
      const confidence = Number(item.confidence || 0);
      if (safety === "blocked" || safety === "conflict_review" || safety === "unsafe") {
        return t("priorityHighRisk");
      }
      if (type === "skill" || type === "skill_patch") {
        return t("prioritySkillChange");
      }
      if (sourceCount >= 2 && confidence >= 0.7) {
        return t("priorityReadyReview");
      }
      return t("priorityNormal");
    }

    function sortedCandidates(items) {
      const copy = items.slice();
      if (candidateSortMode === "newest") {
        copy.sort((a, b) => new Date(b.created_at || 0) - new Date(a.created_at || 0));
      } else if (candidateSortMode === "oldest") {
        copy.sort((a, b) => new Date(a.created_at || 0) - new Date(b.created_at || 0));
      } else if (candidateSortMode === "confidence") {
        copy.sort((a, b) => Number(b.confidence || 0) - Number(a.confidence || 0));
      } else {
        copy.sort((a, b) => candidatePriorityScore(b) - candidatePriorityScore(a) || new Date(b.updated_at || 0) - new Date(a.updated_at || 0));
      }
      return copy;
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
      document.getElementById("candidateSortMode").value = candidateSortMode;
    }

    function renderCandidates() {
      const body = document.getElementById("candidateRows");
      const items = sortedCandidates(visibleCandidates());
      const {pageItems, totalPages} = pagedCandidates(items);
      renderPagination(items.length, totalPages);
      body.innerHTML = "";
      if (!items.length) {
        renderEmptyRow(body, 6, "emptyCandidates");
        return;
      }

      for (const item of pageItems) {
        const row = document.createElement("tr");
        row.className = "candidate-row";
        row.dataset.id = item.id;
        row.tabIndex = 0;
        row.setAttribute("aria-selected", String(String(item.id) === String(window.selectedCandidateId)));
        row.classList.toggle("selected-row", String(item.id) === String(window.selectedCandidateId));
        row.addEventListener("click", () => selectCandidate(item.id));
        row.addEventListener("keydown", (event) => {
          if (event.key === "Enter" || event.key === " ") {
            event.preventDefault();
            selectCandidate(item.id);
          }
        });

        const priorityCell = cell("candidate-col-priority");
        priorityCell.appendChild(tag(candidatePriorityLabel(item), "priority"));
        const priorityScore = document.createElement("div");
        priorityScore.className = "candidate-row-note";
        priorityScore.textContent = `${candidatePriorityScore(item)}`;
        priorityCell.appendChild(priorityScore);
        row.appendChild(priorityCell);

        const typeCell = cell("candidate-col-type");
        typeCell.appendChild(tag(formatType(item.type), item.type));
        row.appendChild(typeCell);

        const titleCell = cell("candidate-col-title");
        const title = document.createElement("div");
        title.className = "candidate-title";
        title.textContent = item.title || item.text || "-";
        const snippet = document.createElement("div");
        snippet.className = "candidate-snippet";
        snippet.textContent = item.text || "";
        const reasons = document.createElement("div");
        reasons.className = "candidate-row-note";
        reasons.textContent = candidatePriorityReasons(item).join(" / ");
        titleCell.append(title, snippet, reasons);
        row.appendChild(titleCell);

        const riskCell = cell("candidate-col-risk");
        riskCell.appendChild(tag(item.safety || "-", String(item.safety || "").toLowerCase().includes("unsafe") ? "review" : "status"));
        row.appendChild(riskCell);

        const statusCell = cell("candidate-col-status");
        statusCell.appendChild(tag(item.status || "-", item.status === "review" ? "review" : "status"));
        const destination = document.createElement("div");
        destination.className = "candidate-row-note";
        destination.textContent = item.destination || "-";
        statusCell.appendChild(destination);
        row.appendChild(statusCell);

        const timeCell = cell("candidate-col-time");
        timeCell.textContent = formatDateTime(item.updated_at || item.created_at);
        row.appendChild(timeCell);

        body.appendChild(row);
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
      selectedAnalysisPayload = null;
      selectedAnalysisLoading = false;
    }

    function selectCandidate(id, options = {}) {
      if (options.sourceContext) {
        workflowSourceContext = options.sourceContext;
      } else if (!options.keepSourceContext) {
        workflowSourceContext = null;
      }
      window.selectedCandidateId = id;
      selectedCandidate = allCandidates.find((item) => String(item.id) === String(id)) || null;
      selectedAnalysisPayload = null;
      selectedAnalysisLoading = false;
      latestPromotionPreview = null;
      renderCandidates();
      renderSelected();
      renderCandidateActionPanel();
      renderPromotionPreview(null);
      renderWorkflowContextPanel();
      if (selectedCandidate) {
        if (options.openDrawer) {
          openCandidateReviewDrawer(options.drawerTab || "detail");
        }
        loadCandidateAnalysis(id);
      }
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
        const evidenceBadge = document.getElementById("selectedEvidenceBadge");
        if (evidenceBadge) {
          evidenceBadge.textContent = t("noneSelected");
          evidenceBadge.className = "tag status";
        }
        const drawerSourceFiles = document.getElementById("drawerSourceFiles");
        if (drawerSourceFiles) {
          drawerSourceFiles.innerHTML = "";
          const item = document.createElement("li");
          item.textContent = "-";
          drawerSourceFiles.appendChild(item);
        }
        setText("drawerRiskCopy", t("selectCandidateHint"));
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
      const drawerSourceFiles = document.getElementById("drawerSourceFiles");
      if (drawerSourceFiles) {
        drawerSourceFiles.innerHTML = "";
      }
      if (!files.length) {
        const item = document.createElement("li");
        item.textContent = "-";
        sourceFiles.appendChild(item);
        if (drawerSourceFiles) {
          drawerSourceFiles.appendChild(item.cloneNode(true));
        }
      } else {
        for (const file of files) {
          const item = document.createElement("li");
          item.textContent = file;
          sourceFiles.appendChild(item);
          if (drawerSourceFiles) {
            drawerSourceFiles.appendChild(item.cloneNode(true));
          }
        }
      }
      const evidenceBadge = document.getElementById("selectedEvidenceBadge");
      if (evidenceBadge) {
        evidenceBadge.textContent = t("sourcesCount", {count: selectedCandidate.source_count || 0});
        evidenceBadge.className = "tag status";
      }
      setText("drawerRiskCopy", candidateRisk(selectedCandidate).text);
      const priorityReasons = document.getElementById("selectedPriorityReasons");
      priorityReasons.innerHTML = "";
      for (const reason of candidatePriorityReasons(selectedCandidate)) {
        const item = document.createElement("li");
        item.textContent = reason;
        priorityReasons.appendChild(item);
      }
    }

    async function refresh(showMessage = false) {
      const payload = await api("/api/summary");
      renderSummary(payload.summary);
      allCandidates = payload.candidates || [];
      hydrateSelection();
      latestPromotionPreview = null;
      renderCandidates();
      renderSelected();
      renderCandidateActionPanel();
      renderPromotionPreview(null);
      renderReviewProgress();
      renderSkillCandidates();
      renderWorkflowContextPanel();
      if (selectedCandidate) {
        await loadCandidateAnalysis(selectedCandidate.id);
      }
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
      if (!(await confirmAction(options.confirmKey, confirmExtra))) {
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

    async function pollRun(runId, successKey = "toastRebuilt") {
      const status = await api(`/api/runs/${runId}`);
      updateProgress(status);
      if (status.status === "running") {
        activeRunTimer = setTimeout(() => pollRun(runId, successKey).catch((error) => {
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
        showToast(t(successKey));
      } else {
        showToast(`${t("rebuildFailed")} ${status.detail || ""}`, "error");
      }
    }

    async function runTrackedJob(path, confirmKey, startedKey, successKey) {
      if (!(await confirmAction(confirmKey))) {
        return;
      }
      clearTimeout(activeRunTimer);
      setBusy(true);
      try {
        const started = await api(path, {method: "POST"});
        activeRunId = started.run_id;
        updateProgress({status: "running", processed: 0, skipped: 0, total: 0, latest_step: null});
        showToast(t(startedKey));
        await pollRun(activeRunId, successKey);
      } catch (error) {
        console.error(error);
        showToast(error.message || t("toastLoadFailed"), "error");
        setBusy(false);
      }
    }

    async function runRebuild() {
      await runTrackedJob("/api/rebuild", "confirmRebuildDatabase", "toastRebuildStarted", "toastRebuilt");
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

    mountOperationsSections();
    bindConfirmModal();

    document.querySelectorAll("#languageToggle button").forEach((button) => {
      button.addEventListener("click", () => {
        currentLanguage = button.dataset.lang;
        localStorage.setItem("codexSilLanguage", currentLanguage);
        applyLanguage();
      });
    });

    document.querySelectorAll("#themeToggle button").forEach((button) => {
      button.addEventListener("click", () => {
        currentTheme = button.dataset.theme;
        localStorage.setItem("codexSilTheme", currentTheme);
        applyTheme();
      });
    });

    document.querySelectorAll("[data-nav]").forEach((button) => {
      button.addEventListener("click", () => {
        workflowSourceContext = null;
        closeCandidateReviewDrawer();
        closeMergeSuggestionsDrawer();
        renderWorkflowContextPanel();
        setView(button.dataset.nav);
      });
    });

    document.querySelectorAll("[data-ops-tab]").forEach((button) => {
      button.addEventListener("click", () => {
        workflowSourceContext = null;
        renderWorkflowContextPanel();
        setView(button.dataset.opsTab);
      });
    });

    function switchWorkflowModule(moduleName) {
      const workspace = document.getElementById("candidateWorkspace");
      if (!workspace) {
        return;
      }
      workspace.dataset.workflowModule = "queue";
      const panel = document.getElementById("workflowReviewQueue");
      if (panel) {
        panel.setAttribute("tabindex", "-1");
      }
    }

    function switchOpsTab(tab) {
      document.querySelectorAll("[data-ops-tab]").forEach((btn) => btn.classList.toggle("active", btn.dataset.opsTab === tab));
      const viewPanel = document.querySelector(".view-panel.active[data-view='operations']");
      if (!viewPanel) return;
      viewPanel.querySelectorAll("section[data-ops-section]").forEach((sec) => {
        const groups = (sec.dataset.opsSection || "").split(",").map((s) => s.trim());
        const visible = groups.includes(tab);
        sec.style.display = visible ? "" : "none";
        sec.classList.toggle("ops-section-active", visible);
      });
    }

    // Initialize default ops tab on load
    switchOpsTab("data");

    document.querySelectorAll("[data-rp-tab]").forEach((button) => {
      button.addEventListener("click", () => {
        setDrawerTab(button.dataset.rpTab || "detail");
      });
    });

    document.getElementById("workflowPrimaryAction").addEventListener("click", () => runWorkflowPrimaryAction().catch((error) => showToast(error.message || t("toastLoadFailed"), "error")));
    document.getElementById("workflowSecondaryAction").addEventListener("click", () => runWorkflowSecondaryAction().catch((error) => showToast(error.message || t("toastLoadFailed"), "error")));
    document.getElementById("workflowContextOpenDetail").addEventListener("click", () => {
      if (!selectedCandidate) {
        showToast(t("selectCandidateFirst"), "warn");
        return;
      }
      openCandidateReviewDrawer("detail");
    });
    document.getElementById("workflowContextOpenApproval").addEventListener("click", () => {
      if (!selectedCandidate) {
        showToast(t("selectCandidateFirst"), "warn");
        return;
      }
      openCandidateReviewDrawer("approval");
    });
    document.getElementById("returnToSkillCandidates").addEventListener("click", () => {
      workflowSourceContext = null;
      closeCandidateReviewDrawer();
      closeMergeSuggestionsDrawer();
      setView("skills");
      renderWorkflowContextPanel();
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

    document.getElementById("candidateSortMode").addEventListener("change", (event) => {
      candidateSortMode = event.target.value || "priority";
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
    document.getElementById("refreshMergeSuggestions").addEventListener("click", () => regenerateMergeSuggestions().catch((error) => showToast(error.message || t("toastLoadFailed"), "error")));
    document.getElementById("refreshMergeSuggestionsInline").addEventListener("click", () => regenerateMergeSuggestions().catch((error) => showToast(error.message || t("toastLoadFailed"), "error")));
    document.getElementById("openMergeSuggestions").addEventListener("click", () => openMergeSuggestionsDrawer());
    document.getElementById("mergeSuggestionsModule").addEventListener("click", (event) => {
      if (!shouldSkipMergeModuleOpen(event.target)) {
        openMergeSuggestionsDrawer();
      }
    });
    document.getElementById("mergeSuggestionsModule").addEventListener("keydown", (event) => {
      if ((event.key === "Enter" || event.key === " ") && !shouldSkipMergeModuleOpen(event.target)) {
        event.preventDefault();
        openMergeSuggestionsDrawer();
      }
    });
    document.getElementById("closeMergeSuggestions").addEventListener("click", () => closeMergeSuggestionsDrawer());
    document.getElementById("mergeSuggestionsBackdrop").addEventListener("click", () => closeMergeSuggestionsDrawer());
    document.getElementById("closeCandidateReviewDrawer").addEventListener("click", () => closeCandidateReviewDrawer());
    document.getElementById("candidateReviewBackdrop").addEventListener("click", () => closeCandidateReviewDrawer());
    document.getElementById("scanAndAnalyzeButton").addEventListener("click", () => runScanAndAnalyze());

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

    document.addEventListener("click", (event) => {
      const button = event.target.closest("[data-skill-candidate-action]");
      if (!button) {
        return;
      }
      handleSkillCandidateAction(button);
    });

    document.getElementById("refreshButton").addEventListener("click", () => refresh(true).catch((error) => showToast(error.message, "error")));
    document.getElementById("initializeData").addEventListener("click", () => runAction(() => api("/api/init", {method: "POST"}), "toastInitialized", {confirmKey: "confirmInitializeData"}));
    document.getElementById("backupDatabase").addEventListener("click", () => runAction(() => api("/api/backup", {method: "POST"}), "toastBackupCreated", {refresh: false, confirmKey: "confirmBackupDatabase"}));
    document.getElementById("installSkills").addEventListener("click", () => runAction(() => api("/api/install/skills", {method: "POST"}), "toastSkillsInstalled", {refresh: false, confirmKey: "confirmInstallSkills"}));
    document.getElementById("installUserTemplate").addEventListener("click", () => runAction(() => api("/api/install/user-template", {method: "POST"}), "toastUserTemplateInstalled", {refresh: false, confirmKey: "confirmInstallUserTemplate"}));
    document.getElementById("scanButton").addEventListener("click", () => runScanOnce());
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
    document.getElementById("previewUserDiff").addEventListener("click", () => runPreviewOnly("user"));
    document.getElementById("previewAgentsDiff").addEventListener("click", () => runPreviewOnly("agents"));
    document.getElementById("previewSkillDiff").addEventListener("click", () => runPreviewOnly("skill"));
    document.getElementById("previewPatchDiff").addEventListener("click", () => runPreviewOnly("patch"));
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
    applyTheme();

    if (window.matchMedia) {
      window.matchMedia("(prefers-color-scheme: dark)").addEventListener("change", (e) => {
        if (!localStorage.getItem("codexSilTheme")) {
          currentTheme = e.matches ? "dark" : "light";
          applyTheme();
        }
      });
    }

    refresh(false).catch((error) => {
      console.error(error);
      showToast(`${t("toastLoadFailed")} ${error.message || ""}`, "error");
    });
