"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getCodesizeFromArtifact = void 0;
/**
 * Get the codesize of a provided artifact.
 */
function getCodesizeFromArtifact(artifact) {
    return (artifact.compilerOutput.evm.bytecode.object.length - 2) / 2;
}
exports.getCodesizeFromArtifact = getCodesizeFromArtifact;
//# sourceMappingURL=codesize.js.map