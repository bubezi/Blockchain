const FederatedLearning = artifacts.require("FederatedLearning");

contract("FederatedLearning", (accounts) => {
    it("should submit and validate an update", async () => {
        const instance = await FederatedLearning.deployed();
        const submitter = accounts[1];
        const validator = accounts[2];

        // Submit an update
        await instance.submitUpdate("QmTestHash", { from: submitter });

        // Validate the update
        await instance.validateUpdate(0, { from: validator });

        const update = await instance.modelUpdates(0);
        assert.equal(update.submitter, submitter, "Incorrect submitter");
        assert.equal(update.ipfsHash, "QmTestHash", "Incorrect IPFS hash");
        assert.equal(update.isValidated, true, "Update not validated");
    });
});
