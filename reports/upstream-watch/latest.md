# Upstream OpenROAD — weekly digest 2026-11-07

- Pinned: `4155ac310149` · master: `8cd363dd1995` · 230 commits ahead (143 non-merge)
- OpenSTA submodule: `cc9027d65` → `f8e13cbf1` (22 commits)
- Window for pull requests and issues: updated since 2026-10-31

## Behaviour changes (regression goldens updated)

| Module | Commit | Title | Goldens |
|---|---|---|---|
| dft | `29432e0625` | dft: add scan optimization algorithm source files | dft_man_tcl_check.ok, dft_readme_msgs_check.ok, place_sort_sky130.ok, scandef_sky130.defok |
| dft | `4923866d03` | dft: add scan_opt regression/CI test | scan_opt_sky130.ok, scan_opt_sky130.vok |
| dft | `d7597ff53f` | dft: revert changes in tests targetting the architect | place_sort_sky130.ok |
| dft | `fb394a30d5` | dft: rever scandef tests | scandef_sky130.defok |
| grt | `baed7deb32` | grt: restart the first soft-NDR demotion from the initial routing | soft_ndr_4w_6s.guideok, soft_ndr_4w_6s.ok, soft_ndr_escalation.guideok, soft_ndr_escalation.ok |
| grt | `5f764243a3` | grt: replace the NDR overflow multiplier with NDR deficits | ndr_1w_3s.guideok, ndr_1w_3s.ok, soft_ndr_4w_6s.guideok, soft_ndr_4w_6s.ok, soft_ndr_escalation.guideok, soft_ndr_escalation.ok |
| dpl | `acabd565a7` | dpl: refresh fixed macro regression outputs | cell_on_block1.ok, cell_on_block2.ok, max_disp1.ok, obstruction2.ok |
| grt | `03a913a622` | grt: update soft NDR goldens for per-edge NDR pricing | soft_ndr_4w_6s.guideok, soft_ndr_4w_6s.ok, soft_ndr_escalation.guideok, soft_ndr_escalation.ok |
| rsz | `676677ec3c` | test: Update rebuffer delay estimate goldens | report_delay_estimator_rebuffer_fanout8.ok, report_delay_estimator_rebuffer_minimal.ok, report_delay_estimator_rebuffer_prebuffered.ok, report_delay_estimator_rebuffer_steiner.ok |
| rsz | `cda63c4d9e` | test: Refresh parallel setup repair goldens | repair_setup_parallel_eval.ok, repair_setup_parallel_eval_max_util.ok, repair_setup_parallel_eval_threads.ok |
| grt | `74d34bd075` | grt: fix stale NDR deficits and the 3D maze gate | ndr_1w_3s.ok |
| psm | `946aa96f4b` | psm: remove solution when voltage or powers are modified | gcd_no_vsrc_reuse_change_voltage.ok |
| gpl | `fdc27966a7` | gpl: refresh placement and flow reference values | ar01.defok, ar01.ok, ar02.defok, ar02.ok, cluster_place01.defok, cluster_place01.ok +56 |
| odb | `fdc27966a7` | gpl: refresh placement and flow reference values | replace_hier_mod1.ok |
| (top) | `fdc27966a7` | gpl: refresh placement and flow reference values | upf_test.ok |
| dft | `91729b3186` | dft: update test goldens after merging master | dft_man_tcl_check.ok, dft_readme_msgs_check.ok, scan_opt_sky130.vok |
| dft | `858ac2fafe` | dft: reorder scan chains safely in scan_opt | scan_opt_sky130.ok |
| dft | `fdd2cccd5f` | dft: document scan_opt and report_chain_metrics | dft_readme_msgs_check.ok |
| dft | `526621408b` | dft: add scan_opt regression tests for edges, rebalancing and reload | scan_opt_edges_sky130.defok, scan_opt_edges_sky130.ok, scan_opt_edges_sky130.vok, scan_opt_rebalance_sky130.defok, scan_opt_rebalance_sky130.ok |
| (top) | `93c73d53b7` | ord: Keep virtual clocks out of timing__fmax | report_fmax_metric_virtual_clock.ok |
| dft | `48c8a85adc` | dft: keep skipped chains intact and enforce the rebalance bit cap | scan_opt_rebalance_cap_sky130.ok, scan_opt_skip_sky130.ok |
| dft | `3929373e9a` | dft: keep chain order and membership unless scan wiring gets shorter | scan_opt_rebalance_cap_sky130.ok, scan_opt_rebalance_sky130.defok, scan_opt_rebalance_sky130.ok |
| grt | `18780f4a9b` | grt: reroute CUGR nets in slack-last, largest-first order | critical_nets_percentage_cugr.guideok, critical_nets_percentage_cugr.ok, cugr_adjustment3.guideok, cugr_adjustment3.ok, cugr_rrr_accept_stop.ok, ndr_rrr_cugr.guideok +14 |
| grt | `1d088a2605` | grt: address review on CUGR reroute order | repair_antennas_only_diodes_cugr.defok, repair_antennas_only_diodes_cugr.guideok, repair_antennas_only_diodes_cugr.ok |
| grt | `30080f582a` | grt: keep the slack-then-size order for incremental CUGR reroutes | remove_buffers2_cugr.segsok, repair_antennas_only_diodes_cugr.defok, repair_antennas_only_diodes_cugr.guideok, repair_antennas_only_diodes_cugr.ok, repair_antennas_post_drt_relief_cugr.ok, repair_antennas_post_drt_relief_ndr_cugr.ok +1 |
| gpl | `6278e896b2` | test: update multiple after gpl change at bin aspect ratio: | mt_invariance01.ok |
| gpl | `f3a75f3ecd` | gpl: update test after fixing bin grid aspect ratio | simple01-td-scan-net.ok |
| rsz | `da3318c001` | rsz: runtime optimization for fullyRebuffer | rebuffer_size_driver.ok |
| dft | `1196b31086` | dft: bind ff state variables by position in scan_replace | scan_replace_state_binding_sky130.ok |
| gpl | `863d566467` | address review feedback for cleaner resetting | convergence01.ok, simple01-td-net-percentage.defok, simple01-td-net-percentage.ok, simple01-td-repair.defok, simple01-td-repair.ok, simple01-td-restart.defok +11 |
| odb | `d8707ee6a2` | test: update after dpl change on overflow updating | replace_hier_mod1.ok |
| dft | `9a6dd21f10` | dft: require matching clock, clear and preset in scan_replace | scan_replace_clock_mismatch_sky130.ok |
| dft | `5b004aab46` | dft: require matching next_state for scan_replace state binding | scan_replace_inverted_data_sky130.ok |
| rsz | `5901841087` | rsz: never swap pins on a cell with an opaque or constant output | swap_pins_constant_output.ok |

## Commits by module (functions from the diff hunk headers)

### dft (41)
- `b31e7cc1ff` dft: add scan pin location to scan cell class — OneBitScanCell::isPlaced, class OneBitScanCell : public ScanCell, class ScanCell
- `29432e0625` dft: add scan optimization algorithm source files — Dft::scanArchitect, ScanCellMock::isPlaced, add_executable, class ScanCellMock : public ScanCell, endif, set, target_link_libraries, tcl_wrap_cc
- `f357f5dcab` dft: implement clustering algorithm for scan chain optimization — Dft::scanArchitect, Dft::scanOpt, OptimizeScanWirelength, TEST, class Dft, proc report_dft_config, report_dft_config, tcl_wrap_cc
- `d47a94535a` dft: refactor executeDftPlan to support scan_opt re-stitching — Dft::executeDftPlan, Dft::scanOpt, Dft::scanReplace, OptimizeScanWirelength, ThreeOptScanChain, add_executable, class Dft, collectChainOrigins, proc report_dft_config, report_dft_config, target_link_libraries
- `6e984a2e77` dft: refactor architect reordering step — ScanArchitectHeuristic::architect, namespace, package
- `66d7490b2a` dft: remove optimizer vertical weight — OptimizeScanWirelength, ThreeOptScanChain, TwoOptScanChain, WeightedDist, struct CandidateEdges
- `18332c1d08` dft: remove optimizer vertical weight tests — TEST
- `4923866d03` dft: add scan_opt regression/CI test — TEST, filegroup, or_integration_tests
- `d7597ff53f` dft: revert changes in tests targetting the architect
- `fb394a30d5` dft: rever scandef tests
- `3cf9dd31ac` Update src/dft/src/optimizer/Opt.cpp — TwoOptScanChain
- `10c5d639ed` Update src/dft/src/optimizer/Opt.cpp — ThreeOptScanChain
- `75b822433c` Update src/dft/src/optimizer/Opt.cpp — ThreeOptScanChain
- `5c2d13870f` dft: fix deque end() dereference in ScanStitch::Stitch — ScanStitch::Stitch
- `d406e4eba6` dft: skip empty scan chains in ScanStitch::Stitch — ScanStitch::Stitch
- `f9edd15582` dft: look up liberty scan pins through dbNetwork in OneBitScanCell — iTermLocation
- `91729b3186` dft: update test goldens after merging master — place_sort
- `4165da4742` dft: apply clang-format to the scan_opt sources — Dft::reportChainMetrics, Dft::scanOpt, KMeansClusters, TEST, ThreeOptScanChain, TwoOptScanChain, class UnplacedScanCellMock : public ScanCell, computeHPWL, iTermLocation, namespace dft, runArchitect, struct CandidateEdges
- `3a22a67dc2` dft: store scan chains in odb from scan-in to scan-out — Dft::scanOpt, Dft::writeToOdb
- `2cf51600b8` dft: add ScanPin::getLocation() — ScanPin::getValue, class ScanPin
- `5e58f060ed` dft: let the scan optimizer start and end at given points — OptimizeScanWirelength, TEST, ThreeOptScanChain, TwoOptScanChain, struct CandidateEdges
- `858ac2fafe` dft: reorder scan chains safely in scan_opt — OdbScanCellAdapter::OdbScanCellAdapter, RestitchChain, class Dft, class OdbScanCellAdapter : public ScanCell, collectChainOrigins, namespace dft, proc report_dft_config, report_dft_config
- `6c2e4f89cf` dft: report scan chain wire length metrics from scan_opt — Dft::scanOpt
- `ce3f49253e` dft: keep rebalanced scan chains within the longest chain's bits — rebalanceChains
- `fdd2cccd5f` dft: document scan_opt and report_chain_metrics
- `1023801df4` dft: apply tclfmt to scan_opt_sky130.tcl — proc place_inst
- `526621408b` dft: add scan_opt regression tests for edges, rebalancing and reload — filegroup
- `110da0ecf3` dft: apply buildifier to the scan_opt BUILD files
- `92848eae3e` dft: give each cell its own cluster when k-means has n <= k — KMeansClusters, TEST, namespace dft
- `48c8a85adc` dft: keep skipped chains intact and enforce the rebalance bit cap — filegroup, proc scan_chain_cells, rebalanceChains, reorderChain, rewriteScanList
- `3929373e9a` dft: keep chain order and membership unless scan wiring gets shorter — Dft::scanOpt, chainLength, rebalanceChains, reorderChain, rewriteScanList, struct OptChain
- `6bbb11e8c9` dft: share the pin-location helper and tidy scan tests — GetClock, IsScanCell, NearestNeighborReorder, OdbScanCellAdapter::isPlaced, OneBitScanCell::isPlaced, TEST, runArchitect
- `e0557f3152` dft: apply const qualifiers in the scan_opt code — Dft::scanOpt, KMeansClusters, NearestNeighborReorder, OptimizeScanWirelength, TEST, ThreeOptScanChain, TwoOptScanChain, class Dft, collectChainOrigins, namespace dft, rebalanceChains, reorderChain …
- `7a1aa34017` dft: fix stale scan_opt comments and use American spelling — Dist, NearestNeighborReorder, OptimizeScanWirelength, ThreeOptScanChain, TwoOptScanChain, class OdbScanCellAdapter : public ScanCell, class ScanCell, namespace, namespace dft, struct CandidateEdges
- `1196b31086` dft: bind ff state variables by position in scan_replace — FindEquivalentPortInScanCell, IsScanEquivalent, RelativeDriveResistanceDiff
- `7d2eeae0e2` dft: check only scan cell ports in IsBoundScanStatePort — BindStatePorts, FindEquivalentPortInScanCell, FuncEquiv
- `9a6dd21f10` dft: require matching clock, clear and preset in scan_replace — FuncEquiv, namespace
- `5b004aab46` dft: require matching next_state for scan_replace state binding — BindStatePorts, FuncEquiv
- `3fa3934228` dft: keep bound state variables out of scan_replace port matching — BindStatePorts, IsScanEquivalent, filegroup
- `234762a147` dft: make scan_opt local search near-linear — OptimizeScanWirelength, TEST, TwoOptScanChain, struct CandidateEdges
- `521b091259` dft: do not create empty scan chains — ScanArchitect::getScanChains, ScanArchitect::inferChainCountFromMaxLength, TEST, class CellMock : public ScanCell, totalBits

### rsz (22)
- `2cdcdfb326` rsz: Refine buffer-tree target load estimate — namespace
- `1f1f7b2e6f` rsz: Cache Vt swap candidate cells — VtSwapMtGenerator::generate, VtSwapMtGenerator::isApplicable, class VtSwapMtGenerator : public MoveGenerator
- `20519508c5` rsz: Cache size-down fanout cell ranking — SizeDownFanoutMtGenerator::prepareInputs, checkMaxSlewViolation, class SizeDownFanoutMtGenerator : public MoveGenerator, measureLoad, measureLoads, measureOutputs, namespace rsz
- `8f67915cba` rsz: Reuse unbuffer slack calculations — Resizer::estimateInputSlewImpact, Resizer::estimateSlewsAfterBufferRemoval, Resizer::estimatedSlackOK, class Resizer : public sta::dbStaState, public sta::dbNetwor, isEligible, makePathDriverTarget, namespace rsz, passesCapGuard, passesSlackGuard, struct UnbufferSelectionContext
- `c6d803072d` rsz: Reduce bottleneck refreshes before WNS tail — SetupParallelEvalPolicy::analyzeBottlenecks, struct BatchPriorityConfig
- `676677ec3c` test: Update rebuffer delay estimate goldens
- `00a664d3f7` rsz: Clarify setup move comments — Resizer::estimateInputSlewImpact, Resizer::estimatedUnbufferSlackOK, VtSwapMtGenerator::generate, VtSwapMtGenerator::isApplicable, checkMaxSlewViolation, class Resizer : public sta::dbStaState, public sta::dbNetwor, class SizeDownFanoutMtGenerator : public MoveGenerator, class VtSwapMtGenerator : public MoveGenerator, makePathDriverTarget, measureOutputs, passesCapGuard, rankSwappableCells …
- `cda63c4d9e` test: Refresh parallel setup repair goldens
- `57ab12ba18` rsz: Document buffer-tree calibration trade-off — namespace
- `8c624da666` rsz: Avoid duplicate VT candidate cache lookup — VtSwapMtGenerator::isApplicable
- `55903e03cb` rsz: preserve UNPLACED status in Resizer::insertBufferPostProcess — Resizer::makeInstance
- `b0a75d9b32` rsz: skip redundant sorting and O(N^2) erasures in performGainBuffering — RepairDesign::performGainBuffering
- `da3318c001` rsz: runtime optimization for fullyRebuffer — Rebuffer::fullyRebuffer
- `f5d15a03b6` rsz: update batching policy — Rebuffer::fullyRebuffer
- `ff589d84b3` rsz: Exclude disabled Liberty arcs in Resizer::driveResistance — Rebuffer::chooseTreeAndDriver, Rebuffer::slackWithDriverCell, Rebuffer::upstreamSideLoadsOk, Resizer::bufferOutput, Resizer::driveResistance, TEST_F, class Resizer : public sta::dbStaState, public sta::dbNetwor, collectFaninSideLoads
- `b08b1e22ff` clang-format — collectFaninSideLoads
- `96b8843fe0` add fallback guard for no arcs — Resizer::driveResistance
- `447a93a5ba` reviewer feedback, remove dirty_level — Rebuffer::fullyRebuffer
- `5901841087` rsz: never swap pins on a cell with an opaque or constant output — SwapPinsGenerator::equivCellPins, equivCellPins, equivCellPinsForSwapReport
- `392fbc43e7` rsz: drop a null function check every output now passes — SwapPinsGenerator::equivCellPins, equivCellPins, equivCellPinsForSwapReport
- `2dd77b815f` rsz: one pin-swap equivalence check for all its callers — Resizer::reportSwappablePins, SwapPinsGenerator::selectSwapPort, class SwapPinsGenerator : public MoveGenerator, equivalentInputs, namespace, namespace rsz
- `10ad32816e` rsz: sort SwapPinsEquivalence into the BUILD source list

### (top) (21)
- `29432e0625` dft: add scan optimization algorithm source files — filegroup
- `f357f5dcab` dft: implement clustering algorithm for scan chain optimization
- `d47a94535a` dft: refactor executeDftPlan to support scan_opt re-stitching
- `ae6b9c4858` dft: update build — filegroup
- `4923866d03` dft: add scan_opt regression/CI test
- `2a8b7f880b` test: raise the jpeg antenna limits for the NDR deficit change
- `ff8d9f6bfb` test: raise ibex_sky130hd skew and aes_sky130hs antenna limits
- `50e9dc630d` update bazel flow test metrics
- `9752406140` test: update ibex and jpeg_sky130hd flow metrics after master merge
- `ac4244c928` docs: gemini: hard stops on review advice that silences errors
- `fdc27966a7` gpl: refresh placement and flow reference values
- `93c73d53b7` ord: Keep virtual clocks out of timing__fmax
- `6b810c9ed9` test: update ibex_sky130hd flow metrics after master merge
- `6278e896b2` test: update multiple after gpl change at bin aspect ratio:
- `80a6c68e15` bazel: take sv-elab from the BCR, turn exact version pins into floors (#12112) — bazel_dep, single_version_override, use_repo
- `218f4ce131` bazel: fetch GNU downloads through ftpmirror.gnu.org (#12104)
- `988511c28c` test: update nangate45 and jpeg flow metrics after master merge
- `73a158b4e0` bazel: fetch GitHub downloads through the BCR's Cloudflare mirror
- `2d7b8a7a67` test: Capture regression output without tee
- `b779ac0695` bazel: 9.3.2
- `2db0cb2d7e` ci(coverity): inject rules_coverity into the Bazel capture — _coverity_bazel, _run, test_static_fails_when_capture_percentage_is_missing, test_static_uses_uncached_local_bazel_capture

### grt (14)
- `baed7deb32` grt: restart the first soft-NDR demotion from the initial routing — FastRouteCore::run, FastRouteCore::setSoftNDR, Graph2D::getCostNDRAware, TEST_F, class FastRouteCore
- `527ad942c9` grt: shorten the soft-NDR restart comments — FastRouteCore::restoreInitialRoutes, FastRouteCore::run, FastRouteCore::saveInitialRoutes, class FastRouteCore
- `5f764243a3` grt: replace the NDR overflow multiplier with NDR deficits — FastRouteCore::StNetOrder, FastRouteCore::computeCongestedNDRnets, FastRouteCore::getMazeRouteNetOrder, FastRouteCore::getOverflow2D, FastRouteCore::getOverflow2Dmaze, FastRouteCore::mazeRouteMSMDSequential, FastRouteCore::newRipupCheck, FastRouteCore::newRipupCongestedL, FastRouteCore::newrouteL, FastRouteCore::newrouteZ, FastRouteCore::newrouteZ_edge, FastRouteCore::routeMonotonic …
- `01b0fe5704` grt: fix clearNDRnets order and edge capacity for a specific location — FastRouteCore::getUsageNDRAware, Graph2D::initNDRnets
- `03a913a622` grt: update soft NDR goldens for per-edge NDR pricing — TEST_F
- `74d34bd075` grt: fix stale NDR deficits and the 3D maze gate — FastRouteCore::getUsageNDRAware, FastRouteCore::run, FastRouteCore::scanOverflow2D, FastRouteCore::scanOverflow2Dmaze, Graph2D::getCostNDRAware, Graph2D::getNDRDeficitIfRouted, Graph2D::releaseNDRCapLayer, TEST_F, class FastRouteCore, class Graph2D, class OverflowTestPeer
- `97c091ce08` grt: reduce memory footprint, don't allocate space for unused information — GlobalRouter::applyNetObstruction
- `1fe08158b2` grt: clear edge NDR deficits in clearNDRnets — Graph2D::clearNDRnets, Graph2D::copyRoutingStateFrom, Graph2D::usedGridsMatchUsage, TEST_F
- `847cfc1a40` grt: use NDR-aware cost in newrouteLInMaze — FastRouteCore::newrouteLInMaze, TEST_F, class OverflowTestPeer
- `18780f4a9b` grt: reroute CUGR nets in slack-last, largest-first order — CUGR::mazeRoute, CUGR::patternRouteWithDetours, CUGR::sortNetIndices, class CUGR
- `1d088a2605` grt: address review on CUGR reroute order — CUGR::reportDebugNetSlack
- `30080f582a` grt: keep the slack-then-size order for incremental CUGR reroutes — CUGR::sortRerouteIndices, class CUGR
- `55fc85f09c` grt: order removed nets last in CUGR net sorts — CUGR::sortNetIndices, CUGR::sortRerouteIndices
- `4941b806a5` grt: keep NDR capacity reservations and NDR nets only where NDR nets are — Graph2D::addCap3D, Graph2D::computeNDRDeficit, Graph2D::computeSuggestedAdjustment, Graph2D::copyRoutingStateFrom, Graph2D::getCostNDRAware, Graph2D::getNDRDeficit, Graph2D::getNDRDeficitIfRouted, Graph2D::printEdgeCapPerLayer, Graph2D::printNDRCap, Graph2D::refitNDRDeficitNets, Graph2D::releaseNDRCapLayer, Graph2D::reserveNDRCapLayer …

### gpl (10)
- `befc1d60d6` gpl: correct CPU FFT bin aspect scaling — CpuFftBackend::CpuFftBackend, TEST
- `d4cf0a7d83` gpl: correct GPU FFT bin aspect scaling — PoissonSolver::solveFieldFromAuv, TEST, divideByWSquare
- `fdc27966a7` gpl: refresh placement and flow reference values — HPWL
- `6278e896b2` test: update multiple after gpl change at bin aspect ratio:
- `f3a75f3ecd` gpl: update test after fixing bin grid aspect ratio
- `ac9033604b` gpl: check density, overflow and wirelength kernels against the math
- `a45d7cb8fe` gpl: ignore a mirror follower's region under -place_ios — IoPinBase::IoPinBase, IoPinBase::initConstraints, TEST_F
- `709551cfaf` gpl: actually reset overflow counters after td — NesterovBase::resetMinSumOverflow, NesterovPlace::runTimingDriven, TEST_F, class TimingRepairIntegrationTest : public tst::IntegratedFi
- `863d566467` address review feedback for cleaner resetting — HPWL, NesterovBase::resetMinSumOverflow, NesterovPlace::runTimingDriven, TEST_F, class NesterovBase, class NesterovPlace
- `bd99f4daf3` gpl: rename cr and n in IoPinBase for readability — IoPinBase::IoPinBase, IoPinBase::initConstraints

### syn (10)
- `59f0bdd207` syn: L-IR core types (ids, ops, constants, names) — messages_txt
- `4e6174f7fb` syn: avoid a 32-bit shift in NameInterner's hash — class NameInterner
- `637e9f7001` syn: clang-tidy cleanups in L-IR tests — TEST
- `1aca55d510` syn: Speed up ACD timing context extraction — populateCutTiming
- `9deb65201f` syn: Add rule to break down carry chains — foldCombinationals
- `1025444000` syn: Add test coverage for new rule — TEST
- `11d158e6ab` syn: rename internBitString, split pool concurrency tests — ConstPool::internFill, TEST, class ConstPool, class ConstView, class ObjAttributes, logicValueChar
- `3cce58c5c6` syn: address review comments on L-IR core types — ConstPool::internBitString, ConstPool::internNormalized, ConstPool::internUint, ConstPool::internUnlocked, NameInterner::contains, NameInterner::find, NameInterner::intern, NameInterner::internPrefixed, NameInterner::internUnlocked, NameInterner::store, checksumCombine, class ConstPool …
- `e53eab8546` syn: rename constant bit planes to bits and x_mask — ConstPool::internUint, ConstView::bit, ConstView::isFill, ConstView::toString, ConstView::toUint64, TEST, class ConstPool, class ConstView, constLastWordMask, logicValueChar, namespace
- `80a6c68e15` bazel: take sv-elab from the BCR, turn exact version pins into floors (#12112) — TEST_F

### web (9)
- `4f70bb1a72` web: require an access token to use the viewer — DetectSession::DetectSession, DetectSession::on_read, HttpSession::on_read, Listener::Listener, Listener::on_accept, TEST, TEST_F, WebServer::serve, assetPathFromTarget, browserHostForBind, browserLaunchFromString, browserSkipReasonText …
- `648e37610c` web: say up front that nobody types the access token
- `cb14951b3f` gui: give every build the gui:: commands — Gui::initCommon, Gui::timingPathsThrough, class Descriptor, class Dialogs, class GuiBackend, class Painter, proc save_image, proc web_load_chiplet_heatmap
- `e15a9ac8c9` web: take the token from web_server -token and keep it out of the log — SessionAuth::SessionAuth, TEST, TEST_F, WebServer::endStartupScripts, WebServer::serve, browserSkipReasonText, class ListenerFixture : public ::testing::Test, class SessionAuth, class WebServer, dispatch_request, handle_request, proc web_server …
- `3c6918c419` web: the slack histogram names its clocks and their periods — TEST_F, TimingReport::getSlackHistogram, computeLogYAxis, describe, serializeSlackHistogram, struct SlackHistogramSeries
- `12c8bff77f` web: "Expand clock" in the timing widget — describe
- `0ef8c76d0b` web: a busy cursor while a timing report is built — describe, onSelectionReset
- `504345e09a` web: send security headers with every HTTP response — TEST_F, applyGLTheme, describe, parseBbox, statusOf, test_loads_the_bundle
- `4791b27674` web: name the WebSocket in connect-src and reject unloadable toolbar icons — DetectSession::reject, TEST, TEST_F, WebViewerHook::addToolbarButton, createToolbar, describe, dispatch_request, expectSecurityHeaders, handle_request, parseBbox, serveEmbeddedAsset, statusOf …

### odb (7)
- `f357f5dcab` dft: implement clustering algorithm for scan chain optimization — class dbScanList : public dbObject, dbScanList::add
- `6395775d6a` odb: add dbDft::reset() to clear scan chain data — class dbDft : public dbObject, dbDft::getScanChains
- `fdc27966a7` gpl: refresh placement and flow reference values
- `70a413d989` odb: destroy scan insts in dbDft::reset() — TEST_F, class dbDft : public dbObject, dbDft::getScanChains
- `7726fdc228` odb: drop dbInst scan inst lookups in dbDft::reset() — TEST_F, dbDft::reset
- `2a3442396f` odb: scan BTerms before ITerms in dbNet::getFirstDriverTerm — dbInsertBuffer::insertBufferBeforeLoads, dbNet::getFirstDriverTerm
- `d8707ee6a2` test: update after dpl change on overflow updating — HPWL

### mpl (5)
- `399ef84ff6` mpl: refactor configuration, one source of defaults — HierRTLMP::HierRTLMP, HierRTLMP::computeWireLength, HierRTLMP::createGroupForCluster, HierRTLMP::setGuidanceRegions, MacroPlacer::MacroPlacer, MacroPlacer::blockMacroChannels, class HierRTLMP, class MacroPlacer, getMacroPlacer, namespace mpl, proc rtl_macro_placer, set_debug_cmd …
- `2dcafbb425` mpl: refactor debug config — HierRTLMP::computeWireLength, HierRTLMP::configure, MacroPlacer::blockMacroChannels, class HierRTLMP, class MacroPlacer, getOptions, namespace mpl, proc parse_macro_name, rtl_macro_placer_cmd, struct MacroPlacerOptions
- `7ff36f5b4b` mpl: rename MacroPlacer::place to run — MacroPlacer::MacroPlacer, class MacroPlacer, rtl_macro_placer_cmd
- `52a84afec9` mpl: prevent crashes when running mpl_debug without gui — Graphics::Graphics, Graphics::penaltyCalculated, Graphics::startSA
- `0f5136b64d` mpl: update report_directory behavior — HierRTLMP::configure, HierRTLMP::placeChildren

### dpl (4)
- `4569e4033e` dpl: respect oriented fixed macro footprints — NegotiationLegalizer::initFromDb, class OpendpTest : public tst::Fixture, filegroup
- `acabd565a7` dpl: refresh fixed macro regression outputs
- `9a36b47d8e` dpl: free the pixel grid when detailed and check placement return — Graphics::drawObjects, Grid::clear, Opendp::checkPlacement, Opendp::detailedPlacement, Opendp::legalCellPos, TEST_F, class Grid
- `e61707c4ee` dpl: test legalCellPos after a fixed-only check and its single rebuild — TEST_F, class Opendp

### drt (4)
- `8d523a27c0` drt: remove redundant GC net rebuild in initMazeCost_connFig — FlexDRWorker::initMazeCost_connFig
- `f0c95c8516` drt: check alternative via enclosures — FlexGCWorker::Impl::checkLef58Enclosure_main, FlexGCWorker::Impl::checkMetalWidthViaTable, TEST_F, class FlexGCWorker::Impl
- `09e522b0f7` drt: skip inapplicable enclosure width rules — FlexGCWorker::Impl::checkLef58Enclosure_main, TEST_P
- `e2e1b62f5a` drt: preserve access-point metadata in segment copies — class frPathSeg : public frShape, drPathSeg::drPathSeg

### sta (3)
- `7a442d4f73` update latest STA
- `33b4422392` update sta to latest master
- `14d6c920fc` update sta with recent changes

### psm (2)
- `946aa96f4b` psm: remove solution when voltage or powers are modified — IRSolver::getVoltage, IRSolver::solve, IRSolver::solveAssembly, PDNSim::clearSolvers, PDNSim::setDebugGui, class IRSolver, class PDNSim : public odb::dbBlockCallBackObj
- `14b7914cfa` psm: only clear when values change — PDNSim::clearSolutions, PDNSim::setDebugGui

### utl (2)
- `4f70bb1a72` web: require an access token to use the viewer — add_library, gtest_discover_tests, test_suite
- `399ef84ff6` mpl: refactor configuration, one source of defaults — convert

### Metrics.tcl (1)
- `93c73d53b7` ord: Keep virtual clocks out of timing__fmax — proc report_fmax_metric

### gui (1)
- `cb14951b3f` gui: give every build the gui:: commands — Gui::init, Gui::requestUserInput, class QtGuiBackend : public GuiBackend, else, enabled, fit, initGui, package, set, trigger_action

### wmk (1)
- `4f70bb1a72` web: require an access token to use the viewer — deriveStageKey, derive_stage_key_cmd, isWatermarkStage, random_hex_cmd

## OpenSTA

- `32e049553` bazel: export dcalc/DmpCeff.hh from opensta_lib
- `8dd7ba8b3` check_setup: follow set_max_delay through, no false positives on macro blocks
- `3121ddf07` write_timing_model: write a constant output as that constant
- `f3114b7b0` check_setup: keep the port warnings' wording
- `124d58e70` write_timing_model: only the netlist's constants become constant outputs
- `554e2f9d6` rename prima4 -> prima10
- `102fc163b` latch d->q timing sense resolve #556
- `cc365d091` PrimaDelayCalc::parasiticDFS loops
- `bebcb14c2` Noise delay bug fixes
- `1d6090128` vcd x transitions count as .5
- `05a727769` check_setup: report a register no clock reaches on its launch edge
- `0727ce854` prima set_driving_cell seg fault resolves #559
- `1ccf5bdfa` multi-driver net missing load pin index (broken by fc6ed303)
- `83ae4068c` Fix map::at in loadSlewChanged for output->output arc fanout (#560)
- `0d29255ae` rename incr_dcalc_out_to_out_arc -> dcalc_incr_out_to_out_arc
- `c0b03e4ee` present segfault on is_clock with blackbox (#561)
- `e67ee8b3c` Levelize: invalidate arrivals when a loop cut moves (#554)
- `bfafd97cc` check_setup: count only the checked mode's clock arrivals
- `935ee8ee9` check_setup: if block instead of continue in the launch edge scan
- `214c110f9` check_setup: find only clock arrivals for -no_clock
- `6ca0e925d` ArrivalVisitor copy keeps clks_only
- `ea312e616` Move clk_arrivals_threads test to search/test

## Pull requests updated this week (100 of 140, most recent first)

- #12138 [open] drt: stop a stubborn-tiles worker whose markers run away
- #12146 [merged] ord: Keep virtual clocks out of timing__fmax
- #11122 [open] Web GUI: add an Instance Groups view to the Hierarchy widget, color-coded in the layout
- #12116 [merged] drt: remove redundant GC net rebuild in initMazeCost_connFig
- #12157 [merged] ci(coverity): inject rules_coverity into the Bazel capture
- #12158 [merged] rsz: never swap pins on a cell with an opaque or constant output
- #12150 [open] odb: avoid segfault in insert_buffer and makeNewName when base name is null
- #12159 [open] bazel: patch sv-elab to avoid duplicate header paths on RBE
- #12032 [open] gpl: Improve GPL runtime by ~4.15x
- #11728 [open] CTS: fix inverter tree classication
- #12156 [merged] bazel: 9.3.2
- #12027 [merged] rsz: Improve setup repair estimation and runtime
- #12155 [open] dbSta: Check cross-layer pin alignment
- #12001 [open] rsz: Tighten driver sizing checks in fullyRebuffer
- #12154 [open] rcx: guard against null rc in extMeasure::calcRes0
- #12153 [open] rsz: Add a relative leakage cost to PARALLEL_EVAL cell swaps
- #12144 [open] ant: Move completed cumulative antenna chain
- #12096 [open] drt: generate pin access points on preferred upper-layer tracks
- #12107 [merged] drt: preserve access-point metadata in segment copies
- #12103 [merged] drt: check alternative via enclosures
- #12053 [open] dpl: Add post-PA placement legalization command
- #12141 [merged] Web GUI: send security headers with every HTTP response
- #11712 [open] Web GUI: replace Leaflet with deck.gl in the layout viewer
- #12082 [open] Web GUI: make tabs that don't fit (like Charts) easy to reach
- #12066 [merged] syn: L-IR core types (ids, ops, constants, names)
- #11739 [merged] Web GUI: require an access token to use the viewer
- #11440 [open] Use Kokkos instead of OpenMP
- #12151 [open] pex: speed up PlanCoversFromProbes unit test
- #12132 [merged] bazel: fetch GitHub downloads through the BCR's Cloudflare mirror
- #12152 [merged] update sta with recent changes
- #12102 [closed] Remove need for ORFS variables.json in git: add yaml2json
- #11860 [merged] web: a busy cursor while a timing report is built (Qt parity)
- #11859 [merged] web: "Expand clock" in the timing widget (Qt parity)
- #11858 [open] web: widening a table column widens the table (Qt parity)
- #12142 [open] build(deps): bump the python group across 2 directories with 20 updates
- #12042 [open] build(deps): bump the actions group across 1 directory with 4 updates
- #11854 [open] build(deps): update Three and regenerate browser bundles
- #12071 [open] dpl: Fix crashes when using hybrid row macros without SITE set
- #12059 [open] grt: 3d fastroute data structure optimizations
- #12137 [open] rsz: preserve pin-level set_propagated_clock across computeSkewBudget
- #12076 [open] par: account for cut delay in timing-aware refinement
- #12149 [open] save goldens as plain files rather than executable files
- #12039 [merged] grt: FastRoute soft NDR congestion recover
- #12124 [merged] dft: bind ff state variables by position in scan_replace
- #12147 [open] cts: latency balancing times only the clock network, CTS 101.8 -> 47.8 GB on XSTile, same tree
- #12120 [merged] dpl: free the pixel grid on return, 116.5 -> 94.3 GiB peak on a 666 M-site core, same checkpoints
- #12140 [open] mpl: create the hard macros in a factory outside the clustering engine
- #12139 [open] mpl: consolidate SA penalties into a vector of Penalty
- #12148 [merged] grt: 16 -> 2 bytes per edge and layer, NDR state kept only where NDR nets are
- #12123 [open] cut: Fix handling of endpoints on combinational cells 
- #10720 [open] upf: add supply-net commands, upf_version, and supply options (#5617)
- #12119 [closed] cts: latency balancing without CRPR, CTS 117 -> 51.5 GiB on a 700k-register top, same tree
- #12145 [open] test: Check metrics cleanup and move antenna test pin
- #12143 [closed] rsz: Use all Liberty arcs for the repair_design load slew
- #12019 [open] ppl: make place_pin snap to edge for all floorplans
- #12045 [open] gui: add grt heatmap to save_image -web
- #12117 [open] gpl: return a PlaceResult from the placement entry points
- #12128 [merged] rsz: Speedup fullyRebuffer() -rebuffer_size_driver by invalidating sta/est less frequently
- #12068 [merged] gpl: Properly reset overflow counters after timing driven
- #12084 [closed] build(deps): bump the python group across 2 directories with 18 updates
- #12106 [open] drt: preserve variable wire end extensions
- #11868 [open] drt: Add closed-loop adaptive search-and-repair policy
- #12131 [open] Simplify some unnecessary overrides.
- #11943 [open] web: a script view for gui:: commands with no Qt window
- #12077 [open] odb: ensure single binding point if a pin contains multiple co-linear wire segments
- #11963 [merged] grt: enhance FastRoute NDR handling
- #12118 [merged] gpl: ignore a mirror follower's region under -place_ios
- #12136 [open] drt: route from iteration 0 when resuming with unrouted nets
- #12056 [merged] psm: remove solution when voltage or powers are modified
- #12134 [open] rsz: Prevent repeater over-sizing during design DRC repair
- #12055 [closed] Reduce module overrides that became unnecesary.
- #12130 [merged] dft: do not create empty scan chains
- #11522 [open] dbSta: check Liberty transition tables and input capacitance in check_ip
- #11995 [merged] dft: fix deque end() dereference in ScanStitch::Stitch
- #11942 [merged] gui: give every build the gui:: commands
- #12129 [merged] dft: make scan_opt local search near-linear
- #12080 [merged] syn: Add rule to break down carry chains
- #12079 [merged] syn: Speed up ACD timing context extraction
- #11772 [open] drt: default pin access
- #12097 [merged] dft: add scan_opt scan chain wirelength optimization
- #12109 [merged] rsz: Exclude disabled Liberty arcs in Resizer::driveResistance
- #11856 [merged] dpl: respect oriented fixed macro footprints
- #12127 [open] ord: Reduce memory leak
- #12111 [open] gpl: add uniform density option to consider macros as placed
- #12126 [merged] update latest STA
- #11857 [merged] web: the slack histogram names its clocks and periods (Qt parity)
- #12125 [open] bazel: add clang-format check and fix targets
- #12121 [closed] grt: resistance-aware final 3D pass once, on its own nets: finalisation 62.1 -> 32.4 s
- #11919 [open] mpl: report a placement blockage in the annealer's location table
- #12018 [merged] docs: gemini: hard stops on review advice that silences errors
- #12104 [merged] bazel: fetch GNU downloads through ftpmirror.gnu.org
- #12112 [merged] bazel: take sv-elab from the BCR, turn exact version pins into floors
- #12074 [merged] grt: reduce memory footprint, don't allocate space for unused information
- #12122 [open] dpl: fail in seconds, not 82 minutes, when no search can legalize within the window
- #12115 [merged] gpl: check density, overflow and wirelength kernels against the math
- #12051 [merged] gpl: correct CPU/GPU FFT bin aspect scaling 
- #12064 [open] gpl: sub dbu movement on ultra low util FPs spuriously fire divergence
- #12098 [open] mpl: Improve macro-placer simulated annealing robustness and packing quality
- #11931 [merged] rsz, odb: preserve UNPLACED buffer status and avoid quadratic buffering bottlenecks
- #12108 [open] drt: align default vias below the routing floor

## Issues updated this week (36)

- #12161 [open] Renaming toplevel `src/` to `openroad/`
- #11668 [closed] timing__fmax includes virtual clocks since ORFS added virtual I/O clocks. Intended?
- #11358 [open] Incremental global placement needs to be timing aware
- #12160 [open] cleanup-opportunity: BUILD files never refer to mockturtle in third-partty/
- #12135 [open] More robust CI: turn off Read the Docs pull request builds; //docs:sphinx_build_test covers them
- #12038 [open] check_placement: padding check flags a legal cell above a fixed block whose bottom is in the upper half of a row
- #12114 [open] cluster_flops: opposite clear polarities can share a class and be automatically selected
- #12113 [closed] scan_replace: capture-avoiding state-variable renaming changes the connected output phase
- #12133 [closed] PDN: regression in pad connections
- #11167 [open] [Security] Fix of vulnerabilities similar to issue #11065
- #11024 [open] sv_elaborate crashes with SIGSEGV
- #11003 [open] SYN: asap7/mock-alu fails when reading sdc
- #11002 [open] SYN: Elaboration failed
- #3605 [open] check_placement should generate a loadable error file
- #11992 [open] drt: one stubborn-tiles worker variant (DRC cost c/2, marker cost 2c) runs 30–49 min, then its result is discarded
- #12075 [open] grt: lower the virtual memory a 9.4 M-instance run must be configured with
- #11985 [closed] dft: ScanStitch::Stitch dereferences std::deque::end() on chains of 3+ cells
- #12012 [closed] psm: analyze_power_grid ignores a set_pdnsim_net_voltage made after the first solve of the net
- #10937 [closed] DRT: PA via candidates importance cohesion
- #11886 [closed] Web GUI: dies with layers of the same name can't be shown or ordered independently
- #11932 [closed] sta: stale arrival after a combinational-loop cut moves makes PathExpanded/PathEnum loop forever
- #10561 [open] ram: add placement sanity checks to the regression tests (`check_placement`, etc.)
- #11664 [open] bazel: bazel build data is huge and takes several hours to remove
- #11735 [closed] dpl: negotiation legalizer blocks the unrotated master footprint for R90/R270/MXR90/MYR90 fixed macros
- #12046 [open] syn: acd_resynth -apply segfaults on a database resynthesized in an earlier process
- #12072 [open] rcx: wrong OVER/UNDER table used when the rules LayerCount exceeds the routing layer count
- #12049 [open] [dbSta] write_spef writes pins of hierarchical cells under instance names that don't exist
- #12110 [open] PDN fails to repair metal1 channels between macros placed 12 µm apart
- #11677 [open] CTS: flops behind a clock inverter get no tree after a macro/register split
- #12095 [open] odb: Bazel build fails on linux/aarch64 — char fc compared to EOF in def/lef lexers
- #11538 [closed] pdn: generated vias can bypass required enclosure validation on narrow overlaps
- #12054 [closed] odb: GDSWriter writes odd-length ASCII string records (GDSII requires even lengths)
- #12052 [open] OpenRCX: extMeasure::calcRes0 segfaults on a null getRes() result when a rules file has sparse per-layer tables
- #11984 [closed] read_upf: UPF-0043 and ODB-0154 abort the process instead of raising a Tcl error
- #11812 [closed] drt: segfault after "initMazeIdx_ap no idx" when a pin is only accessible above the top routing layer
- #12088 [open] [cts] -useful_skew: add a test to document and enforce the intent at block boundaries

