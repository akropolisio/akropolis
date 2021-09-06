import { LogEntry, LogWithDecodedArgs, TransactionReceiptWithDecodedLogs } from 'ethereum-types';
/**
 * Filter logs by event name/type.
 */
export declare function filterLogs<TEventArgs>(logs: LogEntry[], event: string): Array<LogWithDecodedArgs<TEventArgs>>;
/**
 * Filter logs by event name/type and convert to arguments.
 */
export declare function filterLogsToArguments<TEventArgs>(logs: LogEntry[], event: string): TEventArgs[];
/**
 * Verifies that a transaction emitted the expected events of a particular type.
 */
export declare function verifyEvents<TEventArgs>(txReceipt: TransactionReceiptWithDecodedLogs, expectedEvents: TEventArgs[], eventName: string): void;
/**
 * Given a collection of logs, verifies that matching events are identical.
 */
export declare function verifyEventsFromLogs<TEventArgs>(logs: LogEntry[], expectedEvents: TEventArgs[], eventName: string): void;
//# sourceMappingURL=log_utils.d.ts.map