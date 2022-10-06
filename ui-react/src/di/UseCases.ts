import MainNetworkDataSource from "../business/datasource/network/MainNetworkDataSource";
import GetKernelsUseCase from "../business/interactors/GetKernelsUseCase";
import GetDataSetsUseCase from "../business/interactors/GetDataSetsUseCase";
import GetResultsUseCase from "../business/interactors/GetResultsUseCase";
import IUseCases from "./interfaces/IUseCases";
import RunClassificationUseCase from "../business/interactors/RunClassificationUseCase";

export default (mainNetworkDataSource: MainNetworkDataSource): IUseCases => {
  return {
    GetKernelsUseCase: new GetKernelsUseCase(mainNetworkDataSource),
    GetDataSetsUseCase: new GetDataSetsUseCase(mainNetworkDataSource),
    GetResultsUseCase: new GetResultsUseCase(mainNetworkDataSource),
    RunClassificationUseCase: new RunClassificationUseCase(
      mainNetworkDataSource
    ),
  };
};
