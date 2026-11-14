# Upstream OpenROAD — weekly digest 2026-11-14

- Pinned: `4155ac310149` · master: `a8aca68d2018` · 674 commits ahead (178 non-merge)
- OpenSTA submodule: `cc9027d65` → `2947a0cab` (71 commits)
- Window for pull requests and issues: updated since 2026-11-07

## Behaviour changes (regression goldens updated)

| Module | Commit | Title | Goldens |
|---|---|---|---|
| dft | `29432e0625` | dft: add scan optimization algorithm source files | dft_man_tcl_check.ok, dft_readme_msgs_check.ok, place_sort_sky130.ok, scandef_sky130.defok |
| dft | `4923866d03` | dft: add scan_opt regression/CI test | scan_opt_sky130.ok, scan_opt_sky130.vok |
| dft | `d7597ff53f` | dft: revert changes in tests targetting the architect | place_sort_sky130.ok |
| dft | `fb394a30d5` | dft: rever scandef tests | scandef_sky130.defok |
| mpl | `dfb7cc1cf9` | web: add a Clusters panel and a cluster coloring overlay | keep_clustering_data_existing_group.defok, keep_clustering_data_existing_group.ok |
| mpl | `25265c5067` | mpl: revert the pre-existing dbGroup handling | keep_clustering_data_existing_group.defok, keep_clustering_data_existing_group.ok |
| grt | `baed7deb32` | grt: restart the first soft-NDR demotion from the initial routing | soft_ndr_4w_6s.guideok, soft_ndr_4w_6s.ok, soft_ndr_escalation.guideok, soft_ndr_escalation.ok |
| grt | `5f764243a3` | grt: replace the NDR overflow multiplier with NDR deficits | ndr_1w_3s.guideok, ndr_1w_3s.ok, soft_ndr_4w_6s.guideok, soft_ndr_4w_6s.ok, soft_ndr_escalation.guideok, soft_ndr_escalation.ok |
| dpl | `acabd565a7` | dpl: refresh fixed macro regression outputs | cell_on_block1.ok, cell_on_block2.ok, max_disp1.ok, obstruction2.ok |
| rsz | `fa4da7dab1` | rsz: Tighten driver sizing checks in fullyRebuffer | rebuffer_size_driver.ok, rebuffer_size_driver_guards.ok, repair_setup7_limit.ok, report_buffers_ihp.ok |
| rsz | `531f7a1a45` | rsz: Check upstream stages and other inputs before a driver resize | rebuffer_size_driver_checks.ok |
| rsz | `d2cf36aab9` | rsz: Bound every other arc of a resized driver | rebuffer_size_driver_checks.ok |
| rsz | `da967cae63` | rsz: Charge the slowest upstream driver on the timing-path input | rebuffer_size_driver_checks.ok |
| rsz | `3bec6bfc79` | rsz: Prefer the driving cell for a top-level input's resistance | rebuffer_size_driver_checks.ok |
| rsz | `c524fe2f35` | rsz: Take equal-area driver swaps only on near-critical nets | rebuffer_size_driver_tiebreak.ok |
| rsz | `08357fdcd5` | test: Cover the sequential and multi-output guards of driver sizing | rebuffer_size_driver_checks.ok, rebuffer_size_driver_tiebreak.ok |
| rsz | `76f37439ac` | rsz: Check a driver candidate against its rebuffered output's limits | rebuffer_size_driver_port_cap.ok |
| rsz | `953e442167` | test: Isolate the driver candidate max capacitance check | rebuffer_size_driver_checks.ok |
| ppl | `17c7f9cbd4` | ppl: make place_pin snap to edge for all floorplans | place_pin_polygon_blocked.defok, place_pin_polygon_blocked.ok, place_pin_polygon_l.defok, place_pin_polygon_l.ok, place_pin_polygon_t.defok, place_pin_polygon_t.ok +2 |
| grt | `03a913a622` | grt: update soft NDR goldens for per-edge NDR pricing | soft_ndr_4w_6s.guideok, soft_ndr_4w_6s.ok, soft_ndr_escalation.guideok, soft_ndr_escalation.ok |
| rsz | `676677ec3c` | test: Update rebuffer delay estimate goldens | report_delay_estimator_rebuffer_fanout8.ok, report_delay_estimator_rebuffer_minimal.ok, report_delay_estimator_rebuffer_prebuffered.ok, report_delay_estimator_rebuffer_steiner.ok |
| rsz | `cda63c4d9e` | test: Refresh parallel setup repair goldens | repair_setup_parallel_eval.ok, repair_setup_parallel_eval_max_util.ok, repair_setup_parallel_eval_threads.ok |
| grt | `74d34bd075` | grt: fix stale NDR deficits and the 3D maze gate | ndr_1w_3s.ok |
| psm | `946aa96f4b` | psm: remove solution when voltage or powers are modified | gcd_no_vsrc_reuse_change_voltage.ok |
| grt | `f0dcd2c370` | grt: 3d fastroute data structure and optimizations | res_aware_nets_percentage.guideok, res_aware_nets_percentage.ok, resistance_aware_asap7_fr.guideok, resistance_aware_asap7_fr.ok |
| rsz | `75339783ef` | update failing rsz tests | repair_design6.ok, repair_setup_reroute1.ok, repair_setup_reroute2.ok |
| grt | `2e3307cd84` | grt: restore second call to mazeRouteMSMDOrder3D() | res_aware_nets_percentage.guideok, res_aware_nets_percentage.ok, resistance_aware_asap7_fr.guideok, resistance_aware_asap7_fr.ok |
| rsz | `2e3307cd84` | grt: restore second call to mazeRouteMSMDOrder3D() | repair_design6.ok, repair_setup_reroute1.ok, repair_setup_reroute2.ok |
| rcx | `cf1c3b1c28` | odb: ensure single binding point if a pin contain multiple wire segments | colinear_vertices_inside_bpin.ok, colinear_vertices_inside_bpin.spefok |

## Commits by module (functions from the diff hunk headers)

### web (62)
- `a68c832dcc` web: render schematic cells with logic symbols — SelectHandler::handleSchematicCone, SelectHandler::handleSchematicFull, TEST_F, ioTypeToDirection, js_test
- `e745e571c7` web: restore OpenROAD schematic symbol rendering — SelectHandler::handleSchematicCone, SelectHandler::handleSchematicFull, classifyGate, emitSchematicCell, ioTypeToDirection
- `b45cc107ea` web: render schematic cells with OpenROAD logic symbols — SelectHandler::handleSchematicCone, SelectHandler::handleSchematicFull, TEST_F, canonicalizeCell, classifyGate, emitSchematicCell, findConnectedItermForPort, ioTypeToDirection, outputPin, outputPortReferencesState, schematicRegisterCell, scopeCssSelector …
- `0a3bf0ec4a` test: update schematic widget symbol coverage — describe
- `051b83b780` web: refine schematic register symbols — TEST_F, activeLowPortExpr, canonicalizeCell, classifyAoiOai, classifyRegister, describe, findConnectedItermForPort, ioTypeToDirection, js_test, makeClassOnlyInteractiveCell, makeCoordinateMappedCell, normalizedPortMap …
- `6323da62e7` test: document schematic widget DOM setup — cell, js_test
- `1737a99512` web: document schematic widget helpers
- `c18cd425e2` Improve schematic rendering helpers — describe
- `90fa3d3ead` web: add schematic back navigation — describe
- `3123382e6b` web: guard null Liberty port and apply clang-format — TEST_F, classifyGate, struct GateClass
- `7e5da030ee` web: capture schematic expand base before async request
- `0b15a0812b` web: cache group bounds in schematic label placement sort
- `ac50466ee1` web: show timing paths on the schematic view — TimingHandler::handleTimingHighlight, TimingHandler::handleTimingReport, TimingReport::expandPath, TimingReport::getReport, class TimingReport, describe, namespace web, serializeTimingNode
- `88b3fc87a2` web: remove dead and duplicated schematic measurement helpers
- `dc5e3739fa` web: fold schematic test cell builders together and cover the inspect guard — describe, makeWidget
- `4bd588c23c` web: tidy register classification and document gate symbol hints — classifyGate, classifyRegister, outputPortReferencesState
- `0880d48d50` web: stop calling the deprecated LibertyCell::hasSequentials — classifyRegister
- `c3b7b0d835` web: explain why the schematic replaced its pre-existing behaviour — classifyGate, emitSchematicCell
- `8e5871a56d` web: rebuild the schematic from the selected timing path — SelectHandler::handleSchematicCone, SelectHandler::handleSchematicFull, SelectHandler::registerRequests, class SelectHandler, describe, emitSchematicCell, struct WebSocketRequest
- `28af12cb44` web: stop touching master's code where the feature did not need it — canonicalizeCell, scopeCssSelector, skinPidForGatePort
- `91a2b4e639` web: explain the remaining schematic rewrites — skinPidForGatePort
- `dfb7cc1cf9` web: add a Clusters panel and a cluster coloring overlay — SelectHandler::handleSelect, SelectHandler::handleSelectFanoutBin, SelectHandler::handleSelectLayer, SelectHandler::registerRequests, TEST_F, TileGenerator::eagerInit, TileGenerator::generateTile, TileGenerator::geomCache, TileGenerator::renderTileBuffer, TileGenerator::saveImage, TileGenerator::saveImageLayerOrder, TileHandler::handleModuleHierarchy …
- `4a20e9b08a` web: move the Clusters panel into the Hierarchy tab — GroupReport::getReport, SelectHandler::handleFindObjects, SelectHandler::handleSelectGroup, SelectHandler::handleSelectLayer, TEST, TEST_F, TileGenerator::eagerInit, TileGenerator::renderTileBuffer, TileGenerator::saveImage, TileGenerator::saveImageLayerOrder, TileVisibility::parseFromJson, WebServer::saveReport …
- `036fe54759` web: keep a hidden Hierarchy view from collapsing its columns — collectMultiHighlightShapes, describe, function, highlightColors, makeResizableHeaders, showHierarchyView
- `8f741242b9` web: tidy up the hidden-view render fix — describe, js_test, makeResizableHeaders
- `79fbfab9f3` web: name the Hierarchy panel's sources in its dropdown — createMenuBar, describe
- `656148b9b2` web: hide the color overlays with the instances they fill — TEST_F, TileGenerator::renderTileBuffer
- `80cbc93b45` web: assert the overlay gate is per cell type — TEST_F
- `6c7007df86` web: check the overlay color map before classifying the instance — TileGenerator::renderTileBuffer
- `c305e41b93` web: give the find_objects union bbox its own key — SelectHandler::handleFindObjects, SelectHandler::handleSelectGroup, SelectHandler::handleSelectNetLengthBin, TEST_F, class FakeGroupDescriptor : public gui::Descriptor, class GroupSelectTest : public tst::Nangate45Fixture, describe, showFindDialog
- `5100347b78` web: drive both hierarchy overlays from one Display Controls checkbox — SelectHandler::handleSelectGroup, buildTileRequestFor, computeEffectiveColors, createMenuBar, createMockApp, describe, highlightColors, isStaticMode, populateDisplayControls, visibleViews
- `bd4da94373` web: finish schematic timing path view — SelectHandler::handleSchematicCone, TEST_F, activeLowPortExpr, buildSchematicNetlist, canonicalizeCell, class TimingReport, classifyAoiOai, classifyGate, classifyRegister, createMockApp, describe, emitSchematicCell …
- `7153cd6f2a` web: make standard symbols the only schematic view — SelectHandler::handleSchematicFull, SelectHandler::handleSchematicPath, addRegisterOutputs, buildSchematicNetlist, canonicalizeCell, classifyAoiOai, classifyRegister, createMockApp, describe, emitSchematicCell, findItermForPort, outputPortReferencesState
- `6b4311a22b` Update src/web/docs/server-api.md
- `bfd2c23ecc` web: keep the hierarchy coloring when its tab is closed — describe
- `49eea29229` web: give the overlay warning its own message id — TileGenerator::renderImageBuffer
- `b15bd0f746` web: paint the saved image on the viewer's background — TEST_F, TileGenerator::renderImageBuffer, WebServer::saveImage, class TileGenerator, gtest_discover_tests, handleImageDownload, parseIntExact, parseVis
- `002ac24326` web: give every empty tile the same 1x1 blank — buildTileRequest, createOverlayTileLayer, createWebSocketTileLayer, describe, extend, import
- `56be15cb24` web: let the Hierarchy view checkbox drive the coloring — TEST_F, TileGenerator::clearOverlayCaches, TileGenerator::dropOverlayCachesIfStale, TileGenerator::renderImageBuffer, TileGenerator::saveImage, TileHandler::handleSetOwnerColors, TileHandler::handleTile, class TileGenerator, class dbBlock;, describe, extend, populateDisplayControls …
- `cc020bb0e4` web: fix dup msg id — TileGenerator::renderImageBuffer
- `769bca480c` Update src/web/docs/server-api.md
- `0dfc071f05` Update src/web/docs/server-api.md
- `e3b8738337` web: fix the heat map layer and cache the default overlay colors — TEST_F, TileGenerator::dropOverlayCachesIfStale, TileGenerator::renderImageBuffer, TileHandler::handleTile, class TileGenerator, describe, extend, populateDisplayControls, syncHierarchyOverlay
- `3f196bdecf` web: batch schematic label body measurements — describe
- `b731b383f2` web: batch schematic label candidate measurements — describe
- `5615270be3` web: default timing node instance names — struct TimingNode
- `4f70bb1a72` web: require an access token to use the viewer — DetectSession::DetectSession, DetectSession::on_read, HttpSession::on_read, Listener::Listener, Listener::on_accept, TEST, TEST_F, WebServer::serve, assetPathFromTarget, browserHostForBind, browserLaunchFromString, browserSkipReasonText …
- `648e37610c` web: say up front that nobody types the access token
- `439215bb63` web: fix review issues in schematic timing view — SelectHandler::handleSchematicCone, SelectHandler::handleSchematicFull, SelectHandler::handleSchematicInspect, SelectHandler::handleSchematicPath, TEST_F, TimingHandler::handleTimingHighlight, TimingReport::expandPath, addRegisterOutputs, buildSchematicNetlist, classifyGate, clearSelectionHighlights, createWidget …
- `f388723101` web: theme the dark schematic instead of inverting it — describe
- `9ae0ff4995` web: match timing highlights by pin and ignore overlapping Back — TEST_F, TimingHandler::handleTimingHighlight, TimingHandler::handleTimingReport, describe
- `f44c47297a` web: regenerate the dist bundle
- `a66ab524a6` odb: fire callbacks for dbGroup edits — Search::clearInsts, TEST_F, TileGenerator::renderTileBuffer, class Search : public odb::dbBlockCallBackObj
- `d50f5a7f80` web: show bump footprints and logical inter-die links in 3D — SelectHandler::handleGet3DData, SelectHandler::handleSchematicFull, describe, test_suite
- `cb14951b3f` gui: give every build the gui:: commands — Gui::initCommon, Gui::timingPathsThrough, class Descriptor, class Dialogs, class GuiBackend, class Painter, proc save_image, proc web_load_chiplet_heatmap
- `9cb2a3ce6a` test: export native technology metadata with the 3D browser fixtures — class Interconnect3DTest : public tst::Nangate45Fixture
- `f54d81668a` web: report database units for hierarchical chiplets — class Interconnect3DTest : public tst::Nangate45Fixture, serializeTechResponse
- `35100e3750` web: fix review follow-ups in the schematic timing view — DRCHandler::handleDRCHighlight, SelectHandler::handleContextAction, SelectHandler::handleFind, SelectHandler::handleInspect, SelectHandler::handleInspectBack, SelectHandler::handleSchematicCone, SelectHandler::handleSchematicInspect, SelectHandler::handleSchematicPath, SelectHandler::handleSelect, SelectHandler::handleSelectLayer, SelectHandler::handleSetProperty, SelectHandler::handleTriggerAction …
- `e15a9ac8c9` web: take the token from web_server -token and keep it out of the log — SessionAuth::SessionAuth, TEST, TEST_F, WebServer::endStartupScripts, WebServer::serve, browserSkipReasonText, class ListenerFixture : public ::testing::Test, class SessionAuth, class WebServer, dispatch_request, handle_request, proc web_server …
- `95dc15cc08` web: add grt heatmap — TEST_F, TileGenerator::drawRudyLayer, TileGenerator::pseudoLayerDefs, TileGenerator::saveImageLayerOrder, class SaveImageTest : public tst::Nangate45Fixture, class TileGenerator, struct TileVisibility
- `47c1f3ba51` clang-format — class TestRoutingCongestionHeatMap : public web::HeatMapData
- `b2d4d4c992` address reviewer feedback — TEST_F

### rsz (37)
- `fa4da7dab1` rsz: Tighten driver sizing checks in fullyRebuffer — Rebuffer::drvrPinTiming, Rebuffer::sizeDriverWithTree, Rebuffer::slackWithDriverCell, Rebuffer::upstreamSideLoadsOk, class Rebuffer : public sta::dbStaState, or_integration_tests, proc report_opt_config
- `531f7a1a45` rsz: Check upstream stages and other inputs before a driver resize — Rebuffer::chooseTreeAndDriver, Rebuffer::prevStageDriveResistance, Rebuffer::slackWithDriverCell, Rebuffer::upstreamSideLoadsOk, class Rebuffer : public sta::dbStaState, or_integration_tests
- `d2cf36aab9` rsz: Bound every other arc of a resized driver — Rebuffer::chooseTreeAndDriver, Rebuffer::otherInputsMeet, Rebuffer::prevStageDriveResistance, Rebuffer::slackWithDriverCell, Rebuffer::upstreamStagesOk, Resizer::closestDriver, Resizer::maxLoad, class Rebuffer : public sta::dbStaState, class Resizer : public sta::dbStaState, public sta::dbNetwor
- `4b2738598d` rsz: Keep the driver-size checks inside the rebuffer model — Rebuffer::inputCapGrowth, Rebuffer::otherArcsMeet, Rebuffer::slackWithDriverCell
- `da967cae63` rsz: Charge the slowest upstream driver on the timing-path input — Rebuffer::inputCapGrowth, Rebuffer::otherArcsMeet, Rebuffer::slackWithDriverCell, class Rebuffer : public sta::dbStaState
- `2daf71b892` rsz: Use the path transition's upstream drive resistance — Rebuffer::drvrPinTiming, Rebuffer::inputCapGrowth, Rebuffer::otherArcsMeet, Rebuffer::slackWithDriverCell, Rebuffer::upstreamDelay, Rebuffer::upstreamStagesOk, class Rebuffer : public sta::dbStaState
- `3bec6bfc79` rsz: Prefer the driving cell for a top-level input's resistance — Rebuffer::prevStageDriveResistance, proc add_sibling
- `79f5aadd91` rsz: Memoize drive resistance and input cap growth in Rebuffer — Rebuffer::chooseTreeAndDriver, Rebuffer::init, Rebuffer::inputCapGrowth, Rebuffer::prevStageDriveResistance, Rebuffer::setPin, class Rebuffer : public sta::dbStaState
- `c524fe2f35` rsz: Take equal-area driver swaps only on near-critical nets — Rebuffer::chooseTreeAndDriver, Rebuffer::sizeDriverWithTree, or_integration_tests
- `ed54b2647f` rsz: Take equal-area driver swaps only on nets that miss timing — Rebuffer::chooseTreeAndDriver, Rebuffer::sizeDriverWithTree
- `4599f8d93a` rsz: Rename Resizer::maxLoad to outputMaxCap — Rebuffer::slackWithDriverCell, Resizer::bufferSizeOutmatched, Resizer::closestDriver, class Resizer : public sta::dbStaState, public sta::dbNetwor
- `8daab22b44` rsz: Reword the rebuffer lookup cache comments — Rebuffer::portDriveResistance, class Rebuffer : public sta::dbStaState
- `ac73621257` rsz: Document the runtime cost of -rebuffer_size_driver
- `58a4fda451` rsz: Use the scene's view of a driving cell in rebuffer upstream delay — Rebuffer::prevStageDriveResistance
- `5805e1948d` rsz: Time each input once in otherArcsMeet and check slew first — Rebuffer::otherArcsMeet
- `78385eda70` rsz: Bound the driver candidate scan with the exact tree area — Rebuffer::chooseTreeAndDriver
- `c7a2bb89eb` rsz: Correct the driver resize fallback comment and an include — Rebuffer::sizeDriverWithTree
- `08357fdcd5` test: Cover the sequential and multi-output guards of driver sizing
- `76f37439ac` rsz: Check a driver candidate against its rebuffered output's limits — Rebuffer::otherArcsMeet, Rebuffer::slackWithDriverCell, Rebuffer::upstreamDelay, Resizer::outputMaxCap, class Rebuffer : public sta::dbStaState, class Resizer : public sta::dbStaState, public sta::dbNetwor, or_integration_tests
- `28f09999ef` rsz: Skip arcs that STA does not time in otherArcsMeet — Rebuffer::otherArcsMeet
- `953e442167` test: Isolate the driver candidate max capacitance check
- `6c5a09fa25` rsz: Slew check every arc delay calculation times in otherArcsMeet — Rebuffer::otherArcsMeet
- `dbeb471308` rsz: Say which output Resizer::outputMaxCap(cell) reports — class Resizer : public sta::dbStaState, public sta::dbNetwor
- `91cab78b52` rsz: Declare otherArcsMeet's input record once — Rebuffer::otherArcsMeet
- `a87ae0cc8a` rsz: Name the rebuffer lookup cache types — Rebuffer::inputCapGrowth, Rebuffer::portDriveResistance, class Rebuffer : public sta::dbStaState
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
- `75339783ef` update failing rsz tests
- `2e3307cd84` grt: restore second call to mazeRouteMSMDOrder3D()

### odb (16)
- `f357f5dcab` dft: implement clustering algorithm for scan chain optimization — class dbScanList : public dbObject, dbScanList::add
- `6395775d6a` odb: add dbDft::reset() to clear scan chain data — class dbDft : public dbObject, dbDft::getScanChains
- `c9a8232766` odb: add dbTechLayerCutEnclosureTableDefRule schema — TEST_F, _dbTechLayer::_dbTechLayer, _dbTechLayer::collectMemInfo, _dbTechLayer::getObjectTable, _dbTechLayer::~_dbTechLayer, add_library, class _dbTechLayer : public _dbObject, class _dbTechLayerSpacingTablePrlRule;, class dbTechLayer : public dbObject, class dbTechLayerArraySpacingRule;, class dbTechLayerCutEnclosureRule : public dbObject, dbTechLayer::getTechLayerCutEnclosureRules …
- `023dcb3266` odb: dropped minsum from lef58enclosuretable property — TEST_F, _dbTechLayerCutEnclosureTableDefRule::collectMemInfo, class _dbTechLayerCutEnclosureTableDefRule : public _dbObjec, class dbTechLayerCutEnclosureTableDefRule : public dbObject, dbTechLayerCutEnclosureTableDefRule::addWidthRow, dbTechLayerCutEnclosureTableDefRule::getDefaultRows
- `54b7559fe5` odb: gate CutEnclosureTableDefRule deserialization on schema version
- `0950866b65` odb: address review on dbTechLayerCutEnclosureTableDefRule — TEST_F, class dbTechLayerCutEnclosureTableDefRule : public dbObject, dbTechLayerCutEnclosureTableDefRule::destroy
- `864e2de1c5` odb: store DefaultRow/WidthRow structs directly instead of tuples — _dbTechLayerCutEnclosureTableDefRule::_dbTechLayerCutEnclosureTableDefRule, class _dbTechLayerCutEnclosureTableDefRule : public _dbObjec, class dbTechLayerCutEnclosureRule : public dbObject, class dbTechLayerCutEnclosureTableDefRule : public dbObject, dbTechLayerCutEnclosureTableDefRule::addDefaultRow
- `d9a2ef2451` odb: swig-wrap dbTechLayerCutEnclosureTableDefRule's dbSet — WRAP_DB_CONTAINER
- `a66ab524a6` odb: fire callbacks for dbGroup edits — TEST_F, class CallBack : public dbBlockCallBackObj, class dbBlock;, class dbBlockCallBackObj, dbGroup::addGroup, dbGroup::addInst, dbGroup::addModInst, dbGroup::create, dbGroup::destroy, dbGroup::getRegion, dbGroup::removeGroup, dbGroup::removeInst …
- `53ccd1f6cc` odb: regenerate design.odb fixture after schema merge
- `3ef23d9659` odb: restore User Code markers dropped by an earlier regen
- `7765275690` odb: validate above_below at runtime, not via assert — TEST_F, dbTechLayerCutEnclosureTableDefRule::destroy
- `2294eb0fb4` odb: use an enum class for above_below instead of a validated int — TEST_F, class dbHierSearchDir, class dbTechLayerCutEnclosureTableDefRule : public dbObject, dbTechLayerCutEnclosureTableDefRule::destroy
- `afca462a94` odb: drop redundant cut_class_valid from dbTechLayerCutEnclosureRule — TEST_F, class dbTechLayerCutEnclosureRule : public dbObject, dbTechLayerCutEnclosureRule::getNumCorners, lefTechLayerCutEnclosureRuleParser::setCutClass
- `28a0bebb68` odb: add missing trailing newline to generated CutEnclosureTableDefRule files — dbTechLayerCutEnclosureTableDefRule::getWidthRows
- `cf1c3b1c28` odb: ensure single binding point if a pin contain multiple wire segments — WireNormalizer::normalizeWireConnectivity, WireNormalizer::splitBySj, class WireNormalizer

### dft (15)
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

### grt (14)
- `c9a8232766` odb: add dbTechLayerCutEnclosureTableDefRule schema
- `baed7deb32` grt: restart the first soft-NDR demotion from the initial routing — FastRouteCore::run, FastRouteCore::setSoftNDR, Graph2D::getCostNDRAware, TEST_F, class FastRouteCore
- `527ad942c9` grt: shorten the soft-NDR restart comments — FastRouteCore::restoreInitialRoutes, FastRouteCore::run, FastRouteCore::saveInitialRoutes, class FastRouteCore
- `5f764243a3` grt: replace the NDR overflow multiplier with NDR deficits — FastRouteCore::StNetOrder, FastRouteCore::computeCongestedNDRnets, FastRouteCore::getMazeRouteNetOrder, FastRouteCore::getOverflow2D, FastRouteCore::getOverflow2Dmaze, FastRouteCore::mazeRouteMSMDSequential, FastRouteCore::newRipupCheck, FastRouteCore::newRipupCongestedL, FastRouteCore::newrouteL, FastRouteCore::newrouteZ, FastRouteCore::newrouteZ_edge, FastRouteCore::routeMonotonic …
- `8f0bcc61fc` grt: revert unnecessary gcd_grt_cugr.db regeneration
- `01b0fe5704` grt: fix clearNDRnets order and edge capacity for a specific location — FastRouteCore::getUsageNDRAware, Graph2D::initNDRnets
- `03a913a622` grt: update soft NDR goldens for per-edge NDR pricing — TEST_F
- `74d34bd075` grt: fix stale NDR deficits and the 3D maze gate — FastRouteCore::getUsageNDRAware, FastRouteCore::run, FastRouteCore::scanOverflow2D, FastRouteCore::scanOverflow2Dmaze, Graph2D::getCostNDRAware, Graph2D::getNDRDeficitIfRouted, Graph2D::releaseNDRCapLayer, TEST_F, class FastRouteCore, class Graph2D, class OverflowTestPeer
- `f0dcd2c370` grt: 3d fastroute data structure and optimizations — FastRouteCore::addNeighborPoints, FastRouteCore::initAuxVar, FastRouteCore::mazeRouteMSMDOrder3D, FastRouteCore::run, FastRouteCore::setGridsAndLayers, FastRouteCore::setupHeap3D, class FastRouteCore, right_index, struct parent3D
- `2e3307cd84` grt: restore second call to mazeRouteMSMDOrder3D() — FastRouteCore::run
- `301d8564f7` create MinHeap3D class to enable better iteration — FastRouteCore::addNeighborPoints, FastRouteCore::mazeRouteMSMDOrder3D, FastRouteCore::run, FastRouteCore::setGridsAndLayers, FastRouteCore::setupHeap3D, class FastRouteCore, namespace grt, struct parent3D
- `97c091ce08` grt: reduce memory footprint, don't allocate space for unused information — GlobalRouter::applyNetObstruction
- `1fe08158b2` grt: clear edge NDR deficits in clearNDRnets — Graph2D::clearNDRnets, Graph2D::copyRoutingStateFrom, Graph2D::usedGridsMatchUsage, TEST_F
- `847cfc1a40` grt: use NDR-aware cost in newrouteLInMaze — FastRouteCore::newrouteLInMaze, TEST_F, class OverflowTestPeer

### (top) (12)
- `29432e0625` dft: add scan optimization algorithm source files — filegroup
- `f357f5dcab` dft: implement clustering algorithm for scan chain optimization
- `d47a94535a` dft: refactor executeDftPlan to support scan_opt re-stitching
- `ae6b9c4858` dft: update build — filegroup
- `4923866d03` dft: add scan_opt regression/CI test
- `2a8b7f880b` test: raise the jpeg antenna limits for the NDR deficit change
- `211f67c73c` build: refresh generated Bazel registry metadata
- `02868f8910` build: keep shared lockfile repair out of feature changes
- `ff8d9f6bfb` test: raise ibex_sky130hd skew and aes_sky130hs antenna limits
- `422609299e` build(deps): bump setuptools from 84.0.0 to 84.1.0 in /bazel
- `50e9dc630d` update bazel flow test metrics
- `9752406140` test: update ibex and jpeg_sky130hd flow metrics after master merge

### drt (10)
- `4b734fbd99` drt: limit check_drc markers to each worker check region — FlexGCWorker::setDrcBox, TritonRoute::getDRCMarkers, class FlexGCWorker, filegroup, or_integration_tests
- `1cd3cc7a15` drt: use pass/fail checks for worker-boundary Bazel tests — filegroup
- `51488508ce` drt: check the requested region before the worker box — TritonRoute::getDRCMarkers
- `000496e8c6` drt: move worker-boundary coverage to GC unit tests — class FixtureWithParam : public GCFixture,, class TritonRoute : public PinAccessService, filegroup, or_integration_tests, struct GCFixture : public Fixture
- `0ae9e6469e` drt: default pin access from layer routability — FlexPA::EnoughAccessPoints, FlexPA::createMultipleAccessPoints, FlexPA::filterViaAccess, FlexPA::genAllAccessPoints, FlexPA::isIOTerm, class FlexPA, target_include_directories
- `7524159c66` drt: review compliance — FlexPA::filterViaAccess, FlexPA::isIOTerm
- `7afc9dc3f7` drt: restrict imported via figures to the GC context — FlexGCWorker::Impl::initRouteObj, FlexGCWorker::setDrcBox, INSTANTIATE_TEST_SUITE_P, TritonRoute::getDRCMarkers, class FlexGCWorker, class GCWorkerBoundaryFixture : public FixtureWithParam<int>, struct GCFixture : public Fixture
- `afca462a94` odb: drop redundant cut_class_valid from dbTechLayerCutEnclosureRule — io::Parser::setCutLayerProperties
- `f3e80f804c` drt: pa checks for any routing layer above or below when deciding via access — FlexPA::createMultipleAccessPoints, FlexPA::filterViaAccess, FlexPA::isRoutableLayer, INSTANTIATE_TEST_SUITE_P, class FlexPA
- `d694e4262e` drt: keep std cell and macro pins on up-via access — FlexPA::filterViaAccess

### mpl (9)
- `dfb7cc1cf9` web: add a Clusters panel and a cluster coloring overlay — HierRTLMP::commitClusteringDataToDb, HierRTLMP::createGroupForCluster, filegroup, or_integration_tests
- `4a20e9b08a` web: move the Clusters panel into the Hierarchy tab — HierRTLMP::commitClusteringDataToDb, HierRTLMP::createGroupForCluster
- `036fe54759` web: keep a hidden Hierarchy view from collapsing its columns
- `25265c5067` mpl: revert the pre-existing dbGroup handling — HierRTLMP::commitClusteringDataToDb, HierRTLMP::createGroupForCluster, filegroup, or_integration_tests
- `399ef84ff6` mpl: refactor configuration, one source of defaults — HierRTLMP::HierRTLMP, HierRTLMP::computeWireLength, HierRTLMP::createGroupForCluster, HierRTLMP::setGuidanceRegions, MacroPlacer::MacroPlacer, MacroPlacer::blockMacroChannels, class HierRTLMP, class MacroPlacer, getMacroPlacer, namespace mpl, proc rtl_macro_placer, set_debug_cmd …
- `2dcafbb425` mpl: refactor debug config — HierRTLMP::computeWireLength, HierRTLMP::configure, MacroPlacer::blockMacroChannels, class HierRTLMP, class MacroPlacer, getOptions, namespace mpl, proc parse_macro_name, rtl_macro_placer_cmd, struct MacroPlacerOptions
- `7ff36f5b4b` mpl: rename MacroPlacer::place to run — MacroPlacer::MacroPlacer, class MacroPlacer, rtl_macro_placer_cmd
- `52a84afec9` mpl: prevent crashes when running mpl_debug without gui — Graphics::Graphics, Graphics::penaltyCalculated, Graphics::startSA
- `0f5136b64d` mpl: update report_directory behavior — HierRTLMP::configure, HierRTLMP::placeChildren

### syn (3)
- `59f0bdd207` syn: L-IR core types (ids, ops, constants, names) — messages_txt
- `4e6174f7fb` syn: avoid a 32-bit shift in NameInterner's hash — class NameInterner
- `637e9f7001` syn: clang-tidy cleanups in L-IR tests — TEST

### ant (2)
- `4fa5708f3e` test: Check metrics cleanup and move antenna test pin — TEST_F
- `38b664069e` ant: Move completed cumulative antenna chain — AntennaChecker::Impl::calculateCAR

### dpl (2)
- `4569e4033e` dpl: respect oriented fixed macro footprints — NegotiationLegalizer::initFromDb, class OpendpTest : public tst::Fixture, filegroup
- `acabd565a7` dpl: refresh fixed macro regression outputs

### gpl (2)
- `22d6187a40` gpl: sub dbu movement on ultra low util fps spuriously fire divergence — NesterovBase::nesterovUpdateStepLength, TEST_F, class TimingRepairIntegrationTest : public tst::IntegratedFi
- `b02a5cb054` address reviewer feedback — NesterovBase::nesterovUpdateStepLength

### ppl (2)
- `17c7f9cbd4` ppl: make place_pin snap to edge for all floorplans — IOPlacer::excludeBoundaryShape, IOPlacer::getEdgeString, IOPlacer::movePinToTrack, IOPlacer::placePin, class IOPlacer, struct IOPlacer::ManualPinBlocking
- `8be7af101d` ppl: fix wording

### psm (2)
- `946aa96f4b` psm: remove solution when voltage or powers are modified — IRSolver::getVoltage, IRSolver::solve, IRSolver::solveAssembly, PDNSim::clearSolvers, PDNSim::setDebugGui, class IRSolver, class PDNSim : public odb::dbBlockCallBackObj
- `14b7914cfa` psm: only clear when values change — PDNSim::clearSolutions, PDNSim::setDebugGui

### utl (2)
- `4f70bb1a72` web: require an access token to use the viewer — add_library, gtest_discover_tests, test_suite
- `399ef84ff6` mpl: refactor configuration, one source of defaults — convert

### dbSta (1)
- `a7b7b15178` dbSta: check cross-layer pin alignment — IpChecker::checkPinRoutingGridAlignment, class IpChecker, namespace sta, or_integration_tests

### gui (1)
- `cb14951b3f` gui: give every build the gui:: commands — Gui::init, Gui::requestUserInput, class QtGuiBackend : public GuiBackend, else, enabled, fit, initGui, package, set, trigger_action

### rcx (1)
- `cf1c3b1c28` odb: ensure single binding point if a pin contain multiple wire segments — or_integration_tests

### tst (1)
- `4fa5708f3e` test: Check metrics cleanup and move antenna test pin — MetricsCapture::MetricsCapture

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
- `2b8d4dfb4` ChangeLog
- `da5123080` define_scene: reject -liberty/-spef with min/max variants
- `5e0c372c6` prima stiff parasitics resolves #565
- `6ca0e925d` ArrivalVisitor copy keeps clks_only
- `ea312e616` Move clk_arrivals_threads test to search/test
- `c0e900ae3` ArrivalVisitor copy keeps clks_only (#567)
- `1a906936f` gnuplot prima order
- `d3de5b4ab` Liberty hasCcsModels
- `05201d5b6` delay noise ccs warnings
- `b32a2d2fa` noise null net checks
- `3e6416733` noise net driver check
- `213fd6534` noise doc
- `065bd434e` release 3.2.0
- `50f311b73` annotate_noise_delays mcmm support
- `236f7d733` prima warnings
- `bea09a037` DelayNoise::arrivalWindowsOverlap
- `aceb5cbb4` noise warning
- `4eef5e990` noise prima warn
- `13d5720d3` Sta::libraryHasCcsModels leak
- `ebb53fd95` alignAggressors seg fault
- `894e39543` comments
- `c1a9bb65d` noise coupling cap checks
- `0dbcf8367` noise preamble reset
- `7b774e882` report/annotate reuse results
- `73f8326f1` report_noise_delay -max_count sort by max incr
- `f0d188fca` rm read_power_activities
- `57acd3640` Sdc: fix stale port delay leaf pin map entries (#563)
- `b7381ee61` SMALLFIX: Fix Liberty writer for slash and dollar bus names (#464)
- `8bc0bfe9f` const PortDirection singletons
- `e92007612` rm read_power_activities
- `590b89e79` Search::tnsDecr use iter
- `8e8bcf7a4` rm makeVertexSet
- `3b6eff9f0` liberty_write_escaped_names use make_result_file
- `6d552c077` set_sense -type default resolves #562
- `7515b0436` dcalc slew merge ignore constant disabled arcs
- `587f6d2a0` delay noise invalid
- `7fc92e25d` const
- `d7dabfa5d` report_delay_noise -net headers
- `02cb5f8e8` Liberty genclk PR #468
- `816c49e74` saif syntax error
- `036627e2a` Graph::verticesApply
- `b395bb08d` Network::pinIterator()
- `564d3efb5` dcalc slew merge ignore cond disabled arcs
- `a8c6e8245` sdc: clean up and move constraints on deleted pins, instances and nets
- `7feca37ba` sdc: free instance constraints on delete, default moveConstraints nets
- `e09a99715` gzip gcd_sky130 files
- `617319be1` sdc: one moveConstraints per pin, instance or net
- `2ce671ccc` sdc: follow OpenSTA style in constraint moves, guard self-moves
- `0adf965e1` Read long -through name lists in linear time (#573)
- `b8a631ade` Fix fork tests after upstream merge
- `9bc3fa3a9` Sta: move analysis corner SDC constraints in moveConstraints

## Pull requests updated this week (100 of 177, most recent first)

- #10784 [open] ram: integrate OpenSTA for timing and power reporting
- #12197 [open] sv-elab: update to 2026-11-09
- #9910 [closed] Standalone Per-Command OpenROAD Binaries
- #12295 [merged] agents: fix stale facts in skills and relax the src/sta rule
- #12238 [closed] ram: -w_port_words, the words each write port writes
- #12281 [open] ram: add bit-line segmentation and per-slice mux 2 word-select buffering
- #12131 [closed] Simplify some unnecessary overrides.
- #12294 [merged] rsz: add rebuffer reference harness for buffer_varying_lengths
- #12293 [merged] rsz: add driving cell and driver-sizing variant to buffer_varying_lengths
- #12150 [merged] odb: avoid segfault in insert_buffer and makeNewName when base name is null
- #12204 [merged] drt: fix victim and aggressor box y-coordinate corruption across cut checks
- #12274 [merged] odb: Notify move callbacks when the journal restores an orientation
- #12260 [open] drt: Support two WITHIN values for LEF58 ADJACENTCUTS
- #12228 [open] grt: make rudy consider linear nets
- #12195 [merged] rcx: check that the extraction rules cover the layers the design routes on
- #12190 [open] syn: L-IR Liberty cell table, register classes and operator specs
- #12292 [open] odb: preserve EXCEPTPGNET in DEF blockages
- #12267 [open] rsz: Preserve hierarchical clock connectivity during `repair_clock_inverters`
- #12145 [merged] test: Check metrics cleanup and move antenna test pin
- #12136 [merged] drt: route from iteration 0 when resuming with unrouted nets
- #12077 [merged] odb: ensure single binding point if a pin contains multiple co-linear wire segments
- #12123 [open] cut: Fix handling of endpoints on combinational cells 
- #12248 [open] pex: block shapes, the evaluator in the library, and a lane index
- #12019 [merged] ppl: make place_pin snap to edge for all floorplans
- #12011 [closed] dft: do not dereference the deque end when stitching a chain
- #12290 [open] Web GUI: a slack histogram bar lists the endpoints it counted
- #11728 [merged] CTS: fix inverter tree classication
- #12288 [merged] dbSta: build each hierarchical mod net once in Verilog2db
- #12289 [open] build(deps): bump the python group across 2 directories with 25 updates
- #12257 [closed] build(deps): Bump the python group across 2 directories with 23 updates
- #12287 [open] build(deps): bump the actions group across 1 directory with 4 updates
- #12256 [closed] build(deps): Bump the actions group across 1 directory with 3 updates
- #11854 [open] build(deps): bump three from 0.160.0 to 0.187.0 in /src/web in the npm group across 1 directory
- #11841 [closed] rcx: write hierarchical names for objects created in sub-modules
- #12286 [open] mpl: refactor top-level method structure and add support for site grid snap
- #11760 [open] mpl: snap macros to the site grid of the core rows
- #12285 [open] rsz: Don't treat data and clock buffers as equivalent cells in resizing
- #12258 [open] mpl: move feasibility checks to a dedicated abstraction
- #12284 [closed] build: remove unused vendored mockturtle
- #12273 [merged] Enable libc++ fast hardening; log failures with symbolized stack traces
- #10864 [open] cts: add -num_max_leaf_sinks knob and report_clock_tree QoR command
- #12275 [merged] rsz: Bug fixes for resizer for hybrid row design CTS
- #12264 [open] dpl: fix checkPadding for row unaligned instances
- #12261 [open] cts: make register-only clock gates sinks of their parent tree
- #12283 [open] dpl: pdn aware phase 2
- #11122 [merged] Web GUI: add an Instance Groups view to the Hierarchy widget, color-coded in the layout
- #12282 [open] build(deps): Bump soupsieve from 3.0.3 to 4.0 in /bazel
- #12280 [open] grt: save the guides of every net rerouted during FR incremental congestion recovery
- #12253 [closed] grt: fix FastRoute incremental congestion
- #11370 [merged] web: add schematic timing-path views and navigation
- #12177 [open] Make getting processor count more portable.
- #12082 [merged] Web GUI: make tabs that don't fit (like Charts) easy to reach
- #12270 [merged] agents: add run-web-viewer skill
- #12276 [open] syn: Bring changes from sv-elab upstream 
- #12214 [merged] gpl: Fix 2 timing driven design revert bugs when also using -rd
- #12272 [open] odb: use std::ranges::find in dbGroup net removal loops
- #12216 [open] docs: Fix publication link on landing page
- #12266 [merged] drt, odb, rsz: fix out-of-bounds vector iterator operations and lookup clamps
- #12109 [merged] rsz: Exclude disabled Liberty arcs in Resizer::driveResistance
- #12139 [open] mpl: consolidate SA penalties into a vector of Penalty
- #12234 [closed] web: a slack histogram bar drills down with the histogram's filters
- #12149 [open] save goldens as plain files rather than executable files
- #12251 [open] rsz, dbSta: fix repair_clock_inverters crash on hierarchical netlists
- #11858 [merged] web: widening a table column widens the table (Qt parity)
- #12245 [open] drt: rename misnamed hasCornerSpacingConstraint to hasMinStepConstraint
- #12265 [open] update sta
- #12263 [merged] grt: report design-level metrics only, not per incremental reroute
- #11897 [merged] web: show bump footprints and logical inter-die links in 3D
- #11040 [merged] web: add schematic back navigation
- #11440 [open] Use Kokkos instead of OpenMP
- #12233 [closed] dpl: run diamond recovery when negotiation phase 2 hits its iteration limit
- #12122 [open] dpl: fail in seconds, not 82 minutes, when no search can legalize within the window
- #11772 [merged] drt: default pin access
- #12100 [open] gpl, cts: Expand -power_driven mode to clock leaf nets using virtual CTS sink clustering
- #11698 [merged] drt: restrict imported via figures to the GC context
- #12231 [open] fsv: include <stdexcept> in FieldSolver.cpp
- #12147 [open] cts: latency balancing times only the clock network, CTS 101.8 -> 47.8 GB on XSTile, same tree
- #12239 [open] ram: write enable, hold and takes buffered per eight bits
- #11522 [open] dbSta: check Liberty transition tables and input capacitance in check_ip
- #12201 [merged] dft: Speedup executeDftPlan() by preventing repeated full STA rebuilds
- #12096 [open] drt: generate pin access points on preferred upper-layer tracks
- #12211 [open] drt: preserve cut classes on DEF-imported and generated vias
- #12259 [merged] bazel: build everything with BOOST_ASIO_NO_DEPRECATED
- #12242 [merged] rsz: Add regression test for cross-module gate cloning
- #12127 [open] ord: Reduce memory leak
- #11421 [merged] odb: add dbTechLayerCutEnclosureTableDefRule schema
- #12232 [merged] gpl: keep positions when initial placement has nothing to anchor them
- #12255 [merged] utl: fix clang-tidy warnings
- #12219 [closed] build(deps): bump the python group across 2 directories with 22 updates
- #12218 [closed] build(deps): bump the actions group with 2 updates
- #12254 [open] grt: connect pad pins at their core-facing edge
- #10715 [closed] odb: decompose non-rectilinear LEF polygons into rectangles (#10256)
- #12249 [merged] bazel: fix clang-tidy lint binary name; fail CI if clang-tidy breaks
- #12252 [merged] ci: run Gemini triage only in The-OpenROAD-Project/OpenROAD
- #12222 [merged] Update OpenSTA 11/10
- #12169 [open] odb: fix multi-patterning wire mask spacing and recolouring in write_def
- #12098 [closed] mpl: Improve macro-placer simulated annealing robustness and packing quality
- #12236 [open] rsz: Fix VT swap for flows that change dont_use VTs
- #12244 [merged] pex: TestModelBuilder independent of the seed; a resume finds an unfitted planed crossing table
- #12210 [open] dpl: recover insufficient native pin access with legal cell moves

## Issues updated this week (69)

- #11684 [open] RFC: repair_timing, a user callback to end a phase at its knee
- #12198 [closed] drt: SPACINGTABLE ORTHOGONAL marker records its victim boxes with the upper y taken from the x coordinate
- #12052 [closed] OpenRCX: extMeasure::calcRes0 segfaults on a null getRes() result when a rules file has sparse per-layer tables
- #12291 [open] odb: EXCEPTPGNET is lost during DEF import and export
- #11993 [closed] detailed_route: resuming from DRC markers in the db leaves unrouted nets unrouted (ECO after repair_design / repair_antennas)
- #11271 [closed] RCX-0111: `has a loop at ... , on bterm` reported on a net with no loop
- #11677 [closed] CTS: flops behind a clock inverter get no tree after a macro/register split
- #11389 [closed] web: gui cannot be open if firefox is already running in another host
- #7959 [closed] Display MPL cluster results
- #11893 [open] dbSta: top port order in write_verilog -include_pwr_gnd and write_timing_model differs between the pdngen session and a read_db session
- #11222 [closed] gui: Free ruler only works in X
- #4872 [open] Create an IP Checker Utility
- #12171 [open] grt: pad pin with shapes on several layers gets its connection on the bond-pad layer; port on the pad pin is routed as a separate pin
- #10770 [open] `syn` does not infer latches — silently emits a combinational loop
- #12277 [open] syn: division and modulo with a non-constant divisor are dropped at export, leaving outputs undriven
- #11892 [closed] Make it easier to find "Charts" in web GUI
- #12279 [open] dpl: legalCellPos/nearestBlockEdge moves a cell onto an abutting macro
- #12278 [open] rsz: buffers inserted with placement parasitics are left on top of macros
- #11159 [closed] Document the non-local invariants in code: pdn ordering and obstruction rules, and the same pattern in tap and ant
- #11626 [closed] rsz: no regression test reaches hierarchicalConnect through gate cloning (moved loads in another module) — would a test PR be welcome?
- #12271 [open] odb: write_def writes a coloured routing RECT as `RECT MASK <raw byte> ( ... )`, which read_def rejects
- #12269 [open] LEF/DEF lexers hang on a file ending in a comment without a newline where char is unsigned (aarch64, RISC-V)
- #12268 [open] rsz: should the size-up-match count in RSZ-0051 carry over from an earlier repair_timing call?
- #12038 [open] check_placement: padding check flags a legal cell above a fixed block whose bottom is in the upper half of a row
- #12262 [open] dpl: make diamond recovery more informative, and call it when phase 2 reachs max iterations.
- #11167 [open] [Security] Fix of vulnerabilities similar to issue #11065
- #11697 [closed] drt: check_drc reports false spacing markers outside worker regions
- #12016 [closed] insert_buffer segfaults naming the buffer for a single load pin without -buffer_name
- #12250 [open] repair_clock_inverters segfaults when a clock inverter's output pin carries a dbModNet (hierarchical flow)
- #8267 [open] DPL: PDN via awareness
- #12049 [closed] [dbSta] write_spef writes pins of hierarchical cells under instance names that don't exist
- #12202 [open] drt: LEF58 cut spacing ADJACENTCUTS with two WITHIN values keeps only the first, as the upper bound
- #12229 [open] drt: LEF58_MINSTEP EXCEPTRECTANGLE under NOBETWEENEOL, and NOADJACENTEOL with or without MINADJACENTLENGTH
- #12226 [open] drt: LEF58_SPACING ENDOFLINE ... OPPOSITEWIDTH is parsed but never read by the check; is that intended?
- #12166 [open] odb: write_def drops the MASK of every other wire segment, so a round trip recolours routing
- #10561 [open] ram: add placement sanity checks to the regression tests (`check_placement`, etc.)
- #12209 [closed] Testing whether issue assignment works
- #11340 [open] web: Rendering and navigation are glitchy
- #12160 [open] cleanup-opportunity: BUILD files never refer to mockturtle in third-partty/
- #8770 [open] grt/drt: Add support for routing secondary power net from gate to the nearby related strap
- #12207 [open] drt: corner spacing patches run only when the technology has a MINSTEP rule (hasCornerSpacingConstraint_ is set by min-step constraints)
- #12203 [open] drt: LEF58_MAXSPACING via-swap fallback skips updateDRNet, so the worker reports markers for a via that is not in the design
- #12200 [open] drt: after the LEF58_MAXSPACING pin-access re-run, a worker whose box overlaps a pin but holds none of its new access points aborts with DRT-1231
- #12199 [open] drt: LEF58_MAXSPACING repair aborts with DRT-0073 on an already clean route when the avoided via class is the only one that fits a pin
- #12191 [open] drt: min-area patch owner search compares the origin-relative patch box with absolute shapes, so patches are dropped
- #12188 [open] drt: a SAMENET LEF58 cut spacing rule disables different-net checks of the other LEF58 cut spacing rules on the layer
- #12187 [open] drt: LEF58 cut spacing LAYER rule without CUTCLASS, or without a corner keyword, is never checked
- #11537 [open] drt: no convergence-based stop; detailed_route runs to -droute_end_iter after the violation count plateaus
- #11532 [open] drt: is the nightly ISPD run the intended coverage for NEARDRC and the congestion clip growth?
- #12184 [open] drt maze: modInterLayerCutSpacingCost writes past the grid for a cut just above the top routing layer
- #12185 [open] cluster_flops swaps two data connections when only the output bundle member order changes
- #12182 [open] drt LEF58 end-of-line SAMEMASK rule: getEolWithin() returns 0, ignoring WITHIN
- #12181 [open] drt LEF58 end-of-line MINLENGTH/MAXLENGTH TWOSIDES read from the PARALLELEDGE TWOEDGES flag
- #12176 [open] odb LEF58_MINIMUMCUT: per-cut-class form never sets isPerCutClass, so drt silently drops the rule
- #12174 [open] drt: LEF58_SPACING ENDOFLINE ... TOCONCAVECORNER / TONOTCHLENGTH is enforced as plain ENDOFLINE w WITHIN 0, silently
- #12173 [open] drt: LEF58_SPACING ENDOFLINE MINLENGTH l TWOSIDES is checked one-sided (io passes the TWOEDGES flag as TWOSIDES)
- #12170 [open] rsz: repairNetWire wire-split length computed in float cancels to 0 for weak drivers (loops on 26Q1, RSZ-0170 on master)
- #12167 [open] syn: synthesize renumbers a port declared [11:8] to [3:0]
- #12165 [open] odb: write_def emits ')MASK n' without a space, which read_def then rejects
- #11973 [closed] rsz: computeSkewBudget clears pin-scoped propagated-clock state
- #11358 [open] Incremental global placement needs to be timing aware
- #11324 [open] dpl: checkOneSiteGap is implemented twice and the two disagree at the core edge
- #12179 [open] Using abc-0.70-yosyshq beneficial with better slack ?
- #5753 [open] Remove name pattern matching approach to identify buffer types
- #10256 [open] POLYGON statements dropped from LEF
- #12161 [open] Renaming toplevel `src/` to `openroad/`
- #8075 [closed] repair_timing -hold ignores registers sampling clocks
- #11926 [open] LEF58_SPACINGTABLE with a SAMEMASK table and the normal table in one property is dropped (and how SAMEMASK is handled)
- #11668 [closed] timing__fmax includes virtual clocks since ORFS added virtual I/O clocks. Intended?

