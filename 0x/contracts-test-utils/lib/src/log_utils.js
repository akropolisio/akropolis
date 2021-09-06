"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.verifyEventsFromLogs = exports.verifyEvents = exports.filterLogsToArguments = exports.filterLogs = void 0;
const chai_setup_1 = require("./chai_setup");
// tslint:disable no-unnecessary-type-assertion
/**
 * Filter logs by event name/type.
 */
function filterLogs(logs, event) {
    return logs.filter(log => log.event === event);
}
exports.filterLogs = filterLogs;
/**
 * Filter logs by event name/type and convert to arguments.
 */
function filterLogsToArguments(logs, event) {
    return filterLogs(logs, event).map(log => log.args);
}
exports.filterLogsToArguments = filterLogsToArguments;
/**
 * Verifies that a transaction emitted the expected events of a particular type.
 */
function verifyEvents(txReceipt, expectedEvents, eventName) {
    return verifyEventsFromLogs(txReceipt.logs, expectedEvents, eventName);
}
exports.verifyEvents = verifyEvents;
/**
 * Given a collection of logs, verifies that matching events are identical.
 */
function verifyEventsFromLogs(logs, expectedEvents, eventName) {
    const _logs = filterLogsToArguments(logs, eventName);
    chai_setup_1.expect(_logs.length, `Number of ${eventName} events emitted`).to.eq(expectedEvents.length);
    _logs.forEach((log, index) => {
        chai_setup_1.expect(log, `${eventName} event ${index}`).to.deep.equal(Object.assign(Object.assign({}, log), expectedEvents[index]));
    });
}
exports.verifyEventsFromLogs = verifyEventsFromLogs;
//# sourceMappingURL=log_utils.js.map