/** @typedef {{id:number,name:string,sensors:object[],readings:object[]}} Dataset */
/** @typedef {{id:number,name:string,dataset_id:number,steps:object[]}} Plan */
/** @typedef {{id:number,name:string,status:'queued'|'running'|'completed'|'failed'|'invalid',owner:string|null,result:object|null}} Trace */
/** @typedef {{id:number,dataset_id:number,user_id:number,sensor_id:number,user:string,dataset:string}} Assignment */
export {};
