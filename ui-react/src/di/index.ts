import NetworkServices from "./NetworkServices";
import NetworkDataSources from "./NetworkDataSources";
import UseCases from "./UseCases";

const cNetworkServices = NetworkServices();
const cNetworkDataSources = NetworkDataSources(
  cNetworkServices.MainNetworkServiceImpl
);
const cUseCase = UseCases(cNetworkDataSources.MainNetworkDataSourceImpl);

export default {
  GetKernelsUseCase: cUseCase.GetKernelsUseCase,
  GetDataSetsUseCase: cUseCase.GetDataSetsUseCase,
  GetResultsUseCase: cUseCase.GetResultsUseCase,
  RunClassificationUseCase: cUseCase.RunClassificationUseCase,
};
