const FederatedLearning = artifacts.require("FederatedLearning");
const FederatedLearning2 = artifacts.require("FederatedLearning2");

module.exports = function (deployer) {
    deployer.deploy(FederatedLearning);
    deployer.deploy(FederatedLearning2);
};

